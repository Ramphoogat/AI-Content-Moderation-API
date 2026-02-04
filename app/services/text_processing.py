import re
import unicodedata

def normalize_text(text: str) -> str:
    """
    Normalize text: lowercase, remove accents, whitespace cleanup.
    """
    # Unicode normalize (NFKD decompostion)
    text = unicodedata.normalize('NFKD', text)
    # Remove non-ascii marks
    text = text.encode('ASCII', 'ignore').decode('utf-8')
    text = text.lower().strip()
    # Simple regex to collapse whitespace
    text = re.sub(r'\s+', ' ', text)
    return text

def calculate_content_hash(text: str) -> str:
    import hashlib
    return hashlib.sha256(text.encode('utf-8')).hexdigest()
