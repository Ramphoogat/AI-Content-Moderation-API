import re
from typing import List, Tuple

# Simple hardcoded rules for fallback/augmentation
# In production, these should be loaded from a config file or DB
BAD_PATTERNS = {
    "hate": [r"\b(hate|kill)\s+(all|everyone)\b", r"racial_slur_placeholder"],
    "spam": [r"\b(buy|free)\s+(crypto|bitcoin)\b", r"click\s+here"],
    "sexual": [r"xxx", r"porn"]
}

class RuleEngine:
    @staticmethod
    def analyze(text: str) -> Tuple[float, dict, List[str]]:
        """
        Returns (rule_risk_score, category_scores, flagged_phrases)
        """
        flagged = []
        scores = {k: 0.0 for k in ["hate", "harassment", "sexual", "self_harm", "violence", "spam"]}
        
        max_score = 0.0
        
        for category, patterns in BAD_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    flagged.append(pattern)
                    scores[category] = 1.0 # High confidence if keyword matched
                    max_score = max(max_score, 1.0)
                    
        return max_score, scores, flagged
