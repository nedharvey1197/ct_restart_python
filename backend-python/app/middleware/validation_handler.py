from fastapi import Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
import logging

logger = logging.getLogger("clinical_trials")

async def validation_error_handler(request: Request, call_next):
    try:
        return await call_next(request)
    except ValidationError as e:
        logger.warning(f"Validation error: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": "Data validation error",
                "details": e.errors()
            }
        )
    except ValueError as e:
        logger.warning(f"Value error: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": str(e)}
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "Internal server error"}
        ) 