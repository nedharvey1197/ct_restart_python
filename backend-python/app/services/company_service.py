from typing import Optional, List
from bson import ObjectId
from ..models.company import Company
from ..config.database import MongoDB
from datetime import datetime
import logging
from fastapi import HTTPException, status
import asyncio

logger = logging.getLogger(__name__)

class CompanyService:
    COLLECTION = "companies"

    @staticmethod
    async def create_company(company_data: Company) -> Company:
        logger.info(f"Starting create_company for: {company_data.companyName}")
        try:
            async with MongoDB.get_collection(CompanyService.COLLECTION) as collection:
                logger.info("Got MongoDB collection")
                company_dict = company_data.model_dump(exclude={"id"})
                company_dict["updated_at"] = datetime.utcnow()
                
                if not company_dict.get("created_at"):
                    company_dict["created_at"] = company_dict["updated_at"]
                
                logger.info("Attempting to update/create company")
                result = await collection.find_one_and_update(
                    {"companyName": company_data.companyName},
                    {"$set": company_dict},
                    upsert=True,
                    return_document=True
                )
                
                if result:
                    logger.info("Successfully updated/created company")
                    result["_id"] = str(result["_id"])
                    return Company(**result)
                
                logger.error("Failed to create/update company")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create/update company"
                )
        except Exception as e:
            logger.error(f"Error in create_company: {str(e)}")
            raise
        finally:
            logger.info("Finished create_company operation")

    @staticmethod
    async def get_company(company_id: str) -> Optional[Company]:
        async with MongoDB.get_collection(CompanyService.COLLECTION) as collection:
            result = await collection.find_one({"_id": ObjectId(company_id)})
            if result:
                result["_id"] = str(result["_id"])
                return Company(**result)
            return None

    @staticmethod
    async def get_current_company() -> Optional[Company]:
        logger.info("Getting current company")
        try:
            async with MongoDB.get_collection(CompanyService.COLLECTION) as collection:
                # Get the most recently updated company
                result = await collection.find_one(
                    {},  # Empty filter to get any company
                    sort=[("updated_at", -1)]  # Sort by last updated
                )
                
                if result:
                    logger.info(f"Found existing company: {result.get('companyName')}")
                    result["_id"] = str(result["_id"])
                    return Company(**result)
                else:
                    # Create a blank company if none exists
                    logger.info("No companies found, creating blank company")
                    blank_company = Company(
                        companyName="",
                        companyWebsite="",
                        companySize="",
                        therapeuticAreas=[],
                        headquarters="",
                        contactEmail=""
                    )
                    created = await CompanyService.create_company(blank_company)
                    return created
        except Exception as e:
            logger.error(f"Error in get_current_company: {str(e)}")
            raise

    @staticmethod
    async def update_company(company_id: str, company_data: dict) -> Optional[Company]:
        async with MongoDB.get_collection(CompanyService.COLLECTION) as collection:
            company_data["updated_at"] = datetime.utcnow()
            result = await collection.find_one_and_update(
                {"_id": ObjectId(company_id)},
                {"$set": company_data},
                return_document=True
            )
            if result:
                result["_id"] = str(result["_id"])
                return Company(**result)
            return None

# Add this temporary debug logging
current_loop = asyncio.get_running_loop()
logger.info(f"Current event loop: {current_loop}")
logger.info(f"Loop running: {current_loop.is_running()}") 