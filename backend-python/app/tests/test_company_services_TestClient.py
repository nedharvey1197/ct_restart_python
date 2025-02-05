import pytest
from fastapi.testclient import TestClient
from ..main import app  # Ensure this import points to your FastAPI app

SAMPLE_ENHANCED_COMPANY = {
    "name": "Test Company",
    "description": "A test company",
    "website": "https://testcompany.com",
    "industry": "Healthcare",
    "founded_year": 2020,
    "headquarters": "Test City, Test Country",
    "size": "1-10 employees",
    "status": "Active",
    "company_identifiers": {"tax_id": "123456789"},
    "profile": {"mission": "To provide healthcare solutions"}
}

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

def test_create_enhanced_company(client):
    response = client.post("/api/companies", json=SAMPLE_ENHANCED_COMPANY)
    assert response.status_code == 201
    company_id = response.json().get("id")
    assert company_id is not None

def test_get_enhanced_company(client):
    response = client.post("/api/companies", json=SAMPLE_ENHANCED_COMPANY)
    company_id = response.json().get("id")
    response = client.get(f"/api/companies/{company_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == SAMPLE_ENHANCED_COMPANY["name"]
    
    '''
def test_create_company(client):
    response = client.post("/api/companies", json=SAMPLE_ENHANCED_COMPANY)
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["name"] == SAMPLE_ENHANCED_COMPANY["name"]
    assert data["description"] == SAMPLE_ENHANCED_COMPANY["description"]

def test_get_company(client):
    response = client.post("/api/companies", json=SAMPLE_ENHANCED_COMPANY)
    company_id = response.json()["data"]["_id"]
    response = client.get(f"/api/companies/{company_id}")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["name"] == "Test Company"
    assert data["description"] == "A test company"
'''