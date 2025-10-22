"""ML Model endpoints."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.db.database import get_db
from app.models.model import MLModel
from app.schemas.model import MLModel as MLModelSchema, MLModelCreate
from app.services.training_service import TrainingService


router = APIRouter(prefix="/models", tags=["models"])


@router.get("/", response_model=List[MLModelSchema])
async def list_models(
    skip: int = 0,
    limit: int = 100,
    status_filter: str = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """List ML models."""
    query = db.query(MLModel)
    
    if status_filter:
        query = query.filter(MLModel.status == status_filter)
    
    models = query.offset(skip).limit(limit).all()
    return models


@router.post("/", response_model=MLModelSchema, status_code=status.HTTP_201_CREATED)
async def create_model(
    model_data: MLModelCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create a new ML model."""
    model = MLModel(**model_data.dict())
    db.add(model)
    db.commit()
    db.refresh(model)
    
    return model


@router.post("/{model_id}/train", response_model=MLModelSchema)
async def train_model(
    model_id: int,
    background_tasks: BackgroundTasks,
    epochs: int = 10,
    batch_size: int = 32,
    learning_rate: float = 0.001,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Train an ML model."""
    model = db.query(MLModel).filter(MLModel.id == model_id).first()
    
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model not found"
        )
    
    # Start training in background
    background_tasks.add_task(
        TrainingService.train_model,
        model_id,
        db,
        epochs,
        batch_size,
        learning_rate
    )
    
    model.status = "training"
    db.commit()
    db.refresh(model)
    
    return model


@router.post("/{model_id}/predict", response_model=dict)
async def predict(
    model_id: int,
    image_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Run prediction with a trained model."""
    from app.models.image import Image
    
    model = db.query(MLModel).filter(MLModel.id == model_id).first()
    
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model not found"
        )
    
    image = db.query(Image).filter(
        Image.id == image_id,
        Image.uploader_id == int(current_user["id"])
    ).first()
    
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )
    
    try:
        result = await TrainingService.predict(model_id, image.filepath, db)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )


@router.get("/{model_id}", response_model=MLModelSchema)
async def get_model(
    model_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get model details."""
    model = db.query(MLModel).filter(MLModel.id == model_id).first()
    
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model not found"
        )
    
    return model


@router.delete("/{model_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_model(
    model_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Delete a model."""
    model = db.query(MLModel).filter(MLModel.id == model_id).first()
    
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model not found"
        )
    
    db.delete(model)
    db.commit()
    
    return None
