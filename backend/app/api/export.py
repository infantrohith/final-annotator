"""Export endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.db.database import get_db
from app.models.project import Project
from app.services.export_service import ExportService
import os
import tempfile


router = APIRouter(prefix="/export", tags=["export"])


@router.get("/coco/{project_id}")
async def export_coco(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Export project in COCO format."""
    # Verify project exists and user owns it
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == int(current_user["id"])
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Create temporary file
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
    temp_file.close()
    
    try:
        # Export to COCO format
        output_path = ExportService.export_coco(project_id, db, temp_file.name)
        
        return FileResponse(
            output_path,
            media_type="application/json",
            filename=f"{project.name}_coco.json"
        )
    except Exception as e:
        if os.path.exists(temp_file.name):
            os.remove(temp_file.name)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Export failed: {str(e)}"
        )


@router.get("/yolo/{project_id}")
async def export_yolo(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Export project in YOLO format."""
    # Verify project exists and user owns it
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == int(current_user["id"])
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Export to YOLO format
        zip_path = ExportService.export_yolo(project_id, db, temp_dir)
        
        return FileResponse(
            zip_path,
            media_type="application/zip",
            filename=f"{project.name}_yolo.zip"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Export failed: {str(e)}"
        )


@router.get("/pascal-voc/{project_id}")
async def export_pascal_voc(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Export project in Pascal VOC format."""
    # Verify project exists and user owns it
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == int(current_user["id"])
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Export to Pascal VOC format
        zip_path = ExportService.export_pascal_voc(project_id, db, temp_dir)
        
        return FileResponse(
            zip_path,
            media_type="application/zip",
            filename=f"{project.name}_voc.zip"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Export failed: {str(e)}"
        )
