from fastapi import APIRouter
from ..services.model_service import model_service
from ..database import get_db

router = APIRouter()

@router.get("/health")
async def health_check():
    db = get_db()
    return {
        "status": "ok",
        "model_loaded": model_service.is_loaded,
        "model_name": model_service.metadata.get("model_name") if model_service.metadata else None,
        "labels": model_service.labels,
        "db_connected": db is not None,
        "message": "Model not loaded — run: python ml/train.py" if not model_service.is_loaded else "All systems operational"
    }
