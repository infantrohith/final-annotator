"""Image endpoints."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.db.database import get_db
from app.models.image import Image
from app.schemas.image import Image as ImageSchema, ImageUpdate
from app.utils.file_utils import save_upload_file, delete_file
import os


router = APIRouter(prefix="/images", tags=["images"])


@router.get("/", response_model=List[ImageSchema])
async def list_images(
    skip: int = 0,
    limit: int = 100,
    project_id: int = None,
    status_filter: str = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """List all images for current user."""
    query = db.query(Image).filter(Image.uploader_id == int(current_user["id"]))
    
    if project_id:
        query = query.filter(Image.project_id == project_id)
    
    if status_filter:
        query = query.filter(Image.status == status_filter)
    
    images = query.offset(skip).limit(limit).all()
    return images


@router.post("/upload", response_model=ImageSchema, status_code=status.HTTP_201_CREATED)
async def upload_image(
    file: UploadFile = File(...),
    project_id: int = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Upload a single image."""
    try:
        # Save file
        filepath, metadata = await save_upload_file(file)
        
        # Create database entry
        image = Image(
            filename=os.path.basename(filepath),
            filepath=filepath,
            original_filename=file.filename,
            width=metadata.get("width"),
            height=metadata.get("height"),
            file_size=metadata.get("file_size"),
            mime_type=metadata.get("mime_type"),
            project_id=project_id,
            uploader_id=int(current_user["id"]),
        )
        
        db.add(image)
        db.commit()
        db.refresh(image)
        
        return image
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload image: {str(e)}"
        )


@router.post("/upload-batch", response_model=List[ImageSchema], status_code=status.HTTP_201_CREATED)
async def upload_batch(
    files: List[UploadFile] = File(...),
    project_id: int = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Upload multiple images at once."""
    uploaded_images = []
    
    for file in files:
        try:
            # Save file
            filepath, metadata = await save_upload_file(file)
            
            # Create database entry
            image = Image(
                filename=os.path.basename(filepath),
                filepath=filepath,
                original_filename=file.filename,
                width=metadata.get("width"),
                height=metadata.get("height"),
                file_size=metadata.get("file_size"),
                mime_type=metadata.get("mime_type"),
                project_id=project_id,
                uploader_id=int(current_user["id"]),
            )
            
            db.add(image)
            uploaded_images.append(image)
            
        except Exception as e:
            # Continue with other files even if one fails
            continue
    
    db.commit()
    
    # Refresh all images
    for image in uploaded_images:
        db.refresh(image)
    
    return uploaded_images


@router.get("/{image_id}", response_model=ImageSchema)
async def get_image(
    image_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get image details."""
    image = db.query(Image).filter(
        Image.id == image_id,
        Image.uploader_id == int(current_user["id"])
    ).first()
    
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )
    
    return image


@router.get("/{image_id}/file")
async def get_image_file(
    image_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Download image file."""
    image = db.query(Image).filter(
        Image.id == image_id,
        Image.uploader_id == int(current_user["id"])
    ).first()
    
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )
    
    if not os.path.exists(image.filepath):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image file not found"
        )
    
    return FileResponse(
        image.filepath,
        media_type=image.mime_type,
        filename=image.original_filename
    )


@router.put("/{image_id}", response_model=ImageSchema)
async def update_image(
    image_id: int,
    image_data: ImageUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update image metadata."""
    image = db.query(Image).filter(
        Image.id == image_id,
        Image.uploader_id == int(current_user["id"])
    ).first()
    
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )
    
    # Update fields
    for field, value in image_data.dict(exclude_unset=True).items():
        setattr(image, field, value)
    
    db.commit()
    db.refresh(image)
    return image


@router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_image(
    image_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Delete an image."""
    image = db.query(Image).filter(
        Image.id == image_id,
        Image.uploader_id == int(current_user["id"])
    ).first()
    
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )
    
    # Delete file
    delete_file(image.filepath)
    
    # Delete database entry
    db.delete(image)
    db.commit()
    
    return None
