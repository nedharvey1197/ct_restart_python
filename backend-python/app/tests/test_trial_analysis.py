"""
Tests for current trial functionality using CompanyTrialService.

This test file focuses on the current production functionality for managing company trials
and basic analytics. For future/planned functionality tests, see tests/future_concepts/.
"""

import pytest
from ..models.trial import ClinicalTrial, TrialAnalysis
from .fixtures.load_real_data import get_sample_analysis
from httpx import AsyncClient
from datetime import datetime
from ..services.trial_service import CompanyTrialService

@pytest.mark.asyncio
async def test_save_company_trials(test_client: AsyncClient, setup_company):
    """Test saving trials for a company using CompanyTrialService."""
    company_id = setup_company
    
    # Get real analysis data
    analysis_data = await get_sample_analysis()
    assert analysis_data is not None, "No sample data found in database"
    
    # Save analysis using CompanyTrialService
    response = await test_client.post(
        f"/api/companies/{company_id}/trials",
        json={"trials": analysis_data["studies"]}
    )
    assert response.status_code == 200
    
    # Verify saved data
    get_response = await test_client.get(f"/api/companies/{company_id}/trials")
    saved_data = get_response.json()["data"]
    assert len(saved_data) == len(analysis_data["studies"])

@pytest.mark.asyncio
async def test_get_company_trials(test_client: AsyncClient, setup_company):
    """Test retrieving trials for a company."""
    company_id = setup_company
    
    # First save some trials
    analysis_data = await get_sample_analysis()
    await test_client.post(
        f"/api/companies/{company_id}/trials",
        json={"trials": analysis_data["studies"]}
    )
    
    # Test getting trials
    response = await test_client.get(f"/api/companies/{company_id}/trials")
    assert response.status_code == 200
    data = response.json()["data"]
    assert "trials" in data
    assert "analytics" in data
    assert "updated_at" in data

@pytest.mark.asyncio
async def test_get_trial_details(test_client: AsyncClient, setup_company):
    """Test retrieving details for a specific trial."""
    company_id = setup_company
    
    # First save some trials
    analysis_data = await get_sample_analysis()
    await test_client.post(
        f"/api/companies/{company_id}/trials",
        json={"trials": analysis_data["studies"]}
    )
    
    # Get first trial's NCT ID
    first_trial = analysis_data["studies"][0]
    nct_id = first_trial["nctId"]
    
    # Test getting trial details
    response = await test_client.get(f"/api/companies/{company_id}/trials/{nct_id}")
    assert response.status_code == 200
    trial_data = response.json()["data"]
    assert trial_data["nctId"] == nct_id

@pytest.mark.asyncio
async def test_save_trial_analysis(test_client: AsyncClient, setup_company):
    """Test saving trial analysis using CompanyTrialService."""
    company_id = setup_company
    
    # Create analysis data matching current production structure
    analysis_data = {
        "studies": [
            {
                "nctId": "NCT00000000",
                "protocolSection": {
                    "identificationModule": {
                        "briefTitle": "Test Trial"
                    },
                    "statusModule": {
                        "overallStatus": "Completed"
                    },
                    "designModule": {
                        "phases": ["Phase 1"]
                    }
                }
            }
        ],
        "analytics": {
            "phase_distribution": {"Phase 1": 1},
            "status_summary": {"Completed": 1},
            "therapeutic_areas": {},
            "total_trials": 1,
            "enrollment_stats": {
                "total": 0,
                "average": 0,
                "median": 0
            }
        },
        "companyName": "Test Company",
        "queryDate": datetime.utcnow().isoformat()
    }
    
    # Validate test data against model
    analysis = TrialAnalysis(**analysis_data)
    
    # Save using CompanyTrialService endpoint
    response = await test_client.post(
        f"/api/companies/{company_id}/trials/analysis",
        json=analysis.model_dump()
    )
    assert response.status_code == 200
    result = response.json()["data"]
    
    # Verify structure matches CompanyTrialService format
    assert "trialAnalytics" in result
    assert "lastAnalyzed" in result
    assert result["success"] is True

@pytest.mark.asyncio
async def test_update_trial_analysis(test_client: AsyncClient, setup_company):
    """Test updating existing trial analysis."""
    company_id = setup_company
    
    # First save initial analysis
    analysis_data = await get_sample_analysis()
    await test_client.post(
        f"/api/companies/{company_id}/trials/analysis",
        json=analysis_data
    )
    
    # Update with new analysis
    updated_analysis = analysis_data.copy()
    updated_analysis["analytics"]["phase_distribution"]["Phase 2"] = 1
    
    response = await test_client.put(
        f"/api/companies/{company_id}/trials/analysis",
        json=updated_analysis
    )
    assert response.status_code == 200
    
    # Verify update
    get_response = await test_client.get(f"/api/companies/{company_id}/trials/analytics")
    updated_data = get_response.json()["data"]
    assert updated_data["trialAnalytics"]["phase_distribution"]["Phase 2"] == 1 