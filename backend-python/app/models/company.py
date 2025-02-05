"""
Company model for the clinical trials system.
Represents a company entity in the system.

Additional Schema Implementation Notes (2024):
- Uses EnhancedCompany schema from system_specs while maintaining the 'Company' name 
- Maintains backward compatibility with existing code
- Allows for future company-specific logic addition
- Separates data structure (schema) from business logic (model)

KG Schema Mapping:
- Maps to CI.CompetitorTrial for market context
- Links to DS.StrategicDecisionPoint
- Connects to KI.MarketIntelligence

Required Modifications:
- Add contextual intelligence references
- Include strategic decision tracking
- Add market position indicators
"""

from typing import Optional, Dict, List, Any
from pydantic import BaseModel, Field
from datetime import datetime
from ..system_specs.schema_manager import SchemaContext
from ..system_specs.schemas import EnhancedCompany, RelationshipBase
from uuid import UUID

class CompanyAnalytics(BaseModel):
    """Analytics data for a company's trials"""
    phase_distribution: Dict[str, Any] = Field(default_factory=dict)
    status_summary: Dict[str, Any] = Field(default_factory=dict)
    therapeutic_areas: Dict[str, Any] = Field(default_factory=dict)
    total_trials: int = Field(default=0)
    enrollment_stats: Dict[str, Any] = Field(default_factory=dict)
    last_analyzed: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class Company(EnhancedCompany):
    """
    Company model that extends EnhancedCompany with additional functionality.
    Maintains backward compatibility through property getters/setters.
    """
    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

    @property
    def companyName(self) -> str:
        """Backward compatibility for old code using companyName"""
        return self.name
    
    @property
    def companyWebsite(self) -> Optional[str]:
        """Backward compatibility for old code using companyWebsite"""
        return self.company_identifiers.get("website") if self.company_identifiers else None

    @property
    def companySize(self) -> Optional[str]:
        """Backward compatibility for old code using companySize"""
        return self.profile.get("size") if self.profile else None

    @property
    def therapeuticAreas(self) -> List[str]:
        """Backward compatibility for old code using therapeuticAreas"""
        return self.profile.get("therapeutic_areas", []) if self.profile else []

    @property
    def trialAnalytics(self) -> Optional[Dict[str, Any]]:
        """Backward compatibility for old code using trialAnalytics"""
        if not self.trial_analytics:
            return None
        return {
            "phaseDistribution": self.trial_analytics.get("phase_distribution", {}),
            "statusSummary": self.trial_analytics.get("status_summary", {}),
            "therapeuticAreas": self.trial_analytics.get("therapeutic_areas", {}),
            "totalTrials": self.trial_analytics.get("total_trials", 0),
            "enrollmentStats": self.trial_analytics.get("enrollment_stats", {})
        }

    @property
    def clinicalTrials(self) -> List[Dict[str, Any]]:
        """Backward compatibility for old code using clinicalTrials"""
        return self.trials if self.trials else []

    @property
    def lastAnalyzed(self) -> Optional[datetime]:
        """Backward compatibility for old code using lastAnalyzed"""
        return self.updated_at

def create_company_relationship(
    source_id: UUID,
    target_id: UUID,
    relationship_type: str,
    properties: Dict[str, Any] = None
) -> RelationshipBase:
    """Create a new company relationship"""
    return RelationshipBase(
        source_id=source_id,
        target_id=target_id,
        relationship_type=relationship_type,
        properties=properties or {}
    ) 