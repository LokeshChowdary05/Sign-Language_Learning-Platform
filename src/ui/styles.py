"""
UI Styles and CSS for the Sign Language Learning Platform
WCAG 2.1 compliant design with professional educational aesthetic
"""

def get_custom_css() -> str:
    """
    Returns custom CSS for the Streamlit application
    Ensures WCAG 2.1 compliance and professional educational design
    """
    return """
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Root Variables for Color Scheme */
    :root {
        --primary-color: #2E8B57;
        --primary-light: #3CB371;
        --primary-dark: #228B22;
        --secondary-color: #4682B4;
        --secondary-light: #87CEEB;
        --accent-color: #FF6347;
        --accent-light: #FFB347;
        --background-color: #F8F9FA;
        --surface-color: #FFFFFF;
        --text-primary: #2C3E50;
        --text-secondary: #546E7A;
        --text-muted: #78909C;
        --success-color: #28A745;
        --warning-color: #FFC107;
        --error-color: #DC3545;
        --info-color: #17A2B8;
        --border-color: #E0E0E0;
        --shadow-light: 0 2px 4px rgba(0,0,0,0.1);
        --shadow-medium: 0 4px 8px rgba(0,0,0,0.15);
        --shadow-heavy: 0 8px 16px rgba(0,0,0,0.2);
        --border-radius: 12px;
        --border-radius-small: 8px;
        --transition-fast: 0.2s ease;
        --transition-medium: 0.3s ease;
        --transition-slow: 0.5s ease;
    }
    
    /* Base Application Styles */
    .main {
        padding: 1rem 2rem;
        background-color: var(--background-color);
        min-height: 100vh;
    }
    
    /* Typography */
    .main .block-container {
        font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: var(--text-primary);
        line-height: 1.6;
    }
    
    /* Header Styles */
    .header-container {
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 2rem;
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        border-radius: var(--border-radius);
        color: white;
        box-shadow: var(--shadow-medium);
    }
    
    .main-title {
        font-family: 'Poppins', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        letter-spacing: -0.5px;
    }
    
    .subtitle {
        font-size: 1.2rem;
        font-weight: 400;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    /* Sidebar Styles */
    .css-1d391kg {
        background-color: var(--surface-color);
        border-right: 2px solid var(--border-color);
        box-shadow: var(--shadow-light);
    }
    
    .css-1d391kg .css-1v0mbdj {
        border-radius: var(--border-radius-small);
        margin-bottom: 1rem;
    }
    
    /* Navigation Menu Styles */
    .stSelectbox > div > div {
        background-color: var(--surface-color);
        border: 2px solid var(--border-color);
        border-radius: var(--border-radius-small);
        transition: var(--transition-medium);
    }
    
    .stSelectbox > div > div:hover {
        border-color: var(--primary-color);
        box-shadow: var(--shadow-light);
    }
    
    /* Button Styles */
    .stButton > button {
        border-radius: var(--border-radius-small);
        border: 2px solid transparent;
        font-weight: 500;
        font-size: 0.95rem;
        padding: 0.6rem 1.5rem;
        transition: var(--transition-medium);
        cursor: pointer;
        box-shadow: var(--shadow-light);
    }
    
    .stButton > button[data-baseweb="button"][kind="primary"] {
        background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
        color: white;
        border-color: var(--primary-color);
    }
    
    .stButton > button[data-baseweb="button"][kind="primary"]:hover {
        background: linear-gradient(135deg, var(--primary-dark), var(--primary-color));
        transform: translateY(-2px);
        box-shadow: var(--shadow-medium);
    }
    
    .stButton > button[data-baseweb="button"][kind="secondary"] {
        background-color: var(--surface-color);
        color: var(--text-primary);
        border-color: var(--border-color);
    }
    
    .stButton > button[data-baseweb="button"][kind="secondary"]:hover {
        background-color: var(--background-color);
        border-color: var(--secondary-color);
        transform: translateY(-1px);
    }
    
    /* Metric Card Styles */
    .metric-card {
        background: var(--surface-color);
        padding: 1.5rem;
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-light);
        border: 1px solid var(--border-color);
        transition: var(--transition-medium);
        height: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-medium);
    }
    
    .metric-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .metric-value {
        font-family: 'Poppins', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-color);
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 1rem;
        font-weight: 500;
        color: var(--text-secondary);
        margin-bottom: 0.5rem;
    }
    
    .metric-delta {
        font-size: 0.85rem;
        color: var(--success-color);
        font-weight: 500;
    }
    
    /* Language Selector Styles */
    .language-selector {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .language-option {
        background: var(--surface-color);
        border: 2px solid var(--border-color);
        border-radius: var(--border-radius-small);
        padding: 1rem;
        text-align: center;
        cursor: pointer;
        transition: var(--transition-medium);
        position: relative;
        overflow: hidden;
    }
    
    .language-option:hover {
        border-color: var(--primary-color);
        transform: translateY(-2px);
        box-shadow: var(--shadow-light);
    }
    
    .language-option.selected {
        border-color: var(--primary-color);
        background: linear-gradient(135deg, var(--primary-color), var(--primary-light));
        color: white;
    }
    
    .language-flag {
        font-size: 2rem;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    .language-name {
        font-weight: 600;
        font-size: 1rem;
        margin-bottom: 0.25rem;
    }
    
    .language-code {
        font-size: 0.8rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Progress Styles */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        border-radius: var(--border-radius-small);
    }
    
    .stProgress > div > div {
        background-color: var(--border-color);
        border-radius: var(--border-radius-small);
    }
    
    /* Confidence Meter */
    .confidence-meter {
        background: var(--surface-color);
        border-radius: var(--border-radius);
        padding: 1.5rem;
        box-shadow: var(--shadow-light);
        border: 1px solid var(--border-color);
    }
    
    .confidence-value {
        font-family: 'Poppins', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin: 1rem 0;
    }
    
    .confidence-high {
        color: var(--success-color);
    }
    
    .confidence-medium {
        color: var(--warning-color);
    }
    
    .confidence-low {
        color: var(--error-color);
    }
    
    /* Expander Styles */
    .streamlit-expanderHeader {
        background: var(--surface-color);
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius-small);
        font-weight: 600;
        color: var(--text-primary);
    }
    
    .streamlit-expanderContent {
        background: var(--surface-color);
        border: 1px solid var(--border-color);
        border-top: none;
        border-radius: 0 0 var(--border-radius-small) var(--border-radius-small);
    }
    
    /* Alert Styles */
    .stAlert {
        border-radius: var(--border-radius-small);
        border: none;
        box-shadow: var(--shadow-light);
    }
    
    .stAlert[data-baseweb="notification"][kind="success"] {
        background: linear-gradient(135deg, #d4edda, #c3e6cb);
        color: #155724;
        border-left: 4px solid var(--success-color);
    }
    
    .stAlert[data-baseweb="notification"][kind="info"] {
        background: linear-gradient(135deg, #d1ecf1, #bee5eb);
        color: #0c5460;
        border-left: 4px solid var(--info-color);
    }
    
    .stAlert[data-baseweb="notification"][kind="warning"] {
        background: linear-gradient(135deg, #fff3cd, #ffeaa7);
        color: #856404;
        border-left: 4px solid var(--warning-color);
    }
    
    .stAlert[data-baseweb="notification"][kind="error"] {
        background: linear-gradient(135deg, #f8d7da, #f5c6cb);
        color: #721c24;
        border-left: 4px solid var(--error-color);
    }
    
    /* Chart Styles */
    .js-plotly-plot {
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-light);
        border: 1px solid var(--border-color);
        background: var(--surface-color);
    }
    
    /* Input Styles */
    .stTextInput > div > div > input {
        border-radius: var(--border-radius-small);
        border: 2px solid var(--border-color);
        transition: var(--transition-medium);
        font-size: 1rem;
        padding: 0.75rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 2px rgba(46, 139, 87, 0.2);
    }
    
    .stTextArea > div > div > textarea {
        border-radius: var(--border-radius-small);
        border: 2px solid var(--border-color);
        transition: var(--transition-medium);
        font-size: 1rem;
        padding: 0.75rem;
        font-family: inherit;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 2px rgba(46, 139, 87, 0.2);
    }
    
    /* Challenge Card Styles */
    .challenge-card {
        background: var(--surface-color);
        border-radius: var(--border-radius);
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: var(--shadow-light);
        border: 1px solid var(--border-color);
        transition: var(--transition-medium);
    }
    
    .challenge-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-medium);
    }
    
    .challenge-difficulty-easy {
        border-left: 4px solid var(--success-color);
    }
    
    .challenge-difficulty-medium {
        border-left: 4px solid var(--warning-color);
    }
    
    .challenge-difficulty-hard {
        border-left: 4px solid var(--error-color);
    }
    
    /* Learning Module Styles */
    .learning-module {
        background: var(--surface-color);
        border-radius: var(--border-radius);
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: var(--shadow-light);
        border: 1px solid var(--border-color);
    }
    
    .module-available {
        border-left: 4px solid var(--primary-color);
    }
    
    .module-completed {
        border-left: 4px solid var(--success-color);
        background: linear-gradient(135deg, #f8fff8, #f0fff0);
    }
    
    .module-locked {
        border-left: 4px solid var(--text-muted);
        opacity: 0.7;
    }
    
    /* Camera Interface Styles */
    .camera-container {
        background: var(--surface-color);
        border-radius: var(--border-radius);
        padding: 2rem;
        box-shadow: var(--shadow-medium);
        border: 2px solid var(--border-color);
        position: relative;
        overflow: hidden;
    }
    
    .camera-placeholder {
        background: linear-gradient(135deg, #f0f0f0, #e0e0e0);
        border-radius: var(--border-radius-small);
        min-height: 400px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        color: var(--text-secondary);
    }
    
    /* Feedback Overlay */
    .feedback-overlay {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0,0,0,0.8);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        font-weight: 600;
        border-radius: var(--border-radius);
    }
    
    /* Activity Timeline */
    .activity-item {
        background: var(--surface-color);
        border-radius: var(--border-radius-small);
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 3px solid var(--primary-color);
        box-shadow: var(--shadow-light);
        transition: var(--transition-medium);
    }
    
    .activity-item:hover {
        transform: translateX(4px);
    }
    
    /* Recommendation Cards */
    .recommendation-card {
        background: linear-gradient(135deg, var(--surface-color), #f8f9fa);
        border-radius: var(--border-radius-small);
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid var(--border-color);
        transition: var(--transition-medium);
    }
    
    .recommendation-card:hover {
        background: linear-gradient(135deg, #f8f9fa, var(--surface-color));
        box-shadow: var(--shadow-light);
    }
    
    /* Accessibility Improvements */
    @media (prefers-reduced-motion: reduce) {
        * {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
    }
    
    /* High Contrast Mode */
    @media (prefers-contrast: high) {
        :root {
            --border-color: #000000;
            --text-primary: #000000;
            --text-secondary: #333333;
        }
        
        .stButton > button {
            border-width: 3px;
        }
    }
    
    /* Focus Indicators for Accessibility */
    *:focus {
        outline: 3px solid var(--primary-color);
        outline-offset: 2px;
    }
    
    .stButton > button:focus {
        outline: 3px solid var(--accent-color);
        outline-offset: 3px;
    }
    
    /* Loading Animation */
    .loading-spinner {
        border: 4px solid var(--border-color);
        border-top: 4px solid var(--primary-color);
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 1rem auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Success Animation */
    .success-checkmark {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        display: block;
        stroke-width: 2;
        stroke: var(--success-color);
        stroke-miterlimit: 10;
        margin: 1rem auto;
        box-shadow: inset 0px 0px 0px var(--success-color);
        animation: fill 0.4s ease-in-out 0.4s forwards, scale 0.3s ease-in-out 0.9s both;
    }
    
    @keyframes fill {
        100% {
            box-shadow: inset 0px 0px 0px 80px var(--success-color);
        }
    }
    
    @keyframes scale {
        0%, 100% {
            transform: none;
        }
        50% {
            transform: scale3d(1.1, 1.1, 1);
        }
    }
    
    /* Print Styles */
    @media print {
        .stButton, .stSelectbox, .camera-container {
            display: none !important;
        }
        
        .main {
            background: white !important;
        }
        
        * {
            box-shadow: none !important;
        }
    }
    
    /* Footer Styles */
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        border-top: 2px solid var(--border-color);
        color: var(--text-secondary);
        font-style: italic;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
        
        .subtitle {
            font-size: 1rem;
        }
        
        .metric-card {
            padding: 1rem;
        }
        
        .language-selector {
            grid-template-columns: 1fr;
        }
        
        .camera-container {
            padding: 1rem;
        }
    }
    
    @media (max-width: 480px) {
        .main {
            padding: 0.5rem 1rem;
        }
        
        .header-container {
            padding: 1rem;
        }
        
        .main-title {
            font-size: 1.5rem;
        }
        
        .metric-value {
            font-size: 1.5rem;
        }
    }
    </style>
    """
