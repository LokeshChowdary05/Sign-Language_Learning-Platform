"""
Enhanced Camera Interface for Real-time Sign Language Detection
Provides live video feed with hand detection and sign recognition overlay
"""

import cv2
import numpy as np
import streamlit as st
from typing import Dict, List, Optional, Tuple, Any
import logging
import time
from PIL import Image
import base64
import io

logger = logging.getLogger(__name__)

class RealTimeCameraInterface:
    """Real-time camera interface with live video feed and hand detection"""
    
    def __init__(self, camera_manager, quiz_system):
        """Initialize camera interface"""
        self.camera_manager = camera_manager
        self.quiz_system = quiz_system
        self.video_placeholder = None
        self.controls_placeholder = None
        self.current_frame = None
        
    def render_live_practice_interface(self) -> None:
        """Render the complete live practice interface"""
        st.markdown("## 🎯 Live Practice Mode")
        
        # Create main layout
        video_col, control_col = st.columns([2, 1])
        
        with video_col:
            self.render_video_feed()
        
        with control_col:
            self.render_practice_controls()
    
    def render_video_feed(self) -> None:
        """Render live video feed with hand detection overlay"""
        st.markdown("### 📹 Live Camera Feed")
        
        # Video display container
        video_container = st.container()
        
        with video_container:
            # Camera status and controls
            camera_status_col1, camera_status_col2, camera_status_col3 = st.columns(3)
            
            with camera_status_col1:
                if st.button("🎥 Start Camera", key="start_camera_live"):
                    if self.start_camera():
                        st.success("Camera started!")
                        st.rerun()
                    else:
                        st.error("Failed to start camera")
            
            with camera_status_col2:
                if st.button("⏹️ Stop Camera", key="stop_camera_live"):
                    self.stop_camera()
                    st.info("Camera stopped")
                    st.rerun()
            
            with camera_status_col3:
                camera_active = self.camera_manager.is_camera_working()
                status_color = "🟢" if camera_active else "🔴"
                st.markdown(f"**Status:** {status_color} {'Active' if camera_active else 'Inactive'}")
        
        # Video feed placeholder
        self.video_placeholder = st.empty()
        
        # Display live feed if camera is active
        if self.camera_manager.is_camera_working():
            self.display_live_feed()
        else:
            with self.video_placeholder.container():
                st.info("📹 Start camera to see live video feed with hand detection")
                st.markdown("**Features:**")
                st.markdown("• 🟢 Green box around detected hands")
                st.markdown("• 📝 Real-time sign recognition")
                st.markdown("• 🎯 Live accuracy feedback")
                st.markdown("• ⏱️ Practice timer")
    
    def display_live_feed(self) -> None:
        """Display the live camera feed with annotations"""
        try:
            # Get processed frame from camera manager
            frame = self.camera_manager.get_current_frame()
            
            if frame is not None:
                # Add hand detection overlay
                annotated_frame = self.add_hand_detection_overlay(frame)
                
                # Convert to RGB for display
                frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                
                # Display in Streamlit
                with self.video_placeholder.container():
                    st.image(frame_rgb, channels="RGB", use_column_width=True)
                    
                    # Display recognition info below video
                    self.display_recognition_info()
            else:
                with self.video_placeholder.container():
                    st.warning("No video frame available")
                    
        except Exception as e:
            logger.error(f"Error displaying live feed: {str(e)}")
            with self.video_placeholder.container():
                st.error(f"Video display error: {str(e)}")
    
    def add_hand_detection_overlay(self, frame: np.ndarray) -> np.ndarray:
        """Add hand detection overlay with green boxes and sign labels"""
        try:
            annotated_frame = frame.copy()
            height, width = frame.shape[:2]
            
            # Get hand tracking results
            if hasattr(self.camera_manager.hand_tracker, 'results') and self.camera_manager.hand_tracker.results:
                results = self.camera_manager.hand_tracker.results
                
                if hasattr(results, 'multi_hand_landmarks') and results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        # Calculate bounding box for hand
                        x_coords = [landmark.x * width for landmark in hand_landmarks.landmark]
                        y_coords = [landmark.y * height for landmark in hand_landmarks.landmark]
                        
                        x_min, x_max = int(min(x_coords)), int(max(x_coords))
                        y_min, y_max = int(min(y_coords)), int(max(y_coords))
                        
                        # Add padding to bounding box
                        padding = 20
                        x_min = max(0, x_min - padding)
                        y_min = max(0, y_min - padding)
                        x_max = min(width, x_max + padding)
                        y_max = min(height, y_max + padding)
                        
                        # Draw green bounding box
                        cv2.rectangle(annotated_frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 3)
                        
                        # Add "HAND DETECTED" label
                        cv2.putText(annotated_frame, "HAND DETECTED", (x_min, y_min - 10),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                        
                        # Draw hand landmarks
                        self.camera_manager.hand_tracker.draw_landmarks(annotated_frame)
            
            # Add recognition results if available
            recognition_results = self.camera_manager.get_recognition_results()
            if recognition_results:
                self.add_recognition_overlay(annotated_frame, recognition_results)
            
            # Add quiz info if active
            quiz_status = self.quiz_system.get_quiz_status()
            if quiz_status.get('active'):
                self.add_quiz_overlay(annotated_frame, quiz_status)
            
            return annotated_frame
            
        except Exception as e:
            logger.error(f"Error adding overlay: {str(e)}")
            return frame
    
    def add_recognition_overlay(self, frame: np.ndarray, recognition_results: Dict[str, Any]) -> None:
        """Add sign recognition overlay to frame"""
        try:
            height, width = frame.shape[:2]
            
            predicted_sign = recognition_results.get('predicted_sign', 'None')
            confidence = recognition_results.get('confidence', 0)
            is_correct = recognition_results.get('is_correct')
            
            # Recognition info box background
            overlay_height = 80
            cv2.rectangle(frame, (0, height - overlay_height), (width, height), (0, 0, 0), -1)
            cv2.rectangle(frame, (0, height - overlay_height), (width, height), (255, 255, 255), 2)
            
            # Predicted sign text
            sign_text = f"Detected: {predicted_sign}"
            cv2.putText(frame, sign_text, (10, height - 50),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            
            # Confidence bar
            bar_width = 200
            bar_x = 10
            bar_y = height - 30
            
            # Background bar
            cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + 15), (100, 100, 100), -1)
            
            # Confidence fill
            fill_width = int(bar_width * confidence)
            color = (0, 255, 0) if is_correct else (0, 0, 255) if confidence < 0.7 else (0, 255, 255)  # Green for correct, yellow for high confidence
            
            cv2.rectangle(frame, (bar_x, bar_y), (bar_x + fill_width, bar_y + 15), color, -1)
            
            # Confidence percentage
            conf_text = f"{confidence:.1%}"
            cv2.putText(frame, conf_text, (bar_x + bar_width + 10, bar_y + 12),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
        except Exception as e:
            logger.error(f"Error adding recognition overlay: {str(e)}")
    
    def add_quiz_overlay(self, frame: np.ndarray, quiz_status: Dict[str, Any]) -> None:
        """Add quiz information overlay to frame"""
        try:
            height, width = frame.shape[:2]
            progress = quiz_status.get('progress', {})
            current_sign = quiz_status.get('current_sign', '')
            
            # Quiz info box
            box_height = 60
            cv2.rectangle(frame, (0, 0), (width, box_height), (0, 0, 0), -1)
            cv2.rectangle(frame, (0, 0), (width, box_height), (0, 255, 255), 2)
            
            # Current target sign
            target_text = f"Target Sign: {current_sign.upper()}"
            cv2.putText(frame, target_text, (10, 25),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
            
            # Progress and timer
            score = progress.get('score', 0)
            total = progress.get('total_signs', 0)
            time_left = progress.get('time_remaining_formatted', '00:00')
            
            progress_text = f"Score: {score}/{total} | Time: {time_left}"
            cv2.putText(frame, progress_text, (10, 50),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
        except Exception as e:
            logger.error(f"Error adding quiz overlay: {str(e)}")
    
    def display_recognition_info(self) -> None:
        """Display recognition information below video"""
        try:
            recognition_results = self.camera_manager.get_recognition_results()
            
            if recognition_results:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    predicted_sign = recognition_results.get('predicted_sign', 'None')
                    st.metric("🎯 Detected Sign", predicted_sign)
                
                with col2:
                    confidence = recognition_results.get('confidence', 0)
                    st.metric("📊 Confidence", f"{confidence:.1%}")
                
                with col3:
                    is_correct = recognition_results.get('is_correct')
                    if is_correct is not None:
                        status = "✅ Correct" if is_correct else "❌ Incorrect"
                        st.metric("🎯 Status", status)
                    else:
                        hands_detected = self.camera_manager.hand_tracker.is_hand_visible()
                        hand_status = "✅ Detected" if hands_detected else "❌ No Hands"
                        st.metric("👋 Hands", hand_status)
                        
        except Exception as e:
            logger.error(f"Error displaying recognition info: {str(e)}")
    
    def render_practice_controls(self) -> None:
        """Render practice mode controls"""
        st.markdown("### 🎮 Practice Controls")
        
        # Quiz controls
        if st.button("🚀 Start 3-Min Practice Quiz", type="primary", key="start_practice_quiz"):
            self.start_practice_quiz()
        
        # Challenge controls
        if st.button("🎯 Random Sign Challenge", key="start_random_challenge"):
            self.start_random_challenge()
        
        # Current activity status
        quiz_status = self.quiz_system.get_quiz_status()
        if quiz_status.get('active'):
            self.render_active_quiz_controls(quiz_status)
        else:
            self.render_practice_info()
    
    def render_active_quiz_controls(self, quiz_status: Dict[str, Any]) -> None:
        """Render controls for active quiz"""
        st.markdown("### 🎮 Active Quiz")
        
        progress = quiz_status.get('progress', {})
        current_sign = quiz_status.get('current_sign', '')
        
        # Progress display
        progress_percentage = progress.get('progress_percentage', 0)
        st.progress(progress_percentage / 100)
        
        # Current sign display
        if current_sign:
            st.markdown(f"### 🎯 Current Sign: **{current_sign.upper()}**")
            
            # Show reference image placeholder
            st.image(f"https://via.placeholder.com/300x200/4CAF50/white?text={current_sign.replace('_', '+')}", 
                    caption=f"Reference: {current_sign}")
        
        # Quiz metrics
        score = progress.get('score', 0)
        total_signs = progress.get('total_signs', 0)
        time_left = progress.get('time_remaining_formatted', '00:00')
        
        metric_col1, metric_col2 = st.columns(2)
        
        with metric_col1:
            st.metric("Score", f"{score}/{total_signs}")
        
        with metric_col2:
            st.metric("Time Left", time_left)
        
        # Control buttons
        control_col1, control_col2 = st.columns(2)
        
        with control_col1:
            if st.button("⏭️ Skip Sign", key="skip_sign_quiz"):
                self.skip_current_sign()
        
        with control_col2:
            if st.button("🛑 End Quiz", key="end_quiz"):
                self.end_quiz()
    
    def render_practice_info(self) -> None:
        """Render practice information when no quiz is active"""
        st.markdown("### 💡 Ready to Practice!")
        
        st.info("Choose an option above to start practicing")
        
        # Camera status
        if self.camera_manager.is_camera_working():
            st.success("📹 Camera is active and ready")
        else:
            st.warning("📹 Please start the camera first")
        
        # Practice tips
        with st.expander("💡 Practice Tips"):
            st.markdown("• Ensure good lighting")
            st.markdown("• Position hands clearly in frame")
            st.markdown("• Practice signs slowly and clearly")
            st.markdown("• Use the reference images as guides")
    
    def start_camera(self) -> bool:
        """Start the camera"""
        try:
            if self.camera_manager.initialize_camera():
                return self.camera_manager.start_capture()
            return False
        except Exception as e:
            logger.error(f"Error starting camera: {str(e)}")
            return False
    
    def stop_camera(self) -> None:
        """Stop the camera"""
        try:
            self.camera_manager.stop_capture()
        except Exception as e:
            logger.error(f"Error stopping camera: {str(e)}")
    
    def start_practice_quiz(self) -> None:
        """Start a 3-minute practice quiz"""
        try:
            current_language = st.session_state.get('current_language', 'ASL')
            result = self.quiz_system.start_quiz("practice", current_language)
            
            if result.get("success"):
                st.success("🚀 Practice quiz started!")
                # Set first target sign for camera
                first_sign = result.get('first_sign')
                if first_sign and self.camera_manager.is_camera_working():
                    self.camera_manager.set_target_sign(first_sign)
                st.rerun()
            else:
                st.error(f"Failed to start quiz: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            st.error(f"Error starting practice quiz: {str(e)}")
            logger.error(f"Practice quiz error: {str(e)}")
    
    def start_random_challenge(self) -> None:
        """Start a random sign challenge"""
        try:
            # Get random sign from practice database
            quiz_db = self.quiz_system.quiz_database
            practice_questions = quiz_db.get_practice_questions(1)
            
            if practice_questions:
                challenge_sign = practice_questions[0]['sign']
                
                # Store challenge in session state
                st.session_state.current_challenge = {
                    "sign": challenge_sign,
                    "language": st.session_state.get('current_language', 'ASL'),
                    "start_time": time.time(),
                    "type": "random"
                }
                
                # Set target for camera
                if self.camera_manager.is_camera_working():
                    self.camera_manager.set_target_sign(challenge_sign)
                
                st.success(f"🎯 Challenge: Sign '{challenge_sign}'!")
                st.rerun()
            else:
                st.error("Failed to generate challenge")
                
        except Exception as e:
            st.error(f"Error starting challenge: {str(e)}")
            logger.error(f"Challenge error: {str(e)}")
    
    def skip_current_sign(self) -> None:
        """Skip the current sign in quiz"""
        try:
            result = self.quiz_system.skip_current_sign()
            if result.get('quiz_completed'):
                st.balloons()
                st.success("Quiz completed!")
            else:
                next_sign = result.get('next_sign')
                if next_sign and self.camera_manager.is_camera_working():
                    self.camera_manager.set_target_sign(next_sign)
            st.rerun()
        except Exception as e:
            st.error(f"Error skipping sign: {str(e)}")
    
    def end_quiz(self) -> None:
        """End the current quiz"""
        try:
            results = self.quiz_system.end_quiz()
            if results:
                st.balloons()
                self.display_quiz_results(results)
            st.rerun()
        except Exception as e:
            st.error(f"Error ending quiz: {str(e)}")
    
    def display_quiz_results(self, results: Dict[str, Any]) -> None:
        """Display quiz completion results"""
        st.markdown("## 🎉 Quiz Completed!")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Final Score", f"{results['correct_signs']}/{results['total_signs']}")
        
        with col2:
            st.metric("Accuracy", f"{results['accuracy']}%")
        
        with col3:
            st.metric("Grade", results['grade'])
        
        # XP earned
        xp_earned = results.get('xp_earned', 0)
        st.success(f"🎁 +{xp_earned} XP earned!")
        
        # Feedback
        feedback = results.get('feedback', {})
        if results.get('passed'):
            st.success(feedback.get('title', 'Well Done!'))
        else:
            st.warning(feedback.get('title', 'Keep Practicing!'))
        
        st.info(feedback.get('message', 'Good effort!'))
