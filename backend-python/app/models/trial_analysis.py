from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime

class TrialAnalysis(BaseModel):
    """Model for trial analysis data"""
    company_id: str
    analysis_date: datetime = datetime.now()
    metrics: Dict[str, Any]
    insights: List[Dict[str, Any]]
    recommendations: Optional[List[Dict[str, str]]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "company_id": "12345",
                "analysis_date": "2024-01-24T00:00:00",
                "metrics": {
                    "total_trials": 10,
                    "active_trials": 5,
                    "completed_trials": 3,
                    "terminated_trials": 2
                },
                "insights": [
                    {
                        "type": "trend",
                        "description": "Increasing focus on oncology trials",
                        "confidence": 0.85
                    }
                ],
                "recommendations": [
                    {
                        "type": "strategic",
                        "description": "Consider expanding Phase II oncology trials"
                    }
                ]
            }
        } 