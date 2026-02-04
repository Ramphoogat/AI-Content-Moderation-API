from fastapi import APIRouter
from app.api.v1.endpoints import moderate, admin

api_router = APIRouter()
api_router.include_router(moderate.router, tags=["moderation"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
