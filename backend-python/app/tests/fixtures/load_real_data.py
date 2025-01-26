from motor.motor_asyncio import AsyncIOMotorClient
from ...config.settings import get_settings
from typing import List, Dict, Any

async def get_sample_trials() -> List[Dict[str, Any]]:
    """Get real trial data from existing database."""
    settings = get_settings()
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]
    
    # Get a sample company with trials
    company = await db.companies.find_one({"clinicalTrials": {"$exists": True}})
    return company.get("clinicalTrials", []) if company else []

async def get_sample_analysis() -> Dict[str, Any]:
    """Get real analysis data from existing database."""
    settings = get_settings()
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]
    
    # Get a sample company with analysis
    company = await db.companies.find_one({"trialAnalytics": {"$exists": True}})
    return {
        "studies": company.get("clinicalTrials", []),
        "analytics": company.get("trialAnalytics", {}),
        "companyName": company.get("name", ""),
        "queryDate": company.get("lastAnalyzed")
    } if company else None 