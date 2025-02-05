from fastapi import APIRouter, HTTPException, status, BackgroundTasks
from typing import List, Dict, Any, Optional
from ..services.trial_service import TrialAnalysisService, CompanyTrialService, TrialService
from ..models.trial import Trial, TrialAnalytics, TrialAnalysis
from ..services.schema_service import SchemaService
from ..system_specs.schema_manager import SchemaContext
from ..config.database import MongoDB
from bson import ObjectId
from ..services.background_service import BackgroundService
from ..services.cache_service import CacheService
import logging

# Current production endpoints
router = APIRouter(prefix="/api/companies", tags=["trials"])

background_service = BackgroundService()
cache_service = CacheService()

logger = logging.getLogger(__name__)

@router.post("/analyze", response_model=Dict[str, Any])
async def analyze_trials(
    trials: List[Trial],
    options: Optional[Dict[str, Any]] = None
):
    """Generic trial analysis endpoint - can be used for any trials."""
    try:
        analytics = await TrialAnalysisService.analyze_batch(trials, options)
        return {"data": analytics.model_dump()}
    except Exception as e:
        logger.error(f"Error in analyze_trials: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/{company_id}/analysis")
async def save_trial_analysis(
    company_id: str,
    analysis_data: dict
):
    """Save trial analysis with schema validation."""
    try:
        logger.info(f"Saving trial analysis for company {company_id}")
        
        # Get current context
        context = await SchemaService.get_collection_context(CompanyTrialService.COLLECTION)
        
        # Validate analysis data against schema
        if not await SchemaService.validate_document(CompanyTrialService.COLLECTION, analysis_data, context):
            logger.error("Analysis data validation failed")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid analysis data for current schema context"
            )
        
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
    trials: List[Trial],
    background_tasks: BackgroundTasks
):
    """Start trial analysis in background with schema validation."""
    try:
        # Get current context
        context = await SchemaService.get_collection_context(CompanyTrialService.COLLECTION)
        
        # Validate each trial against schema
        for trial in trials:
            trial_dict = trial.model_dump()
            if not await SchemaService.validate_document(TrialService.COLLECTION, trial_dict, context):
                logger.error(f"Trial validation failed for trial {trial.nct_id}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid trial data for current schema context: {trial.nct_id}"
                )
        
        return await background_service.analyze_trials_background(
            company_id,
            trials,
            background_tasks
        )
    except Exception as e:
        logger.error(f"Error in analyze_trials_background: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{company_id}/trials")
async def get_company_trials(company_id: str):
    """Get all trials for a company with caching and schema validation."""
    try:
        # Try cache first
        cached_trials = await cache_service.get_trials(company_id)
        if cached_trials:
            return {"data": cached_trials, "cached": True}

        # Get current context
        context = await SchemaService.get_collection_context(TrialService.COLLECTION)
        
        # Get from database
        trials = await TrialService.get_company_trials(company_id)
        
        # Validate trials against schema
        for trial in trials:
            if not await SchemaService.validate_document(TrialService.COLLECTION, trial, context):
                trial = await SchemaService.migrate_document(
                    collection_name=TrialService.COLLECTION,
                    document=trial,
                    from_context=SchemaContext.LEGACY,
                    to_context=context
                )
        
        # Cache the results
        await cache_service.set_trials(company_id, trials)
        
        return {"data": trials}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error in get_company_trials: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/{company_id}/trials")
async def save_company_trials(
    company_id: str,
    trials: List[Trial]
):
    """Save trials for a company with schema validation."""
    try:
        # Get current context
        context = await SchemaService.get_collection_context(CompanyTrialService.COLLECTION)
        
        # Validate each trial against schema
        for trial in trials:
            trial_dict = trial.model_dump()
            if not await SchemaService.validate_document(TrialService.COLLECTION, trial_dict, context):
                logger.error(f"Trial validation failed for trial {trial.nct_id}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid trial data for current schema context: {trial.nct_id}"
                )
        
        result = await CompanyTrialService.save_company_trials(
            company_id, trials, None  # No advanced analysis options
        )
        return {"data": result}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error in save_company_trials: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{nct_id}")
async def get_trial(nct_id: str):
    """Get trial by NCT ID with schema validation."""
    try:
        trial = await TrialService.get_trial_by_nct_id(nct_id)
        if not trial:
            raise HTTPException(status_code=404, detail="Trial not found")
        
        # Get current context and validate
        context = await SchemaService.get_collection_context(TrialService.COLLECTION)
        if not await SchemaService.validate_document(TrialService.COLLECTION, trial, context):
            trial = await SchemaService.migrate_document(
                collection_name=TrialService.COLLECTION,
                document=trial,
                from_context=SchemaContext.LEGACY,
                to_context=context
            )
        
        return {"data": trial}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_trial: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Future advanced analysis endpoints (not currently in use)
future_router = APIRouter(prefix="/api/future/analysis", tags=["future-analysis"])

@future_router.post("/trials/analyze")
async def future_analyze_trials(
    trials: List[Trial],
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
    trials: List[Trial],
    background_tasks: BackgroundTasks
):
    """Future endpoint: Advanced background analysis of company trials."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="This advanced analysis endpoint is planned for future implementation"
    ) 