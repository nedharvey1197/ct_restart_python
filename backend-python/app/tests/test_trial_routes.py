"""Tests for trial routes with schema validation and context management."""

import pytest
from httpx import AsyncClient
from datetime import datetime
from ..main import app
from ..models.trial import Trial, TrialAnalytics
from ..services.schema_service import SchemaService
from ..system_specs.schema_manager import SchemaContext
from ..config.database import MongoDB
from bson import ObjectId
import json
import time
import asyncio

# Test data
SAMPLE_TRIAL = {
    "nct_id": "NCT12345678",
    "title": "Test Trial",
    "official_title": "Official Test Trial Title",
    "status": "Recruiting",
    "phases": ["Phase 1"],
    "study_type": "Interventional",
    "conditions": ["Test Condition"],
    "keywords": ["test", "trial"],
    "start_date": datetime.utcnow().isoformat(),
    "enrollment_info": {"target": 100},
    "organization": {"name": "Test Org"}
}

SAMPLE_COMPANY_ID = str(ObjectId())

@pytest.fixture
async def setup_test_data():
    """Setup test data in MongoDB."""
    async with MongoDB.get_collection("trials") as collection:
        await collection.delete_many({})  # Clear existing data
        await collection.insert_one({**SAMPLE_TRIAL, "company_id": SAMPLE_COMPANY_ID})
    
    async with MongoDB.get_collection("companies") as collection:
        await collection.delete_many({})
        await collection.insert_one({
            "_id": ObjectId(SAMPLE_COMPANY_ID),
            "name": "Test Company",
            "trials": [SAMPLE_TRIAL]
        })
    yield
    # Cleanup
    async with MongoDB.get_collection("trials") as collection:
        await collection.delete_many({})
    async with MongoDB.get_collection("companies") as collection:
        await collection.delete_many({})

