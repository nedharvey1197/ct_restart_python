import pytest
from httpx import AsyncClient
from .fixtures.trial_data import SAMPLE_TRIAL, SAMPLE_COMPANY
from ..services.cache_service import CacheService

@pytest.fixture
async def setup_company(test_client: AsyncClient):
    """Create a test company and return its ID."""
    response = await test_client.post("/api/companies", json={"name": "Test Co"})
    return response.json()["id"]

@pytest.mark.asyncio
async def test_trial_flow(test_client: AsyncClient, setup_company):
    company_id = setup_company
    
    # Test saving trials
    trials_response = await test_client.post(
        f"/api/trials/companies/{company_id}/trials",
        json=[SAMPLE_TRIAL]
    )
    assert trials_response.status_code == 200
    assert trials_response.json()["data"]["count"] == 1
    
    # Test getting trials (should be cached)
    get_response = await test_client.get(f"/api/trials/companies/{company_id}/trials")
    assert get_response.status_code == 200
    assert len(get_response.json()["data"]) == 1
    assert get_response.json().get("cached") is True
    
    # Test getting single trial
    trial_response = await test_client.get(
        f"/api/trials/{SAMPLE_TRIAL['nctId']}"
    )
    assert trial_response.status_code == 200
    assert trial_response.json()["data"]["nctId"] == SAMPLE_TRIAL["nctId"]

@pytest.mark.asyncio
async def test_cache_invalidation(test_client: AsyncClient, setup_company):
    company_id = setup_company
    cache_service = CacheService()
    
    # Save initial trials
    await test_client.post(
        f"/api/trials/companies/{company_id}/trials",
        json=[SAMPLE_TRIAL]
    )
    
    # Verify cache exists
    cached = await cache_service.get_trials(company_id)
    assert cached is not None
    
    # Update trials
    new_trial = {**SAMPLE_TRIAL, "nctId": "NCT00000001"}
    await test_client.post(
        f"/api/trials/companies/{company_id}/trials",
        json=[new_trial]
    )
    
    # Verify cache was updated
    updated_cache = await cache_service.get_trials(company_id)
    assert len(updated_cache) == 1
    assert updated_cache[0]["nctId"] == "NCT00000001" 