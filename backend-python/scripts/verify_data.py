#!/usr/bin/env python
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import os
import sys
import json

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config.settings import get_settings

async def verify_existing_data():
    settings = get_settings()
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]
    
    try:
        # Check collections
        collections = await db.list_collection_names()
        print(f"Found collections: {collections}")
        
        # Check companies
        companies_count = await db.companies.count_documents({})
        print(f"Found {companies_count} companies")
        
        # Check trials
        sample_company = await db.companies.find_one({"clinicalTrials": {"$exists": True}})
        if sample_company:
            trials_count = len(sample_company.get("clinicalTrials", []))
            print(f"\nCompany details:")
            print(f"ID: {sample_company.get('_id')}")
            print(f"Name field: {sample_company.get('name')}")
            print(f"companyName field: {sample_company.get('companyName')}")  # Check both possible name fields
            print(f"Number of trials: {trials_count}")
            print(f"Has trialAnalytics: {'trialAnalytics' in sample_company}")
            print(f"\nAvailable fields: {list(sample_company.keys())}")
            
            if trials_count > 0:
                print(f"\nSample trial fields: {list(sample_company['clinicalTrials'][0].keys())}")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(verify_existing_data()) 