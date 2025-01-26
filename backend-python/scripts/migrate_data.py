from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

async def migrate_data():
    # Source (Node.js) database
    source_client = AsyncIOMotorClient("mongodb://localhost:27017")
    source_db = source_client["clinical_trials"]
    
    # Target (Python) database - if different
    target_client = AsyncIOMotorClient("mongodb://localhost:27017")
    target_db = target_client["clinical_trials_python"]
    
    # Migrate companies and their trials
    async for company in source_db.companies.find({}):
        await target_db.companies.update_one(
            {"_id": company["_id"]},
            {"$set": company},
            upsert=True
        )
        print(f"Migrated company: {company.get('name')}")

if __name__ == "__main__":
    asyncio.run(migrate_data()) 