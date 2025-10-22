"""Export service for dataset export."""
import json
import os
import zipfile
from typing import List
from sqlalchemy.orm import Session
from app.models.image import Image
from app.models.annotation import Annotation


class ExportService:
    """Service for exporting datasets."""
    
    @staticmethod
    def export_coco(project_id: int, db: Session, output_path: str) -> str:
        """Export dataset in COCO format."""
        images = db.query(Image).filter(Image.project_id == project_id).all()
        
        coco_data = {
            "images": [],
            "annotations": [],
            "categories": [],
        }
        
        # Collect unique labels
        labels = set()
        annotation_id = 1
        
        for img in images:
            # Add image
            coco_data["images"].append({
                "id": img.id,
                "file_name": img.filename,
                "width": img.width,
                "height": img.height,
            })
            
            # Add annotations
            annotations = db.query(Annotation).filter(Annotation.image_id == img.id).all()
            for ann in annotations:
                labels.add(ann.label)
                
                coco_data["annotations"].append({
                    "id": annotation_id,
                    "image_id": img.id,
                    "category_id": ann.label,
                    "bbox": [ann.x, ann.y, ann.width, ann.height] if ann.x is not None else [],
                    "area": (ann.width * ann.height) if ann.width and ann.height else 0,
                    "iscrowd": 0,
                })
                annotation_id += 1
        
        # Add categories
        for idx, label in enumerate(sorted(labels), 1):
            coco_data["categories"].append({
                "id": label,
                "name": label,
                "supercategory": "object",
            })
        
        # Write to file
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(coco_data, f, indent=2)
        
        return output_path
    
    @staticmethod
    def export_yolo(project_id: int, db: Session, output_dir: str) -> str:
        """Export dataset in YOLO format."""
        images = db.query(Image).filter(Image.project_id == project_id).all()
        
        os.makedirs(output_dir, exist_ok=True)
        labels_dir = os.path.join(output_dir, "labels")
        os.makedirs(labels_dir, exist_ok=True)
        
        # Collect unique labels
        all_labels = set()
        
        for img in images:
            annotations = db.query(Annotation).filter(Annotation.image_id == img.id).all()
            
            if not annotations:
                continue
            
            # Create label file
            label_file = os.path.join(labels_dir, f"{os.path.splitext(img.filename)[0]}.txt")
            
            with open(label_file, 'w') as f:
                for ann in annotations:
                    all_labels.add(ann.label)
                    
                    # YOLO format: class_id x_center y_center width height (normalized)
                    if ann.x is not None and img.width and img.height:
                        x_center = (ann.x + ann.width / 2) / img.width
                        y_center = (ann.y + ann.height / 2) / img.height
                        norm_width = ann.width / img.width
                        norm_height = ann.height / img.height
                        
                        class_id = sorted(all_labels).index(ann.label)
                        f.write(f"{class_id} {x_center} {y_center} {norm_width} {norm_height}\n")
        
        # Create classes file
        classes_file = os.path.join(output_dir, "classes.txt")
        with open(classes_file, 'w') as f:
            for label in sorted(all_labels):
                f.write(f"{label}\n")
        
        # Create zip
        zip_path = f"{output_dir}.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(output_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, output_dir)
                    zipf.write(file_path, arcname)
        
        return zip_path
    
    @staticmethod
    def export_pascal_voc(project_id: int, db: Session, output_dir: str) -> str:
        """Export dataset in Pascal VOC format."""
        images = db.query(Image).filter(Image.project_id == project_id).all()
        
        os.makedirs(output_dir, exist_ok=True)
        annotations_dir = os.path.join(output_dir, "Annotations")
        os.makedirs(annotations_dir, exist_ok=True)
        
        for img in images:
            annotations = db.query(Annotation).filter(Annotation.image_id == img.id).all()
            
            if not annotations:
                continue
            
            # Create XML file
            xml_content = f"""<annotation>
    <folder>images</folder>
    <filename>{img.filename}</filename>
    <size>
        <width>{img.width}</width>
        <height>{img.height}</height>
        <depth>3</depth>
    </size>
"""
            
            for ann in annotations:
                if ann.x is not None:
                    xml_content += f"""    <object>
        <name>{ann.label}</name>
        <bndbox>
            <xmin>{int(ann.x)}</xmin>
            <ymin>{int(ann.y)}</ymin>
            <xmax>{int(ann.x + ann.width)}</xmax>
            <ymax>{int(ann.y + ann.height)}</ymax>
        </bndbox>
    </object>
"""
            
            xml_content += "</annotation>"
            
            xml_file = os.path.join(annotations_dir, f"{os.path.splitext(img.filename)[0]}.xml")
            with open(xml_file, 'w') as f:
                f.write(xml_content)
        
        # Create zip
        zip_path = f"{output_dir}.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(output_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, output_dir)
                    zipf.write(file_path, arcname)
        
        return zip_path
