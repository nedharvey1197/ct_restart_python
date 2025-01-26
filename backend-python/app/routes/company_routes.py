from fastapi import APIRouter, HTTPException, Response, status
from typing import Optional, List, Dict, Any
from ..models.company import Company
from ..services.company_service import CompanyService
from bson.errors import InvalidId
from bson.objectid import ObjectId
from ..config.database import MongoDB
from datetime import datetime
import logging

router = APIRouter(prefix="/companies", tags=["companies"])

logger = logging.getLogger(__name__)

@router.post("", response_model=Company, status_code=status.HTTP_201_CREATED)
async def create_company(company: Company):
    """Create a new company."""
    try:
        return await CompanyService.create_company(company)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/current", response_model=Optional[Company])
async def get_current_company():
    """Get the most recently created company."""
    try:
        company = await CompanyService.get_current_company()
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No companies found"
            )
        return company
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{company_id}")
async def get_company(company_id: str):
    """Get company by ID"""
    try:
        async with MongoDB.get_collection("companies") as collection:
            company = await collection.find_one({"_id": ObjectId(company_id)})
            
            if not company:
                raise HTTPException(status_code=404, detail="Company not found")
            
            return {
                "data": {
                    "hasAnalytics": company.get("hasAnalytics", False),
                    "analytics": company.get("trialAnalytics", {}),
                    "trialsCount": company.get("trialsCount", 0)
                }
            }
            
    except Exception as e:
        logger.error(f"Error getting company: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{company_id}", response_model=Company)
async def update_company(company_id: str, company_data: dict):
    """Update a company's information."""
    try:
        updated_company = await CompanyService.update_company(company_id, company_data)
        if not updated_company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company not found"
            )
        return updated_company
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid company ID format"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/all", response_model=List[Company])
async def get_all_companies():
    """Get all companies."""
    try:
        async with MongoDB.get_collection(CompanyService.COLLECTION) as collection:
            companies = []
            cursor = collection.find({}).sort("updated_at", -1)
            async for doc in cursor:
                doc["_id"] = str(doc["_id"])
                companies.append(Company(**doc))
            return companies
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.delete("/{company_id}")
async def delete_company(company_id: str):
    """Delete a specific company."""
    try:
        async with MongoDB.get_collection(CompanyService.COLLECTION) as collection:
            result = await collection.delete_one({"_id": ObjectId(company_id)})
            if result.deleted_count:
                return {"message": "Company deleted successfully"}
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company not found"
            )
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid company ID"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/{company_id}/trials", response_model=Dict[str, Any])
async def save_trial_analysis(company_id: str, trial_data: Dict[str, Any]):
    """Save trial analysis data for a company."""
    try:
        logger.info(f"Saving trial analysis for company {company_id}")
        logger.debug(f"Raw trial data: {trial_data}")
        
        # Extract the actual analytics data
        analytics = {
            "phaseDistribution": trial_data.get("topLevel", {}).get("phaseDistribution", {}),
            "statusSummary": trial_data.get("topLevel", {}).get("statusSummary", {}),
            "therapeuticAreas": trial_data.get("topLevel", {}).get("therapeuticAreas", {}),
            "totalTrials": trial_data.get("studies", {}).get("count", 0)
        }
        
        logger.info(f"Structured analytics: {analytics}")
        
        async with MongoDB.get_collection(CompanyService.COLLECTION) as collection:
            update_data = {
                "trialAnalytics": analytics,
                "hasTrialAnalytics": True,
                "lastAnalyzed": datetime.utcnow(),
                "trialsCount": analytics["totalTrials"]
            }
            
            result = await collection.update_one(
                {"_id": ObjectId(company_id)},
                {"$set": update_data}
            )
            
            if result.modified_count:
                logger.info(f"Successfully updated company {company_id} with analytics")
                return {"success": True, "savedAnalytics": True}
            logger.error(f"Company {company_id} not found")
            raise HTTPException(status_code=404, detail="Company not found")
    except Exception as e:
        logger.error(f"Error saving trial analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 