import uuid
import io
import pandas as pd
from datetime import datetime, timezone
from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from ..services.model_service import model_service
from ..database import get_db
from ..config import settings

router = APIRouter()

@router.post("/analysis/upload")
async def upload_and_analyze(
    file: UploadFile = File(...),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=50, le=500)
):
    """Upload a CSV file and run sentiment analysis on all comments."""
    # Validate file extension
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted")
    
    content = await file.read()
    
    # Check file size
    if len(content) > settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=413, 
            detail=f"File exceeds {settings.MAX_UPLOAD_SIZE_MB}MB limit"
        )

    # Read CSV with fallback encoding
    df = None
    for encoding in ["utf-8", "utf-8-sig", "latin-1", "cp1252"]:
        try:
            df = pd.read_csv(io.BytesIO(content), encoding=encoding, on_bad_lines="skip")
            break
        except Exception:
            continue
    
    if df is None or df.empty:
        raise HTTPException(status_code=400, detail="Could not read CSV file")

    # Find comment column
    comment_col = None
    candidates = [settings.COMMENT_COLUMN, "comment_text", "text", "comment", "Comment", "body", "content"]
    for col in candidates:
        if col in df.columns:
            comment_col = col
            break
    
    if not comment_col:
        raise HTTPException(
            status_code=400,
            detail=f"CSV must contain a 'comment_text' column. Found columns: {list(df.columns)[:10]}"
        )

    # Clean and validate rows
    df = df.dropna(subset=[comment_col]).copy()
    df[comment_col] = df[comment_col].astype(str).str.strip()
    df = df[df[comment_col].str.len() >= 2]
    df = df.reset_index(drop=True)

    if df.empty:
        raise HTTPException(status_code=400, detail="No valid comments found in CSV")

    texts = df[comment_col].tolist()

    # Batch predict
    try:
        predictions = model_service.predict_batch(texts)
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

    # Build enriched results
    enriched = []
    extra_cols = ["video_title", "channel_username", "author", "published_at", "like_count", "reply_count", "video_id"]
    
    for pred, (_, row) in zip(predictions, df.iterrows()):
        record = {
            "commentText": pred["text"],
            "sentiment": pred["sentiment"],
            "confidence": pred["confidence"],
            "probabilities": pred["probabilities"],
        }
        for col in extra_cols:
            if col in df.columns:
                val = row.get(col, "")
                record[col] = str(val) if pd.notna(val) else ""
        enriched.append(record)

    # Compute stats
    pos = sum(1 for r in enriched if r["sentiment"] == "positive")
    neu = sum(1 for r in enriched if r["sentiment"] == "neutral")
    neg = sum(1 for r in enriched if r["sentiment"] == "negative")
    total = len(enriched)
    avg_conf = round(sum(r["confidence"] for r in enriched) / total, 4)

    analysis_id = f"ANL-{uuid.uuid4().hex[:8].upper()}"
    
    summary = {
        "totalComments": total,
        "positiveCount": pos,
        "neutralCount": neu,
        "negativeCount": neg,
        "positivePercentage": round((pos / total) * 100, 1),
        "neutralPercentage": round((neu / total) * 100, 1),
        "negativePercentage": round((neg / total) * 100, 1),
        "averageConfidence": avg_conf
    }

    # Save to MongoDB (if available)
    db = get_db()
    if db is not None:
        try:
            analysis_doc = {
                "analysisId": analysis_id,
                "sourceType": "csv",
                "fileName": file.filename,
                "createdAt": datetime.now(timezone.utc),
                **summary
            }
            await db.analyses.insert_one(analysis_doc)
            
            # Store up to 5000 predictions
            if enriched:
                batch_size = 500
                docs = [{**r, "analysisId": analysis_id, "createdAt": datetime.now(timezone.utc)} 
                        for r in enriched[:5000]]
                for i in range(0, len(docs), batch_size):
                    await db.comment_predictions.insert_many(docs[i:i+batch_size])
        except Exception as e:
            print(f"⚠️  MongoDB save failed: {e}")

    # Paginate results
    start = (page - 1) * limit
    paginated = enriched[start: start + limit]

    return {
        "success": True,
        "analysisId": analysis_id,
        "summary": summary,
        "results": paginated,
        "total": total,
        "page": page,
        "limit": limit
    }


