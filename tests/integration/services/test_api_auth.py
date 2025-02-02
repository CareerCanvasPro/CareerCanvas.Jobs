import pytest
from httpx import AsyncClient
from services.job_api.main import app

@pytest.mark.asyncio
async def test_api_auth():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Test without API key
        response = await client.get("/api/v1/jobs")
        assert response.status_code == 403
        
        # Test with invalid API key
        response = await client.get(
            "/api/v1/jobs",
            headers={"X-API-Key": "invalid_key"}
        )
        assert response.status_code == 403
        
        # Test with valid API key
        response = await client.get(
            "/api/v1/jobs",
            headers={"X-API-Key": "test_api_key"}
        )
        assert response.status_code == 200