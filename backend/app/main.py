from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .config import settings
from .database import connect_db, close_db
from .routes import health, prediction, analysis
from .services.model_service import model_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    model_service.load_model()
    yield
    await close_db()

app = FastAPI(
    title="Sentiview AI API",
    description="YouTube Comment Sentiment Analysis API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(prediction.router, prefix="/api", tags=["Prediction"])
app.include_router(analysis.router, prefix="/api", tags=["Analysis"])

@app.get("/")
async def root():
    return {"message": "Sentiview AI API", "docs": "/docs", "health": "/api/health"}
