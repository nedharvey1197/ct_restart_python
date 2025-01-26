from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List

class Settings(BaseSettings):
    # API Settings
    API_V1_PREFIX: str = "/api"
    PROJECT_NAME: str = "Clinical Trials API"
    DEBUG: bool = False
    
    # CORS
    ALLOWED_HOSTS: List[str] = [
        "http://localhost:5173",  # Vite default
        "http://localhost:5174",  # Vite alternate
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174"
    ]
    
    # Database
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "clinical_trials"
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = ""  # Optional, for production
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings() 