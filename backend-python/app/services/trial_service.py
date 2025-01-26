from typing import Dict, List, Any, Optional
from datetime import datetime
from ..models.trial import ClinicalTrial, TrialAnalytics, TrialAnalysis
from ..config.database import MongoDB
from bson import ObjectId
from .trial_analysis import FutureAdvancedTrialAnalyzer
from .ml_analysis import FutureMLAnalyzer as TrialMLAnalyzer
from .comparative_analysis import FutureComparativeAnalyzer as ComparativeAnalyzer
from .cache_service import CacheService
import logging

logger = logging.getLogger("clinical_trials")

class TrialAnalysisService:
    """
    Generic service for analyzing clinical trials data.
    Currently implements basic analysis, with hooks for future advanced features.
    """
    
    @staticmethod
    async def analyze_batch(
        trials: List[ClinicalTrial],
        analysis_options: Optional[Dict[str, Any]] = None
    ) -> TrialAnalytics:
        """Enhanced batch analysis with multiple analysis types."""
        analyzer = FutureAdvancedTrialAnalyzer()

        # Basic analysis - currently active
        basic_analysis = {
            "phases": analyzer.analyze_phases(trials),
            "therapeutic_areas": analyzer.analyze_therapeutic_areas(trials),
            "enrollment": analyzer.analyze_enrollment(trials),
            "timeline": analyzer.analyze_timeline(trials)
        }

        # Future advanced analysis features - currently disabled
        # if analysis_options and analysis_options.get("include_advanced", False):
        #     from .ml_analysis import FutureMLAnalyzer
        #     from .comparative_analysis import FutureComparativeAnalyzer
        #     
        #     ml_analyzer = FutureMLAnalyzer()
        #     comparative_analyzer = FutureComparativeAnalyzer()
        #     
        #     basic_analysis.update({
        #         "trends": analyzer.analyze_trends(trials),
        #         "geographic": analyzer.analyze_geographic_distribution(trials),
        #         "interventions": analyzer.analyze_intervention_patterns(trials),
        #         "outcomes": analyzer.analyze_outcome_measures(trials),
        #         "clusters": ml_analyzer.cluster_trials(trials),
        #         "success_factors": ml_analyzer.predict_success_factors(trials),
        #         "industry_comparison": comparative_analyzer.analyze_relative_to_industry(
        #             trials, 
        #             analysis_options.get("industry_data", {})
        #         ),
        #         "therapeutic_trends": comparative_analyzer.analyze_therapeutic_trends(
        #             trials,
        #             analysis_options.get("historical_data", {})
        #         )
        #     })

        return TrialAnalytics(**basic_analysis)

