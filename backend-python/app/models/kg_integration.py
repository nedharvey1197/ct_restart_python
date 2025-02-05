"""
Knowledge Graph Integration Models

This module defines Pydantic models that serve as bridges between MongoDB storage
and the Knowledge Graph schema layers. It implements reference tracking and 
relationship mapping for future KG integration.

The models follow the three-layer KG architecture:
- Meta-Schema Layer (Schema Registry)
- Core Support Schema Layer
- Baseline Implementation Layer
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime

class KGReference(BaseModel):
    """
    Base model for tracking Knowledge Graph node references.
    Used to maintain links between MongoDB documents and KG nodes.
    
    Attributes:
        node_id: Unique identifier in the Knowledge Graph
        schema_layer: Which KG layer this reference belongs to
        entity_type: The specific entity type in the KG schema
        last_synced: When this reference was last synchronized
    """
    node_id: str
    schema_layer: str
    entity_type: str
    last_synced: datetime

class StudyKGReferences(BaseModel):
    """
    Tracks KG references for clinical trial study data.
    Maps to Baseline Implementation Layer and Core Support Layer entities.
    
    Attributes:
        bil_study: Reference to BIL Study entity
        bil_protocol: Reference to BIL Protocol entity
        tst_status: References to Trial State Tracking status nodes
        ci_protocol: Reference to Contextual Intelligence protocol node
    """
    bil_study: Optional[KGReference]
    bil_protocol: Optional[KGReference]
    tst_status: Optional[List[KGReference]]
    ci_protocol: Optional[KGReference]

class AnalyticsKGReferences(BaseModel):
    """
    Tracks KG references for trial analytics data.
    Maps primarily to Core Support Layer entities.
    
    Attributes:
        sg_signals: References to Signal Generation nodes
        ds_impacts: References to Decision Support impact nodes
        ki_insights: References to Knowledge Integration insight nodes
    """
    sg_signals: Optional[List[KGReference]]
    ds_impacts: Optional[List[KGReference]]
    ki_insights: Optional[List[KGReference]]

class CompanyKGReferences(BaseModel):
    """
    Tracks KG references for company data.
    Maps to Contextual Intelligence and Decision Support entities.
    
    Attributes:
        ci_competitor: Reference to CI CompetitorTrial nodes
        ci_market: Reference to CI MarketCondition nodes
        ds_strategy: References to Decision Support strategy nodes
    """
    ci_competitor: Optional[KGReference]
    ci_market: Optional[List[KGReference]]
    ds_strategy: Optional[List[KGReference]]