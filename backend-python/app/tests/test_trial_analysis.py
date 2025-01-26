import pytest
from ..services.trial_analysis import TrialAnalyzer
from ..models.trial import ClinicalTrial
from .fixtures.load_real_data import get_sample_analysis
from fastapi.testclient import AsyncClient
from datetime import datetime

@pytest.fixture
def sample_trials():
    return [
        ClinicalTrial(
            protocolSection=ProtocolSection(
                identificationModule=IdentificationModule(
                    nctId="NCT00000001",
                    briefTitle="Test Trial 1"
                ),
                statusModule=StatusModule(
                    overallStatus="Recruiting",
                    startDateStruct={"date": "2023-01-01"}
                ),
                designModule=DesignModule(
                    phases=["Phase 1"],
                    enrollmentInfo={"count": 100}
                ),
                conditionsModule=ConditionsModule(
                    conditions=["Cancer"]
                )
            )
        ),
        # Add more sample trials...
    ]

@pytest.mark.asyncio
async def test_phase_analysis(sample_trials):
    analyzer = TrialAnalyzer()
    result = analyzer.analyze_phases(sample_trials)
    assert "Phase 1" in result
    assert result["Phase 1"] == 1

@pytest.mark.asyncio
async def test_therapeutic_area_analysis(sample_trials):
    analyzer = TrialAnalyzer()
    result = analyzer.analyze_therapeutic_areas(sample_trials)
    assert "Oncology" in result
    assert result["Oncology"]["conditions"]["Cancer"] == 1

@pytest.mark.asyncio
async def test_save_comprehensive_analysis(test_client: AsyncClient, setup_company):
    """Test saving complete analysis from frontend."""
    company_id = setup_company
    
    # Get real analysis data
    analysis_data = await get_sample_analysis()
    assert analysis_data is not None, "No sample data found in database"
    
    # Save analysis
    response = await test_client.post(
        f"/api/companies/{company_id}/analysis",
        json=analysis_data
    )
    assert response.status_code == 200
    
    # Verify saved data
    get_response = await test_client.get(f"/api/companies/{company_id}/trials")
    saved_data = get_response.json()["data"]
    assert len(saved_data) == len(analysis_data["studies"])
    
    # Verify analytics
    analytics_response = await test_client.get(
        f"/api/companies/{company_id}/trials/analytics"
    )
    saved_analytics = analytics_response.json()["data"]
    assert saved_analytics["trialAnalytics"] == analysis_data["analytics"]

@pytest.mark.asyncio
async def test_save_frontend_analysis(test_client: AsyncClient, setup_company):
    """Test saving analysis with exact frontend structure"""
    company_id = setup_company
    
    # Create analysis data matching frontend structure
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
            "phaseDistribution": {"Phase 1": 1},
            "statusSummary": {"Completed": 1},
            "therapeuticAreas": {},
            "totalTrials": 1,
            "enrollmentStats": {
                "total": 0,
                "average": 0,
                "median": 0
            }
        },
        "companyName": "Test Company",
        "queryDate": datetime.utcnow().isoformat()
    }
    
    response = await test_client.post(
        f"/api/companies/{company_id}/analysis",
        json=analysis_data
    )
    assert response.status_code == 200
    result = response.json()["data"]
    
    # Verify structure matches
    assert "trialAnalytics" in result
    assert "lastAnalyzed" in result
    assert result["success"] is True 