from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.config import get_settings
from app.api.v1.api import api_router
from app.db.init_db import init_db

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Init DB
    # In production, use Alembic for migrations.
    # This is a simple dev auto-create.
    try:
        await init_db()
    except Exception as e:
        print(f"DB Init Warning (might be expected if DB not ready): {e}")
    yield
    # Shutdown logic if needed

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "message": "AI Content Moderation API is running", 
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}
