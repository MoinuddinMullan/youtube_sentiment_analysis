from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AnalysisSummary(BaseModel):
    analysisId: str
    sourceType: str
    fileName: Optional[str] = None
    totalComments: int
    positiveCount: int
    neutralCount: int
    negativeCount: int
    positivePercentage: float
    neutralPercentage: float
    negativePercentage: float
    averageConfidence: float
    createdAt: datetime

class AnalysisUploadResponse(BaseModel):
    success: bool = True
    analysisId: str
    summary: dict
    results: list[dict]
    total: int
    page: int
    limit: int
