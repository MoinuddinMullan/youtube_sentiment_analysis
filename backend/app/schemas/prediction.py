from pydantic import BaseModel, field_validator
from typing import Optional

class SinglePredictionRequest(BaseModel):
    text: str

    @field_validator("text")
    @classmethod
    def text_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Comment text cannot be empty")
        if len(v.strip()) < 2:
            raise ValueError("Comment text is too short (minimum 2 characters)")
        return v.strip()

class PredictionResponse(BaseModel):
    success: bool = True
    sentiment: str
    confidence: float
    probabilities: dict[str, float]

class BatchPredictionRequest(BaseModel):
    comments: list[str]

    @field_validator("comments")
    @classmethod
    def comments_must_not_be_empty(cls, v):
        if not v:
            raise ValueError("Comments list cannot be empty")
        if len(v) > 10000:
            raise ValueError("Maximum 10,000 comments per batch request")
        return [c.strip() for c in v if c and c.strip()]

class BatchPredictionResponse(BaseModel):
    success: bool = True
    total: int
    results: list[dict]
