from fastapi import APIRouter, HTTPException, status, BackgroundTasks
from typing import List, Dict, Any, Optional
from ..services.trial_service import TrialAnalysisService, CompanyTrialService, TrialService
from ..models.trial import ClinicalTrial
from ..config.database import MongoDB
from bson import ObjectId
from ..services.background_service import BackgroundService
from ..services.cache_service import CacheService
from ..models.trial_analysis import TrialAnalysis
import logging

# Current production endpoints
router = APIRouter(prefix="/api/companies", tags=["trials"])

background_service = BackgroundService()
cache_service = CacheService()

logger = logging.getLogger(__name__)

@router.post("/analyze", response_model=Dict[str, Any])
async def analyze_trials(
    trials: List[ClinicalTrial],
    options: Optional[Dict[str, Any]] = None
):
    """Generic trial analysis endpoint - can be used for any trials."""
    try:
        analytics = await TrialAnalysisService.analyze_batch(trials, options)
        return {"data": analytics.dict()}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/{company_id}/analysis")
async def save_trial_analysis(
    company_id: str,
    analysis_data: dict
):
    """Save trial analysis matching Node.js endpoint"""
    try:
        logger.info("=== Debug: save_trial_analysis ===")
        logger.info(f"Company ID: {company_id}")
        logger.info(f"Analysis data type: {type(analysis_data)}")
        logger.info(f"Analysis data keys: {analysis_data.keys()}")
        logger.debug(f"Analysis data: {analysis_data}")
        logger.info("=================================")
        
        result = await CompanyTrialService.save_trial_analysis(
            company_id=company_id,
            analysis_data=analysis_data
        )
        return {"data": result}
    except ValueError as e:
        logger.error(f"ValueError in save_trial_analysis: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error in save_trial_analysis: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/{company_id}/trials/analyze")
async def analyze_trials_background(
    company_id: str,
    trials: List[ClinicalTrial],
    background_tasks: BackgroundTasks
):
    """Start trial analysis in background."""
    return await background_service.analyze_trials_background(
        company_id,
        trials,
        background_tasks
    )

@router.get("/{company_id}/trials")
async def get_company_trials(company_id: str):
    """Get all trials for a company with caching."""
    try:
        # Try cache first
        cached_trials = await cache_service.get_trials(company_id)
        if cached_trials:
            return {"data": cached_trials, "cached": True}

        # Get from database
        trials = await TrialService.get_company_trials(company_id)
        
        # Cache the results
        await cache_service.set_trials(company_id, trials)
        
        return {"data": trials}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/{company_id}/trials")
async def save_company_trials(
    company_id: str,
    trials: List[ClinicalTrial]
):
    """Save trials for a company."""
    try:
        result = await CompanyTrialService.save_company_trials(
            company_id, trials, None  # No advanced analysis options
        )
        return {"data": result}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.get("/{nct_id}")
async def get_trial(nct_id: str):
    """Get trial by NCT ID."""
    trial = await TrialService.get_trial_by_nct_id(nct_id)
    if not trial:
        raise HTTPException(status_code=404, detail="Trial not found")
    return {"data": trial}

# Future advanced analysis endpoints (not currently in use)
future_router = APIRouter(prefix="/api/future/analysis", tags=["future-analysis"])

@future_router.post("/trials/analyze")
async def future_analyze_trials(
    trials: List[ClinicalTrial],
    options: Optional[Dict[str, Any]] = None
):
    """Future endpoint: Advanced trial analysis with ML and comparative features."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="This advanced analysis endpoint is planned for future implementation"
    )

@future_router.post("/companies/{company_id}/trials/analyze")
async def future_analyze_company_trials(
    company_id: str,
    trials: List[ClinicalTrial],
    background_tasks: BackgroundTasks
):
    """Future endpoint: Advanced background analysis of company trials."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="This advanced analysis endpoint is planned for future implementation"
    ) 