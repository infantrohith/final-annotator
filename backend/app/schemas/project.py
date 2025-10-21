"""Project schemas."""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ProjectBase(BaseModel):
    """Base project schema."""
    name: str
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    """Project creation schema."""
    pass


class ProjectUpdate(BaseModel):
    """Project update schema."""
    name: Optional[str] = None
    description: Optional[str] = None


class Project(ProjectBase):
    """Project response schema."""
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
