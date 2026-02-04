from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import engine
from app.models.db_models import Base

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
