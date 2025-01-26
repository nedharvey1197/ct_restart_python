from fastapi import Request, HTTPException
from pydantic import ValidationError

async def validation_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except ValidationError as e:
        return JSONResponse(
            status_code=422,
            content={"errors": e.errors()}
        ) 