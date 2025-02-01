import pytest
import logging
from fastapi.testclient import TestClient
from ..main import app  # Ensure this import points to your FastAPI app

# Configure logging
logging.basicConfig(level=logging.INFO)
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
    response = client.post("/api/companies", json={"name": "Test Company"})
    logger.info(f"Response status code: {response.status_code}")
    assert response.status_code == 200
    data = response.json()
    logger.info(f"Response data: {data}")
    assert data["name"] == "Test Company"

def test_get_company(client):
    logger.info("Starting test_get_company")
    response = client.post("/api/companies", json=SAMPLE_COMPANY)
    company_id = response.json()["data"]["_id"]
    logger.info(f"Created company ID: {company_id}")
    response = client.get(f"/api/companies/{company_id}")
    logger.info(f"Response status code: {response.status_code}")
    assert response.status_code == 200
    data = response.json()["data"]
    logger.info(f"Response data: {data}")
    assert data["name"] == "Test Company"
    assert data["description"] == "A test company"