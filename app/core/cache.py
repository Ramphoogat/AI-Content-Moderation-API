from app.core.config import get_settings
import redis.asyncio as redis

settings = get_settings()

# In-memory fallback
_local_cache = {}

class MockRedis:
    """Simulates basic Redis behavior for development"""
    async def get(self, key):
        return _local_cache.get(key)
    
    async def set(self, key, value, ex=None):
        _local_cache[key] = value

try:
    if settings.REDIS_URL.strip() and "localhost" not in settings.REDIS_URL:
         redis_client = redis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
    elif "redis://" in settings.REDIS_URL:
         # Try connecting, if fails, use mock? 
         # For simplicity in this logic, we will assume if REDIS_URL is default but Docker is off, we might fail hard.
         # So we'll try-except the connection at runtime or usage.
         redis_client = redis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
    else:
        redis_client = MockRedis()
except:
    print("Warning: Redis not available. Using in-memory cache.")
    redis_client = MockRedis()

# Wrapper to safely handle connection errors during app runtime
async def get_cached_result(key: str):
    try:
        return await redis_client.get(key)
    except Exception:
        return _local_cache.get(key)

async def set_cached_result(key: str, value: str, expire: int = 3600):
    try:
        await redis_client.set(key, value, ex=expire)
    except Exception:
        _local_cache[key] = value
