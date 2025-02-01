"""
Test data loading fixtures.
"""
from motor.motor_asyncio import AsyncIOMotorClient
from app.config.settings import get_settings
from app.models.trial import TrialAnalysis, TrialAnalytics
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

async def get_sample_trials() -> List[Dict[str, Any]]:
    """Get real trial data from existing database."""
    try:
        settings = get_settings()
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        db = client[settings.DATABASE_NAME]
        
        # Get a sample company with trials
        company = await db.companies.find_one({"clinicalTrials": {"$exists": True}})
        if not company:
            logger.warning("No sample trials found in database")
            return []
        return company.get("clinicalTrials", [])
    except Exception as e:
        logger.error(f"Error loading sample trials: {str(e)}")
        return []

async def get_sample_analysis() -> Optional[Dict[str, Any]]:
    """Get real analysis data from existing database."""
    try:
        settings = get_settings()
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        db = client[settings.DATABASE_NAME]
        
        # Get a sample company with analysis
        company = await db.companies.find_one({"trialAnalytics": {"$exists": True}})
        if not company:
            logger.warning("No sample analysis found in database")
            return None
            
        analytics = company.get("trialAnalytics", {})
        data = {
            "studies": company.get("clinicalTrials", []),
            "analytics": {
                "phase_distribution": analytics.get("phaseDistribution", {}),
                "status_summary": analytics.get("statusSummary", {}),
                "therapeutic_areas": analytics.get("therapeuticAreas", {}),
                "total_trials": len(company.get("clinicalTrials", [])),
                "enrollment_stats": analytics.get("enrollmentStats", {
                    "total": 0,
                    "average": 0,
                    "median": 0
                })
            },
            "companyName": company.get("name", ""),
            "queryDate": company.get("lastAnalyzed")
        }
        
        # Validate against model
        analysis = TrialAnalysis(**data)
        return analysis.model_dump()
    except Exception as e:
        logger.error(f"Error loading sample analysis: {str(e)}")
        return None 