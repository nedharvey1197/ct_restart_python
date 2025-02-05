"""
Knowledge Graph Storage Models

Defines the permanent storage structures needed in MongoDB to maintain 
relationships with the Knowledge Graph. These models represent the core
document structures that will store KG node references.
"""

from pydantic import BaseModel, Field
from typing import Dict, List
from bson import ObjectId

class MongoDBPermanentStorage:
    company = {
        "_id": "ObjectId",  # Primary identifier
        "companyName": "string",  # KG link point for CI.CompetitorTrial
        "basic_info": {
            # Current implementation fields
        },
        "kg_references": {
            "context_nodes": ["node_ids"],  # CI Schema references
            "decision_points": ["node_ids"], # DS Schema references
            "risk_indicators": ["node_ids"]  # SG Schema references
        }
    }

    clinical_trial = {
        "nct_id": "string",  # Primary & KG BIL.Study reference
        "company_id": "ObjectId",
        "modules": {
            # Current CT.gov data modules
        },
        "kg_references": {
            "study_node": "node_id",        # BIL.Study reference
            "protocol_node": "node_id",     # CI.Protocol reference
            "performance_nodes": ["node_ids"] # TST Schema references
        }
    }

    trial_analytics = {
        "company_id": "ObjectId",
        "base_analytics": {
            # Current analytics implementation
        },
        "kg_references": {
            "signal_nodes": ["node_ids"],    # SG Schema references
            "impact_nodes": ["node_ids"],    # DS Schema references
            "knowledge_nodes": ["node_ids"]  # KI Schema references
        }
    } 