@router.get("/analysis/stats/overview")
async def get_overview_stats():
    """Get aggregate stats across all analyses."""
    db = get_db()
    if db is None:
        return {"success": True, "data": {"totalAnalyses": 0, "totalComments": 0, "avgPositive": 0, "avgNeutral": 0, "avgNegative": 0}}
    
    try:
        pipeline = [
            {"$group": {
                "_id": None,
                "totalAnalyses": {"$sum": 1},
                "totalComments": {"$sum": "$totalComments"},
                "avgPositive": {"$avg": "$positivePercentage"},
                "avgNeutral": {"$avg": "$neutralPercentage"},
                "avgNegative": {"$avg": "$negativePercentage"},
                "avgConfidence": {"$avg": "$averageConfidence"}
            }}
        ]
        result = await db.analyses.aggregate(pipeline).to_list(length=1)
        if result:
            r = result[0]
            r.pop("_id", None)
            # Round floats
            for key in ["avgPositive", "avgNeutral", "avgNegative", "avgConfidence"]:
                if key in r:
                    r[key] = round(r[key], 1)
            return {"success": True, "data": r}
    except Exception as e:
        print(f"⚠️  Stats query failed: {e}")
    
    return {"success": True, "data": {"totalAnalyses": 0, "totalComments": 0}}


@router.get("/analysis/history")
async def get_history(
    page: int = Query(default=1, ge=1), 
    limit: int = Query(default=20, le=100)
):
    """Get list of all previous analyses."""
    db = get_db()
    if db is None:
        return {"success": True, "data": [], "total": 0, "page": page, "limit": limit}
    
    try:
        skip = (page - 1) * limit
        cursor = db.analyses.find({}, {"_id": 0}).sort("createdAt", -1).skip(skip).limit(limit)
        data = await cursor.to_list(length=limit)
        total = await db.analyses.count_documents({})
        # Convert datetime objects to ISO strings for JSON serialization
        for item in data:
            if "createdAt" in item and hasattr(item["createdAt"], "isoformat"):
                item["createdAt"] = item["createdAt"].isoformat()
        return {"success": True, "data": data, "total": total, "page": page, "limit": limit}
    except Exception as e:
        print(f"⚠️  History query failed: {e}")
        return {"success": True, "data": [], "total": 0}


@router.get("/analysis/{analysis_id}")
async def get_analysis_detail(
    analysis_id: str,
    sentiment: str = Query(default="all"),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=50, le=500)
):
    """Get detailed analysis with paginated comments."""
    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database unavailable")
    
    try:
        analysis = await db.analyses.find_one({"analysisId": analysis_id}, {"_id": 0})
        if not analysis:
            raise HTTPException(status_code=404, detail=f"Analysis {analysis_id} not found")
        
        if "createdAt" in analysis and hasattr(analysis["createdAt"], "isoformat"):
            analysis["createdAt"] = analysis["createdAt"].isoformat()
        
        query = {"analysisId": analysis_id}
        if sentiment != "all" and sentiment in ["positive", "neutral", "negative"]:
            query["sentiment"] = sentiment
        
        skip = (page - 1) * limit
        cursor = db.comment_predictions.find(query, {"_id": 0}).skip(skip).limit(limit)
        comments = await cursor.to_list(length=limit)
        total = await db.comment_predictions.count_documents(query)
        
        for c in comments:
            if "createdAt" in c and hasattr(c["createdAt"], "isoformat"):
                c["createdAt"] = c["createdAt"].isoformat()
        
        return {
            "success": True,
            "analysis": analysis,
            "comments": comments,
            "total": total,
            "page": page,
            "limit": limit
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving analysis: {str(e)}")
