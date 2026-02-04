from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Content Moderation API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./local_dev.db"
    
    # Redis
    # Empty string or "disabled" triggers local dict cache in our logic
    REDIS_URL: str = "redis://localhost:6379/0" 
    
    # Security
    # In production, this should be loaded from a secure source or DB
    API_KEYS: list[str] = ["test-key-123", "admin-key-456"]
    
    # AI Provider
    OPENAI_API_KEY: str | None = None
    
    # Moderation Settings
    DEFAULT_LANGUAGE: str = "en"
    STRICTNESS_LEVELS: dict = {
        "low": 0.85,
        "medium": 0.65,
        "high": 0.35
    }

    class Config:
        case_sensitive = True
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
