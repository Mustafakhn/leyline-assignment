import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "version" in data
    assert "date" in data
    assert "kubernetes" in data

@pytest.mark.asyncio
async def test_metrics():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/metrics")
    assert response.status_code == 200
    assert "histogram" in response.text
