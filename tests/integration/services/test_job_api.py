import pytest
from httpx import AsyncClient
from services.job_api.main import app

@pytest.mark.asyncio
async def test_get_jobs():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/jobs")
        assert response.status_code == 200
        assert "items" in response.json()

@pytest.mark.asyncio
async def test_get_job_by_id():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/jobs/1")
        assert response.status_code in [200, 404]

@pytest.mark.asyncio
async def test_search_jobs():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/jobs", params={
            "keyword": "python",
            "location": "Remote",
            "job_type": "FULL_TIME"
        })
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data

@pytest.mark.asyncio
async def test_invalid_job_search():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/jobs", params={
            "page": -1,
            "limit": 1000
        })
        assert response.status_code == 422