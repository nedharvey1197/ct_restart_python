from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config.database import MongoDB
from .config.settings import get_settings
from .config.logging_config import setup_logging
from .middleware.logging import logging_middleware
from .routes import company_routes, trial_routes
from .services.cache_service import CacheService
import logging

# Configure detailed logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Log to console
        logging.FileHandler('app.log')  # Log to file
    ]
)
logger = logging.getLogger(__name__)

# Setup logging
settings = get_settings()
cache_service = CacheService()

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG
)

# Add middleware
app.middleware("http")(logging_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database events
@app.on_event("startup")
async def startup_db_client():
    logger.info("Starting up FastAPI application")
    try:
        await MongoDB.connect()
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_db_client():
    logger.info("Shutting down FastAPI application")
    try:
        await MongoDB.close()
        await cache_service.close()
        logger.info("All connections closed")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")
        raise

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

# Include current production routers
app.include_router(company_routes.router, prefix=settings.API_V1_PREFIX)
app.include_router(trial_routes.router, prefix=settings.API_V1_PREFIX)

# Future advanced analysis endpoints (commented out until ready for use)
# app.include_router(trial_routes.future_router, prefix=settings.API_V1_PREFIX)
