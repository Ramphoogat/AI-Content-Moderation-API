from fastapi import Security, HTTPException, status, Request
from fastapi.security.api_key import APIKeyHeader
from app.core.config import get_settings

api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)
settings = get_settings()

async def get_api_key(api_key: str = Security(api_key_header)):
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API Key"
        )
        
    if api_key not in settings.API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key"
        )
    return api_key