class CompanyTrialService:
    """Service specifically for handling company-related trial operations."""
    
    COLLECTION = "companies"

    @staticmethod
    async def save_company_trials(
        company_id: str,
        trials: List[ClinicalTrial],
        analysis_options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Save and analyze trials specifically for a company."""
        analytics = await TrialAnalysisService.analyze_batch(trials, analysis_options)
        
        async with MongoDB.get_collection(CompanyTrialService.COLLECTION) as collection:
            result = await collection.find_one_and_update(
                {"_id": ObjectId(company_id)},
                {
                    "$set": {
                        "clinicalTrials": [trial.dict() for trial in trials],
                        "trialAnalytics": analytics.dict(),
                        "lastAnalyzed": datetime.utcnow()
                    }
                },
                return_document=True
            )
            
            if not result:
                raise ValueError("Company not found")

            return {
                "trialAnalytics": result["trialAnalytics"],
                "lastAnalyzed": result["lastAnalyzed"]
            }

    @staticmethod
    async def get_company_trials(company_id: str) -> Dict[str, Any]:
        """Get all trials and analytics for a company."""
        async with MongoDB.get_collection(CompanyTrialService.COLLECTION) as collection:
            company = await collection.find_one({"_id": ObjectId(company_id)})
            if not company:
                raise ValueError("Company not found")
            
            return {
                "trials": company.get("clinicalTrials", []),
                "analytics": company.get("trialAnalytics", {}),
                "lastAnalyzed": company.get("lastAnalyzed")
            }

    @staticmethod
    async def update_trial_analysis(company_id: str, trials: List[ClinicalTrial]) -> Dict[str, Any]:
        """Update existing trial analysis."""
        analytics = await TrialAnalysisService.analyze_batch(trials)
        
        # Update with new analysis but keep existing trials
        async with MongoDB.get_collection(CompanyTrialService.COLLECTION) as collection:
            result = await collection.find_one_and_update(
                {"_id": ObjectId(company_id)},
                {
                    "$set": {
                        "trialAnalytics": analytics.dict(),
                        "lastAnalyzed": datetime.utcnow()
                    }
                },
                return_document=True
            )
            
            if not result:
                raise ValueError("Company not found")
            
            return {
                "trialAnalytics": result["trialAnalytics"],
                "lastAnalyzed": result["lastAnalyzed"]
            }

    @staticmethod
    async def get_trial_details(company_id: str, trial_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information for a specific trial."""
        async with MongoDB.get_collection(CompanyTrialService.COLLECTION) as collection:
            result = await collection.find_one(
                {"_id": ObjectId(company_id)},
                {"clinicalTrials": {"$elemMatch": {"protocolSection.identificationModule.nctId": trial_id}}}
            )
            
            if not result or not result.get("clinicalTrials"):
                return None
                
            return result["clinicalTrials"][0]

    @staticmethod
    async def save_trial_analysis(company_id: str, analysis_data: dict):
        """Save trial analysis matching Node.js endpoint structure"""
        try:
            async with MongoDB.get_collection("companies") as collection:
                # Transform incoming data to match Node.js structure
                update_data = {
                    "clinicalTrials": analysis_data["studies"],
                    "trialAnalytics": {
                        "phaseDistribution": analysis_data["analytics"]["phaseDistribution"],
                        "statusSummary": analysis_data["analytics"]["statusSummary"],
                        "therapeuticAreas": analysis_data["analytics"]["therapeuticAreas"]
                    },
                    "hasAnalytics": True,
                    "lastUpdated": datetime.utcnow(),
                    "trialsCount": analysis_data["analytics"]["totalTrials"],
                    # Keep additional metadata
                    "analyticsMetadata": analysis_data["metadata"]
                }
                
                logger.info(f"Saving analysis for company {company_id}")
                logger.debug(f"Update data structure: {update_data.keys()}")
                
                result = await collection.update_one(
                    {"_id": ObjectId(company_id)},
                    {"$set": update_data}
                )
                
                if result.modified_count == 0:
                    raise ValueError(f"Company {company_id} not found")
                    
                return {
                    "success": True,
                    "data": update_data
                }
                
        except Exception as e:
            logger.error(f"Error in save_trial_analysis: {str(e)}")
            raise e

class TrialService:
    """Core trial data operations matching Node.js backend"""
    COLLECTION = "trials"

    @staticmethod
    async def get_trial_data(trial_id: str) -> Optional[Dict[str, Any]]:
        """Get raw trial data"""
        async with MongoDB.get_collection(TrialService.COLLECTION) as collection:
            trial = await collection.find_one({"_id": trial_id})
            return trial if trial else None

    @staticmethod
    async def save_trial_data(company_id: str, trials: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Save raw trial data for a company"""
        async with MongoDB.get_collection("companies") as collection:
            result = await collection.find_one_and_update(
                {"_id": ObjectId(company_id)},
                {"$set": {"clinicalTrials": trials}},
                return_document=True
            )
            if not result:
                raise ValueError("Company not found")
            return {"success": True, "count": len(trials)}

    @staticmethod
    async def get_company_trials(company_id: str) -> List[Dict[str, Any]]:
        """Get all trials for a company"""
        async with MongoDB.get_collection("companies") as collection:
            company = await collection.find_one({"_id": ObjectId(company_id)})
            if not company:
                raise ValueError("Company not found")
            return company.get("clinicalTrials", [])

    @staticmethod
    async def get_trial_by_nct_id(nct_id: str) -> Optional[Dict[str, Any]]:
        """Get trial by NCT ID"""
        async with MongoDB.get_collection(TrialService.COLLECTION) as collection:
            return await collection.find_one({"nctId": nct_id}) 