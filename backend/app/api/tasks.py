"""Vision task endpoints."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.db.database import get_db
from app.models.task import VisionTask
from app.models.image import Image
from app.schemas.task import VisionTask as VisionTaskSchema, VisionTaskCreate
from app.services.vision_service import VisionService


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=List[VisionTaskSchema])
async def list_tasks(
    skip: int = 0,
    limit: int = 100,
    task_type: str = None,
    status_filter: str = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """List vision tasks."""
    query = db.query(VisionTask)
    
    if task_type:
        query = query.filter(VisionTask.task_type == task_type)
    
    if status_filter:
        query = query.filter(VisionTask.status == status_filter)
    
    tasks = query.offset(skip).limit(limit).all()
    return tasks


@router.post("/", response_model=VisionTaskSchema, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: VisionTaskCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create a new vision task."""
    task = VisionTask(**task_data.dict())
    db.add(task)
    db.commit()
    db.refresh(task)
    
    return task


@router.post("/detect/{image_id}", response_model=VisionTaskSchema)
async def detect_objects(
    image_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Run object detection on an image."""
    # Verify image exists and user owns it
    image = db.query(Image).filter(
        Image.id == image_id,
        Image.uploader_id == int(current_user["id"])
    ).first()
    
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )
    
    # Create task
    task = VisionTask(
        name=f"Object Detection - {image.filename}",
        task_type="detection",
        status="pending",
        config={"image_id": image_id}
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    
    # Run detection in background
    background_tasks.add_task(VisionService.detect_objects, image.filepath, task.id, db)
    
    return task


@router.post("/classify/{image_id}", response_model=VisionTaskSchema)
async def classify_image(
    image_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Run classification on an image."""
    # Verify image exists and user owns it
    image = db.query(Image).filter(
        Image.id == image_id,
        Image.uploader_id == int(current_user["id"])
    ).first()
    
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )
    
    # Create task
    task = VisionTask(
        name=f"Classification - {image.filename}",
        task_type="classification",
        status="pending",
        config={"image_id": image_id}
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    
    # Run classification in background
    background_tasks.add_task(VisionService.classify_image, image.filepath, task.id, db)
    
    return task


@router.post("/auto-annotate/{image_id}", response_model=dict)
async def auto_annotate(
    image_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Auto-annotate an image using vision models."""
    # Verify image exists and user owns it
    image = db.query(Image).filter(
        Image.id == image_id,
        Image.uploader_id == int(current_user["id"])
    ).first()
    
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )
    
    # Run auto-annotation in background
    background_tasks.add_task(VisionService.auto_annotate, image_id, db)
    
    return {"message": "Auto-annotation started", "image_id": image_id}


@router.get("/{task_id}", response_model=VisionTaskSchema)
async def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get task details."""
    task = db.query(VisionTask).filter(VisionTask.id == task_id).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Delete a task."""
    task = db.query(VisionTask).filter(VisionTask.id == task_id).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    db.delete(task)
    db.commit()
    
    return None
