"""File utilities for upload handling."""
import os
import uuid
from pathlib import Path
from typing import Tuple
from PIL import Image
from fastapi import UploadFile, HTTPException
from app.core.config import settings


def validate_image_file(file: UploadFile) -> None:
    """Validate uploaded image file."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type {file_ext} not allowed. Allowed types: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )


async def save_upload_file(file: UploadFile, upload_dir: str = None) -> Tuple[str, dict]:
    """Save uploaded file and return filepath and metadata."""
    validate_image_file(file)
    
    # Create upload directory if it doesn't exist
    if upload_dir is None:
        upload_dir = settings.UPLOAD_FOLDER
    
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate unique filename
    file_ext = Path(file.filename).suffix.lower()
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    filepath = os.path.join(upload_dir, unique_filename)
    
    # Save file
    try:
        contents = await file.read()
        
        # Check file size
        if len(contents) > settings.MAX_CONTENT_LENGTH:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Max size: {settings.MAX_CONTENT_LENGTH / 1024 / 1024}MB"
            )
        
        with open(filepath, "wb") as f:
            f.write(contents)
        
        # Get image metadata
        metadata = get_image_metadata(filepath)
        metadata["file_size"] = len(contents)
        metadata["mime_type"] = file.content_type
        
        return filepath, metadata
        
    except Exception as e:
        # Clean up file if something went wrong
        if os.path.exists(filepath):
            os.remove(filepath)
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")


def get_image_metadata(filepath: str) -> dict:
    """Get image metadata using PIL."""
    try:
        with Image.open(filepath) as img:
            return {
                "width": img.width,
                "height": img.height,
                "format": img.format,
            }
    except Exception as e:
        return {
            "width": None,
            "height": None,
            "format": None,
        }


def delete_file(filepath: str) -> None:
    """Delete a file safely."""
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
    except Exception:
        pass  # Silent fail for file deletion
