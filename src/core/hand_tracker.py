"""
HandTracker using MediaPipe for real-time hand tracking and gesture recognition
"""

import cv2
import numpy as np
from typing import List, Dict, Optional, Tuple, Any
import logging
from src.config.settings import MODEL_CONFIG

try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False
    print("⚠️ MediaPipe not available. Hand tracking will use fallback mode.")

logger = logging.getLogger(__name__)

class HandTracker:
    """Real-time hand tracking using MediaPipe"""
    
    def __init__(self):
        """Initialize MediaPipe hand tracking components"""
        if MEDIAPIPE_AVAILABLE:
            self.mp_hands = mp.solutions.hands
            self.mp_drawing = mp.solutions.drawing_utils
            self.mp_drawing_styles = mp.solutions.drawing_styles
            
            # Initialize hands model with configuration
            hand_config = MODEL_CONFIG["hand_tracking"]
            self.hands = self.mp_hands.Hands(
                model_complexity=hand_config["model_complexity"],
                min_detection_confidence=hand_config["min_detection_confidence"],
                min_tracking_confidence=hand_config["min_tracking_confidence"],
                max_num_hands=hand_config["max_num_hands"]
            )
        else:
            self.mp_hands = None
            self.mp_drawing = None
            self.mp_drawing_styles = None
            self.hands = None
            
        self.results = None
        self.fallback_mode = not MEDIAPIPE_AVAILABLE
        
    def process_frame(self, frame: np.ndarray) -> Tuple[np.ndarray, bool]:
        """
        Process a video frame and detect hands
        
        Args:
            frame: Input BGR image frame
            
        Returns:
            Tuple of (processed_frame, hands_detected)
        """
        try:
            if self.fallback_mode:
                # Fallback mode: simulate hand detection
                return frame, True
            
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb_frame.flags.writeable = False
            
            # Process frame
            self.results = self.hands.process(rgb_frame)
            
            # Convert back to BGR for display
            rgb_frame.flags.writeable = True
            bgr_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)
            
            hands_detected = self.results.multi_hand_landmarks is not None
            
            return bgr_frame, hands_detected
            
        except Exception as e:
            logger.error(f"Error processing frame: {str(e)}")
            return frame, False
    
    def draw_landmarks(self, frame: np.ndarray) -> np.ndarray:
        """
        Draw hand landmarks on the frame
        
        Args:
            frame: Input BGR image frame
            
        Returns:
            Frame with landmarks drawn
        """
        if self.results and self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                # Draw landmarks
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style()
                )
        
        return frame
    
    def get_landmarks(self) -> List[Dict[str, Any]]:
        """
        Extract normalized hand landmarks
        
        Returns:
            List of dictionaries containing hand landmarks data
        """
        landmarks_data = []
        
        if self.fallback_mode:
            # Return dummy landmarks for demo
            dummy_landmarks = []
            for i in range(21):  # 21 landmarks per hand
                dummy_landmarks.append({
                    'x': 0.5 + (i * 0.02),
                    'y': 0.5 + (i * 0.01),
                    'z': 0.0
                })
            
            landmarks_data.append({
                'hand_label': 'Right',
                'landmarks': dummy_landmarks,
                'confidence': 0.8
            })
            return landmarks_data
        
        if self.results and self.results.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(self.results.multi_hand_landmarks):
                # Get hand classification (Left/Right)
                hand_label = "Unknown"
                if self.results.multi_handedness:
                    hand_label = self.results.multi_handedness[idx].classification[0].label
                
                # Extract landmark coordinates
                landmarks = []
                for landmark in hand_landmarks.landmark:
                    landmarks.append({
                        'x': landmark.x,
                        'y': landmark.y,
                        'z': landmark.z
                    })
                
                landmarks_data.append({
                    'hand_label': hand_label,
                    'landmarks': landmarks,
                    'confidence': self.results.multi_handedness[idx].classification[0].score if self.results.multi_handedness else 0.0
                })
        
        return landmarks_data
    
    def get_hand_features(self) -> Optional[np.ndarray]:
        """
        Extract hand features for sign language recognition
        
        Returns:
            Numpy array of hand features or None if no hands detected
        """
        landmarks_data = self.get_landmarks()
        
        if not landmarks_data:
            return None
        
        features = []
        
        for hand_data in landmarks_data:
            landmarks = hand_data['landmarks']
            
            # Extract basic landmark coordinates
            coords = []
            for landmark in landmarks:
                coords.extend([landmark['x'], landmark['y'], landmark['z']])
            
            # Calculate distances between key landmarks
            distances = self._calculate_landmark_distances(landmarks)
            
            # Calculate angles between landmarks
            angles = self._calculate_landmark_angles(landmarks)
            
            # Combine all features
            hand_features = coords + distances + angles
            features.extend(hand_features)
        
        return np.array(features) if features else None
    
    def _calculate_landmark_distances(self, landmarks: List[Dict]) -> List[float]:
        """Calculate distances between key hand landmarks"""
        distances = []
        
        # Key landmark indices for sign language recognition
        key_pairs = [
            (0, 4),   # thumb tip to wrist
            (0, 8),   # index finger tip to wrist
            (0, 12),  # middle finger tip to wrist
            (0, 16),  # ring finger tip to wrist
            (0, 20),  # pinky tip to wrist
            (4, 8),   # thumb to index finger
            (8, 12),  # index to middle finger
            (12, 16), # middle to ring finger
            (16, 20), # ring to pinky finger
        ]
        
        for p1, p2 in key_pairs:
            if p1 < len(landmarks) and p2 < len(landmarks):
                dist = self._euclidean_distance(landmarks[p1], landmarks[p2])
                distances.append(dist)
        
        return distances
    
    def _calculate_landmark_angles(self, landmarks: List[Dict]) -> List[float]:
        """Calculate angles between landmark triplets"""
        angles = []
        
        # Key angle triplets (middle point, point1, point2)
        angle_triplets = [
            (0, 1, 2),   # wrist angle
            (1, 2, 3),   # thumb base angle
            (5, 6, 7),   # index finger angle
            (9, 10, 11), # middle finger angle
            (13, 14, 15), # ring finger angle
            (17, 18, 19), # pinky angle
        ]
        
        for mid, p1, p2 in angle_triplets:
            if all(i < len(landmarks) for i in [mid, p1, p2]):
                angle = self._calculate_angle(landmarks[mid], landmarks[p1], landmarks[p2])
                angles.append(angle)
        
        return angles
    
    def _euclidean_distance(self, p1: Dict, p2: Dict) -> float:
        """Calculate Euclidean distance between two 3D points"""
        return np.sqrt(
            (p1['x'] - p2['x'])**2 + 
            (p1['y'] - p2['y'])**2 + 
            (p1['z'] - p2['z'])**2
        )
    
    def _calculate_angle(self, center: Dict, p1: Dict, p2: Dict) -> float:
        """Calculate angle between three points"""
        # Vector from center to p1
        v1 = np.array([p1['x'] - center['x'], p1['y'] - center['y'], p1['z'] - center['z']])
        
        # Vector from center to p2
        v2 = np.array([p2['x'] - center['x'], p2['y'] - center['y'], p2['z'] - center['z']])
        
        # Calculate angle using dot product
        cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        cos_angle = np.clip(cos_angle, -1.0, 1.0)  # Ensure valid range
        
        angle = np.arccos(cos_angle)
        return np.degrees(angle)
    
    def get_hand_bounding_box(self) -> Optional[Tuple[int, int, int, int]]:
        """
        Get bounding box around detected hands
        
        Returns:
            Tuple of (x, y, width, height) or None if no hands detected
        """
        if not self.results or not self.results.multi_hand_landmarks:
            return None
        
        all_x = []
        all_y = []
        
        for hand_landmarks in self.results.multi_hand_landmarks:
            for landmark in hand_landmarks.landmark:
                all_x.append(landmark.x)
                all_y.append(landmark.y)
        
        if not all_x or not all_y:
            return None
        
        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)
        
        # Add padding
        padding = 0.1
        width = max_x - min_x
        height = max_y - min_y
        
        min_x = max(0, min_x - padding * width)
        min_y = max(0, min_y - padding * height)
        max_x = min(1, max_x + padding * width)
        max_y = min(1, max_y + padding * height)
        
        return (min_x, min_y, max_x - min_x, max_y - min_y)
    
    def is_hand_visible(self) -> bool:
        """Check if any hand is currently visible"""
        if self.fallback_mode:
            return True  # Always return true in fallback mode
        return self.results is not None and self.results.multi_hand_landmarks is not None
    
    def get_hand_count(self) -> int:
        """Get number of hands currently detected"""
        if self.fallback_mode:
            return 1  # Return 1 hand in fallback mode
        if self.results and self.results.multi_hand_landmarks:
            return len(self.results.multi_hand_landmarks)
        return 0
    
    def close(self):
        """Clean up resources"""
        if hasattr(self, 'hands'):
            self.hands.close()
