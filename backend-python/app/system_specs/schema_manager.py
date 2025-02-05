"""
Schema Management System
Handles schema versioning, context switching, and schema evolution.
Supports legacy, current, and future schema versions.
"""
from typing import Dict, Type, Optional, Any, List
from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from uuid import UUID
from app.system_specs.schemas import Company
from app.config.database import MongoDB


class SchemaVersion:
    """Represents a specific version of a schema"""
    def __init__(self, major: int, minor: int, patch: int):
        self.major = major
        self.minor = minor
        self.patch = patch
        
    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"
        
    def __lt__(self, other):
        return (self.major, self.minor, self.patch) < (other.major, other.minor, other.patch)

class SchemaContext(str, Enum):
    """Available schema contexts"""
    LEGACY = "legacy"
    ENHANCED = "enhanced"
    FUTURE = "future"
    CUSTOM = "custom"
    CURRENT = "current"

class SchemaMetadata:
    """Metadata for a schema version"""
    def __init__(
        self,
        version: SchemaVersion,
        schema: Type[BaseModel],
        context: SchemaContext,
        valid_from: datetime,
        valid_to: Optional[datetime] = None,
        migration_rules: Optional[Dict[str, Any]] = None
    ):
        self.version = version
        self.schema = schema
        self.context = context
        self.valid_from = valid_from
        self.valid_to = valid_to
        self.migration_rules = migration_rules or {}

class SchemaEvolution:
    """Handles schema evolution and migration rules"""
    def __init__(self):
        self.migrations: Dict[str, Dict[str, Any]] = {}
        
    def add_migration(
        self,
        from_version: SchemaVersion,
        to_version: SchemaVersion,
        rules: Dict[str, Any]
    ):
        key = f"{from_version}->{to_version}"
        self.migrations[key] = rules
        
    def get_migration_path(
        self,
        from_version: SchemaVersion,
        to_version: SchemaVersion
    ) -> List[Dict[str, Any]]:
        """Gets the sequence of migrations needed to evolve from one version to another"""
        if from_version == to_version:
            return []
            
        # Find direct path
        direct_key = f"{from_version}->{to_version}"
        if direct_key in self.migrations:
            return [self.migrations[direct_key]]
            
        # TODO: Implement path finding for multi-step migrations
        raise NotImplementedError("Multi-step migration path finding not yet implemented")

class SchemaManager:
    """
    Central manager for schema versioning and context handling.
    Supports multiple schema versions and contexts.
    """
    def __init__(self):
        self._schemas: Dict[str, Dict[SchemaVersion, SchemaMetadata]] = {}
        self._evolution = SchemaEvolution()
        self._active_context = SchemaContext.CURRENT
        self._legacy_schemas = {}  # Store legacy schemas separately
        
    async def register_schema(
        self,
        name: str,
        schema: Type[BaseModel],
        version: SchemaVersion,
        context: SchemaContext = SchemaContext.CURRENT,
        valid_from: datetime = datetime.utcnow(),
        valid_to: Optional[datetime] = None,
        migration_rules: Optional[Dict[str, Any]] = None
    ):
        """Register a schema version"""
        if name not in self._schemas:
            self._schemas[name] = {}
            
        metadata = SchemaMetadata(
            version=version,
            schema=schema,
            context=context,
            valid_from=valid_from,
            valid_to=valid_to,
            migration_rules=migration_rules
        )
        
        self._schemas[name][version] = metadata
        await self.save_schema_to_db(name, version)

    async def save_schema_to_db(self, name, version):
        async with MongoDB.get_collection("schemas") as collection:
            await collection.update_one(
                {"name": name},
                {"$set": {"version": str(version)}},
                upsert=True
            )
    
    def register_legacy_schema(self, name: str, schema: Type[BaseModel]):
        """Register a legacy schema version"""
        self._legacy_schemas[f"{name}_Legacy"] = schema
        
    def get_schema(
        self,
        name: str,
        context: Optional[SchemaContext] = None,
        version: Optional[SchemaVersion] = None
    ) -> Type[BaseModel]:
        """Get schema by name and optionally context or version"""
        if name not in self._schemas:
            raise ValueError(f"Schema {name} not registered")
            
        if version:
            if version not in self._schemas[name]:
                raise ValueError(f"Version {version} of schema {name} not found")
            return self._schemas[name][version].schema
            
        context = context or self._active_context
        
        # Find latest version for context
        matching_versions = [
            v for v, m in self._schemas[name].items()
            if m.context == context
            and (m.valid_to is None or m.valid_to > datetime.utcnow())
        ]
        
        if not matching_versions:
            raise ValueError(f"No valid schema found for {name} in context {context}")
            
        latest_version = max(matching_versions)
        return self._schemas[name][latest_version].schema
        
    def list_registered_schemas(self):
        return {name: list(versions.keys()) for name, versions in self._schemas.items()}

    def set_active_context(self, context: SchemaContext):
        """Set the active schema context"""
        self._active_context = context
        
    def get_active_context(self) -> SchemaContext:
        """Get the current active schema context"""
        return self._active_context
        
    def get_available_versions(self, name: str) -> List[SchemaVersion]:
        """Get all available versions for a schema"""
        if name not in self._schemas:
            raise ValueError(f"Schema {name} not registered")
        return sorted(self._schemas[name].keys())
        
    def get_migration_rules(
        self,
        name: str,
        from_version: SchemaVersion,
        to_version: SchemaVersion
    ) -> List[Dict[str, Any]]:
        """Get rules for migrating between schema versions"""
        if name not in self._schemas:
            raise ValueError(f"Schema {name} not registered")
            
        return self._evolution.get_migration_path(from_version, to_version)
        
    def validate_data(
        self,
        name: str,
        data: Dict[str, Any],
        context: Optional[SchemaContext] = None,
        version: Optional[SchemaVersion] = None
    ) -> bool:
        """Validate data against a schema version"""
        schema = self.get_schema(name, context, version)
        try:
            schema(**data)
            return True
        except Exception:
            return False
            
    def migrate_data(
        self,
        name: str,
        data: Dict[str, Any],
        from_version: SchemaVersion,
        to_version: SchemaVersion
    ) -> Dict[str, Any]:
        """Migrate data from one schema version to another"""
        migration_rules = self.get_migration_rules(name, from_version, to_version)
        
        migrated_data = data.copy()
        for rules in migration_rules:
            # Apply each migration rule
            for field, rule in rules.items():
                if callable(rule):
                    migrated_data[field] = rule(migrated_data)
                else:
                    migrated_data[field] = rule
                    
        return migrated_data

    def get_schema_for_context(self, name: str, context: str = "current") -> Type[BaseModel]:
        """Get schema by name and context using the simplified approach"""
        if context == "legacy":
            # Return legacy schema version if available
            legacy_name = f"{name}_Legacy"
            if legacy_name in self._legacy_schemas:
                return self._legacy_schemas[legacy_name]
        return self.get_schema(name)

    async def load_schemas_from_db(self):
        async with MongoDB.get_collection("schemas") as collection:
            schemas = await collection.find().to_list(None)
            for schema in schemas:
                name = schema['name']
                version = SchemaVersion(*map(int, schema['version'].split('.')))
                # Assuming schema classes are defined and imported
                schema_class = globals().get(name)
                if schema_class:
                    self.register_schema(name, schema_class, version)

    async def initialize_schemas(self):
        """Load schemas from the database on startup"""
        await self.load_schemas_from_db()

# Create global instance
schema_manager = SchemaManager() 