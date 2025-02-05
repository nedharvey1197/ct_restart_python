"""
Service for handling schema operations using the schema manager.
Provides high-level operations for schema-related tasks.
"""

from typing import Dict, Any, Optional
from datetime import datetime
from app.system_specs.schema_manager import schema_manager, SchemaContext
from app.config.database import MongoDB


class SchemaService:
    """Service for handling schema operations"""

    SINGULAR_EXCEPTIONS = {
        "companies": "companies",  # Prevent "companie" error
        "trials": "trials",
        "analyses": "analysis"  # Example case where plural is different
    }  # ✅ FIXED: Closing bracket added

    @staticmethod
    async def validate_document(
        collection_name: str,
        document: Dict[str, Any],
        context: Optional[SchemaContext] = None
        ) -> bool:
        """
        Validate a document against the appropriate schema.
        Returns True if valid, False otherwise.
        """
        schema_name = SchemaService.SINGULAR_EXCEPTIONS.get(collection_name, collection_name.rstrip('s'))  # Use mapping
        return schema_manager.validate_data(
            name=schema_name,
            data=document,
            context=context
        )

    @staticmethod
    async def migrate_document(
        collection_name: str,
        document: Dict[str, Any],
        from_context: SchemaContext,
        to_context: SchemaContext
        ) -> Dict[str, Any]:
        """
        Migrate a document from one context to another.
        Returns the migrated document.
        """
        schema_name = SchemaService.SINGULAR_EXCEPTIONS.get(collection_name, collection_name.rstrip('s'))

        # Get versions for the contexts
        from_version = next(
            v for v, m in schema_manager._schemas[schema_name].items()
            if m.context == from_context
        )
        to_version = next(
            v for v, m in schema_manager._schemas[schema_name].items()
            if m.context == to_context
        )

        return schema_manager.migrate_data(
            name=schema_name,
            data=document,
            from_version=from_version,
            to_version=to_version
        )
    
    @staticmethod
    async def get_schema_info(collection_name: str) -> Dict[str, Any]:
        """Get schema info with better singular handling"""
        schema_name = SchemaService.SINGULAR_EXCEPTIONS.get(collection_name, collection_name.rstrip('s'))

        if schema_name not in schema_manager._schemas:
            raise ValueError(f"No schemas registered for {collection_name}")

        versions = schema_manager.get_available_versions(schema_name)
        contexts = {
            str(v): m.context
            for v, m in schema_manager._schemas[schema_name].items()
        }

        return {
            "name": schema_name,
            "versions": [str(v) for v in versions],
            "contexts": contexts,
            "active_context": schema_manager.get_active_context()
        }
    

    
    @staticmethod
    async def set_collection_context(
        collection_name: str,
        context: SchemaContext
    ):
        """Set the active context for a collection"""
        async with MongoDB.get_collection(collection_name) as collection:
            # Update collection metadata
            await collection.update_one(
                {"_id": "schema_metadata"},
                {
                    "$set": {
                        "active_context": context,
                        "updated_at": datetime.utcnow()
                    }
                },
                upsert=True
            )
        
        # Set active context in schema manager
        schema_manager.set_active_context(context)
    
    @staticmethod
    async def get_collection_context(collection_name: str) -> SchemaContext:
        """Get the active context for a collection"""
        async with MongoDB.get_collection(collection_name) as collection:
            # Get collection metadata
            metadata = await collection.find_one({"_id": "schema_metadata"})
            if metadata and "active_context" in metadata:
                return SchemaContext(metadata["active_context"])
        
        return schema_manager.get_active_context()
    
    @staticmethod
    async def migrate_collection(
        collection_name: str,
        from_context: SchemaContext,
        to_context: SchemaContext
    ):
        """Migrate all documents in a collection from one context to another"""
        async with MongoDB.get_collection(collection_name) as collection:
            # Get all documents except schema metadata
            cursor = collection.find({"_id": {"$ne": "schema_metadata"}})
            
            async for document in cursor:
                # Migrate document
                migrated = await SchemaService.migrate_document(
                    collection_name=collection_name,
                    document=document,
                    from_context=from_context,
                    to_context=to_context
                )
                
                # Update document
                await collection.update_one(
                    {"_id": document["_id"]},
                    {"$set": migrated}
                )
            
            # Update collection context
            await SchemaService.set_collection_context(
                collection_name=collection_name,
                context=to_context
            ) 