"""Annotation schemas."""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, List, Any


class AnnotationBase(BaseModel):
    """Base annotation schema."""
    label: str
    annotation_type: str


class AnnotationCreate(AnnotationBase):
    """Annotation creation schema."""
    image_id: int
    x: Optional[float] = None
    y: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None
    coordinates: Optional[List[Dict[str, float]]] = None
    confidence: Optional[float] = None
    annotation_metadata: Optional[Dict[str, Any]] = None


class AnnotationUpdate(BaseModel):
    """Annotation update schema."""
    label: Optional[str] = None
    x: Optional[float] = None
    y: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None
    coordinates: Optional[List[Dict[str, float]]] = None
    confidence: Optional[float] = None
    annotation_metadata: Optional[Dict[str, Any]] = None


class Annotation(AnnotationBase):
    """Annotation response schema."""
    id: int
    image_id: int
    x: Optional[float]
    y: Optional[float]
    width: Optional[float]
    height: Optional[float]
    coordinates: Optional[List[Dict[str, float]]]
    confidence: Optional[float]
    annotation_metadata: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
