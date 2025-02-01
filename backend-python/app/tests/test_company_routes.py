"""Tests for company routes with schema validation and context management."""

import pytest
from httpx import AsyncClient
from datetime import datetime
from ..main import app
from ..models.company import Company
from ..models.trial import Trial
from ..services.schema_service import SchemaService
from ..system_specs.schema_manager import SchemaContext
from ..config.database import MongoDB
from bson import ObjectId
import json
import time
import asyncio

# Test data
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
async def setup_test_data():
    """Setup test data in MongoDB."""
    company_id = str(ObjectId())
    async with MongoDB.get_collection("companies") as collection:
        await collection.delete_many({})  # Clear existing data
        await collection.insert_one({
            "_id": ObjectId(company_id),
            **SAMPLE_COMPANY
        })
    yield company_id
    # Cleanup
    async with MongoDB.get_collection("companies") as collection:
        await collection.delete_many({})

@pytest.mark.asyncio
async def test_create_company(test_client: AsyncClient):
    """Test company creation endpoint."""
    response = await test_client.post("/api/companies", json=SAMPLE_COMPANY)
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["name"] == SAMPLE_COMPANY["name"]
    assert data["description"] == SAMPLE_COMPANY["description"]
    return data["_id"]

@pytest.mark.asyncio
async def test_get_company(test_client: AsyncClient):
    """Test getting company details."""
    company_id = await test_create_company(test_client)
    response = await test_client.get(f"/api/companies/{company_id}")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["name"] == SAMPLE_COMPANY["name"]
    assert data["description"] == SAMPLE_COMPANY["description"]

@pytest.mark.asyncio
async def test_update_company(test_client: AsyncClient):
    """Test updating company details."""
    company_id = await test_create_company(test_client)
    updated_data = SAMPLE_COMPANY.copy()
    updated_data["name"] = "Updated Company Name"
    
    response = await test_client.put(f"/api/companies/{company_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["name"] == updated_data["name"]

@pytest.mark.asyncio
async def test_delete_company(test_client: AsyncClient):
    """Test deleting a company."""
    company_id = await test_create_company(test_client)
    response = await test_client.delete(f"/api/companies/{company_id}")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["success"] is True

@pytest.mark.asyncio
async def test_list_companies(test_client: AsyncClient):
    """Test listing all companies."""
    # Create a test company first
    await test_create_company(test_client)
    
    response = await test_client.get("/api/companies")
    assert response.status_code == 200
    data = response.json()["data"]
    assert isinstance(data, list)
    assert len(data) > 0

@pytest.mark.asyncio
async def test_get_current_company(test_client: AsyncClient, setup_test_data):
    """Test getting current company with schema validation."""
    response = await test_client.get("/api/companies/current")
    assert response.status_code == 200
    data = response.json()["data"]
    assert "name" in data
    assert "profile" in data
    assert "trial_analytics" in data

@pytest.mark.asyncio
async def test_invalid_company_schema(test_client: AsyncClient):
    """Test handling of invalid company schema."""
    invalid_company = {
        "name": "",  # Invalid empty name
        "profile": {
            "size": "Invalid Size"  # Invalid size value
        }
    }
    response = await test_client.post(
        "/api/companies",
        json=invalid_company
    )
    assert response.status_code == 400
    assert "validation" in response.json()["detail"].lower()

@pytest.mark.asyncio
async def test_company_migration(test_client: AsyncClient):
    """Test company schema migration."""
    legacy_company = {
        "companyName": "Legacy Company",  # Old field name
        "companyWebsite": "https://legacy.com",
        "companySize": "Small",
        "therapeuticAreas": ["Oncology"],
        "lastAnalyzed": datetime.utcnow().isoformat()
    }
    
    # Insert legacy company
    company_id = str(ObjectId())
    async with MongoDB.get_collection("companies") as collection:
        await collection.insert_one({
            "_id": ObjectId(company_id),
            **legacy_company
        })
    
    # Try to get it (should trigger migration)
    response = await test_client.get(f"/api/companies/{company_id}")
    assert response.status_code == 200
    data = response.json()["data"]
    
    # Verify migrated format
    assert data["name"] == legacy_company["companyName"]  # Migrated field
    assert data["company_identifiers"]["website"] == legacy_company["companyWebsite"]
    assert data["profile"]["size"] == legacy_company["companySize"]
    assert data["profile"]["therapeutic_areas"] == legacy_company["therapeuticAreas"]

@pytest.mark.asyncio
async def test_company_validation_rules(test_client: AsyncClient):
    """Test specific company validation rules."""
    invalid_cases = [
        # Test invalid website format
        {
            **SAMPLE_COMPANY,
            "company_identifiers": {"website": "not-a-url"}
        },
        # Test invalid therapeutic areas
        {
            **SAMPLE_COMPANY,
            "profile": {**SAMPLE_COMPANY["profile"], "therapeutic_areas": ["Invalid Area"]}
        },
        # Test invalid analytics format
        {
            **SAMPLE_COMPANY,
            "trial_analytics": {
                "phase_distribution": {"Invalid Phase": 1}
            }
        }
    ]
    
    for invalid_case in invalid_cases:
        response = await test_client.post(
            "/api/companies",
            json=invalid_case
        )
        assert response.status_code == 400
        assert "validation" in response.json()["detail"].lower()

@pytest.mark.asyncio
async def test_company_relationships(test_client: AsyncClient, setup_test_data):
    """Test company relationship operations."""
    company_id = await setup_test_data
    relationship_data = {
        "target_company_id": str(ObjectId()),
        "relationship_type": "COMPETITOR",
        "properties": {
            "market_overlap": 0.75,
            "therapeutic_areas": ["Oncology"]
        }
    }
    
    # Create relationship
    response = await test_client.post(
        f"/api/companies/{company_id}/relationships",
        json=relationship_data
    )
    assert response.status_code == 200
    
    # Get relationships
    response = await test_client.get(f"/api/companies/{company_id}/relationships")
    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data) > 0
    assert data[0]["relationship_type"] == "COMPETITOR"

