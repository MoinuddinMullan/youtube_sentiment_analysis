from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CommentPredictionModel(BaseModel):
    """MongoDB document model for individual comment predictions."""
    analysisId: str
    commentText: str
    sentiment: str  # positive, neutral, negative
    confidence: float
    probabilities: dict
    video_title: Optional[str] = ""
    channel_username: Optional[str] = ""
    author: Optional[str] = ""
    published_at: Optional[str] = ""
    like_count: Optional[str] = "0"
    reply_count: Optional[str] = "0"
    createdAt: datetime = Field(default_factory=datetime.utcnow)
