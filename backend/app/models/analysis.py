from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class AnalysisModel(BaseModel):
    """MongoDB document model for sentiment analyses."""
    analysisId: str
    sourceType: str = "csv"
    fileName: Optional[str] = None
    totalComments: int = 0
    positiveCount: int = 0
    neutralCount: int = 0
    negativeCount: int = 0
    positivePercentage: float = 0.0
    neutralPercentage: float = 0.0
    negativePercentage: float = 0.0
    averageConfidence: float = 0.0
    createdAt: datetime = Field(default_factory=datetime.utcnow)
