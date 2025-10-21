"""ML Model schemas."""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any


class MLModelBase(BaseModel):
    """Base ML model schema."""
    name: str
    model_type: str


class MLModelCreate(MLModelBase):
    """ML model creation schema."""
    config: Optional[Dict[str, Any]] = None


class MLModel(MLModelBase):
    """ML model response schema."""
    id: int
    status: str
    accuracy: Optional[float]
    loss: Optional[float]
    epochs_trained: int
    config: Optional[Dict[str, Any]]
    model_path: Optional[str]
    training_info: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True
