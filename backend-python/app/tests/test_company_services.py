import pytest
from httpx import AsyncClient
from ..models.company import Company
from ..services.company_service import CompanyService
from ..main import app  # Ensure this import points to your FastAPI app
from fastapi.testclient import TestClient
from fastapi.lifespan import LifespanManager

SAMPLE_COMPANY = {
    "name": "Test Company",
    "description": "A test company",
    "website": "https://testcompany.com",
    "industry": "Healthcare",
    "founded_year": 2020,
    "headquarters": "Test City, Test Country",
    "size": "1-10 employees",
    "status": "Active"
}

@pytest.mark.asyncio
async def test_create_company():
    async with AsyncClient(base_url="http://testserver") as async_client:
        async with LifespanManager(app):
            response = await async_client.post("/api/companies", json=SAMPLE_COMPANY)
            assert response.status_code == 200
            data = response.json()["data"]
            assert data["name"] == SAMPLE_COMPANY["name"]
            assert data["description"] == SAMPLE_COMPANY["description"]
            return data["_id"]

@pytest.mark.asyncio
async def test_get_company():
    async with AsyncClient(base_url="http://testserver") as async_client:
        async with LifespanManager(app):
            company_id = await test_create_company()
            response = await async_client.get(f"/api/companies/{company_id}")
            assert response.status_code == 200
            data = response.json()["data"]
            assert data["name"] == "Test Company"
            assert data["description"] == "A test company"