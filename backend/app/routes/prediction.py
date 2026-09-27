import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from ..schemas.prediction import (
    SinglePredictionRequest, PredictionResponse,
    BatchPredictionRequest, BatchPredictionResponse
)
from ..services.model_service import model_service
from ..database import get_db

router = APIRouter()


@router.post("/predict", response_model=PredictionResponse)
async def predict_single(req: SinglePredictionRequest):
    """Predict sentiment for a single comment and persist to MongoDB."""
    try:
        result = model_service.predict_single(req.text)
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

    # ── Persist to MongoDB (non-blocking: failures are logged, never raised) ──
    db = get_db()
    if db is not None:
        try:
            analysis_id = f"QT-{uuid.uuid4().hex[:8].upper()}"
            now = datetime.now(timezone.utc)
            sentiment = result["sentiment"]

            analysis_doc = {
                "analysisId":          analysis_id,
                "sourceType":          "single",
                "fileName":            None,
                "totalComments":       1,
                "positiveCount":       1 if sentiment == "positive" else 0,
                "neutralCount":        1 if sentiment == "neutral"  else 0,
                "negativeCount":       1 if sentiment == "negative" else 0,
                "positivePercentage":  100.0 if sentiment == "positive" else 0.0,
                "neutralPercentage":   100.0 if sentiment == "neutral"  else 0.0,
                "negativePercentage":  100.0 if sentiment == "negative" else 0.0,
                "averageConfidence":   round(float(result["confidence"]), 4),
                "createdAt":           now,
            }
            await db.analyses.insert_one(analysis_doc)

            comment_doc = {
                "analysisId":   analysis_id,
                "commentText":  req.text,
                "sentiment":    sentiment,
                "confidence":   round(float(result["confidence"]), 4),
                "probabilities": result["probabilities"],
                "createdAt":    now,
            }
            await db.comment_predictions.insert_one(comment_doc)

        except Exception as db_err:
            print(f"⚠️  MongoDB save failed (single predict): {db_err}")

    return PredictionResponse(success=True, **result)


@router.post("/predict/batch", response_model=BatchPredictionResponse)
async def predict_batch(req: BatchPredictionRequest):
    """Predict sentiment for multiple comments and persist to MongoDB."""
    try:
        results = model_service.predict_batch(req.comments)
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch prediction failed: {str(e)}")

    # ── Persist to MongoDB (non-blocking: failures are logged, never raised) ──
    db = get_db()
    if db is not None:
        try:
            analysis_id = f"BT-{uuid.uuid4().hex[:8].upper()}"
            now = datetime.now(timezone.utc)
            total = len(results)

            if total > 0:
                pos      = sum(1 for r in results if r["sentiment"] == "positive")
                neu      = sum(1 for r in results if r["sentiment"] == "neutral")
                neg      = sum(1 for r in results if r["sentiment"] == "negative")
                avg_conf = round(sum(r["confidence"] for r in results) / total, 4)

                analysis_doc = {
                    "analysisId":         analysis_id,
                    "sourceType":         "batch_api",
                    "fileName":           None,
                    "totalComments":      total,
                    "positiveCount":      pos,
                    "neutralCount":       neu,
                    "negativeCount":      neg,
                    "positivePercentage": round((pos / total) * 100, 1),
                    "neutralPercentage":  round((neu / total) * 100, 1),
                    "negativePercentage": round((neg / total) * 100, 1),
                    "averageConfidence":  avg_conf,
                    "createdAt":          now,
                }
                await db.analyses.insert_one(analysis_doc)

                docs = [
                    {
                        "analysisId":   analysis_id,
                        "commentText":  r["text"],
                        "sentiment":    r["sentiment"],
                        "confidence":   round(float(r["confidence"]), 4),
                        "probabilities": r["probabilities"],
                        "createdAt":    now,
                    }
                    for r in results
                ]
                batch_size = 500
                for i in range(0, len(docs), batch_size):
                    await db.comment_predictions.insert_many(docs[i : i + batch_size])

        except Exception as db_err:
            print(f"⚠️  MongoDB save failed (batch predict): {db_err}")

    return BatchPredictionResponse(
        success=True,
        total=len(results),
        results=results
    )
