from sqlalchemy import Column, String, Float, Boolean, DateTime, JSON, Text, Integer, ARRAY
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class ModerationLog(Base):
    __tablename__ = "moderation_logs"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String, index=True, unique=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Store hash of content for privacy
    content_hash = Column(String, index=True)
    
    # Request details
    language_detected = Column(String)
    strictness = Column(String)
    
    # Result
    allowed = Column(Boolean)
    risk_score = Column(Float)
    
    # JSON breakdown
    categories = Column(JSON)
    
    # Latency tracking
    processing_time_ms = Column(Float)
    
    # Client info (API Key prefix or ID)
    client_id = Column(String, index=True)
