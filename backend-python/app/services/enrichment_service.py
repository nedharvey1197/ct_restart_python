from typing import List, Dict, Any

class EnrichmentService:
    """Company and trial data enrichment"""
    
    @staticmethod
    async def enrich_company_data(company_id: str) -> Dict[str, Any]:
        """Add additional company information"""
        # This matches the Node.js enrichment process
        company = await get_company(company_id)
        if not company:
            raise ValueError("Company not found")
            
        enriched_data = {
            "trials": await get_company_trials(company_id),
            "metadata": await get_company_metadata(company_id)
        }
        return enriched_data

    @staticmethod
    async def enrich_trial_data(trials: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enrich trial data with additional context"""
        # This matches the Node.js trial enrichment
        enriched_trials = []
        for trial in trials:
            enriched_trial = {
                **trial,
                "metadata": await get_trial_metadata(trial["nctId"]),
                "status": await get_trial_status(trial["nctId"])
            }
            enriched_trials.append(enriched_trial)
        return enriched_trials 