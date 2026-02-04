from fastapi import APIRouter, Depends, HTTPException
from app.schemas.moderation import ModerationRequest, ModerationResponse
from app.services.moderator import ModerationWorkflow
from app.core.security import get_api_key
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.db_models import ModerationLog
from app.services.text_processing import calculate_content_hash

router = APIRouter()

@router.post("/moderate/text", response_model=ModerationResponse)
async def moderate_text(
    request: ModerationRequest,
    api_key: str = Depends(get_api_key),
    db: AsyncSession = Depends(get_db)
):
    """
    Moderate text content for hate speech, violence, and other categories.
    """
    try:
        # Run workflow
        result = await ModerationWorkflow.process(request)
        
        # Async Log to DB (Fire and forget in production, or awaited here)
        log_entry = ModerationLog(
            request_id=result.request_id,
            content_hash=calculate_content_hash(request.content),
            language_detected=request.language,
            strictness=request.strictness,
            allowed=result.allowed,
            risk_score=result.risk_score,
            categories=result.categories.model_dump(),
            client_id=api_key[:8] + "..." # Log partial key
        )
        db.add(log_entry)
        await db.commit()
        
        return result
    except Exception as e:
        # Log error in production
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error during moderation")
