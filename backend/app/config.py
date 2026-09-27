from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "Sentiview AI"
    ENVIRONMENT: str = "development"
    MONGODB_URI: str = "mongodb+srv://placeholder:placeholder@cluster.mongodb.net/?retryWrites=true&w=majority"
    MONGODB_DATABASE: str = "sentiview_db"
    MODEL_PATH: str = "ml/artifacts/sentiment_model.joblib"
    VECTORIZER_PATH: str = "ml/artifacts/tfidf_vectorizer.joblib"
    METADATA_PATH: str = "ml/artifacts/model_metadata.json"
    CORS_ORIGINS: str = "http://localhost:5173"
    MAX_UPLOAD_SIZE_MB: int = 25
    COMMENT_COLUMN: str = "comment_text"
    SENTIMENT_COLUMN: str = "label_sentiment"

    class Config:
        env_file = ".env"

settings = Settings()
