"""
Advanced Computer Vision Fallback System
When camera fails, this system provides comprehensive computer vision analysis
using multiple techniques for hand detection and sign recognition
"""

import cv2
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
import logging
from datetime import datetime
import base64
import io
from PIL import Image, ImageEnhance, ImageFilter
import math

logger = logging.getLogger(__name__)

class ComputerVisionFallback:
    """Advanced computer vision fallback system for sign language recognition"""
    
    def __init__(self):
        """Initialize the computer vision fallback system"""
        self.skin_detector = SkinDetector()
        self.contour_analyzer = ContourAnalyzer()
        self.gesture_recognizer = GestureRecognizer()
        self.background_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=500, varThreshold=50, detectShadows=True
        )
        
        # Initialize cascade classifiers
        self.cascades = self._load_cascades()
        
    def _load_cascades(self) -> Dict[str, Any]:
        """Load available cascade classifiers"""
        cascades = {}
        
        try:
            # Try to load hand cascade
            cascades['hand'] = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_hand.xml'
            )
        except:
            logger.warning("Hand cascade not found")
        
        try:
            # Face cascade as backup
            cascades['face'] = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
        except:
            logger.warning("Face cascade not found")
        
        try:
            # Eye cascade for better gesture detection
            cascades['eye'] = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_eye.xml'
            )
        except:
            logger.warning("Eye cascade not found")
        
        return cascades
    
    def process_image(self, image: np.ndarray) -> Dict[str, Any]:
        """
        Comprehensive image processing with multiple computer vision techniques
        
        Args:
            image: Input BGR image
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            # Initialize results
            results = {
                'hands_detected': False,
                'hand_regions': [],
                'skin_regions': [],
                'contours': [],
                'gestures': [],
                'confidence': 0.0,
                'processed_image': None,
                'analysis_methods': []
            }
            
            # 1. Skin detection
            skin_analysis = self.skin_detector.detect_skin(image)
            if skin_analysis['skin_detected']:
                results['skin_regions'] = skin_analysis['regions']
                results['analysis_methods'].append('skin_detection')
                results['confidence'] += 0.2
            
            # 2. Cascade detection
            cascade_analysis = self._cascade_detection(image)
            if cascade_analysis['objects_detected']:
                results['hand_regions'].extend(cascade_analysis['regions'])
                results['analysis_methods'].append('cascade_detection')
                results['confidence'] += 0.3
            
            # 3. Contour analysis
            contour_analysis = self.contour_analyzer.analyze_contours(image)
            if contour_analysis['hand_like_contours']:
                results['contours'] = contour_analysis['contours']
                results['analysis_methods'].append('contour_analysis')
                results['confidence'] += 0.25
            
            # 4. Motion detection (if background subtraction is available)
            motion_analysis = self._detect_motion(image)
            if motion_analysis['motion_detected']:
                results['hand_regions'].extend(motion_analysis['regions'])
                results['analysis_methods'].append('motion_detection')
                results['confidence'] += 0.15
            
            # 5. Gesture recognition
            if results['hand_regions'] or results['skin_regions']:
                gesture_analysis = self.gesture_recognizer.recognize_gestures(
                    image, results['hand_regions'] + results['skin_regions']
                )
                results['gestures'] = gesture_analysis['gestures']
                if gesture_analysis['gestures']:
                    results['analysis_methods'].append('gesture_recognition')
                    results['confidence'] += 0.1
            
            # 6. Create processed image with annotations
            results['processed_image'] = self._create_annotated_image(image, results)
            
            # Determine if hands are detected
            results['hands_detected'] = (
                len(results['hand_regions']) > 0 or 
                len(results['skin_regions']) > 0 or
                results['confidence'] > 0.3
            )
            
            # Normalize confidence
            results['confidence'] = min(1.0, results['confidence'])
            
            logger.info(f"CV Fallback analysis complete. Methods used: {results['analysis_methods']}")
            return results
            
        except Exception as e:
            logger.error(f"Error in computer vision processing: {str(e)}")
            return {
                'hands_detected': False,
                'hand_regions': [],
                'error': str(e),
                'processed_image': image
            }
    
    def _cascade_detection(self, image: np.ndarray) -> Dict[str, Any]:
        """Detect objects using cascade classifiers"""
        results = {
            'objects_detected': False,
            'regions': [],
            'detections': {}
        }
        
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            for cascade_name, cascade in self.cascades.items():
                if cascade.empty():
                    continue
                
                detections = cascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(30, 30),
                    maxSize=(300, 300)
                )
                
                if len(detections) > 0:
                    results['objects_detected'] = True
                    results['detections'][cascade_name] = detections
                    
                    for (x, y, w, h) in detections:
                        results['regions'].append({
                            'bbox': (x, y, w, h),
                            'type': cascade_name,
                            'confidence': 0.7  # Base confidence for cascade detection
                        })
            
            return results
            
        except Exception as e:
            logger.error(f"Error in cascade detection: {str(e)}")
            return results
    
    def _detect_motion(self, image: np.ndarray) -> Dict[str, Any]:
        """Detect motion using background subtraction"""
        results = {
            'motion_detected': False,
            'regions': [],
            'foreground_mask': None
        }
        
        try:
            # Apply background subtraction
            fg_mask = self.background_subtractor.apply(image)
            
            # Morphological operations to clean up the mask
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
            fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)
            
            # Find contours in the mask
            contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                
                # Filter contours by area (potential hand regions)
                if 1000 < area < 10000:
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # Check aspect ratio (hands are typically not too elongated)
                    aspect_ratio = w / h
                    if 0.5 < aspect_ratio < 2.0:
                        results['motion_detected'] = True
                        results['regions'].append({
                            'bbox': (x, y, w, h),
                            'type': 'motion',
                            'confidence': min(0.8, area / 5000)  # Scale confidence by area
                        })
            
            results['foreground_mask'] = fg_mask
            return results
            
        except Exception as e:
            logger.error(f"Error in motion detection: {str(e)}")
            return results
    
    def _create_annotated_image(self, image: np.ndarray, results: Dict[str, Any]) -> np.ndarray:
        """Create annotated image with detection results"""
        try:
            annotated = image.copy()
            
            # Draw hand regions
            for region in results['hand_regions']:
                bbox = region['bbox']
                x, y, w, h = bbox
                
                # Color based on detection type
                color_map = {
                    'hand': (0, 255, 0),      # Green
                    'face': (255, 0, 0),      # Blue  
                    'eye': (0, 255, 255),     # Yellow
                    'motion': (255, 0, 255),  # Magenta
                    'skin': (0, 165, 255)     # Orange
                }
                
                color = color_map.get(region['type'], (255, 255, 255))
                
                # Draw bounding box
                cv2.rectangle(annotated, (x, y), (x + w, y + h), color, 2)
                
                # Add label
                label = f"{region['type']}: {region['confidence']:.2f}"
                cv2.putText(annotated, label, (x, y - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            
            # Draw skin regions
            for region in results['skin_regions']:
                bbox = region['bbox']
                x, y, w, h = bbox
                cv2.rectangle(annotated, (x, y), (x + w, y + h), (0, 165, 255), 1)
                cv2.putText(annotated, "Skin", (x, y - 5), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 165, 255), 1)
            
            # Draw contours
            if results['contours']:
                cv2.drawContours(annotated, results['contours'], -1, (255, 255, 0), 2)
            
            # Add analysis information
            methods_text = f"Methods: {', '.join(results['analysis_methods'])}"
            confidence_text = f"Confidence: {results['confidence']:.2f}"
            
            cv2.putText(annotated, methods_text, (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.putText(annotated, confidence_text, (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            return annotated
            
        except Exception as e:
            logger.error(f"Error creating annotated image: {str(e)}")
            return image
    
    def enhance_image_quality(self, image: np.ndarray) -> np.ndarray:
        """Enhance image quality for better detection"""
        try:
            # Convert to PIL for enhancement
            pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(pil_image)
            pil_image = enhancer.enhance(1.2)
            
            # Enhance brightness
            enhancer = ImageEnhance.Brightness(pil_image)
            pil_image = enhancer.enhance(1.1)
            
            # Sharpen the image
            pil_image = pil_image.filter(ImageFilter.UnsharpMask(radius=1, percent=150, threshold=3))
            
            # Convert back to OpenCV format
            enhanced = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            
            return enhanced
            
        except Exception as e:
            logger.error(f"Error enhancing image: {str(e)}")
            return image


class SkinDetector:
    """Skin detection using multiple color spaces"""
    
    def __init__(self):
        """Initialize skin detector"""
        # HSV ranges for skin detection
        self.hsv_lower = np.array([0, 20, 70], dtype=np.uint8)
        self.hsv_upper = np.array([20, 255, 255], dtype=np.uint8)
        
        # YCrCb ranges for skin detection
        self.ycrcb_lower = np.array([0, 135, 85], dtype=np.uint8)
        self.ycrcb_upper = np.array([255, 180, 135], dtype=np.uint8)
    
    def detect_skin(self, image: np.ndarray) -> Dict[str, Any]:
        """Detect skin regions in the image"""
        try:
            # Convert to different color spaces
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
            
            # Create masks
            hsv_mask = cv2.inRange(hsv, self.hsv_lower, self.hsv_upper)
            ycrcb_mask = cv2.inRange(ycrcb, self.ycrcb_lower, self.ycrcb_upper)
            
            # Combine masks
            skin_mask = cv2.bitwise_and(hsv_mask, ycrcb_mask)
            
            # Morphological operations to clean up
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
            skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_OPEN, kernel)
            skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_CLOSE, kernel)
            
            # Find contours
            contours, _ = cv2.findContours(skin_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            regions = []
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 1000:  # Filter small regions
                    x, y, w, h = cv2.boundingRect(contour)
                    regions.append({
                        'bbox': (x, y, w, h),
                        'type': 'skin',
                        'confidence': min(1.0, area / 5000),
                        'area': area
                    })
            
            return {
                'skin_detected': len(regions) > 0,
                'regions': regions,
                'mask': skin_mask
            }
            
        except Exception as e:
            logger.error(f"Error in skin detection: {str(e)}")
            return {'skin_detected': False, 'regions': []}


class ContourAnalyzer:
    """Analyze contours for hand-like shapes"""
    
    def analyze_contours(self, image: np.ndarray) -> Dict[str, Any]:
        """Analyze image contours for hand-like shapes"""
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply Gaussian blur
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Edge detection
            edges = cv2.Canny(blurred, 50, 150)
            
            # Find contours
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            hand_like_contours = []
            
            for contour in contours:
                area = cv2.contourArea(contour)
                
                # Filter by area
                if 1000 < area < 20000:
                    # Calculate contour properties
                    perimeter = cv2.arcLength(contour, True)
                    hull = cv2.convexHull(contour)
                    hull_area = cv2.contourArea(hull)
                    
                    # Solidity (hand-like shapes have moderate solidity)
                    solidity = area / hull_area if hull_area > 0 else 0
                    
                    # Aspect ratio
                    x, y, w, h = cv2.boundingRect(contour)
                    aspect_ratio = w / h
                    
                    # Check if contour is hand-like
                    if 0.5 < solidity < 0.95 and 0.5 < aspect_ratio < 2.0:
                        hand_like_contours.append(contour)
            
            return {
                'hand_like_contours': len(hand_like_contours) > 0,
                'contours': hand_like_contours,
                'total_contours': len(contours)
            }
            
        except Exception as e:
            logger.error(f"Error in contour analysis: {str(e)}")
            return {'hand_like_contours': False, 'contours': []}


class GestureRecognizer:
    """Basic gesture recognition using geometric features"""
    
    def recognize_gestures(self, image: np.ndarray, regions: List[Dict]) -> Dict[str, Any]:
        """Recognize basic gestures from detected regions"""
        try:
            gestures = []
            
            for region in regions:
                x, y, w, h = region['bbox']
                roi = image[y:y+h, x:x+w]
                
                if roi.size == 0:
                    continue
                
                # Analyze gesture based on geometric properties
                gesture_type = self._analyze_gesture_geometry(roi, (x, y, w, h))
                
                if gesture_type:
                    gestures.append({
                        'type': gesture_type,
                        'bbox': (x, y, w, h),
                        'confidence': region.get('confidence', 0.5)
                    })
            
            return {
                'gestures': gestures,
                'gesture_count': len(gestures)
            }
            
        except Exception as e:
            logger.error(f"Error in gesture recognition: {str(e)}")
            return {'gestures': []}
    
    def _analyze_gesture_geometry(self, roi: np.ndarray, bbox: Tuple[int, int, int, int]) -> Optional[str]:
        """Analyze ROI for basic gesture patterns"""
        try:
            x, y, w, h = bbox
            
            # Basic gesture classification based on dimensions
            aspect_ratio = w / h
            area = w * h
            
            if aspect_ratio > 1.5:
                return "horizontal_gesture"
            elif aspect_ratio < 0.7:
                return "vertical_gesture"
            elif area > 5000:
                return "open_hand"
            elif area < 2000:
                return "closed_hand"
            else:
                return "neutral_hand"
                
        except Exception as e:
            logger.error(f"Error analyzing gesture geometry: {str(e)}")
            return None
