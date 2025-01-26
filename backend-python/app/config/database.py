from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from contextlib import asynccontextmanager
from typing import Optional
from .settings import get_settings
import asyncio
import logging

settings = get_settings()

logger = logging.getLogger("clinical_trials")

class DatabaseConnectionManager:
    MAX_RETRIES = 5
    RETRY_DELAY = 1  # seconds

    @classmethod
    async def connect_with_retry(cls, mongodb_url: str) -> AsyncIOMotorClient:
        for attempt in range(cls.MAX_RETRIES):
            try:
                client = AsyncIOMotorClient(mongodb_url)
                # Verify connection
                await client.admin.command('ping')
                logger.info("Successfully connected to MongoDB")
                return client
            except ConnectionFailure as e:
                if attempt == cls.MAX_RETRIES - 1:
                    logger.error("Failed to connect to MongoDB after max retries")
                    raise
                logger.warning(f"Connection attempt {attempt + 1} failed, retrying...")
                await asyncio.sleep(cls.RETRY_DELAY * (attempt + 1))

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None
    TIMEOUT = 5.0  # 5 seconds timeout

    @classmethod
    @asynccontextmanager
    async def get_collection(cls, collection_name: str):
        if not cls.client:
            logger.info("No client exists, connecting...")
            await cls.connect()
        
        logger.info(f"Getting collection: {collection_name}")
        try:
            collection = cls.db[collection_name]
            yield collection
            logger.info(f"Operation completed for collection: {collection_name}")
        except asyncio.TimeoutError:
            logger.error(f"Operation timed out for collection: {collection_name}")
            raise
        except Exception as e:
            logger.error(f"Error in collection operation: {str(e)}")
            raise
        finally:
            logger.info(f"Exiting collection context for: {collection_name}")

    @classmethod
    async def connect(cls):
        if cls.client is None:
            try:
                logger.info("Connecting to MongoDB...")
                cls.client = AsyncIOMotorClient(
                    settings.MONGODB_URL,
                    serverSelectionTimeoutMS=5000,  # 5 second timeout for server selection
                    connectTimeoutMS=5000,         # 5 second timeout for initial connection
                    socketTimeoutMS=5000           # 5 second timeout for socket operations
                )
                # Test the connection with timeout
                await asyncio.wait_for(
                    cls.client.admin.command('ping'),
                    timeout=cls.TIMEOUT
                )
                cls.db = cls.client[settings.DATABASE_NAME]
                logger.info("Successfully connected to MongoDB")
            except (ConnectionFailure, ServerSelectionTimeoutError) as e:
                logger.error(f"Failed to connect to MongoDB: {str(e)}")
                cls.client = None
                cls.db = None
                raise
            except asyncio.TimeoutError:
                logger.error("MongoDB connection timed out")
                cls.client = None
                cls.db = None
                raise
            except Exception as e:
                logger.error(f"Unexpected error connecting to MongoDB: {str(e)}")
                cls.client = None
                cls.db = None
                raise

    @classmethod
    async def close(cls):
        if cls.client:
            try:
                logger.info("Closing MongoDB connection")
                cls.client.close()
                await asyncio.wait_for(
                    cls.client.admin.command('ping'),
                    timeout=cls.TIMEOUT
                )
            except Exception as e:
                logger.error(f"Error during MongoDB shutdown: {str(e)}")
            finally:
                cls.client = None
                cls.db = None
                logger.info("MongoDB connection closed") 