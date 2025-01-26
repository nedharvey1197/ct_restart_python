import pytest
from httpx import AsyncClient
from ..main import app
from datetime import datetime
from ..models.trial import ClinicalTrial, ProtocolSection

@pytest.fixture
def sample_trial_data():
    return {
        "protocolSection": {
            "identificationModule": {
                "nctId": "NCT00000000",
                "briefTitle": "Test Trial"
            },
            "statusModule": {
                "overallStatus": "Recruiting",
                "startDateStruct": {"date": "2023-01-01"}
            },
            "designModule": {
                "phases": ["Phase 1"],
                "enrollmentInfo": {"count": 100}
            },
            "conditionsModule": {
                "conditions": ["Cancer"]
            }
        }
    }

@pytest.mark.asyncio
async def test_trial_analysis_flow(test_client: AsyncClient, test_db):
    # First create a company
    company_data = {"name": "Test Company"}
    company_response = await test_client.post("/api/companies", json=company_data)
    company_id = company_response.json()["id"]

    # Save trial analysis
    trials_data = [sample_trial_data()]
    response = await test_client.post(
        f"/api/companies/{company_id}/trials",
        json=trials_data
    )
    assert response.status_code == 200
    
    # Verify analytics
    analytics = response.json()["data"]["trialAnalytics"]
    assert analytics["totalTrials"] == 1
    assert analytics["phaseDistribution"]["Phase 1"] == 1
    assert analytics["statusSummary"]["Recruiting"] == 1
    assert analytics["therapeuticAreas"]["Cancer"] == 1

@pytest.mark.asyncio
async def test_save_trial_analysis():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Test data
        analysis_data = {
            "studies": [],
            "analytics": {
                "phaseDistribution": {"Phase 1": 1},
                "statusSummary": {"Completed": 1},
                "therapeuticAreas": {"Oncology": 1},
                "totalTrials": 1
            },
            "companyName": "Test Company",
            "queryDate": datetime.utcnow().isoformat()
        }

        response = await client.post(
            "/api/companies/123/trials",
            json=analysis_data
        )
        assert response.status_code == 200
        assert "trialAnalytics" in response.json()["data"]

@pytest.mark.asyncio
async def test_generic_trial_analysis(test_client: AsyncClient, sample_trials):
    """Test generic trial analysis without company association."""
    response = await test_client.post(
        "/api/trials/analyze",
        json={
            "trials": sample_trials,
            "options": {
                "include_detailed_enrollment": True,
                "categorize_conditions": True
            }
        }
    )
    assert response.status_code == 200
    analytics = response.json()["data"]
    assert "phaseDistribution" in analytics
    assert "therapeuticAreas" in analytics

@pytest.mark.asyncio
async def test_company_trial_analysis(test_client: AsyncClient, test_db, sample_trials):
    """Test company-specific trial analysis and storage."""
    # First create a company
    company_data = {"name": "Test Company"}
    company_response = await test_client.post("/api/companies", json=company_data)
    company_id = company_response.json()["id"]

    # Save and analyze trials for company
    response = await test_client.post(
        f"/api/companies/{company_id}/trials",
        json={
            "trials": sample_trials,
            "options": {
                "include_historical": True
            }
        }
    )
    assert response.status_code == 200
    assert "trialAnalytics" in response.json()["data"] 