import pytest
import logging
from fastapi.testclient import TestClient
from ..main import app  # Ensure this import points to your FastAPI app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

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

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

def test_create_company(client):
    logger.info("Starting test_create_company")
    response = client.post("/api/companies", json=SAMPLE_COMPANY)
    logger.info(f"Response JSON: {response.json()}")
    assert response.status_code == 201
    company_id = response.json().get("id")
    assert company_id is not None
    logger.info(f"Created company ID: {company_id}")

def test_get_company(client):
    logger.info("Starting test_get_company")
    response = client.post("/api/companies", json=SAMPLE_COMPANY)
    company_id = response.json().get("id")
    response = client.get(f"/api/companies/{company_id}")
    logger.info(f"Response status code: {response.status_code}")
    assert response.status_code == 200
    data = response.json()
    logger.info(f"Response data: {data}")
    assert data["name"] == SAMPLE_COMPANY["name"]
    assert data["description"] == SAMPLE_COMPANY["description"]

def test_update_company(client):
    logger.info("Starting test_update_company")
    response = client.post("/api/companies", json=SAMPLE_COMPANY)
    company_id = response.json().get("id")
    updated_data = SAMPLE_COMPANY.copy()
    updated_data["description"] = "An updated test company"
    response = client.put(f"/api/companies/{company_id}", json=updated_data)
    logger.info(f"Response status code: {response.status_code}")
    assert response.status_code == 200
    data = response.json()
    logger.info(f"Response data: {data}")
    assert data["description"] == "An updated test company"

def test_delete_company(client):
    logger.info("Starting test_delete_company")
    response = client.post("/api/companies", json=SAMPLE_COMPANY)
    company_id = response.json().get("id")
    response = client.delete(f"/api/companies/{company_id}")
    logger.info(f"Response status code: {response.status_code}")
    assert response.status_code == 200
    message = response.json().get("message")
    assert message == "Company deleted successfully"