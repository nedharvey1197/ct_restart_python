from fastapi import APIRouter
from app.system_specs.schema_manager import schema_manager

router = APIRouter(prefix="/schemas", tags=["schemas"])

@router.get("/all")
async def get_registered_schemas():
    return schema_manager.list_registered_schemas()