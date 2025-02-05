"""
Analysis Options Model

Current Purpose:
- Defines configuration options for trial analysis
- Sets parameters for analytics generation

KG Schema Mapping:
- Maps to Decision Support (DS) Schema's SuccessCriteria
- Relates to Signal Generation (SG) Schema's TrendPattern configurations

Required Modifications:
- Add KG reference tracking for analysis configurations
- Include metadata for DS Schema integration
- Add validation rules that align with KG schema requirements
"""
from pydantic import BaseModel
from typing import Optional, Dict, Any

class AnalysisOptions(BaseModel):
    include_advanced: bool = False
    include_ml_insights: bool = False
    include_comparative: bool = False
    industry_data: Optional[Dict[str, Any]] = None
    historical_data: Optional[Dict[str, Any]] = None
    custom_metrics: Optional[Dict[str, Any]] = None
    filtering_criteria: Optional[Dict[str, Any]] = None
    aggregation_level: str = "detailed"
    time_range: Optional[Dict[str, str]] = None

class KGIntegrationPoints:
    baseline_layer = {
        "study_data": {
            "source": "clinical_trial.modules",
            "target_entities": ["Study", "Protocol", "StudyArm"],
            "status": "not_implemented"
        },
        "clinical_data": {
            "source": "clinical_trial.modules",
            "target_entities": ["Condition", "Intervention"],
            "status": "not_implemented"
        }
    }

    core_support_layer = {
        "trial_state": {
            "source": "trial_analytics",
            "target_schema": "TST",
            "status": "future"
        },
        "context_intelligence": {
            "source": ["company", "clinical_trial"],
            "target_schema": "CI",
            "status": "future"
        }
    } 