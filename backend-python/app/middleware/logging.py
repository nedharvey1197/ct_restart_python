from fastapi import Request
import time
import logging
import json

logger = logging.getLogger("clinical_trials")

async def logging_middleware(request: Request, call_next):
    start_time = time.time()
    
    # Log request start
    logger.info(f">>> Starting {request.method} request to {request.url.path}")
    
    try:
        # Get request body if it exists
        body = None
        if request.method in ["POST", "PUT"]:
            try:
                body = await request.json()
                logger.info(f"Request body: {json.dumps(body, indent=2)}")
            except:
                pass
                
        response = await call_next(request)
        
        # Log request completion
        duration = time.time() - start_time
        logger.info(
            f"<<< Completed {request.method} {request.url.path} "
            f"Status: {response.status_code} "
            f"Duration: {duration:.2f}s"
        )
        
        return response
    except Exception as e:
        logger.error(f"Request failed: {str(e)}")
        raise 