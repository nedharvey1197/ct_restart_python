"""
Knowledge Graph Relationship Definitions

This module defines the relationships between different entities in the Knowledge Graph.
It maps out how different components of the schema interact with each other across:
- Internal Context (within same schema layer)
- External Context (between different schemas)
- Cross-Context (bridging different context types)
"""

class SchemaInterconnections:
    # Internal Context Relationships
    protocol_to_safety = {
        "relationship": "INFLUENCES_SAFETY",
        "properties": {"strength", "mechanism"}
    }
    
    # External Context Relationships
    regulatory_to_market = {
        "relationship": "IMPACTS_MARKET",
        "properties": {"strength", "direction"}
    }
    
    # Cross-Context Relationships
    market_to_performance = {
        "relationship": "INFLUENCES_PERFORMANCE",
        "properties": {"impact_type", "confidence"}
    }