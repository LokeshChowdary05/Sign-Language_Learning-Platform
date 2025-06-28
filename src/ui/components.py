"""
UI Components for Sign Language Learning Platform
Reusable UI components and widgets
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

class UIComponents:
    """Reusable UI components for the application"""
    
    def __init__(self):
        """Initialize UI components"""
        pass
    
    def render_language_selector(self, languages: Dict[str, Dict], current_language: str) -> str:
        """Render language selector with flags and details"""
        
        # Create options with flags and names
        options = []
        values = []
        current_index = 0
        
        for i, (code, info) in enumerate(languages.items()):
            flag = info.get('flag', '🏳️')
            name = info.get('name', code)
            option_text = f"{flag} {name}"
            options.append(option_text)
            values.append(code)
            
            if code == current_language:
                current_index = i
        
        # Language selector
        selected_option = st.selectbox(
            "Choose Sign Language:",
            options,
            index=current_index,
            key="language_selector",
            help="Select your preferred sign language to learn"
        )
        
        # Get the corresponding language code
        selected_index = options.index(selected_option)
        selected_code = values[selected_index]
        
        # Show language details
        if selected_code in languages:
            lang_info = languages[selected_code]
            with st.expander("ℹ️ Language Details", expanded=False):
                st.markdown(f"**Region:** {lang_info.get('region', 'Unknown')}")
                st.markdown(f"**Difficulty:** {lang_info.get('difficulty', 'Unknown')}")
                st.markdown(f"**Active Users:** {lang_info.get('users', 'Unknown')}")
                st.markdown(f"**Description:** {lang_info.get('description', 'No description available.')}")
        
        return selected_code
    
    def render_metric_card(self, title: str, value: str, icon: str, delta: str = None):
        """Render a metric card with styling"""
        
        delta_color = "normal"
        if delta:
            if "+" in delta:
                delta_color = "normal"
            elif "-" in delta:
                delta_color = "inverse"
        
        col1, col2 = st.columns([1, 4])
        
        with col1:
            st.markdown(f"<div style='font-size: 2rem; text-align: center;'>{icon}</div>", 
                       unsafe_allow_html=True)
        
        with col2:
            st.metric(
                label=title,
                value=value,
                delta=delta,
                delta_color=delta_color
            )
    
    def render_confidence_meter(self, confidence: float):
        """Render a visual confidence meter"""
        
        # Determine color based on confidence
        if confidence >= 80:
            color = "green"
            status = "Excellent"
        elif confidence >= 60:
            color = "orange" 
            status = "Good"
        else:
            color = "red"
            status = "Needs Improvement"
        
        # Create gauge chart
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = confidence,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': f"Confidence: {status}"},
            delta = {'reference': 80},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': color},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)
