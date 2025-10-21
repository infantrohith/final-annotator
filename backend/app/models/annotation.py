"""Annotation model."""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class Annotation(Base):
    """Annotation model for storing image annotations."""
    
    __tablename__ = "annotations"
    
    id = Column(Integer, primary_key=True, index=True)
    image_id = Column(Integer, ForeignKey("images.id"), nullable=False)
    label = Column(String, nullable=False, index=True)
    annotation_type = Column(String, nullable=False)  # bbox, polygon, point, etc.
    
    # Bounding box coordinates
    x = Column(Float)
    y = Column(Float)
    width = Column(Float)
    height = Column(Float)
    
    # For complex shapes (polygons, etc.)
    coordinates = Column(JSON)
    
    # Additional metadata
    confidence = Column(Float)
    metadata = Column(JSON)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    image = relationship("Image", back_populates="annotations")
