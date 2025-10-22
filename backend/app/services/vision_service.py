"""Vision service for AI tasks."""
import cv2
import numpy as np
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.task import VisionTask
from app.models.image import Image
from app.models.annotation import Annotation


class VisionService:
    """Service for vision-related tasks."""
    
    @staticmethod
    async def detect_objects(image_path: str, task_id: int, db: Session) -> Dict[str, Any]:
        """Run object detection on an image."""
        try:
            # Update task status
            task = db.query(VisionTask).filter(VisionTask.id == task_id).first()
            if task:
                task.status = "running"
                task.progress = 10
                db.commit()
            
            # Load image
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError("Failed to load image")
            
            # Simple contour detection as a demo
            # In production, you'd use a real model like YOLO
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            edges = cv2.Canny(blurred, 50, 150)
            
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            detections = []
            for i, contour in enumerate(contours[:20]):  # Limit to 20 detections
                x, y, w, h = cv2.boundingRect(contour)
                area = cv2.contourArea(contour)
                
                # Filter small detections
                if area > 100:
                    detections.append({
                        "bbox": [int(x), int(y), int(w), int(h)],
                        "confidence": min(0.5 + (area / 10000), 0.99),
                        "class": "object",
                    })
            
            # Update task
            if task:
                task.status = "completed"
                task.progress = 100
                task.results = {"detections": detections, "count": len(detections)}
                db.commit()
            
            return {"detections": detections, "count": len(detections)}
            
        except Exception as e:
            if task:
                task.status = "failed"
                task.error_message = str(e)
                db.commit()
            raise
    
    @staticmethod
    async def classify_image(image_path: str, task_id: int, db: Session) -> Dict[str, Any]:
        """Classify an image."""
        try:
            task = db.query(VisionTask).filter(VisionTask.id == task_id).first()
            if task:
                task.status = "running"
                task.progress = 10
                db.commit()
            
            # Simple color-based classification as demo
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError("Failed to load image")
            
            # Calculate dominant color
            avg_color = np.mean(img, axis=(0, 1))
            b, g, r = avg_color
            
            # Simple classification based on dominant color
            if r > g and r > b:
                label = "red-dominant"
                confidence = r / 255.0
            elif g > r and g > b:
                label = "green-dominant"
                confidence = g / 255.0
            else:
                label = "blue-dominant"
                confidence = b / 255.0
            
            result = {
                "class": label,
                "confidence": float(confidence),
                "all_scores": {
                    "red-dominant": float(r / 255.0),
                    "green-dominant": float(g / 255.0),
                    "blue-dominant": float(b / 255.0),
                }
            }
            
            if task:
                task.status = "completed"
                task.progress = 100
                task.results = result
                db.commit()
            
            return result
            
        except Exception as e:
            if task:
                task.status = "failed"
                task.error_message = str(e)
                db.commit()
            raise
    
    @staticmethod
    async def auto_annotate(image_id: int, db: Session) -> List[Annotation]:
        """Auto-annotate an image using vision models."""
        image = db.query(Image).filter(Image.id == image_id).first()
        if not image:
            raise ValueError("Image not found")
        
        # Create a vision task
        task = VisionTask(
            name=f"Auto-annotate image {image_id}",
            task_type="detection",
            status="running",
        )
        db.add(task)
        db.commit()
        
        try:
            # Run detection
            results = await VisionService.detect_objects(image.filepath, task.id, db)
            
            # Create annotations from detections
            annotations = []
            for detection in results.get("detections", []):
                bbox = detection["bbox"]
                annotation = Annotation(
                    image_id=image_id,
                    label=detection.get("class", "object"),
                    annotation_type="bbox",
                    x=bbox[0],
                    y=bbox[1],
                    width=bbox[2],
                    height=bbox[3],
                    confidence=detection.get("confidence"),
                )
                db.add(annotation)
                annotations.append(annotation)
            
            db.commit()
            return annotations
            
        except Exception as e:
            task.status = "failed"
            task.error_message = str(e)
            db.commit()
            raise
