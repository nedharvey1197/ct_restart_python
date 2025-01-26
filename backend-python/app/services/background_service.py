from fastapi.background import BackgroundTasks
from typing import List
from ..models.trial import ClinicalTrial
from .trial_service import TrialService
from .cache_service import CacheService

class BackgroundService:
    def __init__(self):
        self.cache = CacheService()

    async def analyze_trials_background(
        self,
        company_id: str,
        trials: List[ClinicalTrial],
        background_tasks: BackgroundTasks
    ):
        """Queue trial analysis as background task."""
        # Start analysis immediately but don't wait
        background_tasks.add_task(
            self._run_analysis,
            company_id,
            trials
        )
        
        return {"status": "Analysis started", "company_id": company_id}

    async def _run_analysis(self, company_id: str, trials: List[ClinicalTrial]):
        """Run the actual analysis."""
        try:
            analytics = await TrialService.analyze_trials(trials)
            await TrialService.save_trial_analysis(company_id, trials)
            await self.cache.set_trial_analytics(company_id, analytics.dict())
        except Exception as e:
            # Log error and possibly notify monitoring system
            logger.error(f"Background analysis failed: {e}") 