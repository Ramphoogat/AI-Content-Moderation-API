from pydantic import BaseModel, Field, validator
from typing import List, Optional, Literal

class ModerationRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=10000, description="The text content to moderate")
    language: str = Field(default="auto", description="Language code (e.g., 'en', 'hi') or 'auto'")
    strictness: Literal["low", "medium", "high"] = Field(default="medium", description="Sensitivity of the AI moderation")
    return_spans: bool = Field(default=False, description="Whether to return specific flagged phrases")

class CategoryScores(BaseModel):
    hate: float = 0.0
    harassment: float = 0.0
    sexual: float = 0.0
    self_harm: float = 0.0
    violence: float = 0.0
    spam: float = 0.0

class ModerationResponse(BaseModel):
    allowed: bool
    risk_score: float = Field(..., ge=0, le=100, description="Overall risk score 0-100")
    categories: CategoryScores
    flagged_phrases: List[str] = []
    explanation: Optional[str] = None
    request_id: str

class ErrorResponse(BaseModel):
    error_code: str
    message: str
