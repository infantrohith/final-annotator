"""Vision task schemas."""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any


class VisionTaskBase(BaseModel):
    """Base vision task schema."""
    name: str
    task_type: str


class VisionTaskCreate(VisionTaskBase):
    """Vision task creation schema."""
    config: Optional[Dict[str, Any]] = None


class VisionTask(VisionTaskBase):
    """Vision task response schema."""
    id: int
    status: str
    progress: int
    config: Optional[Dict[str, Any]]
    results: Optional[Dict[str, Any]]
    error_message: Optional[str]
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True
