import openai
from app.core.config import get_settings
from app.schemas.moderation import CategoryScores
import asyncio
import json

settings = get_settings()

class AIService:
    def __init__(self):
        self.client = None
        if settings.OPENAI_API_KEY:
            self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def moderate_text(self, text: str) -> dict:
        """
        Returns raw AI scores.
        """
        if self.client:
            try:
                response = await self.client.moderations.create(input=text)
                result = response.results[0]
                
                # Normalize OpenAIs 0-1 scores
                categories = {
                    "hate": max(result.category_scores.hate, result.category_scores.hate_threatening),
                    "harassment": max(result.category_scores.harassment, result.category_scores.harassment_threatening),
                    "sexual": max(result.category_scores.sexual, result.category_scores.sexual_minors),
                    "self_harm": result.category_scores.self_harm,
                    "violence": max(result.category_scores.violence, result.category_scores.violence_graphic),
                    "spam": 0.0 # OpenAI doesn't natively do spam in this endpoint usually, fallback to 0
                }
                
                return categories
            except Exception as e:
                print(f"OpenAI Error: {e}")
                # Fallback to empty if AI fails
                return {k: 0.0 for k in CategoryScores.model_fields.keys()}
        
        # Local Dummy Mode (if no API Key)
        # Mocking basic "AI" detection for demo purposes
        return {k: 0.0 for k in CategoryScores.model_fields.keys()}

ai_service = AIService()
