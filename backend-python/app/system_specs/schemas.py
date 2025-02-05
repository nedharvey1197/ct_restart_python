"""
Authoritative source for system schemas and data models
Version: 1.0
Last Updated: [date]
"""

from datetime import datetime
from typing import Dict, List, Optional, Any, Type
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

class EntityBase(BaseModel):
    """Base class for all entities with common tracking fields"""
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    version: int = Field(default=1)
    status: str = Field(default="active")
    metadata: Dict[str, Any] = Field(default_factory=dict)
    audit_trail: List[Dict[str, Any]] = Field(default_factory=list)

class RelationshipBase(BaseModel):
    """Base class for all relationships"""
    source_id: UUID
    target_id: UUID
    relationship_type: str
    properties: Dict[str, Any] = Field(default_factory=dict)
    valid_from: datetime = Field(default_factory=datetime.utcnow)
    valid_to: Optional[datetime] = None
    confidence: float = Field(default=1.0)
    source: str = Field(description="Source of this relationship")
    metadata: Dict[str, Any] = Field(default_factory=dict)

class Company(BaseModel):
    """Enhanced company schema"""
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Core company data
    name: str
    company_identifiers: Dict[str, str] = Field(
        default_factory=dict,
        description="Map of identifier types to values"
    )
    
    # Flexible profile storage
    profile: Dict[str, Any] = Field(
        default_factory=dict,
        description="Structured company profile data"
    )
    
    # Relationship tracking
    trial_ids: List[str] = Field(
        default_factory=list,
        description="List of associated trial IDs"
    )
    relationships: Dict[str, List[Dict[str, Any]]] = Field(
        default_factory=dict,
        description="Categorized relationships"
    )
    
    # Metadata & tracking
    status: str = "active"
    metadata: Dict[str, Any] = Field(default_factory=dict)

class EnhancedCompany(EntityBase):
    """Enhanced company schema with flexible relationships"""
    company_identifiers: Dict[str, str] = Field(
        default_factory=dict,
        description="Map of identifier types to values"
    )
    name: str
    relationships: Dict[str, List[RelationshipBase]] = Field(
        default_factory=dict,
        description="Categorized relationships to any entity type"
    )
    kg_references: Dict[str, Any] = Field(
        default_factory=dict,
        description="References to KG entities"
    )
    profile: Dict[str, Any] = Field(
        default_factory=dict,
        description="Flexible company profile data"
    )
    context_cache: Dict[str, Any] = Field(
        default_factory=dict,
        description="Cached contextual data"
    )

class EnhancedTrial(EntityBase):
    """Enhanced trial schema with flexible relationships"""
    trial_identifiers: Dict[str, str] = Field(
        description="Map of identifier types to values (NCT, EudraCT, etc)"
    )
    title: str
    phase: Optional[str]
    status: str
    relationships: Dict[str, List[RelationshipBase]] = Field(
        default_factory=dict,
        description="Categorized relationships to any entity type"
    )
    kg_references: Dict[str, Any] = Field(
        default_factory=dict,
        description="References to KG entities"
    )
    data_sources: Dict[str, Any] = Field(
        default_factory=dict,
        description="Track data sources and updates"
    )
    context_cache: Dict[str, Any] = Field(
        default_factory=dict,
        description="Cached contextual data"
    )

class SchemaRegistry:
    """
    Central registry for all system schemas
    Maintains versioned references to authorized schemas
    """
    _schemas: Dict[str, Type[BaseModel]] = {}
    _versions: Dict[str, str] = {}

    @classmethod
    def register_schema(cls, name: str, schema: Type[BaseModel], version: str):
        cls._schemas[name] = schema
        cls._versions[name] = version

    @classmethod
    def get_schema(cls, name: str) -> Type[BaseModel]:
        if name not in cls._schemas:
            raise ValueError(f"Schema {name} not found in registry")
        return cls._schemas[name]

    @classmethod
    def get_version(cls, name: str) -> str:
        return cls._versions.get(name)

# Register core schemas
SchemaRegistry.register_schema("EntityBase", EntityBase, "1.0")
SchemaRegistry.register_schema("RelationshipBase", RelationshipBase, "1.0")
SchemaRegistry.register_schema("EnhancedCompany", EnhancedCompany, "1.0")
SchemaRegistry.register_schema("EnhancedTrial", EnhancedTrial, "1.0")  
SchemaRegistry.register_schema("Company", Company, "1.0")