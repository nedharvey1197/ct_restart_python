"""
Validation decorators and utilities for schema compliance
Version: 1.0
"""

from functools import wraps
from typing import Type, Dict, Any
from pydantic import BaseModel, ValidationError
from .schemas import SchemaRegistry

def validate_schema_compliance(schema_name: str):
    """
    Decorator to validate function inputs/outputs against registered schemas
    
    Args:
        schema_name: Name of the schema to validate against
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get authorized schema
            schema = SchemaRegistry.get_schema(schema_name)
            
            try:
                # Execute function
                result = await func(*args, **kwargs)
                
                # Validate result against schema
                if isinstance(result, dict):
                    return schema(**result)
                elif isinstance(result, BaseModel):
                    # If already a model, validate it's the correct type
                    if not isinstance(result, schema):
                        raise ValidationError(f"Result must be instance of {schema_name}")
                    return result
                    
                return result
                
            except ValidationError as e:
                raise ValidationError(
                    f"Schema validation failed for {schema_name}: {str(e)}"
                )
            except Exception as e:
                raise Exception(f"Error in {func.__name__}: {str(e)}")
                
        return wrapper
    return decorator

def validate_relationship(
    source_schema: str,
    target_schema: str,
    relationship_type: str
):
    """
    Decorator to validate relationship creation between entities
    
    Args:
        source_schema: Schema name for source entity
        target_schema: Schema name for target entity
        relationship_type: Type of relationship being created
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get schemas
            source_schema_cls = SchemaRegistry.get_schema(source_schema)
            target_schema_cls = SchemaRegistry.get_schema(target_schema)
            
            try:
                # Execute function
                result = await func(*args, **kwargs)
                
                # Validate relationship structure
                if not isinstance(result, dict):
                    raise ValidationError("Relationship must return a dictionary")
                    
                # Validate source and target entities
                if "source" in result and not isinstance(result["source"], source_schema_cls):
                    raise ValidationError(f"Source must be instance of {source_schema}")
                if "target" in result and not isinstance(result["target"], target_schema_cls):
                    raise ValidationError(f"Target must be instance of {target_schema}")
                    
                return result
                
            except Exception as e:
                raise Exception(f"Error validating relationship: {str(e)}")
                
        return wrapper
    return decorator

class DataValidator:
    """Utility class for common validation operations"""
    
    @staticmethod
    def validate_entity(data: Dict[str, Any], schema_name: str) -> BaseModel:
        """
        Validate data against a schema
        
        Args:
            data: Data to validate
            schema_name: Name of schema to validate against
        """
        schema = SchemaRegistry.get_schema(schema_name)
        return schema(**data)
    
    @staticmethod
    def validate_relationship_data(
        source_id: str,
        target_id: str,
        relationship_type: str,
        properties: Dict[str, Any]
    ) -> bool:
        """
        Validate relationship data structure
        
        Args:
            source_id: ID of source entity
            target_id: ID of target entity
            relationship_type: Type of relationship
            properties: Additional relationship properties
        """
        if not all([source_id, target_id, relationship_type]):
            return False
            
        if not isinstance(properties, dict):
            return False
            
        return True