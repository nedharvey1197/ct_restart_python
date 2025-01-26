from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

async def upgrade(db: AsyncIOMotorClient):
    """Initial database setup."""
    # Create indexes
    await db.companies.create_index("companyName", unique=True)
    await db.companies.create_index("created_at")
    
    # Add lastAnalyzed field to existing companies
    await db.companies.update_many(
        {"lastAnalyzed": {"$exists": False}},
        {"$set": {"lastAnalyzed": datetime.utcnow()}}
    )

async def downgrade(db: AsyncIOMotorClient):
    """Rollback changes."""
    await db.companies.drop_index("companyName_1")
    await db.companies.drop_index("created_at_1") 