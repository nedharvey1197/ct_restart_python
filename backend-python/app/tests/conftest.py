import pytest
import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from app.config.settings import get_settings
from httpx import AsyncClient
from redis import Redis
from app.main import app
from fastapi.testclient import TestClient

@pytest.fixture(scope="session")
def test_client():
    with TestClient(app) as client:
        yield client

def pytest_configure(config):
    """Configure pytest."""
    # Add custom marker for future tests
    config.addinivalue_line(
        "markers", "future: mark test as future functionality"
    )

def pytest_collection_modifyitems(config, items):
    """Modify test collection to exclude future tests by default."""
    if not os.getenv("INCLUDE_FUTURE_TESTS"):
        for item in items:
            if "future_concepts" in str(item.fspath):
                item.add_marker(pytest.mark.skip(reason="Future functionality tests not enabled"))

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
'''
@pytest.fixture(scope="session")
async def test_client():
    """
    Fixture to provide an asynchronous HTTP client for testing.
    Uses httpx.AsyncClient to interact with the FastAPI app asynchronously.
    Ensures that all requests are made in an async context, which is necessary
    for testing async endpoints in FastAPI.
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
'''
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