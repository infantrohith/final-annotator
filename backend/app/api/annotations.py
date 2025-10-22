"""Annotation endpoints."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.db.database import get_db
from app.models.annotation import Annotation
from app.models.image import Image
from app.schemas.annotation import Annotation as AnnotationSchema, AnnotationCreate, AnnotationUpdate


router = APIRouter(prefix="/annotations", tags=["annotations"])


@router.get("/", response_model=List[AnnotationSchema])
async def list_annotations(
    skip: int = 0,
    limit: int = 100,
    image_id: int = None,
    label: str = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """List annotations."""
    query = db.query(Annotation)
    
    if image_id:
        # Verify user owns the image
        image = db.query(Image).filter(
            Image.id == image_id,
            Image.uploader_id == int(current_user["id"])
        ).first()
        
        if not image:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Image not found"
            )
        
        query = query.filter(Annotation.image_id == image_id)
    
    if label:
        query = query.filter(Annotation.label == label)
    
    annotations = query.offset(skip).limit(limit).all()
    return annotations


@router.post("/", response_model=AnnotationSchema, status_code=status.HTTP_201_CREATED)
async def create_annotation(
    annotation_data: AnnotationCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create a new annotation."""
    # Verify user owns the image
    image = db.query(Image).filter(
        Image.id == annotation_data.image_id,
        Image.uploader_id == int(current_user["id"])
    ).first()
    
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )
    
    annotation = Annotation(**annotation_data.dict())
    db.add(annotation)
    db.commit()
    db.refresh(annotation)
    
    # Update image status
    if image.status == "pending":
        image.status = "annotating"
        db.commit()
    
    return annotation


@router.post("/batch", response_model=List[AnnotationSchema], status_code=status.HTTP_201_CREATED)
async def create_batch_annotations(
    annotations_data: List[AnnotationCreate],
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create multiple annotations at once."""
    created_annotations = []
    
    for annotation_data in annotations_data:
        # Verify user owns the image
        image = db.query(Image).filter(
            Image.id == annotation_data.image_id,
            Image.uploader_id == int(current_user["id"])
        ).first()
        
        if not image:
            continue  # Skip invalid images
        
        annotation = Annotation(**annotation_data.dict())
        db.add(annotation)
        created_annotations.append(annotation)
        
        # Update image status
        if image.status == "pending":
            image.status = "annotating"
    
    db.commit()
    
    # Refresh all annotations
    for annotation in created_annotations:
        db.refresh(annotation)
    
    return created_annotations


@router.get("/{annotation_id}", response_model=AnnotationSchema)
async def get_annotation(
    annotation_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get a specific annotation."""
    annotation = db.query(Annotation).filter(Annotation.id == annotation_id).first()
    
    if not annotation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Annotation not found"
        )
    
    # Verify user owns the image
    image = db.query(Image).filter(
        Image.id == annotation.image_id,
        Image.uploader_id == int(current_user["id"])
    ).first()
    
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Annotation not found"
        )
    
    return annotation


@router.put("/{annotation_id}", response_model=AnnotationSchema)
async def update_annotation(
    annotation_id: int,
    annotation_data: AnnotationUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update an annotation."""
    annotation = db.query(Annotation).filter(Annotation.id == annotation_id).first()
    
    if not annotation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Annotation not found"
        )
    
    # Verify user owns the image
    image = db.query(Image).filter(
        Image.id == annotation.image_id,
        Image.uploader_id == int(current_user["id"])
    ).first()
    
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Annotation not found"
        )
    
    # Update fields
    for field, value in annotation_data.dict(exclude_unset=True).items():
        setattr(annotation, field, value)
    
    db.commit()
    db.refresh(annotation)
    return annotation


@router.delete("/{annotation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_annotation(
    annotation_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Delete an annotation."""
    annotation = db.query(Annotation).filter(Annotation.id == annotation_id).first()
    
    if not annotation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Annotation not found"
        )
    
    # Verify user owns the image
    image = db.query(Image).filter(
        Image.id == annotation.image_id,
        Image.uploader_id == int(current_user["id"])
    ).first()
    
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Annotation not found"
        )
    
    db.delete(annotation)
    db.commit()
    
    return None
