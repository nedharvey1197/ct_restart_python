from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any, Optional
from datetime import datetime

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
    """Matches frontend analytics structure exactly"""
    phaseDistribution: Dict[str, int] = Field(..., description="Distribution of trial phases")
    statusSummary: Dict[str, int] = Field(..., description="Summary of trial statuses")
    therapeuticAreas: Dict[str, Any] = Field(..., description="Analysis of therapeutic areas")
    totalTrials: int = Field(..., ge=0)
    enrollmentStats: Dict[str, Any] = Field(..., description="Enrollment statistics")

    @validator('enrollmentStats')
    def validate_enrollment_stats(cls, v):
        required_keys = {'total', 'average', 'median'}
        if not all(key in v for key in required_keys):
            raise ValueError(f"enrollmentStats must contain: {required_keys}")
        if not all(isinstance(v[key], (int, float)) for key in required_keys):
            raise ValueError("enrollmentStats values must be numbers")
        return v

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