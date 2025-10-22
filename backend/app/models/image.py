"""Image model."""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class Image(Base):
    """Image model for storing uploaded images."""
    
    __tablename__ = "images"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False, unique=True)
    original_filename = Column(String, nullable=False)
    width = Column(Integer)
    height = Column(Integer)
    file_size = Column(Integer)
    mime_type = Column(String)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    uploader_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String, default="pending")  # pending, annotating, completed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="images")
    uploader = relationship("User", back_populates="images")
    annotations = relationship("Annotation", back_populates="image", cascade="all, delete-orphan")
