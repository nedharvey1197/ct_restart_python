import pytest
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from ..config.settings import get_settings
from ..main import app
from httpx import AsyncClient
from redis import Redis

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def test_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture(scope="session")
async def test_db():
    settings = get_settings()
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME + "_test"]
    yield db
    await client.drop_database(settings.DATABASE_NAME + "_test")
    client.close()

@pytest.fixture(scope="session")
async def test_redis():
    settings = get_settings()
    redis = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=1  # Use different DB for testing
    )
    yield redis
    redis.flushdb()  # Clear test database
    redis.close() 