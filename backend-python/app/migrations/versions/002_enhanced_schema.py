"""
Migration to enhanced schemas for companies and trials.
Handles company data transformation and trial schema setup.
"""
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from uuid import uuid4
from typing import Dict, Any, List

def transform_company(old_company: Dict[str, Any]) -> Dict[str, Any]:
    """Transform old company format to enhanced schema."""
    if not old_company:
        return None
        
    # Create base structure
    new_company = {
        "id": str(uuid4()),  # New UUID for the company
        "name": old_company.get("companyName", ""),
        "company_identifiers": {
            "mongodb_id": str(old_company.get("_id", "")),
            "website": old_company.get("companyWebsite", "")
        },
        "profile": {
            "size": old_company.get("companySize", ""),
            "headquarters": old_company.get("headquarters", ""),
            "contact_email": old_company.get("contactEmail", ""),
            "therapeutic_areas": old_company.get("therapeuticAreas", []) or []
        },
        "relationships": {},  # Will be populated from trials
        "kg_references": {},  # Empty initially, to be populated by KG integration
        "context_cache": {
            "enriched_data": old_company.get("enrichedData", {}) or {},
            "contextual_data": old_company.get("contextualData", {}) or {},
            "trial_analytics": old_company.get("trialAnalytics", {}) or {}
        },
        "status": "active",
        "metadata": {
            "last_enriched": old_company.get("lastEnriched", None),
            "enrichment_status": old_company.get("enrichmentStatus", "none"),
            "last_analyzed": old_company.get("lastAnalyzed", None)
        },
        "created_at": old_company.get("createdAt", datetime.utcnow()),
        "updated_at": old_company.get("updatedAt", datetime.utcnow()),
        "version": 1,
        "audit_trail": []
    }

    # Transform trials into relationships if they exist
    clinical_trials = old_company.get("clinicalTrials", []) or []
    if clinical_trials:
        trial_relationships = []
        for trial in clinical_trials:
            if isinstance(trial, dict) and "protocolSection" in trial:
                protocol = trial.get("protocolSection", {})
                identification = protocol.get("identificationModule", {})
                if "nctId" in identification:
                    trial_relationships.append({
                        "source_id": new_company["id"],
                        "target_id": identification["nctId"],
                        "relationship_type": "SPONSOR",
                        "properties": {
                            "role": "PRIMARY_SPONSOR",
                            "status": "ACTIVE"
                        }
                    })
        if trial_relationships:
            new_company["relationships"]["trials"] = trial_relationships

    return new_company

async def upgrade(db: AsyncIOMotorClient):
    """Upgrade to enhanced schemas."""
    print("Starting migration to enhanced schemas...")
    
    try:
        # 1. Set up collection for tracking migration state
        try:
            await db.create_collection("migration_state", capped=True, size=1048576)
        except Exception as e:
            print(f"Migration state collection may already exist: {e}")
            
        await db.migration_state.insert_one({
            "migration_id": "002_enhanced_schema",
            "started_at": datetime.utcnow(),
            "status": "in_progress"
        })

        # 2. Transform companies to enhanced schema
        print("Fetching existing companies...")
        companies = await db.companies.find().to_list(length=None)
        print(f"Found {len(companies)} companies to migrate")
        
        for company in companies:
            enhanced_company = transform_company(company)
            if enhanced_company:
                await db.companies_enhanced.insert_one(enhanced_company)
                print(f"Migrated company: {enhanced_company['name']}")
        
        # 3. Set up indexes for enhanced companies
        print("Setting up indexes for enhanced companies...")
        await db.companies_enhanced.create_index("name", unique=True)
        await db.companies_enhanced.create_index("company_identifiers.mongodb_id")
        await db.companies_enhanced.create_index("status")
        await db.companies_enhanced.create_index([("created_at", -1)])
        
        # 4. Set up trial collection with proper schema validation
        print("Setting up trial collection...")
        try:
            await db.create_collection("trials_enhanced")
        except Exception as e:
            print(f"Trial collection may already exist: {e}")
            
        await db.trials_enhanced.create_index("trial_identifiers.nct_id", unique=True)
        await db.trials_enhanced.create_index("status")
        await db.trials_enhanced.create_index([("created_at", -1)])
        
        # 5. If successful, rename collections
        migrated_count = await db.companies_enhanced.count_documents({})
        if migrated_count == len(companies):
            try:
                await db.companies.rename("companies_old")
            except Exception as e:
                print(f"Error renaming old companies collection: {e}")
                return
                
            try:
                await db.companies_enhanced.rename("companies")
            except Exception as e:
                print(f"Error renaming enhanced companies collection: {e}")
                # Try to restore old collection name
                await db.companies_old.rename("companies")
                return
                
            print("Successfully migrated companies to enhanced schema")
        else:
            print(f"Error: Company count mismatch after migration. Expected {len(companies)}, got {migrated_count}")
            return
        
        # 6. Update migration state
        await db.migration_state.update_one(
            {"migration_id": "002_enhanced_schema"},
            {
                "$set": {
                    "completed_at": datetime.utcnow(),
                    "status": "completed"
                }
            }
        )
        print("Migration completed successfully")
        
    except Exception as e:
        print(f"Error during migration: {e}")
        # Try to restore original state
        try:
            if await db.companies_old.count_documents({}) > 0:
                await db.companies.drop()
                await db.companies_old.rename("companies")
        except Exception as rollback_error:
            print(f"Error during rollback: {rollback_error}")
        raise

async def downgrade(db: AsyncIOMotorClient):
    """Rollback changes."""
    # Only rollback if the migration was completed
    migration_state = await db.migration_state.find_one({"migration_id": "002_enhanced_schema"})
    if migration_state and migration_state.get("status") == "completed":
        # Restore old collections
        if await db.companies_old.count_documents({}) > 0:
            await db.companies.drop()
            await db.companies_old.rename("companies")
        
        # Drop enhanced trial collection
        await db.trials_enhanced.drop()
        
        # Update migration state
        await db.migration_state.update_one(
            {"migration_id": "002_enhanced_schema"},
            {
                "$set": {
                    "rolled_back_at": datetime.utcnow(),
                    "status": "rolled_back"
                }
            }
        )
        print("Successfully rolled back migration") 
