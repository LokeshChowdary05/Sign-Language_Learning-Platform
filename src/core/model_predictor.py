"""
ModelPredictor using fine-tuned MobileNetV3 for sign language recognition
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Any
import logging
from pathlib import Path
import cv2
from src.config.settings import MODEL_CONFIG, PATHS

try:
    import tensorflow as tf
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    print("⚠️ TensorFlow not available. Model prediction will use fallback mode.")

logger = logging.getLogger(__name__)

class ModelPredictor:
    """Sign language recognition using fine-tuned MobileNetV3 model"""
    
    def __init__(self):
        """Initialize the model predictor"""
        self.model_config = MODEL_CONFIG["sign_recognition"]
        self.preprocessing_config = MODEL_CONFIG["preprocessing"]
        self.model = None
        self.class_names = []
        self.is_loaded = False
        
        # Try to load the model
        self._load_model()
    
    def _load_model(self) -> bool:
        """Load the trained MobileNetV3 model"""
        try:
            if not TENSORFLOW_AVAILABLE:
                logger.warning("TensorFlow not available. Using demo mode.")
                self._create_demo_model()
                return False
            
            model_path = Path(PATHS["models"]) / "mobilenetv3_sign_language.h5"
            
            if model_path.exists():
                self.model = tf.keras.models.load_model(str(model_path))
                self.is_loaded = True
                logger.info(f"Model loaded successfully from {model_path}")
                
                # Load class names
                self._load_class_names()
                
                return True
            else:
                logger.warning(f"Model file not found at {model_path}. Using demo mode.")
                self._create_demo_model()
                return False
                
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            self._create_demo_model()
            return False
    
    def _create_demo_model(self):
        """Create a demo model for demonstration purposes"""
        try:
            if TENSORFLOW_AVAILABLE:
                # Create a simple MobileNetV3 architecture for demo
                base_model = tf.keras.applications.MobileNetV3Large(
                    input_shape=self.model_config["input_shape"],
                    include_top=False,
                    weights='imagenet'
                )
                
                # Add classification head
                self.model = tf.keras.Sequential([
                    base_model,
                    tf.keras.layers.GlobalAveragePooling2D(),
                    tf.keras.layers.Dense(128, activation='relu'),
                    tf.keras.layers.Dropout(0.5),
                    tf.keras.layers.Dense(64, activation='relu'),
                    tf.keras.layers.Dense(26, activation='softmax')  # 26 classes for demo
                ])
                
                logger.info("Demo model created successfully")
            else:
                # Fallback mode without TensorFlow
                self.model = None
                logger.info("Running in fallback mode without TensorFlow")
            
            # Create demo class names (A-Z)
            self.class_names = [chr(ord('A') + i) for i in range(26)]
            self.is_loaded = True
            
        except Exception as e:
            logger.error(f"Error creating demo model: {str(e)}")
            self.is_loaded = False
    
    def _load_class_names(self):
        """Load class names for the trained model"""
        try:
            class_names_path = Path(PATHS["models"]) / "class_names.txt"
            
            if class_names_path.exists():
                with open(class_names_path, 'r') as f:
                    self.class_names = [line.strip() for line in f.readlines()]
            else:
                # Default class names for demo
                self.class_names = [
                    "hello", "thank_you", "please", "sorry", "yes", "no", 
                    "help", "water", "food", "more", "stop", "good", 
                    "bad", "happy", "sad", "love", "family", "friend",
                    "work", "home", "school", "car", "money", "time",
                    "day", "night"
                ]
                
            logger.info(f"Loaded {len(self.class_names)} class names")
            
        except Exception as e:
            logger.error(f"Error loading class names: {str(e)}")
            self.class_names = ["unknown"]
    
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess image for model prediction
        
        Args:
            image: Input BGR image
            
        Returns:
            Preprocessed image ready for model inference
        """
        try:
            # Convert BGR to RGB
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Resize to model input size
            target_size = self.preprocessing_config["image_size"]
            resized_image = cv2.resize(rgb_image, target_size)
            
            # Normalize pixel values
            normalized_image = resized_image.astype(np.float32) / 255.0
            
            # Apply ImageNet normalization
            mean = np.array(self.preprocessing_config["normalization_mean"])
            std = np.array(self.preprocessing_config["normalization_std"])
            
            normalized_image = (normalized_image - mean) / std
            
            # Add batch dimension
            batch_image = np.expand_dims(normalized_image, axis=0)
            
            return batch_image
            
        except Exception as e:
            logger.error(f"Error preprocessing image: {str(e)}")
            return None
    
    def predict(self, image: np.ndarray) -> Dict[str, Any]:
        """
        Predict sign language from image
        
        Args:
            image: Input BGR image
            
        Returns:
            Dictionary containing prediction results
        """
        if not self.is_loaded or self.model is None:
            return {
                "predicted_class": "unknown",
                "confidence": 0.0,
                "top_predictions": [],
                "error": "Model not loaded"
            }
        
        try:
            # Preprocess image
            processed_image = self.preprocess_image(image)
            
            if processed_image is None:
                return {
                    "predicted_class": "unknown",
                    "confidence": 0.0,
                    "top_predictions": [],
                    "error": "Image preprocessing failed"
                }
            
            # Make prediction
            if self.model and TENSORFLOW_AVAILABLE:
                predictions = self.model.predict(processed_image, verbose=0)
                probabilities = predictions[0]
            else:
                # Fallback: generate random probabilities
                probabilities = np.random.rand(len(self.class_names))
                probabilities = probabilities / np.sum(probabilities)  # Normalize
            
            # Get top predictions
            top_indices = np.argsort(probabilities)[::-1][:5]
            top_predictions = []
            
            for idx in top_indices:
                class_name = self.class_names[idx] if idx < len(self.class_names) else f"class_{idx}"
                confidence = float(probabilities[idx])
                
                top_predictions.append({
                    "class": class_name,
                    "confidence": confidence
                })
            
            # Get best prediction
            best_idx = top_indices[0]
            predicted_class = self.class_names[best_idx] if best_idx < len(self.class_names) else "unknown"
            confidence = float(probabilities[best_idx])
            
            return {
                "predicted_class": predicted_class,
                "confidence": confidence,
                "top_predictions": top_predictions,
                "error": None
            }
            
        except Exception as e:
            logger.error(f"Error during prediction: {str(e)}")
            return {
                "predicted_class": "unknown",
                "confidence": 0.0,
                "top_predictions": [],
                "error": str(e)
            }
    
    def predict_with_features(self, hand_features: np.ndarray) -> Dict[str, Any]:
        """
        Predict sign language from hand features
        
        Args:
            hand_features: Extracted hand features from MediaPipe
            
        Returns:
            Dictionary containing prediction results
        """
        # For demo purposes, simulate prediction from hand features
        try:
            if hand_features is None or len(hand_features) == 0:
                return {
                    "predicted_class": "unknown",
                    "confidence": 0.0,
                    "top_predictions": [],
                    "error": "No hand features provided"
                }
            
            # Simulate prediction (in real implementation, this would use a trained model)
            # Generate random but consistent predictions based on feature hash
            feature_hash = hash(tuple(hand_features.flatten())) % len(self.class_names)
            predicted_class = self.class_names[feature_hash]
            
            # Generate confidence based on feature variance
            confidence = min(0.95, max(0.3, 0.5 + np.var(hand_features) * 10))
            
            # Generate top predictions
            top_predictions = []
            for i in range(min(5, len(self.class_names))):
                idx = (feature_hash + i) % len(self.class_names)
                conf = confidence * (0.9 ** i)
                top_predictions.append({
                    "class": self.class_names[idx],
                    "confidence": float(conf)
                })
            
            return {
                "predicted_class": predicted_class,
                "confidence": float(confidence),
                "top_predictions": top_predictions,
                "error": None
            }
            
        except Exception as e:
            logger.error(f"Error predicting from features: {str(e)}")
            return {
                "predicted_class": "unknown",
                "confidence": 0.0,
                "top_predictions": [],
                "error": str(e)
            }
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model"""
        if not self.is_loaded or self.model is None:
            return {
                "model_name": "None",
                "input_shape": None,
                "num_classes": 0,
                "parameters": 0,
                "is_loaded": False
            }
        
        return {
            "model_name": "MobileNetV3",
            "input_shape": self.model_config["input_shape"],
            "num_classes": len(self.class_names),
            "parameters": self.model.count_params() if hasattr(self.model, 'count_params') else 0,
            "is_loaded": self.is_loaded
        }
    
    def get_confidence_feedback(self, confidence: float) -> Dict[str, str]:
        """
        Get user feedback based on confidence score
        
        Args:
            confidence: Prediction confidence (0-1)
            
        Returns:
            Dictionary with feedback message and type
        """
        if confidence >= 0.9:
            return {
                "message": "Excellent! Your sign is perfectly recognized.",
                "type": "success",
                "suggestion": "Great job! Try practicing another sign."
            }
        elif confidence >= 0.7:
            return {
                "message": "Good! Your sign is well recognized.",
                "type": "success",
                "suggestion": "Nice work! Small adjustments can improve accuracy."
            }
        elif confidence >= 0.5:
            return {
                "message": "Fair attempt. Your sign is partially recognized.",
                "type": "warning",
                "suggestion": "Try adjusting your hand position and finger placement."
            }
        else:
            return {
                "message": "Sign not recognized clearly.",
                "type": "error",
                "suggestion": "Check the reference video and ensure good lighting."
            }
    
    def validate_prediction(self, target_sign: str, predicted_sign: str, confidence: float) -> Dict[str, Any]:
        """
        Validate if the prediction matches the target sign
        
        Args:
            target_sign: Expected sign
            predicted_sign: Predicted sign
            confidence: Prediction confidence
            
        Returns:
            Validation result dictionary
        """
        is_correct = target_sign.lower() == predicted_sign.lower()
        threshold = self.model_config["confidence_threshold"]
        
        return {
            "is_correct": is_correct,
            "meets_threshold": confidence >= threshold,
            "accuracy_percentage": int(confidence * 100),
            "feedback": self.get_confidence_feedback(confidence),
            "target_sign": target_sign,
            "predicted_sign": predicted_sign
        }
