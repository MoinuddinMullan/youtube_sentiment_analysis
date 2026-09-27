import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.services.model_service import model_service

@pytest.mark.asyncio
async def test_predict_returns_503_when_model_not_loaded():
    """Should return 503 if model is not loaded."""
    # Save current state
    was_loaded = model_service.is_loaded
    model_service.is_loaded = False
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/predict", json={"text": "Great video!"})
    
    model_service.is_loaded = was_loaded
    assert response.status_code == 503

@pytest.mark.asyncio
async def test_predict_requires_text():
    """Should return 422 for empty text."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/predict", json={"text": ""})
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_batch_predict_empty_list():
    """Should return 422 for empty comments list."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/predict/batch", json={"comments": []})
    assert response.status_code == 422
