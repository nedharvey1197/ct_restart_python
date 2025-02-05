"""
Migration script to register schemas with the schema manager.
Handles legacy, current, and enhanced schemas.
"""
from datetime import datetime
from app.system_specs.schema_manager import (
    schema_manager,
    SchemaVersion,
    SchemaContext
)
from app.system_specs.schemas import (
    Company,
    EnhancedCompany,
    Trial,
    EnhancedTrial
)

async def upgrade():
    """Register schemas and set up migration rules"""
    # Register legacy schemas with version 0.9
    schema_manager.register_legacy_schema("Company", Company)
    schema_manager.register_legacy_schema("Trial", Trial)
    
    # Register enhanced schemas
    enhanced_company = SchemaVersion(2, 0, 0)
    enhanced_trial = SchemaVersion(2, 0, 0)
    
    schema_manager.register_schema(
        name="company",
        schema=EnhancedCompany,
        version=enhanced_company,
        context=SchemaContext.ENHANCED,
        valid_from=datetime(2024, 1, 1)
    )
    
    schema_manager.register_schema(
        name="trial",
        schema=EnhancedTrial,
        version=enhanced_trial,
        context=SchemaContext.ENHANCED,
        valid_from=datetime(2024, 1, 1)
    )
    
    # Migration rules remain the same
    company_migration_rules = {
        "id": lambda x: str(x.get("_id")),
        "company_identifiers": lambda x: [{
            "id": str(x.get("_id")),
            "type": "internal",
            "source": "legacy"
        }],
        "name": lambda x: x.get("companyName"),
        "relationships": lambda x: [],
        "kg_references": lambda x: [],
        "context_cache": lambda x: x.get("contextual_data", {}),
        "profile": lambda x: {
            "website": x.get("companyWebsite"),
            "contact_email": x.get("contactEmail"),
            "company_size": x.get("companySize"),
            "headquarters": x.get("headquarters"),
            "therapeutic_areas": x.get("therapeutic_areas", []),
            "trial_analytics": x.get("trial_analytics", {})
        },
        "status": "active",
        "metadata": lambda x: {
            "created_at": x.get("created_at", datetime.utcnow()),
            "updated_at": datetime.utcnow(),
            "source": "migration"
        },
        "audit_trail": lambda x: [{
            "action": "migrated",
            "timestamp": datetime.utcnow(),
            "details": "Migrated from legacy schema"
        }]
    }
    
    # Add migration rules for legacy to enhanced
    legacy_version = SchemaVersion(0, 9, 0)  # Legacy version 0.9
    schema_manager._evolution.add_migration(
        from_version=legacy_version,
        to_version=enhanced_company,
        rules=company_migration_rules
    )
    
    # Trial migration rules remain the same
    trial_migration_rules = {
        "trial_identification": lambda x: {
            "trial_id": str(x.get("_id")),
            "nct_id": x.get("nct_id"),
            "external_ids": []
        },
        "relationships": lambda x: [],
        "kg_references": lambda x: [],
        "conditions": lambda x: x.get("conditions", []),
        "interventions": lambda x: x.get("interventions", []),
        "metadata": lambda x: {
            "created_at": x.get("created_at", datetime.utcnow()),
            "updated_at": datetime.utcnow(),
            "source": "migration"
        }
    }
    
    schema_manager._evolution.add_migration(
        from_version=legacy_version,
        to_version=enhanced_trial,
        rules=trial_migration_rules
    )
    
    print("Successfully registered schemas and migration rules")

async def downgrade():
    """Remove registered schemas"""
    # Note: This is a simplified downgrade that just resets the schema manager
    schema_manager._schemas = {}
    schema_manager._evolution = SchemaEvolution()
    schema_manager._active_context = SchemaContext.CURRENT
    
    print("Successfully removed registered schemas") 