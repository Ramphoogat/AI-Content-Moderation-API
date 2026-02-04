import re
from typing import List, Tuple

# Simple hardcoded rules for fallback/augmentation
# In production, these should be loaded from a config file or DB
# Expanded BAD_PATTERNS (Safe, scalable)

# 🔴 HATE / ABUSE
HATE_PATTERNS = [
    r"\b(hate|kill|destroy)\s+(all|every|those|everyone|everybody|everything)\b",
    r"\b(go\s+back\s+to\s+your)\b",
    r"\b(you\s+people)\b",
    r"\b(subhuman|vermin|scum)\b",
    r"\b(dirty|filthy)\s+(people|group)\b",
    r"\b(we\s+should\s+wipe\s+out)\b",
    r"\b(they\s+don’t\s+belong)\b",
    r"\b(send\s+them\s+back)\b",
]

# 🟠 HARASSMENT / BULLYING
HARASSMENT_PATTERNS = [
    r"\b(you\s+are\s+(stupid|idiot|dumb|useless))\b",
    r"\b(no\s+one\s+likes\s+you)\b",
    r"\b(kys|kill\s+yourself)\b",
    r"\b(loser|pathetic|worthless)\b",
    r"\b(shut\s+up|get\s+lost)\b",
    r"\b(embarrassing|cringe)\b",
    r"\b(i\s+hate\s+you)\b",
]

# 🔵 SEXUAL / NSFW
SEXUAL_PATTERNS = [
    r"\b(xxx|porn|nude|nsfw)\b",
    r"\b(sex|oral|anal)\b",
    r"\b(dick|pussy|cock|boobs)\b",
    r"\b(fetish|kink)\b",
    r"\b(cam\s+girl|onlyfans)\b",
    r"\b(hardcore|softcore)\b",
    r"\b(jerk\s+off|masturbate)\b",
]

# 🟣 SELF-HARM / SUICIDE
SELF_HARM_PATTERNS = [
    r"\b(kill\s+myself|end\s+my\s+life)\b",
    r"\b(i\s+want\s+to\s+die)\b",
    r"\b(no\s+reason\s+to\s+live)\b",
    r"\b(suicide|self\s+harm)\b",
    r"\b(cut\s+myself|cutting)\b",
    r"\b(overdose)\b",
]

# ⚫ VIOLENCE / THREATS
VIOLENCE_PATTERNS = [
    r"\b(i\s+will\s+kill\s+you)\b",
    r"\b(shoot|stab|bomb)\b",
    r"\b(burn\s+them\s+alive)\b",
    r"\b(attack|massacre)\b",
    r"\b(behead|execute)\b",
    r"\b(threaten|hunt\s+down)\b",
]

# 🟢 SPAM / SCAMS
SPAM_PATTERNS = [
    r"\b(buy\s+now|limited\s+offer)\b",
    r"\b(free\s+crypto|free\s+bitcoin)\b",
    r"\b(click\s+here)\b",
    r"\b(make\s+money\s+fast)\b",
    r"\b(work\s+from\s+home)\b",
    r"\b(guaranteed\s+profits)\b",
    r"\b(telegram\s+me|dm\s+me)\b",
]

BAD_PATTERNS = {
    "hate": HATE_PATTERNS,
    "harassment": HARASSMENT_PATTERNS,
    "sexual": SEXUAL_PATTERNS,
    "self_harm": SELF_HARM_PATTERNS,
    "violence": VIOLENCE_PATTERNS,
    "spam": SPAM_PATTERNS,
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
