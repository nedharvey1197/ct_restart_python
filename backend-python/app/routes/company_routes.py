"""
Company Routes Module

Handles all company-related API endpoints including:
- Company listing and retrieval
- Company updates
- Trial data management
- Analytics processing
"""

from fastapi import APIRouter, HTTPException, Response, status
from typing import Optional, List, Dict, Any
from ..models.company import Company
from ..services.company_service import CompanyService
from bson.errors import InvalidId
from bson.objectid import ObjectId
from ..config.database import MongoDB
from datetime import datetime
import logging
from ..system_specs.schema_manager import schema_manager, SchemaContext

router = APIRouter(prefix="/companies", tags=["companies"])

logger = logging.getLogger(__name__)

# List Operations - Should come first
@router.get("/all", response_model=List[Company])
async def get_all_companies(schema_name: str = "Enhanced"):
    """Get all companies."""
    logger.info(f"API call to get all companies using schema: {schema_name}")
    try:
        async with MongoDB.get_collection(CompanyService.COLLECTION) as collection:
            companies = []
            cursor = collection.find({})
            async for doc in cursor:
                doc["_id"] = str(doc["_id"])
                companies.append(schema_manager.get_schema(schema_name)(**doc))
            return companies
    except Exception as e:
        logger.error(f"Error retrieving all companies: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
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

@router.post("/")
async def create_company(company_data: dict, schema_name: str = "EnhancedCompany"):
    logger.info(f"API call to create company with schema: {schema_name}")
    company_id = await CompanyService.create_company(company_data, schema_name)
    if not company_id:
        logger.error("Company creation failed")
        raise HTTPException(status_code=400, detail="Company creation failed")
    logger.info(f"Company created with ID: {company_id}")
    return {"id": company_id}

# Specific Company Operations
@router.get("/{company_id}")
async def get_company(company_id: str, schema_name: str = "EnhancedCompany"):
    logger.info(f"API call to get company with ID: {company_id} using schema: {schema_name}")
    company = await CompanyService.get_company(company_id, schema_name)
    if not company:
        logger.warning(f"Company not found with ID: {company_id}")
        raise HTTPException(status_code=404, detail="Company not found")
    logger.info(f"Company retrieved: {company}")
    return company

@router.put("/{company_id}", response_model=Company)
async def update_company(company_id: str, company_data: dict, schema_name: str = "EnhancedCompany"):
    """Update a company's information."""
    logger.info(f"API call to update company with ID: {company_id} using schema: {schema_name}")
    try:
        updated_company = await CompanyService.update_company(company_id, company_data, schema_name)
        if not updated_company:
            logger.warning(f"Company not found with ID: {company_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company not found"
            )
        logger.info(f"Company updated: {updated_company}")
        return updated_company
    except InvalidId:
        logger.error(f"Invalid company ID format: {company_id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid company ID format"
        )
    except Exception as e:
        logger.error(f"Error updating company: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.delete("/{company_id}")
async def delete_company(company_id: str):
    """Delete a specific company."""
    logger.info(f"API call to delete company with ID: {company_id}")
    try:
        success = await CompanyService.delete_company(company_id)
        if success:
            logger.info(f"Company deleted with ID: {company_id}")
            return {"message": "Company deleted successfully"}
        logger.warning(f"Company not found with ID: {company_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    except InvalidId:
        logger.error(f"Invalid company ID: {company_id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid company ID"
        )
    except Exception as e:
        logger.error(f"Error deleting company: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
        
''' Compsny trisl routs id Depricated and now handles by trial services and routes
@router.post("/{company_id}/trials/data")
async def save_trial_data(company_id: str, trial_data: List[Dict]):
    """Save raw trial data from comprehensiveTrialAnalysis"""
    try:
        logger.info(f'Receiving trials data for company {company_id}')
        logger.info(f'Trials data received, count: {len(trial_data)}')
        
        async with MongoDB.get_collection("companies") as collection:
            update_data = {
                "clinicalTrials": trial_data,
                "lastUpdated": datetime.utcnow()
            }
            result = await collection.update_one(
                {"_id": ObjectId(company_id)},
                {"$set": update_data}
            )
            logger.info('Trials data saved successfully')
            return {"success": True, "trialsCount": len(trial_data)}
    except Exception as e:
        logger.error(f"Error saving trial data: {str(e)}")
        raise e

@router.post("/{company_id}/analysis")
async def save_trial_analysis(company_id: str, analysis_data: Dict):
    """Save analytics and metadata from comprehensiveTrialAnalysis"""
    try:
        logger.info(f'Receiving analysis data for company {company_id}')
        logger.info(f'Analysis data keys: {list(analysis_data.keys())}')
        
        async with MongoDB.get_collection("companies") as collection:
            update_data = {
                "trialAnalytics": analysis_data,
                "lastAnalyzed": datetime.utcnow()
            }
            result = await collection.update_one(
                {"_id": ObjectId(company_id)},
                {"$set": update_data}
            )
            logger.info('Analysis data saved successfully')
            return {"success": True}
    except Exception as e:
        logger.error(f"Error saving analysis data: {str(e)}")
        raise '''