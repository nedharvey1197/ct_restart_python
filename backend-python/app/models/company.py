from typing import Optional, Dict, List, Any
from pydantic import BaseModel, Field
from datetime import datetime

class TrialAnalytics(BaseModel):
    phaseDistribution: Dict[str, Any] = Field(default_factory=dict)
    statusSummary: Dict[str, Any] = Field(default_factory=dict)
    therapeuticAreas: Dict[str, Any] = Field(default_factory=dict)

class Company(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    companyName: str
    companyWebsite: Optional[str] = None
    companySize: Optional[str] = None
    headquarters: Optional[str] = None
    contactEmail: Optional[str] = None
    enrichedData: Optional[Dict[str, Any]] = None
    contextualData: Optional[Dict[str, Any]] = None
    trialAnalytics: Optional[TrialAnalytics] = None
    clinicalTrials: Optional[List[Dict[str, Any]]] = None
    lastEnriched: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow, alias="createdAt")
    updated_at: datetime = Field(default_factory=datetime.utcnow, alias="updatedAt")
    therapeuticAreas: Optional[List[str]] = None
    enrichmentStatus: Optional[str] = None
    lastAnalyzed: Optional[datetime] = None

    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        } 