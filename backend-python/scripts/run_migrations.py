import asyncio
import importlib
import os
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from app.config.settings import get_settings

async def run_migrations():
    settings = get_settings()
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]

    # Get all migration files
    migrations_path = Path("app/migrations/versions")
    migration_files = sorted(
        [f for f in migrations_path.glob("*.py") if f.stem != "__init__"]
    )

    for migration_file in migration_files:
        module_name = f"app.migrations.versions.{migration_file.stem}"
        migration = importlib.import_module(module_name)
        
        try:
            print(f"Running migration: {migration_file.stem}")
            await migration.upgrade(db)
            print(f"Completed migration: {migration_file.stem}")
        except Exception as e:
            print(f"Error in migration {migration_file.stem}: {e}")
            raise

if __name__ == "__main__":
    asyncio.run(run_migrations()) 