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