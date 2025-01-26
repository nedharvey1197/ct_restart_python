import pytest
from httpx import AsyncClient
from ..models.company import Company

@pytest.mark.asyncio
async def test_company_crud_operations(test_client: AsyncClient, test_db):
    # Create company
    company_data = {
        "name": "Test Company",
        "website": "https://test.com"
    }
    response = await test_client.post("/api/companies", json=company_data)
    assert response.status_code == 201
    
    # Get company
    company_id = response.json()["id"]
    response = await test_client.get(f"/api/companies/{company_id}")
    assert response.status_code == 200 