from ..database import get_db
from datetime import datetime, timezone
from typing import Optional

async def get_latest_analysis():
    """Retrieve the most recent analysis from MongoDB."""
    db = get_db()
    if db is None:
        return None
    try:
        result = await db.analyses.find_one({}, {"_id": 0}, sort=[("createdAt", -1)])
        return result
    except Exception:
        return None

async def get_analysis_comments(
    analysis_id: str,
    sentiment: str = "all",
    page: int = 1,
    limit: int = 50
) -> dict:
    """Get paginated comments for an analysis."""
    db = get_db()
    if db is None:
        return {"comments": [], "total": 0}
    
    try:
        query = {"analysisId": analysis_id}
        if sentiment != "all":
            query["sentiment"] = sentiment
        
        skip = (page - 1) * limit
        cursor = db.comment_predictions.find(query, {"_id": 0}).skip(skip).limit(limit)
        comments = await cursor.to_list(length=limit)
        total = await db.comment_predictions.count_documents(query)
        return {"comments": comments, "total": total}
    except Exception as e:
        print(f"⚠️  Comment retrieval failed: {e}")
        return {"comments": [], "total": 0}
