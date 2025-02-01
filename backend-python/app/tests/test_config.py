"""
Test configuration and settings.
"""
from typing import Dict, Any
import os

# Test database configuration
TEST_DB_CONFIG = {
    "database": "clinical_trials_test",
    "collection": "companies_test"
}

# Test data configuration
TEST_DATA_CONFIG = {
    "min_trials": 1,
    "max_trials": 10
}

# Test environment configuration
def get_test_settings() -> Dict[str, Any]:
    """Get test environment settings."""
    return {
        "MONGODB_URL": os.getenv("TEST_MONGODB_URL", "mongodb://localhost:27017"),
        "DATABASE_NAME": TEST_DB_CONFIG["database"],
        "COLLECTION_NAME": TEST_DB_CONFIG["collection"],
        "REDIS_HOST": os.getenv("TEST_REDIS_HOST", "localhost"),
        "REDIS_PORT": int(os.getenv("TEST_REDIS_PORT", "6379")),
        "TESTING": True
    }

# Test data validation
def validate_test_data(data: Dict[str, Any]) -> bool:
    """Validate test data structure."""
    required_fields = ["studies", "analytics", "companyName", "queryDate"]
    return all(field in data for field in required_fields) 