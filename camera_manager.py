import streamlit as st
import cv2
from typing import List, Dict, Any

class CameraManager:
    def __init__(self):
        self.camera = None
        self.active = False

    def start_camera(self):
        self.camera = cv2.VideoCapture(0)
        self.active = self.camera.isOpened()

    def stop_camera(self):
        if self.camera:
            self.camera.release()
        self.active = False

    def get_frame(self):
        if not self.active:
            raise Exception("Camera is not active")
        ret, frame = self.camera.read()
        if not ret:
            raise Exception("Failed to capture image")
        return frame

    def is_active(self) -> bool:
        return self.active

class CameraInterface:
    def __init__(self, manager: CameraManager):
        self.manager = manager

    def display_camera(self):
        if self.manager.is_active():
            frame = self.manager.get_frame()
            st.image(frame, channels='BGR')
        else:
            st.write("Camera not active")