@pytest.mark.asyncio
async def test_analyze_trials(setup_test_data, test_client: AsyncClient):
    """Test trial analysis endpoint."""
    response = await test_client.post(
        "/api/companies/analyze",
        json={"trials": [SAMPLE_TRIAL]}
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert "phase_distribution" in data
    assert "status_summary" in data
    assert data["total_trials"] == 1

'''@pytest.mark.asyncio
async def test_save_trial_analysis(setup_test_data):
    """Test saving trial analysis with schema validation."""
    analysis_data = {
        "studies": [SAMPLE_TRIAL],
        "analytics": {
            "phase_distribution": {"Phase 1": 1},
            "status_summary": {"Recruiting": 1},
            "therapeutic_areas": {},
            "total_trials": 1,
            "enrollment_stats": {
                "total": 100,
                "average": 100,
                "median": 100
            }
        }
    }
    
    response = client.post(
        f"/api/companies/{SAMPLE_COMPANY_ID}/analysis",
        json=analysis_data
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert "trials" in data
    assert "trial_analytics" in data
'''
@pytest.mark.asyncio
async def test_analyze_trials_background(setup_test_data, test_client: AsyncClient):
    """Test background trial analysis with schema validation."""
    response = await test_client.post(
        f"/api/companies/{SAMPLE_COMPANY_ID}/trials/analyze",
        json={"trials": [SAMPLE_TRIAL]}
    )
    assert response.status_code == 200
    data = response.json()
    assert "task_id" in data

'''@pytest.mark.asyncio
async def test_get_company_trials(setup_test_data):
    """Test getting company trials with schema validation."""
    response = client.get(f"/api/companies/{SAMPLE_COMPANY_ID}/trials")
    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data) > 0
    assert data[0]["nct_id"] == SAMPLE_TRIAL["nct_id"]



@pytest.mark.asyncio
async def test_save_company_trials(setup_test_data):
    """Test saving company trials with schema validation."""
    new_trial = {**SAMPLE_TRIAL, "nct_id": "NCT87654321"}
    response = client.post(
        f"/api/companies/{SAMPLE_COMPANY_ID}/trials",
        json={"trials": [new_trial]}
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert "trials" in data
    assert len(data["trials"]) == 1
'''
@pytest.mark.asyncio
async def test_get_trial(setup_test_data, test_client: AsyncClient):
    """Test getting trial by NCT ID with schema validation."""
    response = await test_client.get(f"/api/companies/{SAMPLE_TRIAL['nct_id']}")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["nct_id"] == SAMPLE_TRIAL["nct_id"]

@pytest.mark.asyncio
async def test_invalid_trial_schema(test_client: AsyncClient):
    """Test handling of invalid trial schema."""
    invalid_trial = {
        "nct_id": "NCT12345678",
        # Missing required fields
    }
    response = await test_client.post(
        f"/api/companies/{SAMPLE_COMPANY_ID}/trials",
        json={"trials": [invalid_trial]}
    )
    assert response.status_code == 400
    assert "Invalid trial data" in response.json()["detail"]

@pytest.mark.asyncio
async def test_trial_migration(setup_test_data, test_client: AsyncClient):
    """Test trial schema migration."""
    legacy_trial = {
        "nctId": "NCT12345678",  # Old field name
        "protocolSection": {
            "identificationModule": {
                "briefTitle": "Test Trial"
            },
            "statusModule": {
                "overallStatus": "Recruiting"
            }
        }
    }
    
    # Insert legacy trial
    async with MongoDB.get_collection("trials") as collection:
        await collection.insert_one({**legacy_trial, "company_id": SAMPLE_COMPANY_ID})
    
    # Try to get it (should trigger migration)
    response = await test_client.get(f"/api/companies/NCT12345678")
    assert response.status_code == 200
    data = response.json()["data"]
    
    # Verify migrated format
    assert "nct_id" in data  # New field name
    assert data["title"] == "Test Trial"  # Migrated field
    assert data["status"] == "Recruiting"  # Migrated field

@pytest.mark.asyncio
async def test_cache_handling(setup_test_data, test_client: AsyncClient):
    """Test trial caching functionality."""
    # First request (no cache)
    response1 = await test_client.get(f"/api/companies/{SAMPLE_COMPANY_ID}/trials")
    assert response1.status_code == 200
    assert not response1.json().get("cached", False)
    
    # Second request (should be cached)
    response2 = await test_client.get(f"/api/companies/{SAMPLE_COMPANY_ID}/trials")
    assert response2.status_code == 200
    assert response2.json().get("cached", False)

@pytest.mark.asyncio
async def test_error_handling(test_client: AsyncClient):
    """Test error handling in routes."""
    # Test invalid company ID
    response = await test_client.get("/api/companies/invalid_id/trials")
    assert response.status_code == 404
    
    # Test invalid trial data
    response = await test_client.post(
        f"/api/companies/{SAMPLE_COMPANY_ID}/trials",
        json={"trials": [{"invalid": "data"}]}
    )
    assert response.status_code == 400

# Helper functions for tests
async def create_test_trial():
    """Create a test trial with valid schema."""
    return Trial(**SAMPLE_TRIAL)

async def create_test_analytics():
    """Create test analytics data."""
    return TrialAnalytics(
        phase_distribution={"Phase 1": 1},
        status_summary={"Recruiting": 1},
        therapeutic_areas={},
        total_trials=1,
        enrollment_stats={
            "total": 100,
            "average": 100,
            "median": 100
        }
    )

@pytest.mark.asyncio
async def test_trial_company_integration(test_client: AsyncClient):
    """Test integration between trial operations and company updates."""
    # Create a test company first
    company_data = {
        "name": "Trial Integration Company",
        "company_identifiers": {"website": "https://trial-integration.com"},
        "profile": {"size": "Small", "therapeutic_areas": ["Oncology"]}
    }
    company_response = await test_client.post("/api/companies", json=company_data)
    company_id = company_response.json()["data"]["_id"]
    
    # Add multiple trials in batch
    batch_trials = [
        {
            "nct_id": f"NCT_BATCH_{i}",
            "title": f"Batch Trial {i}",
            "status": "Recruiting",
            "phases": ["Phase 1"],
            "conditions": ["Test Condition"],
            "enrollment_info": {"target": 100}
        } for i in range(3)
    ]
    
    # Test batch trial addition
    batch_response = await test_client.post(
        f"/api/companies/{company_id}/trials",
        json={"trials": batch_trials}
    )
    assert batch_response.status_code == 200
    
    # Verify company analytics updated for batch
    company_response = await test_client.get(f"/api/companies/{company_id}")
    company_data = company_response.json()["data"]
    assert company_data["trial_analytics"]["total_trials"] == 3
    
    # Test trial updates and company analytics sync
    trial_updates = [
        {"status": "Completed", "nct_id": "NCT_BATCH_0"},
        {"status": "Terminated", "nct_id": "NCT_BATCH_1"},
        {"status": "Active", "nct_id": "NCT_BATCH_2"}
    ]
    
    for update in trial_updates:
        response = await test_client.patch(
            f"/api/companies/{company_id}/trials/{update['nct_id']}",
            json=update
        )
        assert response.status_code == 200
    
    # Verify company analytics reflect all updates
    updated_company = await test_client.get(f"/api/companies/{company_id}").json()["data"]
    status_summary = updated_company["trial_analytics"]["status_summary"]
    assert status_summary["Completed"] == 1
    assert status_summary["Terminated"] == 1
    assert status_summary["Active"] == 1

@pytest.mark.asyncio
async def test_trial_schema_performance():
    """Test performance of trial schema operations with company integration."""
    # Create test company
    company_response = await test_client.post("/api/companies", json={
        "name": "Trial Performance Company",
        "company_identifiers": {"website": "https://trial-perf.com"},
        "profile": {"size": "Medium", "therapeutic_areas": ["Oncology"]}
    })
    company_id = company_response.json()["data"]["_id"]
    
    # Create test trials
    test_trials = [
        {
            "nct_id": f"NCT_PERF_{i}",
            "title": f"Performance Trial {i}",
            "status": "Recruiting",
            "phases": ["Phase 1"],
            "conditions": ["Test Condition"],
            "enrollment_info": {"target": 100}
        } for i in range(20)  # Test with 20 trials
    ]
    
    # Measure batch validation and insertion performance
    start_time = time.time()
    context = await SchemaService.get_collection_context("trials")
    
    validation_times = []
    for trial in test_trials:
        validation_start = time.time()
        is_valid = await SchemaService.validate_document("trials", trial, context)
        validation_times.append(time.time() - validation_start)
        assert is_valid
    
    # Test batch insertion
    insertion_start = time.time()
    response = await test_client.post(
        f"/api/companies/{company_id}/trials",
        json={"trials": test_trials}
    )
    insertion_time = time.time() - insertion_start
    
    total_time = time.time() - start_time
    avg_validation_time = sum(validation_times) / len(validation_times)
    
    # Performance assertions
    assert avg_validation_time < 0.05  # Trial validation should be faster than company validation
    assert insertion_time < 2.0  # Batch insertion under 2 seconds
    assert total_time < 3.0  # Total operation under 3 seconds
    
    # Verify company analytics performance
    analytics_start = time.time()
    company_response = await test_client.get(f"/api/companies/{company_id}")
    analytics_time = time.time() - analytics_start
    
    assert analytics_time < 0.5  # Analytics calculation should be under 500ms
    assert company_response.json()["data"]["trial_analytics"]["total_trials"] == 20

@pytest.mark.asyncio
async def test_concurrent_trial_operations():
    """Test concurrent trial operations with company integration."""
    # Setup test company
    company_response = await test_client.post("/api/companies", json={
        "name": "Concurrent Trial Company",
        "company_identifiers": {"website": "https://concurrent-trials.com"},
        "profile": {"size": "Large", "therapeutic_areas": ["Oncology"]}
    })
    company_id = company_response.json()["data"]["_id"]
    
    # Create concurrent trial operations
    async def process_trial(trial_data):
        context = await SchemaService.get_collection_context("trials")
        # Validate and potentially migrate trial data
        if not await SchemaService.validate_document("trials", trial_data, context):
            trial_data = await SchemaService.migrate_document(
                collection_name="trials",
                document=trial_data,
                from_context=SchemaContext.LEGACY,
                to_context=context
            )
        # Insert trial
        async with MongoDB.get_collection("trials") as collection:
            await collection.insert_one({**trial_data, "company_id": company_id})
        return trial_data
    
    # Mix of current and legacy format trials
    test_trials = [
        # Current format
        {
            "nct_id": "NCT_CONCURRENT_1",
            "title": "Concurrent Trial 1",
            "status": "Recruiting",
            "phases": ["Phase 1"],
            "enrollment_info": {"target": 100}
        },
        # Legacy format
        {
            "nctId": "NCT_CONCURRENT_2",
            "briefTitle": "Legacy Concurrent Trial",
            "overallStatus": "Active",
            "phase": "Phase 2",
            "enrollment": 200
        }
    ]
    
    # Execute concurrent operations
    start_time = time.time()
    tasks = [process_trial(trial) for trial in test_trials]
    results = await asyncio.gather(*tasks)
    total_time = time.time() - start_time
    
    # Verify results
    assert len(results) == len(test_trials)
    for result in results:
        assert "nct_id" in result  # All should be in current format
        assert "status" in result
    
    # Performance assertions
    assert total_time < 1.0  # Concurrent operations should complete under 1 second
    
    # Verify company analytics updated correctly
    company_data = await test_client.get(f"/api/companies/{company_id}").json()["data"]
    assert company_data["trial_analytics"]["total_trials"] == len(test_trials)

@pytest.mark.asyncio
async def test_get_trial_analytics(test_client: AsyncClient):
    """Test getting trial analytics."""
    response = await test_client.get(f"/api/trials/{SAMPLE_TRIAL['nct_id']}/analytics")
    assert response.status_code == 200
    data = response.json()["data"]
    assert "phase_info" in data
    assert "status_info" in data

@pytest.mark.asyncio
async def test_get_trial_details(test_client: AsyncClient):
    """Test getting trial details."""
    response = await test_client.get(f"/api/trials/{SAMPLE_TRIAL['nct_id']}")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["nct_id"] == SAMPLE_TRIAL["nct_id"]
    assert data["title"] == SAMPLE_TRIAL["title"]

@pytest.mark.asyncio
async def test_update_trial_analytics(test_client: AsyncClient):
    """Test updating trial analytics."""
    analytics_data = {
        "phase_info": {"current_phase": "Phase 1"},
        "status_info": {"current_status": "Recruiting"},
        "last_updated": datetime.utcnow().isoformat()
    }
    
    response = await test_client.put(
        f"/api/trials/{SAMPLE_TRIAL['nct_id']}/analytics",
        json=analytics_data
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["phase_info"]["current_phase"] == analytics_data["phase_info"]["current_phase"]
    assert data["status_info"]["current_status"] == analytics_data["status_info"]["current_status"]

@pytest.mark.asyncio
async def test_get_company_trials(test_client: AsyncClient):
    """Test getting trials for a company."""
    response = await test_client.get(f"/api/companies/{SAMPLE_COMPANY_ID}/trials")
    assert response.status_code == 200
    data = response.json()["data"]
    assert isinstance(data, list)
    
@pytest.mark.asyncio
async def test_save_company_trials(test_client: AsyncClient):
    """Test saving trials for a company."""
    trials_data = {
        "company_id": SAMPLE_COMPANY_ID,
        "trials": [SAMPLE_TRIAL]
    }
    response = await test_client.post("/api/companies/trials", json=trials_data)
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["success"] is True
    assert data["count"] == 1 