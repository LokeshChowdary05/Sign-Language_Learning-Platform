"""
Unit tests for the HandTracker module
"""

import pytest
import numpy as np
import cv2
from unittest.mock import Mock, patch
from src.core.hand_tracker import HandTracker

class TestHandTracker:
    """Test cases for HandTracker class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.tracker = HandTracker()
        self.sample_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    
    def test_initialization(self):
        """Test HandTracker initialization"""
        assert self.tracker.mp_hands is not None
        assert self.tracker.mp_drawing is not None
        assert self.tracker.hands is not None
        assert self.tracker.results is None
    
    def test_process_frame_no_hands(self):
        """Test frame processing with no hands detected"""
        with patch.object(self.tracker.hands, 'process') as mock_process:
            mock_process.return_value = Mock(multi_hand_landmarks=None)
            
            processed_frame, hands_detected = self.tracker.process_frame(self.sample_frame)
            
            assert processed_frame is not None
            assert hands_detected is False
    
    def test_process_frame_with_hands(self):
        """Test frame processing with hands detected"""
        with patch.object(self.tracker.hands, 'process') as mock_process:
            mock_landmarks = Mock()
            mock_process.return_value = Mock(multi_hand_landmarks=[mock_landmarks])
            
            processed_frame, hands_detected = self.tracker.process_frame(self.sample_frame)
            
            assert processed_frame is not None
            assert hands_detected is True
    
    def test_get_landmarks_no_hands(self):
        """Test landmark extraction with no hands"""
        self.tracker.results = Mock(multi_hand_landmarks=None)
        landmarks = self.tracker.get_landmarks()
        
        assert landmarks == []
    
    def test_get_landmarks_with_hands(self):
        """Test landmark extraction with hands detected"""
        # Mock hand landmarks
        mock_landmark = Mock()
        mock_landmark.x = 0.5
        mock_landmark.y = 0.5
        mock_landmark.z = 0.0
        
        mock_hand_landmarks = Mock()
        mock_hand_landmarks.landmark = [mock_landmark] * 21  # 21 landmarks per hand
        
        mock_classification = Mock()
        mock_classification.label = "Right"
        mock_classification.score = 0.9
        
        mock_handedness = Mock()
        mock_handedness.classification = [mock_classification]
        
        self.tracker.results = Mock(
            multi_hand_landmarks=[mock_hand_landmarks],
            multi_handedness=[mock_handedness]
        )
        
        landmarks = self.tracker.get_landmarks()
        
        assert len(landmarks) == 1
        assert landmarks[0]['hand_label'] == "Right"
        assert landmarks[0]['confidence'] == 0.9
        assert len(landmarks[0]['landmarks']) == 21
    
    def test_get_hand_features_no_hands(self):
        """Test feature extraction with no hands"""
        self.tracker.results = Mock(multi_hand_landmarks=None)
        features = self.tracker.get_hand_features()
        
        assert features is None
    
    def test_get_hand_features_with_hands(self):
        """Test feature extraction with hands detected"""
        # Mock hand landmarks
        mock_landmark = Mock()
        mock_landmark.x = 0.5
        mock_landmark.y = 0.5
        mock_landmark.z = 0.0
        
        mock_hand_landmarks = Mock()
        mock_hand_landmarks.landmark = [mock_landmark] * 21
        
        mock_classification = Mock()
        mock_classification.label = "Right"
        mock_classification.score = 0.9
        
        mock_handedness = Mock()
        mock_handedness.classification = [mock_classification]
        
        self.tracker.results = Mock(
            multi_hand_landmarks=[mock_hand_landmarks],
            multi_handedness=[mock_handedness]
        )
        
        features = self.tracker.get_hand_features()
        
        assert features is not None
        assert isinstance(features, np.ndarray)
        assert len(features) > 0
    
    def test_is_hand_visible(self):
        """Test hand visibility check"""
        # No hands
        self.tracker.results = None
        assert self.tracker.is_hand_visible() is False
        
        # With hands
        self.tracker.results = Mock(multi_hand_landmarks=[Mock()])
        assert self.tracker.is_hand_visible() is True
    
    def test_get_hand_count(self):
        """Test hand count functionality"""
        # No hands
        self.tracker.results = None
        assert self.tracker.get_hand_count() == 0
        
        # One hand
        self.tracker.results = Mock(multi_hand_landmarks=[Mock()])
        assert self.tracker.get_hand_count() == 1
        
        # Two hands
        self.tracker.results = Mock(multi_hand_landmarks=[Mock(), Mock()])
        assert self.tracker.get_hand_count() == 2
    
    def test_euclidean_distance(self):
        """Test Euclidean distance calculation"""
        p1 = {'x': 0.0, 'y': 0.0, 'z': 0.0}
        p2 = {'x': 3.0, 'y': 4.0, 'z': 0.0}
        
        distance = self.tracker._euclidean_distance(p1, p2)
        
        assert abs(distance - 5.0) < 0.01  # 3-4-5 triangle
    
    def test_calculate_angle(self):
        """Test angle calculation"""
        center = {'x': 0.0, 'y': 0.0, 'z': 0.0}
        p1 = {'x': 1.0, 'y': 0.0, 'z': 0.0}
        p2 = {'x': 0.0, 'y': 1.0, 'z': 0.0}
        
        angle = self.tracker._calculate_angle(center, p1, p2)
        
        assert abs(angle - 90.0) < 0.01  # 90 degree angle
    
    def test_close(self):
        """Test resource cleanup"""
        # Should not raise any exceptions
        self.tracker.close()

if __name__ == "__main__":
    pytest.main([__file__])
