from typing import Optional, List
from bson import ObjectId
from ..models.company import Company
from ..config.database import MongoDB
from datetime import datetime
import logging
from fastapi import HTTPException, status
import asyncio
from app.system_specs.schema_manager import schema_manager, SchemaContext

logger = logging.getLogger(__name__)

class CompanyService:
    COLLECTION = "companies"

    @staticmethod
    async def create_company(company_data: dict, schema_name: str = "Enhanced") -> dict:
        logger.info(f"Creating company with schema: {schema_name}")
        schema = schema_manager.get_schema(schema_name)
        validated_data = schema(**company_data).dict()
        async with MongoDB.get_collection(CompanyService.COLLECTION) as collection:
            result = await collection.find_one_and_update(
                {"name": validated_data["name"]},
                {"$set": validated_data},
                upsert=True,
                return_document=True
            )
            if result:
                logger.info(f"Company created with ID: {result['_id']}")
                result["_id"] = str(result["_id"])
                return result
            logger.error("Failed to create/update company")
            raise HTTPException(status_code=500, detail="Failed to create/update company")

    @staticmethod
    async def get_company(company_id: str, schema_name: str = "Enhanced") -> dict:
        logger.info(f"Retrieving company with ID: {company_id} using schema: {schema_name}")
        async with MongoDB.get_collection(CompanyService.COLLECTION) as collection:
            result = await collection.find_one({"_id": ObjectId(company_id)})
            if result:
                logger.info(f"Company retrieved: {result}")
                result["_id"] = str(result["_id"])
                return result
            logger.warning(f"Company not found with ID: {company_id}")
            raise HTTPException(status_code=404, detail="Company not found")

    @staticmethod
    async def get_current_company(schema_name: str = "Enhanced") -> Optional[Company]:
        logger.info("Getting current company")
        try:
            async with MongoDB.get_collection(CompanyService.COLLECTION) as collection:
                result = await collection.find_one(
                    {},  # Empty filter to get any company
                    sort=[("updated_at", -1)]  # Sort by last updated
                )
                
                if result:
                    logger.info(f"Found existing company: {result.get('name', result.get('companyName', ''))}")
                    result["_id"] = str(result["_id"])
                    return schema_manager.get_schema(schema_name)(**result)
                else:
                    logger.info("No companies found, creating blank company")
                    blank_company = schema_manager.get_schema(schema_name)(
                        name="",
                        company_identifiers={"website": ""},
                        profile={"size": "", "therapeutic_areas": []}
                    )
                    created = await CompanyService.create_company(blank_company.dict(), schema_name)
                    return created
        except Exception as e:
            logger.error(f"Error in get_current_company: {str(e)}")
            raise

    @staticmethod
    async def update_company(company_id: str, company_data: dict, schema_name: str = "Enhanced") -> Optional[Company]:
        logger.info(f"Updating company with ID: {company_id} using schema: {schema_name}")
        async with MongoDB.get_collection(CompanyService.COLLECTION) as collection:
            company_data["updated_at"] = datetime.utcnow()
            result = await collection.find_one_and_update(
                {"_id": ObjectId(company_id)},
                {"$set": company_data},
                return_document=True
            )
            if result:
                logger.info(f"Company updated: {result}")
                result["_id"] = str(result["_id"])
                return schema_manager.get_schema(schema_name)(**result)
            logger.warning(f"Company not found with ID: {company_id}")
            return None

@staticmethod
async def delete_company(company_id: str) -> bool:
    logger.info(f"Deleting company with ID: {company_id}")
    async with MongoDB.get_collection(CompanyService.COLLECTION) as collection:
        result = await collection.delete_one({"_id": ObjectId(company_id)})
        if result.deleted_count:
            logger.info(f"Company deleted with ID: {company_id}")
            return True
        logger.warning(f"Company not found with ID: {company_id}")
        return False