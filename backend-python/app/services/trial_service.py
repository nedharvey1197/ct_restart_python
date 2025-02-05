"""
Clinical Trials Service Module

Current Implementation:
- CompanyTrialService: Handles company-trial relationships and storage
  - save_company_trials: Store trials and analytics for a company
  - get_company_trials: Retrieve trials and analytics
  - save_trial_analysis: Store analysis matching Node.js structure

Future Implementation:
- Advanced trial analysis (see future_concepts/future_trial_analysis.py)
- ML-based analysis (see future_concepts/future_ml_analysis.py)
- Comparative analysis (see future_concepts/future_comparative_analysis.py)
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from ..models.trial import ClinicalTrial, TrialAnalytics, TrialAnalysis
from ..config.database import MongoDB
from bson import ObjectId
from .cache_service import CacheService
from ..services.schema_service import SchemaService
from ..system_specs.schema_manager import SchemaContext
import logging

# Future functionality imports (currently unused)
"""
from .future_concepts.future_trial_analysis import FutureAdvancedTrialAnalyzer
from .future_concepts.future_ml_analysis import FutureMLAnalyzer
from .future_concepts.future_comparative_analysis import FutureComparativeAnalyzer
"""

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
        context = await SchemaService.get_collection_context(CompanyTrialService.COLLECTION)
        analytics = await TrialAnalysisService.analyze_batch(trials, analysis_options)
        
        async with MongoDB.get_collection(CompanyTrialService.COLLECTION) as collection:
            # First validate the existing document
            company = await collection.find_one({"_id": ObjectId(company_id)})
            if company:
                if not await SchemaService.validate_document(CompanyTrialService.COLLECTION, company, context):
                    company = await SchemaService.migrate_document(
                        collection_name=CompanyTrialService.COLLECTION,
                        document=company,
                        from_context=SchemaContext.LEGACY,
                        to_context=context
                    )

            # Prepare update data
            update_data = {
                "trials": [trial.model_dump() for trial in trials],
                "trial_analytics": analytics.model_dump(),
                "updated_at": datetime.utcnow()
            }
            
            # Validate update data against current context
            if not await SchemaService.validate_document(CompanyTrialService.COLLECTION, update_data, context):
                logger.error("Update data validation failed")
                raise ValueError("Invalid update data for current schema context")
            
            result = await collection.find_one_and_update(
                {"_id": ObjectId(company_id)},
                {"$set": update_data},
                return_document=True
            )
            
            if not result:
                raise ValueError("Company not found")

            result["_id"] = str(result["_id"])
            return result

    @staticmethod
    async def get_company_trials(company_id: str) -> Dict[str, Any]:
        """Get all trials and analytics for a company."""
        context = await SchemaService.get_collection_context(CompanyTrialService.COLLECTION)
        async with MongoDB.get_collection(CompanyTrialService.COLLECTION) as collection:
            result = await collection.find_one(
                {"_id": ObjectId(company_id)},
                {"trials": 1, "trial_analytics": 1, "updated_at": 1}
            )
            
            if not result:
                raise ValueError("Company not found")
            
            # Validate and potentially migrate document
            if not await SchemaService.validate_document(CompanyTrialService.COLLECTION, result, context):
                result = await SchemaService.migrate_document(
                    collection_name=CompanyTrialService.COLLECTION,
                    document=result,
                    from_context=SchemaContext.LEGACY,
                    to_context=context
                )
            
            result["_id"] = str(result["_id"])
            return {
                "trials": result.get("trials", []),
                "analytics": result.get("trial_analytics", {}),
                "updated_at": result.get("updated_at")
            }

    @staticmethod
    async def update_trial_analysis(company_id: str, trials: List[ClinicalTrial]) -> Dict[str, Any]:
        """Update existing trial analysis."""
        context = await SchemaService.get_collection_context(CompanyTrialService.COLLECTION)
        analytics = await TrialAnalysisService.analyze_batch(trials)
        
        update_data = {
            "trial_analytics": analytics.model_dump(),
            "updated_at": datetime.utcnow()
        }
        
        # Validate update data against current context
        if not await SchemaService.validate_document(CompanyTrialService.COLLECTION, update_data, context):
            logger.error("Update data validation failed")
            raise ValueError("Invalid update data for current schema context")
        
        async with MongoDB.get_collection(CompanyTrialService.COLLECTION) as collection:
            result = await collection.find_one_and_update(
                {"_id": ObjectId(company_id)},
                {"$set": update_data},
                return_document=True
            )
            
            if not result:
                raise ValueError("Company not found")
            
            result["_id"] = str(result["_id"])
            return result

    @staticmethod
    async def get_trial_details(company_id: str, trial_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information for a specific trial."""
        context = await SchemaService.get_collection_context(CompanyTrialService.COLLECTION)
        async with MongoDB.get_collection(CompanyTrialService.COLLECTION) as collection:
            result = await collection.find_one(
                {"_id": ObjectId(company_id)},
                {"trials": {"$elemMatch": {"nct_id": trial_id}}}
            )
            
            if not result or not result.get("trials"):
                return None
            
            # Validate and potentially migrate document
            if not await SchemaService.validate_document(CompanyTrialService.COLLECTION, result, context):
                result = await SchemaService.migrate_document(
                    collection_name=CompanyTrialService.COLLECTION,
                    document=result,
                    from_context=SchemaContext.LEGACY,
                    to_context=context
                )
            
            return result["trials"][0]

    @staticmethod
    async def save_trial_analysis(company_id: str, analysis_data: dict):
        """Save trial analysis matching Node.js endpoint structure"""
        try:
            async with MongoDB.get_collection("companies") as collection:
                # Transform incoming data to match Node.js structure exactly
                update_data = {
                    "clinicalTrials": analysis_data["studies"],
                    "trialAnalytics": {
                        "phaseDistribution": analysis_data["analytics"]["phaseDistribution"],
                        "statusSummary": analysis_data["analytics"]["statusSummary"],
                        "therapeuticAreas": analysis_data["analytics"]["therapeuticAreas"]
                    },
                    "hasAnalytics": True,
                    "lastUpdated": datetime.utcnow(),
                    "trialsCount": len(analysis_data["studies"])  # Calculate from array length
                }
                
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
        """Get trial data by ID."""
        context = await SchemaService.get_collection_context(TrialService.COLLECTION)
        async with MongoDB.get_collection(TrialService.COLLECTION) as collection:
            result = await collection.find_one({"_id": ObjectId(trial_id)})
            if result:
                result["_id"] = str(result["_id"])
                # Validate and potentially migrate document
                if not await SchemaService.validate_document(TrialService.COLLECTION, result, context):
                    result = await SchemaService.migrate_document(
                        collection_name=TrialService.COLLECTION,
                        document=result,
                        from_context=SchemaContext.LEGACY,
                        to_context=context
                    )
                return result
            return None

    @staticmethod
    async def save_trial_data(company_id: str, trials: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Save trial data."""
        context = await SchemaService.get_collection_context(TrialService.COLLECTION)
        async with MongoDB.get_collection(TrialService.COLLECTION) as collection:
            for trial in trials:
                trial["company_id"] = company_id
                trial["updated_at"] = datetime.utcnow()
                if not trial.get("created_at"):
                    trial["created_at"] = trial["updated_at"]
                
                # Validate trial data against current context
                if not await SchemaService.validate_document(TrialService.COLLECTION, trial, context):
                    logger.error("Trial data validation failed")
                    raise ValueError("Invalid trial data for current schema context")
                
                await collection.find_one_and_update(
                    {"nct_id": trial["nct_id"]},
                    {"$set": trial},
                    upsert=True
                )
            
            return {"success": True, "count": len(trials)}

    @staticmethod
    async def get_company_trials(company_id: str) -> List[Dict[str, Any]]:
        """Get all trials for a company."""
        context = await SchemaService.get_collection_context(TrialService.COLLECTION)
        async with MongoDB.get_collection(TrialService.COLLECTION) as collection:
            cursor = collection.find({"company_id": company_id})
            trials = []
            async for trial in cursor:
                trial["_id"] = str(trial["_id"])
                # Validate and potentially migrate document
                if not await SchemaService.validate_document(TrialService.COLLECTION, trial, context):
                    trial = await SchemaService.migrate_document(
                        collection_name=TrialService.COLLECTION,
                        document=trial,
                        from_context=SchemaContext.LEGACY,
                        to_context=context
                    )
                trials.append(trial)
            return trials

    @staticmethod
    async def get_trial_by_nct_id(nct_id: str) -> Optional[Dict[str, Any]]:
        """Get trial by NCT ID."""
        context = await SchemaService.get_collection_context(TrialService.COLLECTION)
        async with MongoDB.get_collection(TrialService.COLLECTION) as collection:
            result = await collection.find_one({"nct_id": nct_id})
            if result:
                result["_id"] = str(result["_id"])
                # Validate and potentially migrate document
                if not await SchemaService.validate_document(TrialService.COLLECTION, result, context):
                    result = await SchemaService.migrate_document(
                        collection_name=TrialService.COLLECTION,
                        document=result,
                        from_context=SchemaContext.LEGACY,
                        to_context=context
                    )
                return result
            return None 