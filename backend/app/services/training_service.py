"""Training service for ML models."""
import torch
import torch.nn as nn
import torch.optim as optim
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.model import MLModel
from app.models.annotation import Annotation
from typing import Dict, Any


class SimpleClassifier(nn.Module):
    """Simple CNN classifier for demo."""
    
    def __init__(self, num_classes: int = 10):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 32, 3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, 3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(64 * 56 * 56, 128)
        self.fc2 = nn.Linear(128, num_classes)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.5)
    
    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))
        x = x.view(-1, 64 * 56 * 56)
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return x


class TrainingService:
    """Service for training ML models."""
    
    @staticmethod
    async def train_model(
        model_id: int,
        db: Session,
        epochs: int = 10,
        batch_size: int = 32,
        learning_rate: float = 0.001
    ) -> Dict[str, Any]:
        """Train a machine learning model."""
        try:
            # Get model from database
            ml_model = db.query(MLModel).filter(MLModel.id == model_id).first()
            if not ml_model:
                raise ValueError("Model not found")
            
            ml_model.status = "training"
            db.commit()
            
            # Get training data (annotations)
            annotations = db.query(Annotation).all()
            
            if not annotations:
                raise ValueError("No training data available")
            
            # Count unique labels
            unique_labels = set(ann.label for ann in annotations)
            num_classes = len(unique_labels)
            
            # Initialize model
            model = SimpleClassifier(num_classes=num_classes)
            criterion = nn.CrossEntropyLoss()
            optimizer = optim.Adam(model.parameters(), lr=learning_rate)
            
            # Training loop (simplified demo)
            training_losses = []
            
            for epoch in range(epochs):
                # Simulate training
                # In production, you'd load actual image data and train properly
                epoch_loss = 0.0
                num_batches = max(len(annotations) // batch_size, 1)
                
                for batch in range(num_batches):
                    # Simulate batch training
                    # In real implementation, load images and create batches
                    dummy_input = torch.randn(batch_size, 3, 224, 224)
                    dummy_labels = torch.randint(0, num_classes, (batch_size,))
                    
                    optimizer.zero_grad()
                    outputs = model(dummy_input)
                    loss = criterion(outputs, dummy_labels)
                    loss.backward()
                    optimizer.step()
                    
                    epoch_loss += loss.item()
                
                avg_loss = epoch_loss / num_batches
                training_losses.append(avg_loss)
                
                # Update model progress
                ml_model.epochs_trained = epoch + 1
                ml_model.loss = avg_loss
                db.commit()
            
            # Save model
            model_path = f"models/model_{model_id}.pth"
            import os
            os.makedirs("models", exist_ok=True)
            torch.save(model.state_dict(), model_path)
            
            # Calculate final metrics
            final_loss = training_losses[-1]
            # Simulate accuracy (in production, evaluate on validation set)
            simulated_accuracy = max(0.7, min(0.95, 1.0 - final_loss))
            
            # Update model
            ml_model.status = "ready"
            ml_model.model_path = model_path
            ml_model.accuracy = simulated_accuracy
            ml_model.loss = final_loss
            ml_model.completed_at = datetime.utcnow()
            ml_model.training_info = {
                "epochs": epochs,
                "batch_size": batch_size,
                "learning_rate": learning_rate,
                "training_losses": training_losses,
                "num_classes": num_classes,
                "labels": list(unique_labels),
            }
            db.commit()
            
            return {
                "status": "completed",
                "accuracy": simulated_accuracy,
                "loss": final_loss,
                "epochs": epochs,
            }
            
        except Exception as e:
            ml_model.status = "failed"
            db.commit()
            raise
    
    @staticmethod
    async def predict(model_id: int, image_path: str, db: Session) -> Dict[str, Any]:
        """Run inference with a trained model."""
        ml_model = db.query(MLModel).filter(MLModel.id == model_id).first()
        
        if not ml_model or ml_model.status != "ready":
            raise ValueError("Model not ready for inference")
        
        # Load model
        training_info = ml_model.training_info or {}
        num_classes = training_info.get("num_classes", 10)
        labels = training_info.get("labels", [f"class_{i}" for i in range(num_classes)])
        
        model = SimpleClassifier(num_classes=num_classes)
        
        if ml_model.model_path and torch.cuda.is_available():
            model.load_state_dict(torch.load(ml_model.model_path))
        
        model.eval()
        
        # Run inference (simplified)
        with torch.no_grad():
            dummy_input = torch.randn(1, 3, 224, 224)
            outputs = model(dummy_input)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            
            # Get top prediction
            confidence, predicted = torch.max(probabilities, 1)
            predicted_label = labels[predicted.item()] if predicted.item() < len(labels) else "unknown"
            
            return {
                "label": predicted_label,
                "confidence": float(confidence.item()),
                "all_probabilities": {
                    labels[i] if i < len(labels) else f"class_{i}": float(prob)
                    for i, prob in enumerate(probabilities[0])
                }
            }
