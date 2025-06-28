"""
Camera Manager for Sign Language Learning Platform
Handles real camera capture, processing, and sign recognition with visual feedback
"""

import cv2
import numpy as np
import streamlit as st
from typing import Dict, List, Optional, Tuple, Any, Callable
import threading
import time
import logging
from datetime import datetime
import base64
import io
from PIL import Image

logger = logging.getLogger(__name__)

class CameraManager:
    """Comprehensive camera management for real-time sign language recognition"""
    
    def __init__(self, hand_tracker, model_predictor):
        """Initialize camera manager with tracking and prediction components"""
        self.hand_tracker = hand_tracker
        self.model_predictor = model_predictor
        self.cap = None
        self.is_running = False
        self.current_frame = None
        self.processed_frame = None
        self.recognition_results = {}
        self.feedback_overlay = None
        self.recording_session = False
        self.session_data = []
        self.fallback_mode = False
        self.camera_available = False
        self.initialization_attempts = 0
        self.max_init_attempts = 3
        
        # Camera settings
        self.camera_index = 0
        self.frame_width = 1280
        self.frame_height = 720
        self.fps = 30
        self.mirror_mode = True
        self.show_landmarks = True
        self.confidence_threshold = 0.7
        
        # Threading for real-time processing
        self.processing_thread = None
        self.frame_lock = threading.Lock()
        
    def initialize_camera(self, camera_index: int = 0) -> bool:
        """Initialize camera capture with robust fallback handling"""
        self.initialization_attempts += 1
        
        # Try multiple camera indices if first one fails
        camera_indices = [camera_index, 0, 1, 2] if camera_index != 0 else [0, 1, 2]
        
        for cam_idx in camera_indices:
            try:
                logger.info(f"Attempting to initialize camera {cam_idx}")
                self.camera_index = cam_idx
                
                # Try different backends
                backends = [cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_ANY] if hasattr(cv2, 'CAP_DSHOW') else [cv2.CAP_ANY]
                
                for backend in backends:
                    try:
                        self.cap = cv2.VideoCapture(cam_idx, backend)
                        
                        if self.cap.isOpened():
                            # Test camera by reading a frame
                            ret, test_frame = self.cap.read()
                            
                            if ret and test_frame is not None:
                                # Set camera properties
                                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
                                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)
                                self.cap.set(cv2.CAP_PROP_FPS, self.fps)
                                self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                                
                                # Try MJPG codec for better performance
                                try:
                                    self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
                                except:
                                    pass  # Codec not supported, continue anyway
                                
                                self.camera_available = True
                                self.fallback_mode = False
                                logger.info(f"Camera {cam_idx} initialized successfully with backend {backend}")
                                return True
                        
                        self.cap.release()
                        
                    except Exception as be:
                        logger.warning(f"Backend {backend} failed for camera {cam_idx}: {str(be)}")
                        if self.cap:
                            self.cap.release()
                        continue
                        
            except Exception as e:
                logger.warning(f"Failed to initialize camera {cam_idx}: {str(e)}")
                continue
        
        # All camera initialization attempts failed
        logger.error("All camera initialization attempts failed. Entering fallback mode.")
        self.camera_available = False
        self.fallback_mode = True
        self.cap = None
        
        # Create fallback hand tracker if needed
        if not hasattr(self.hand_tracker, 'fallback_mode') or not self.hand_tracker.fallback_mode:
            try:
                from .hand_tracker_fallback import HandTrackerFallback
                self.hand_tracker = HandTrackerFallback()
                logger.info("Switched to fallback hand tracker")
            except Exception as e:
                logger.error(f"Failed to initialize fallback hand tracker: {str(e)}")
        
        return False
    
    def start_capture(self) -> bool:
        """Start camera capture and processing"""
        if not self.cap or not self.cap.isOpened():
            if not self.initialize_camera():
                return False
        
        self.is_running = True
        self.processing_thread = threading.Thread(target=self._processing_loop, daemon=True)
        self.processing_thread.start()
        
        logger.info("Camera capture started")
        return True
    
    def stop_capture(self):
        """Stop camera capture and processing"""
        self.is_running = False
        
        if self.processing_thread:
            self.processing_thread.join(timeout=2.0)
        
        if self.cap:
            self.cap.release()
            self.cap = None
        
        logger.info("Camera capture stopped")
    
    def _processing_loop(self):
        """Main processing loop for camera frames with robust error handling"""
        consecutive_failures = 0
        max_consecutive_failures = 10
        
        while self.is_running:
            try:
                # Check if camera is available
                if not self.camera_available or not self.cap or not self.cap.isOpened():
                    if consecutive_failures < max_consecutive_failures:
                        logger.warning("Camera not available, attempting to reinitialize...")
                        if self.initialize_camera(self.camera_index):
                            consecutive_failures = 0
                            continue
                        else:
                            consecutive_failures += 1
                            time.sleep(1.0)  # Wait before retry
                            continue
                    else:
                        logger.error("Max camera failures reached, staying in fallback mode")
                        self.fallback_mode = True
                        break
                
                ret, frame = self.cap.read()
                
                if not ret or frame is None:
                    consecutive_failures += 1
                    logger.warning(f"Failed to read frame from camera (attempt {consecutive_failures})")
                    
                    if consecutive_failures >= max_consecutive_failures:
                        logger.error("Too many consecutive frame read failures, switching to fallback")
                        self.fallback_mode = True
                        break
                    
                    time.sleep(0.1)
                    continue
                
                # Reset failure counter on successful frame read
                consecutive_failures = 0
                
                # Validate frame dimensions
                if frame.shape[0] < 100 or frame.shape[1] < 100:
                    logger.warning("Frame too small, skipping")
                    continue
                
                # Mirror the frame if enabled
                if self.mirror_mode:
                    frame = cv2.flip(frame, 1)
                
                # Process frame with hand tracking
                try:
                    processed_frame, hands_detected = self.hand_tracker.process_frame(frame.copy())
                except Exception as ht_error:
                    logger.error(f"Hand tracking error: {str(ht_error)}")
                    processed_frame = frame.copy()
                    hands_detected = False
                
                # Add visual feedback overlay
                if hands_detected:
                    try:
                        self._add_hand_landmarks(processed_frame)
                        
                        # Get hand features for recognition
                        hand_features = self.hand_tracker.get_hand_features()
                        if hand_features is not None:
                            self._process_sign_recognition(processed_frame, hand_features)
                    except Exception as proc_error:
                        logger.error(f"Processing error: {str(proc_error)}")
                
                # Add UI overlays
                try:
                    self._add_ui_overlays(processed_frame)
                except Exception as ui_error:
                    logger.error(f"UI overlay error: {str(ui_error)}")
                
                # Store processed frame safely
                try:
                    with self.frame_lock:
                        self.current_frame = frame.copy()
                        self.processed_frame = processed_frame.copy()
                except Exception as store_error:
                    logger.error(f"Frame storage error: {str(store_error)}")
                
                # Control frame rate
                time.sleep(max(0.01, 1.0 / self.fps))
                
            except Exception as e:
                consecutive_failures += 1
                logger.error(f"Error in processing loop: {str(e)}")
                
                if consecutive_failures >= max_consecutive_failures:
                    logger.error("Too many processing loop failures, entering fallback mode")
                    self.fallback_mode = True
                    break
                
                time.sleep(0.5)
    
    def _add_hand_landmarks(self, frame: np.ndarray):
        """Add hand landmark visualization to frame"""
        if self.show_landmarks and self.hand_tracker.results:
            frame = self.hand_tracker.draw_landmarks(frame)
    
    def _process_sign_recognition(self, frame: np.ndarray, hand_features: np.ndarray):
        """Process sign recognition and add feedback"""
        try:
            # Get prediction from model
            prediction_result = self.model_predictor.predict_with_features(hand_features)
            
            if prediction_result["error"] is None:
                confidence = prediction_result["confidence"]
                predicted_sign = prediction_result["predicted_class"]
                
                # Check if we have a target sign for validation
                target_sign = getattr(self, 'target_sign', None)
                is_correct = None
                
                if target_sign:
                    is_correct = predicted_sign.lower() == target_sign.lower() and confidence >= 0.7
                    
                    # Store validation result
                    if not hasattr(self, 'validation_attempts'):
                        self.validation_attempts = []
                    
                    self.validation_attempts.append({
                        "target": target_sign,
                        "predicted": predicted_sign,
                        "confidence": confidence,
                        "is_correct": is_correct,
                        "timestamp": datetime.now().isoformat()
                    })
                
                # Store recognition results
                self.recognition_results = {
                    "predicted_sign": predicted_sign,
                    "confidence": confidence,
                    "timestamp": datetime.now(),
                    "top_predictions": prediction_result["top_predictions"],
                    "target_sign": target_sign,
                    "is_correct": is_correct
                }
                
                # Add visual feedback to frame
                self._add_recognition_feedback(frame, predicted_sign, confidence, target_sign, is_correct)
                
                # Record session data if recording
                if self.recording_session:
                    self.session_data.append({
                        "timestamp": datetime.now().isoformat(),
                        "predicted_sign": predicted_sign,
                        "confidence": confidence,
                        "hand_features": hand_features.tolist(),
                        "target_sign": target_sign,
                        "is_correct": is_correct
                    })
            
        except Exception as e:
            logger.error(f"Error in sign recognition: {str(e)}")
    
    def _add_recognition_feedback(self, frame: np.ndarray, predicted_sign: str, confidence: float, target_sign: str = None, is_correct: bool = None):
        """Add recognition feedback overlay to frame with validation status"""
        height, width = frame.shape[:2]
        
        # Validation status overlay (if target sign is provided)
        if target_sign and is_correct is not None:
            status_color = (0, 255, 0) if is_correct else (0, 0, 255)  # Green for correct, Red for incorrect
            status_text = "✓ CORRECT" if is_correct else "✗ INCORRECT"
            
            # Large status overlay
            overlay = frame.copy()
            cv2.rectangle(overlay, (0, 0), (width, 80), status_color, -1)
            cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
            
            # Status text
            cv2.putText(frame, status_text, (20, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
            
            # Target vs Predicted
            target_text = f"Target: {target_sign}"
            predicted_text = f"You signed: {predicted_sign}"
            cv2.putText(frame, target_text, (width - 300, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, predicted_text, (width - 300, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Confidence bar
        bar_width = 300
        bar_height = 20
        bar_x = width - bar_width - 20
        bar_y = height - 100
        
        # Background for confidence bar
        cv2.rectangle(frame, (bar_x - 5, bar_y - 30), 
                     (bar_x + bar_width + 5, bar_y + bar_height + 10), 
                     (0, 0, 0), -1)
        
        # Confidence bar background
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (50, 50, 50), -1)
        
        # Confidence fill with dynamic color
        fill_width = int(bar_width * confidence)
        if confidence >= 0.8:
            color = (0, 255, 0)  # Green
        elif confidence >= 0.6:
            color = (0, 255, 255)  # Yellow
        else:
            color = (0, 0, 255)  # Red
        
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + fill_width, bar_y + bar_height), color, -1)
        
        # Confidence text
        confidence_text = f"Confidence: {confidence:.1%}"
        cv2.putText(frame, confidence_text, (bar_x, bar_y - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Predicted sign text (if no target sign)
        if not target_sign:
            sign_text = f"Detected: {predicted_sign}"
            text_size = cv2.getTextSize(sign_text, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 2)[0]
            text_x = (width - text_size[0]) // 2
            text_y = height - 150
            
            # Background for sign text
            cv2.rectangle(frame, (text_x - 10, text_y - text_size[1] - 10), 
                         (text_x + text_size[0] + 10, text_y + 10), (0, 0, 0), -1)
            
            cv2.putText(frame, sign_text, (text_x, text_y), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
    
    def _add_ui_overlays(self, frame: np.ndarray):
        """Add UI overlays and information to frame"""
        height, width = frame.shape[:2]
        
        # Recording indicator
        if self.recording_session:
            cv2.circle(frame, (30, 30), 15, (0, 0, 255), -1)
            cv2.putText(frame, "REC", (50, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # Hand detection status
        hands_detected = self.hand_tracker.is_hand_visible()
        status_text = "Hands Detected" if hands_detected else "No Hands Detected"
        status_color = (0, 255, 0) if hands_detected else (0, 0, 255)
        
        cv2.putText(frame, status_text, (20, height - 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
        
        # Timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        cv2.putText(frame, timestamp, (width - 100, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    def get_current_frame(self) -> Optional[np.ndarray]:
        """Get current processed frame"""
        with self.frame_lock:
            return self.processed_frame.copy() if self.processed_frame is not None else None
    
    def get_frame_as_base64(self) -> Optional[str]:
        """Get current frame as base64 encoded string"""
        frame = self.get_current_frame()
        if frame is None:
            return None
        
        try:
            # Convert frame to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Convert to PIL Image
            pil_image = Image.fromarray(frame_rgb)
            
            # Convert to base64
            buffer = io.BytesIO()
            pil_image.save(buffer, format='JPEG', quality=85)
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            return f"data:image/jpeg;base64,{img_str}"
            
        except Exception as e:
            logger.error(f"Error converting frame to base64: {str(e)}")
            return None
    
    def capture_screenshot(self) -> Optional[np.ndarray]:
        """Capture a screenshot of current frame"""
        with self.frame_lock:
            if self.current_frame is not None:
                return self.current_frame.copy()
        return None
    
    def start_recording_session(self, target_sign: str = None):
        """Start recording a practice session"""
        self.recording_session = True
        self.session_data = []
        self.target_sign = target_sign
        logger.info("Recording session started")
    
    def stop_recording_session(self) -> Dict[str, Any]:
        """Stop recording session and return session data"""
        self.recording_session = False
        session_summary = {
            "session_duration": len(self.session_data),
            "total_frames": len(self.session_data),
            "target_sign": getattr(self, 'target_sign', None),
            "recognition_data": self.session_data.copy(),
            "average_confidence": np.mean([d["confidence"] for d in self.session_data]) if self.session_data else 0,
            "session_end_time": datetime.now().isoformat()
        }
        
        self.session_data.clear()
        logger.info("Recording session stopped")
        return session_summary
    
    def get_recognition_results(self) -> Dict[str, Any]:
        """Get latest recognition results"""
        return self.recognition_results.copy()
    
    def set_camera_settings(self, **settings):
        """Update camera settings"""
        if 'mirror_mode' in settings:
            self.mirror_mode = settings['mirror_mode']
        
        if 'show_landmarks' in settings:
            self.show_landmarks = settings['show_landmarks']
        
        if 'confidence_threshold' in settings:
            self.confidence_threshold = settings['confidence_threshold']
        
        if 'frame_width' in settings and 'frame_height' in settings:
            self.frame_width = settings['frame_width']
            self.frame_height = settings['frame_height']
            
            if self.cap and self.cap.isOpened():
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)
        
        logger.info(f"Camera settings updated: {settings}")
    
    def get_camera_info(self) -> Dict[str, Any]:
        """Get camera information and status"""
        info = {
            "is_running": self.is_running,
            "camera_index": self.camera_index,
            "frame_width": self.frame_width,
            "frame_height": self.frame_height,
            "fps": self.fps,
            "mirror_mode": self.mirror_mode,
            "show_landmarks": self.show_landmarks,
            "hands_detected": self.hand_tracker.is_hand_visible(),
            "recording_session": self.recording_session
        }
        
        if self.cap and self.cap.isOpened():
            info.update({
                "actual_width": int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                "actual_height": int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                "actual_fps": int(self.cap.get(cv2.CAP_PROP_FPS))
            })
        
        return info
    
    def validate_sign_attempt(self, target_sign: str, duration_seconds: int = 3) -> Dict[str, Any]:
        """Validate a sign attempt over a duration"""
        if not self.is_running:
            return {"error": "Camera not running"}
        
        start_time = time.time()
        attempts = []
        
        while time.time() - start_time < duration_seconds:
            if self.recognition_results:
                attempts.append({
                    "predicted_sign": self.recognition_results["predicted_sign"],
                    "confidence": self.recognition_results["confidence"],
                    "timestamp": self.recognition_results["timestamp"]
                })
            time.sleep(0.1)
        
        if not attempts:
            return {
                "success": False,
                "message": "No sign detected during validation period",
                "target_sign": target_sign,
                "attempts": 0
            }
        
        # Analyze attempts
        correct_attempts = [a for a in attempts if a["predicted_sign"].lower() == target_sign.lower()]
        average_confidence = np.mean([a["confidence"] for a in correct_attempts]) if correct_attempts else 0
        
        success = len(correct_attempts) >= len(attempts) * 0.6  # 60% of attempts must be correct
        
        return {
            "success": success,
            "target_sign": target_sign,
            "total_attempts": len(attempts),
            "correct_attempts": len(correct_attempts),
            "accuracy_rate": len(correct_attempts) / len(attempts) if attempts else 0,
            "average_confidence": average_confidence,
            "message": "Sign validated successfully!" if success else "Sign validation failed. Try again.",
            "detailed_attempts": attempts
        }
    
    def set_target_sign(self, target_sign: str) -> None:
        """Set target sign for validation"""
        self.target_sign = target_sign
        self.validation_attempts = []
        logger.info(f"Target sign set to: {target_sign}")
    
    def clear_target_sign(self) -> None:
        """Clear target sign"""
        self.target_sign = None
        if hasattr(self, 'validation_attempts'):
            self.validation_attempts.clear()
    
    def get_validation_results(self) -> List[Dict[str, Any]]:
        """Get validation results for current target sign"""
        return getattr(self, 'validation_attempts', [])
    
    def is_camera_working(self) -> bool:
        """Check if camera is working properly"""
        return (
            self.camera_available and 
            self.cap is not None and 
            self.cap.isOpened() and 
            self.current_frame is not None
        )
    
    def __del__(self):
        """Cleanup when object is destroyed"""
        if hasattr(self, 'is_running'):
            self.stop_capture()
