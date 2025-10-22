"""Image schemas."""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ImageBase(BaseModel):
    """Base image schema."""
    filename: str
    original_filename: str


class ImageCreate(ImageBase):
    """Image creation schema."""
    filepath: str
    width: Optional[int] = None
    height: Optional[int] = None
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    project_id: Optional[int] = None


class ImageUpdate(BaseModel):
    """Image update schema."""
    status: Optional[str] = None
    project_id: Optional[int] = None


class Image(ImageBase):
    """Image response schema."""
    id: int
    filepath: str
    width: Optional[int]
    height: Optional[int]
    file_size: Optional[int]
    mime_type: Optional[str]
    project_id: Optional[int]
    uploader_id: int
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
