from fastapi import Request, status
from fastapi.responses import JSONResponse
from typing import Union
import logging

logger = logging.getLogger("clinical_trials")

class APIError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message

async def error_handler_middleware(
    request: Request,
    call_next
) -> Union[Response, JSONResponse]:
    try:
        return await call_next(request)
    except APIError as e:
        logger.warning(f"API Error: {e.message}")
        return JSONResponse(
            status_code=e.status_code,
            content={"error": e.message}
        )
    except Exception as e:
        logger.error(f"Unhandled error: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "Internal server error"}
        ) 