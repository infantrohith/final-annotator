"""ML Model model."""
from sqlalchemy import Column, Integer, String, DateTime, JSON, Text, Float
from datetime import datetime
from app.db.database import Base


class MLModel(Base):
    """ML Model for training and inference."""
    
    __tablename__ = "ml_models"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    model_type = Column(String, nullable=False)  # yolo, faster_rcnn, etc.
    status = Column(String, default="training")  # training, ready, failed
    
    # Training metrics
    accuracy = Column(Float)
    loss = Column(Float)
    epochs_trained = Column(Integer, default=0)
    
    # Configuration
    config = Column(JSON)
    
    # Model path
    model_path = Column(String)
    
    # Training info
    training_info = Column(JSON)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime)
