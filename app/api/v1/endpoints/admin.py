from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.db_models import ModerationLog
from app.core.security import get_api_key

router = APIRouter()

@router.get("/metrics")
async def get_metrics(
    api_key: str = Depends(get_api_key),
    db: AsyncSession = Depends(get_db)
):
    """
    Admin: Get simple usage metrics.
    """
    # Total requests
    result_total = await db.execute(select(func.count(ModerationLog.id)))
    total = result_total.scalar() or 0
    
    # Blocked count (allowed = False)
    result_blocked = await db.execute(select(func.count(ModerationLog.id)).where(ModerationLog.allowed == False))
    blocked = result_blocked.scalar() or 0
    
    flagged_percentage = (blocked / total * 100) if total > 0 else 0.0
    
    return {
        "total_requests": total,
        "flagged_requests": blocked,
        "flagged_percentage": round(flagged_percentage, 2)
    }

@router.get("/export_csv")
async def export_logs(
    limit: int = 1000,
    api_key: str = Depends(get_api_key),
    db: AsyncSession = Depends(get_db)
):
    """
    Admin: Export audit log (last N records).
    """
    result = await db.execute(
        select(ModerationLog).order_by(ModerationLog.timestamp.desc()).limit(limit)
    )
    logs = result.scalars().all()
    
    # In a real app, use StreamingResponse with csv writer
    # Returning JSON primarily here for simplicity in this endpoint demo
    data = []
    for log in logs:
        data.append({
            "id": log.request_id,
            "timestamp": log.timestamp.isoformat(),
            "allowed": log.allowed,
            "score": log.risk_score,
            "hash": log.content_hash
        })
        
    return data
