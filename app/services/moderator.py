from app.services.text_processing import normalize_text, calculate_content_hash
from app.services.rule_engine import RuleEngine
from app.services.ai_service import ai_service
from app.schemas.moderation import ModerationRequest, ModerationResponse, CategoryScores
from app.core.config import get_settings
import uuid

settings = get_settings()

from app.core.cache import get_cached_result, set_cached_result
import json

class ModerationWorkflow:
    @staticmethod
    async def process(request: ModerationRequest) -> ModerationResponse:
        # 1. Normalize
        clean_text = normalize_text(request.content)
        content_hash = calculate_content_hash(clean_text)
        
        # 2. Check Cache
        cached_data = await get_cached_result(f"mod_cache:{content_hash}")
        if cached_data:
            data = json.loads(cached_data)
            max_risk = data["max_risk"]
            final_categories = data["categories"]
            rule_flags = data["flagged"]
        else:
            # 3. Process (Rules + AI)
            rule_score, rule_cats, rule_flags = RuleEngine.analyze(clean_text)
            ai_cats = await ai_service.moderate_text(clean_text)
            
            final_categories = {}
            max_risk = 0.0
            
            for cat in CategoryScores.model_fields.keys():
                score = max(rule_cats.get(cat, 0.0), ai_cats.get(cat, 0.0))
                final_categories[cat] = score
                max_risk = max(max_risk, score)
            
            # Save to Cache
            cache_payload = {
                "max_risk": max_risk,
                "categories": final_categories,
                "flagged": rule_flags
            }
            try:
                await set_cached_result(f"mod_cache:{content_hash}", json.dumps(cache_payload))
            except Exception as e:
                print(f"Cache Error: {e}")

        # 4. Determine Threshold
        threshold = settings.STRICTNESS_LEVELS.get(request.strictness, 0.5)
        allowed = max_risk < threshold
        
        # 5. Construct Response
        return ModerationResponse(
            allowed=allowed,
            risk_score=round(max_risk * 100, 2),
            categories=CategoryScores(**final_categories),
            flagged_phrases=rule_flags if request.return_spans else [],
            explanation="Content flagged due to high risk score." if not allowed else None,
            request_id=str(uuid.uuid4())
        )
