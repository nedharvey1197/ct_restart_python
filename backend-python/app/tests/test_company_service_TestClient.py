import pytest
from bson import ObjectId
from ..models.company import Company
from ..services.company_service import CompanyService

def test_create_company(test_client):
    company_data = {
        "name": "Test Company",
        "description": "A test company",
        "website": "https://testcompany.com",
        "industry": "Healthcare",
        "founded_year": 2020,
        "headquarters": "Test City, Test Country",
        "size": "1-10 employees",
        "status": "Active"
    }
    
    response = test_client.post("/api/companies", json=company_data)
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["name"] == company_data["name"]
    assert data["description"] == company_data["description"]
    return data["_id"]

def test_get_company(test_client):
    company_id = test_create_company(test_client)
    response = test_client.get(f"/api/companies/{company_id}")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["name"] == "Test Company"
    assert data["description"] == "A test company"

def pytest_collection_modifyitems(config, items):
    """Modify test collection to exclude future tests by default."""
    if not os.getenv("INCLUDE_FUTURE_TESTS"):
        for item in items:
            if "future_concepts" in str(item.fspath):
                item.add_marker(pytest.mark.skip(reason="Future functionality tests not enabled"))