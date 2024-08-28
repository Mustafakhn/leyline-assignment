import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_lookup():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/v1/tools/lookup?domain=example.com")
    assert response.status_code == 200
    data = response.json()
    assert "ipv4_addresses" in data
    assert len(data["ipv4_addresses"]) > 0