@pytest.mark.asyncio
async def test_error_handling(test_client: AsyncClient, setup_test_data):
    """Test error handling in company routes."""
    # Test invalid company ID
    response = await test_client.get("/api/companies/invalid_id")
    assert response.status_code == 404
    
    # Test duplicate company name
    await setup_test_data
    response = await test_client.post(
        "/api/companies",
        json=SAMPLE_COMPANY
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"].lower()

# Helper functions for tests
async def create_test_company():
    """Create a test company with valid schema."""
    return Company(**SAMPLE_COMPANY)

async def verify_company_schema(company_data: dict) -> bool:
    """Verify company data against current schema context."""
    context = await SchemaService.get_collection_context("companies")
    return await SchemaService.validate_document("companies", company_data, context)

@pytest.mark.asyncio
async def test_company_trial_integration(test_client: AsyncClient):
    """Test integration between company and trial routes."""
    # Create a new company
    company_data = {
        "name": "Integration Test Company",
        "company_identifiers": {
            "website": "https://integration-test.com"
        },
        "profile": {
            "size": "Small",
            "therapeutic_areas": ["Oncology"]
        }
    }
    
    company_response = await test_client.post(
        "/api/companies",
        json=company_data
    )
    assert company_response.status_code == 200
    company_id = company_response.json()["data"]["_id"]
    
    # Add trials to the company
    trial_data = {
        "trials": [{
            "nct_id": "NCT_INT_TEST",
            "title": "Integration Test Trial",
            "status": "Recruiting",
            "phases": ["Phase 1"],
            "conditions": ["Test Condition"],
            "enrollment_info": {"target": 100}
        }]
    }
    
    trial_response = await test_client.post(
        f"/api/companies/{company_id}/trials",
        json=trial_data
    )
    assert trial_response.status_code == 200
    
    # Verify company has updated trial analytics
    company_get_response = await test_client.get(f"/api/companies/{company_id}")
    assert company_get_response.status_code == 200
    company_data = company_get_response.json()["data"]
    assert "trial_analytics" in company_data
    assert company_data["trial_analytics"]["total_trials"] == 1
    
    # Verify trials can be retrieved
    trials_response = await test_client.get(f"/api/companies/{company_id}/trials")
    assert trials_response.status_code == 200
    trials = trials_response.json()["data"]
    assert len(trials) == 1
    assert trials[0]["nct_id"] == "NCT_INT_TEST"

@pytest.mark.asyncio
async def test_company_trial_relationship_sync(test_client: AsyncClient):
    """Test synchronization between company and trial data."""
    # Create company with initial trial
    company_data = {
        "name": "Sync Test Company",
        "company_identifiers": {"website": "https://sync-test.com"},
        "profile": {
            "size": "Medium",
            "therapeutic_areas": ["Cardiology"]
        }
    }
    
    company_response = await test_client.post("/api/companies", json=company_data)
    company_id = company_response.json()["data"]["_id"]
    
    # Add trial through trial routes
    trial_data = {
        "nct_id": "NCT_SYNC_TEST",
        "title": "Sync Test Trial",
        "status": "Active",
        "phases": ["Phase 2"],
        "conditions": ["Heart Disease"],
        "enrollment_info": {"target": 200}
    }
    
    async with MongoDB.get_collection("trials") as collection:
        await collection.insert_one({
            **trial_data,
            "company_id": company_id
        })
    
    # Verify company analytics updated
    company_get_response = await test_client.get(f"/api/companies/{company_id}")
    company_data = company_get_response.json()["data"]
    assert "trial_analytics" in company_data
    assert "Cardiology" in company_data["trial_analytics"]["therapeutic_areas"]
    
    # Update trial status
    trial_update = {
        "status": "Completed"
    }
    await test_client.patch(f"/api/companies/{company_id}/trials/NCT_SYNC_TEST", json=trial_update)
    
    # Verify company analytics reflect the change
    updated_company = (await test_client.get(f"/api/companies/{company_id}")).json()["data"]
    assert "Completed" in updated_company["trial_analytics"]["status_summary"]

@pytest.mark.asyncio
async def test_schema_validation_performance():
    """Test performance of schema validation operations."""
    # Create test data
    test_companies = [
        {
            "name": f"Performance Test Company {i}",
            "company_identifiers": {"website": f"https://perf-test-{i}.com"},
            "profile": {
                "size": "Large",
                "therapeutic_areas": ["Oncology", "Neurology"]
            }
        } for i in range(10)  # Test with 10 companies
    ]
    
    # Measure validation time
    start_time = time.time()
    context = await SchemaService.get_collection_context("companies")
    
    validation_times = []
    for company in test_companies:
        validation_start = time.time()
        is_valid = await SchemaService.validate_document("companies", company, context)
        validation_times.append(time.time() - validation_start)
        assert is_valid
    
    total_time = time.time() - start_time
    avg_validation_time = sum(validation_times) / len(validation_times)
    
    # Assert reasonable performance (adjust thresholds as needed)
    assert avg_validation_time < 0.1  # Average validation should be under 100ms
    assert total_time < 2.0  # Total operation should be under 2 seconds

@pytest.mark.asyncio
async def test_schema_migration_performance(test_client: AsyncClient):
    """Test performance of schema migration operations."""
    # Create legacy format test data
    legacy_companies = [
        {
            "companyName": f"Legacy Company {i}",
            "companyWebsite": f"https://legacy-{i}.com",
            "companySize": "Small",
            "therapeuticAreas": ["Oncology"],
            "lastAnalyzed": datetime.utcnow().isoformat()
        } for i in range(5)  # Test with 5 companies
    ]
    
    # Insert legacy data
    company_ids = []
    async with MongoDB.get_collection("companies") as collection:
        for company in legacy_companies:
            result = await collection.insert_one(company)
            company_ids.append(str(result.inserted_id))
    
    # Measure migration performance
    start_time = time.time()
    migration_times = []
    
    for company_id in company_ids:
        migration_start = time.time()
        response = await test_client.get(f"/api/companies/{company_id}")
        assert response.status_code == 200
        migration_times.append(time.time() - migration_start)
        
        # Verify migration success
        migrated_data = response.json()["data"]
        assert "name" in migrated_data  # New schema field
        assert "company_identifiers" in migrated_data  # New schema structure
    
    total_time = time.time() - start_time
    avg_migration_time = sum(migration_times) / len(migration_times)
    
    # Assert reasonable performance (adjust thresholds as needed)
    assert avg_migration_time < 0.2  # Average migration should be under 200ms
    assert total_time < 3.0  # Total operation should be under 3 seconds
    
    # Cleanup
    async with MongoDB.get_collection("companies") as collection:
        await collection.delete_many({"_id": {"$in": [ObjectId(id) for id in company_ids]}})

@pytest.mark.asyncio
async def test_concurrent_schema_operations():
    """Test performance of concurrent schema validation and migration."""
    # Create mixed test data (both current and legacy format)
    test_data = [
        # Current format
        {
            "name": "Concurrent Test Company 1",
            "company_identifiers": {"website": "https://concurrent-1.com"},
            "profile": {"size": "Large", "therapeutic_areas": ["Oncology"]}
        },
        # Legacy format
        {
            "companyName": "Legacy Concurrent Company",
            "companyWebsite": "https://legacy-concurrent.com",
            "companySize": "Medium",
            "therapeuticAreas": ["Cardiology"]
        }
    ]
    
    # Test concurrent operations
    start_time = time.time()
    
    async def process_company(company_data):
        context = await SchemaService.get_collection_context("companies")
        if await SchemaService.validate_document("companies", company_data, context):
            return company_data
        else:
            return await SchemaService.migrate_document(
                collection_name="companies",
                document=company_data,
                from_context=SchemaContext.LEGACY,
                to_context=context
            )
    
    tasks = [process_company(company) for company in test_data]
    results = await asyncio.gather(*tasks)
    
    total_time = time.time() - start_time
    
    # Verify results
    assert len(results) == len(test_data)
    for result in results:
        assert "name" in result  # All should be in current format
        assert "company_identifiers" in result
    
    # Assert reasonable performance
    assert total_time < 1.0  # Concurrent operations should complete under 1 second

@pytest.mark.asyncio
async def test_company_routes(test_client: AsyncClient):
    """Test company routes using the async test client."""
    # Your test code here
    pass 