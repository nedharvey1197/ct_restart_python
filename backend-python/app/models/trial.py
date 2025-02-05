"""
Trial model for the clinical trials system.
Represents a clinical trial entity in the system.

Additional Schema Implementation Notes (2024):
- Uses EnhancedTrial schema from system_specs while maintaining the 'Trial' name
- Maintains backward compatibility with existing code through property getters/setters
- Allows for future trial-specific logic addition
- Separates data structure (schema) from business logic (model)

KG Schema Mapping:
- Primary link to BIL.Study
- Maps modules to BIL entities
- Connects to CI.Protocol

Required Modifications:
- Add BIL entity references
- Include protocol state tracking
- Add module-specific KG mappings
"""

from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any, Optional
from datetime import datetime
from ..system_specs.schema_manager import SchemaContext
from ..system_specs.schemas import EnhancedTrial, RelationshipBase
from uuid import UUID

class ConditionsModule(BaseModel):
    conditions: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)

class DesignModule(BaseModel):
    phases: List[str] = Field(default_factory=list)
    studyType: str = "Interventional"
    enrollmentInfo: Dict[str, Any] = Field(default_factory=dict)
    designInfo: Dict[str, Any] = Field(default_factory=dict)

class StatusModule(BaseModel):
    overallStatus: str
    startDateStruct: Dict[str, str]
    completionDateStruct: Optional[Dict[str, str]]
    primaryCompletionDateStruct: Optional[Dict[str, str]]

class IdentificationModule(BaseModel):
    nctId: str
    briefTitle: str
    officialTitle: Optional[str]
    organization: Dict[str, Any] = Field(default_factory=dict)

class ProtocolSection(BaseModel):
    identificationModule: IdentificationModule
    statusModule: StatusModule
    designModule: DesignModule
    conditionsModule: ConditionsModule = Field(default_factory=ConditionsModule)
    sponsorCollaboratorsModule: Dict[str, Any] = Field(default_factory=dict)

class ClinicalTrial(BaseModel):
    protocolSection: ProtocolSection
    hasResults: bool = False

class TrialAnalytics(BaseModel):
    """Analytics data structure matching frontend requirements"""
    phase_distribution: Dict[str, int] = Field(..., description="Distribution of trial phases")
    status_summary: Dict[str, int] = Field(..., description="Summary of trial statuses")
    therapeutic_areas: Dict[str, Any] = Field(..., description="Analysis of therapeutic areas")
    total_trials: int = Field(..., ge=0)
    enrollment_stats: Dict[str, Any] = Field(..., description="Enrollment statistics")

    @validator('enrollment_stats')
    def validate_enrollment_stats(cls, v):
        required_keys = {'total', 'average', 'median'}
        if not all(key in v for key in required_keys):
            raise ValueError(f"enrollment_stats must contain: {required_keys}")
        if not all(isinstance(v[key], (int, float)) for key in required_keys):
            raise ValueError("enrollment_stats values must be numbers")
        return v

    # Backward compatibility properties
    @property
    def phaseDistribution(self) -> Dict[str, int]:
        return self.phase_distribution

    @property
    def statusSummary(self) -> Dict[str, int]:
        return self.status_summary

    @property
    def therapeuticAreas(self) -> Dict[str, Any]:
        return self.therapeutic_areas

    @property
    def totalTrials(self) -> int:
        return self.total_trials

    @property
    def enrollmentStats(self) -> Dict[str, Any]:
        return self.enrollment_stats

class TrialAnalysis(BaseModel):
    """Matches frontend ComprehensiveTrialAnalyzer payload exactly"""
    studies: List[Dict[str, Any]] = Field(..., min_items=1)
    analytics: TrialAnalytics
    companyName: str = Field(..., min_length=1)
    queryDate: datetime

    @validator('studies')
    def validate_studies(cls, v):
        for study in v:
            if 'nctId' not in study:
                raise ValueError("Each study must have an nctId")
            if 'protocolSection' not in study:
                raise ValueError("Each study must have a protocolSection")
        return v

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        schema_extra = {
            "example": {
                "studies": [{
                    "nctId": "NCT00000000",
                    "protocolSection": {
                        "identificationModule": {"briefTitle": "Example Trial"}
                    }
                }],
                "analytics": {
                    "phaseDistribution": {"Phase 1": 1},
                    "statusSummary": {"Completed": 1},
                    "therapeuticAreas": {},
                    "totalTrials": 1,
                    "enrollmentStats": {
                        "total": 100,
                        "average": 50,
                        "median": 50
                    }
                },
                "companyName": "Example Company",
                "queryDate": "2024-01-01T00:00:00Z"
            }
        }

class Trial(EnhancedTrial):
    """
    Trial model that extends EnhancedTrial with additional functionality.
    Maintains backward compatibility through property getters/setters.
    """
    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

    @property
    def nctId(self) -> str:
        """Backward compatibility for old code using nctId"""
        return self.nct_id

    @property
    def protocolSection(self) -> Dict[str, Any]:
        """Backward compatibility for old code using protocolSection"""
        return {
            "identificationModule": {
                "nctId": self.nct_id,
                "briefTitle": self.title,
                "officialTitle": self.official_title,
                "organization": self.organization or {}
            },
            "statusModule": {
                "overallStatus": self.status,
                "startDateStruct": {"date": self.start_date.isoformat() if self.start_date else None},
                "completionDateStruct": {"date": self.completion_date.isoformat() if self.completion_date else None},
                "primaryCompletionDateStruct": {"date": self.primary_completion_date.isoformat() if self.primary_completion_date else None}
            },
            "designModule": {
                "phases": self.phases,
                "studyType": self.study_type,
                "enrollmentInfo": self.enrollment_info or {},
                "designInfo": self.design_info or {}
            },
            "conditionsModule": {
                "conditions": self.conditions or [],
                "keywords": self.keywords or []
            },
            "sponsorCollaboratorsModule": self.sponsor_collaborators or {}
        }

def create_trial_relationship(
    source_id: UUID,
    target_id: UUID,
    relationship_type: str,
    properties: Dict[str, Any] = None
) -> RelationshipBase:
    """Create a new trial relationship"""
    return RelationshipBase(
        source_id=source_id,
        target_id=target_id,
        relationship_type=relationship_type,
        properties=properties or {}
    ) 