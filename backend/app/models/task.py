"""Vision task model."""
from sqlalchemy import Column, Integer, String, DateTime, JSON, Text
from datetime import datetime
from app.db.database import Base


class VisionTask(Base):
    """Vision task model for AI processing tasks."""
    
    __tablename__ = "vision_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    task_type = Column(String, nullable=False)  # detection, classification, segmentation
    status = Column(String, default="pending")  # pending, running, completed, failed
    progress = Column(Integer, default=0)
    
    # Configuration
    config = Column(JSON)
    
    # Results
    results = Column(JSON)
    error_message = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime)
