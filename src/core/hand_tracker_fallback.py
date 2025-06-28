"""
Fallback Hand Tracker for Python 3.13 compatibility
When MediaPipe is not available, use OpenCV-based hand detection
"""

import cv2
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
import logging

logger = logging.getLogger(__name__)

class HandTrackerFallback:
    """Fallback hand tracker using OpenCV when MediaPipe is unavailable"""
    
    def __init__(self):
        """Initialize fallback hand tracker"""
        self.results = None
        self.hands_detected = False
        self.hand_landmarks = None
        
        # Initialize cascade classifier for hand detection
        self.hand_cascade = None
        try:
            # Try to load hand cascade (if available)
            self.hand_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_hand.xml')
        except:
            logger.warning("Hand cascade not available, using face cascade as fallback")
            self.hand_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    def process_frame(self, frame: np.ndarray) -> Tuple[np.ndarray, bool]:
        """Process frame and detect hands using OpenCV"""
        try:
            # Convert to grayscale for detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect hands/objects
            detections = []
            if self.hand_cascade:
                detections = self.hand_cascade.detectMultiScale(
                    gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
                )
            
            self.hands_detected = len(detections) > 0
            
            # Draw rectangles around detected regions
            for (x, y, w, h) in detections:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, "Hand Detected", (x, y - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Create mock results for compatibility
            self.results = {
                'multi_hand_landmarks': detections if len(detections) > 0 else None,
                'detections': detections
            }
            
            return frame, self.hands_detected
            
        except Exception as e:
            logger.error(f"Error in fallback hand tracking: {str(e)}")
            return frame, False
    
    def get_hand_features(self) -> Optional[np.ndarray]:
        """Get mock hand features for compatibility"""
        if self.hands_detected and self.results and self.results['detections'] is not None:
            # Create mock feature vector based on detected regions
            detections = self.results['detections']
            if len(detections) > 0:
                # Create a simple feature vector from bounding box
                x, y, w, h = detections[0]
                features = np.array([
                    x/640.0, y/480.0, w/640.0, h/480.0,  # Normalized position and size
                    (x+w/2)/640.0, (y+h/2)/480.0,        # Center point
                ] + [0.0] * 42)  # Padding to match expected feature length
                return features[:48]  # Return consistent feature length
        return None
    
    def is_hand_visible(self) -> bool:
        """Check if hands are currently visible"""
        return self.hands_detected
    
    def draw_landmarks(self, frame: np.ndarray) -> np.ndarray:
        """Draw landmarks on frame (simplified for fallback)"""
        if self.hands_detected and self.results and self.results['detections'] is not None:
            for (x, y, w, h) in self.results['detections']:
                # Draw simple landmarks as circles
                center_x, center_y = x + w//2, y + h//2
                cv2.circle(frame, (center_x, center_y), 5, (255, 0, 0), -1)
                cv2.circle(frame, (x + w//4, y + h//4), 3, (0, 255, 255), -1)
                cv2.circle(frame, (x + 3*w//4, y + h//4), 3, (0, 255, 255), -1)
                cv2.circle(frame, (x + w//4, y + 3*h//4), 3, (0, 255, 255), -1)
                cv2.circle(frame, (x + 3*w//4, y + 3*h//4), 3, (0, 255, 255), -1)
        return frame

# Try to import MediaPipe, fall back to our implementation
try:
    import mediapipe as mp
    # If MediaPipe is available, use the original implementation
    from .hand_tracker import HandTracker
    logger.info("MediaPipe available, using original HandTracker")
except ImportError:
    logger.warning("MediaPipe not available, using fallback implementation")
    
    class HandTracker(HandTrackerFallback):
        """Alias for fallback implementation when MediaPipe is not available"""
        pass
