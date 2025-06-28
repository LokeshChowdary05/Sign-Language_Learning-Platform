"""
Configuration settings for the Sign Language Learning Platform
Contains language definitions, UI configuration, and application constants
"""

from typing import Dict, List, Any

# Supported Sign Languages with their metadata
SUPPORTED_LANGUAGES: Dict[str, Dict[str, Any]] = {
    "ASL": {
        "name": "American Sign Language",
        "country": "United States",
        "flag": "🇺🇸",
        "code": "asl",
        "region": "North America",
        "active_users": 500000,
        "difficulty": "Medium"
    },
    "BSL": {
        "name": "British Sign Language", 
        "country": "United Kingdom",
        "flag": "🇬🇧",
        "code": "bsl",
        "region": "Europe",
        "active_users": 150000,
        "difficulty": "Medium"
    },
    "LSP": {
        "name": "Portuguese Sign Language",
        "country": "Portugal",
        "flag": "🇵🇹",
        "code": "lsp",
        "region": "Europe",
        "active_users": 60000,
        "difficulty": "Medium"
    },
    "LSE": {
        "name": "Spanish Sign Language",
        "country": "Spain", 
        "flag": "🇪🇸",
        "code": "lse",
        "region": "Europe",
        "active_users": 120000,
        "difficulty": "Medium"
    },
    "DGS": {
        "name": "German Sign Language",
        "country": "Germany",
        "flag": "🇩🇪", 
        "code": "dgs",
        "region": "Europe",
        "active_users": 80000,
        "difficulty": "Hard"
    },
    "LSF": {
        "name": "French Sign Language",
        "country": "France",
        "flag": "🇫🇷",
        "code": "lsf", 
        "region": "Europe",
        "active_users": 100000,
        "difficulty": "Medium"
    },
    "JSL": {
        "name": "Japanese Sign Language",
        "country": "Japan",
        "flag": "🇯🇵",
        "code": "jsl",
        "region": "Asia",
        "active_users": 320000,
        "difficulty": "Hard"
    },
    "CSL": {
        "name": "Chinese Sign Language",
        "country": "China",
        "flag": "🇨🇳",
        "code": "csl",
        "region": "Asia", 
        "active_users": 20000000,
        "difficulty": "Hard"
    },
    "AUSLAN": {
        "name": "Australian Sign Language",
        "country": "Australia",
        "flag": "🇦🇺",
        "code": "auslan",
        "region": "Oceania",
        "active_users": 16000,
        "difficulty": "Medium"
    },
    "NZSL": {
        "name": "New Zealand Sign Language", 
        "country": "New Zealand",
        "flag": "🇳🇿",
        "code": "nzsl",
        "region": "Oceania",
        "active_users": 24000,
        "difficulty": "Medium"
    },
    "ISL": {
        "name": "Italian Sign Language",
        "country": "Italy",
        "flag": "🇮🇹",
        "code": "isl",
        "region": "Europe",
        "active_users": 40000,
        "difficulty": "Medium"
    },
    "RSL": {
        "name": "Russian Sign Language",
        "country": "Russia",
        "flag": "🇷🇺",
        "code": "rsl", 
        "region": "Europe/Asia",
        "active_users": 120000,
        "difficulty": "Hard"
    },
    "LIBRAS": {
        "name": "Brazilian Sign Language",
        "country": "Brazil",
        "flag": "🇧🇷",
        "code": "libras",
        "region": "South America",
        "active_users": 5000000,
        "difficulty": "Medium"
    },
    "LSM": {
        "name": "Mexican Sign Language",
        "country": "Mexico",
        "flag": "🇲🇽",
        "code": "lsm",
        "region": "North America",
        "active_users": 100000,
        "difficulty": "Medium"
    },
    "ISN": {
        "name": "Nicaraguan Sign Language",
        "country": "Nicaragua",
        "flag": "🇳🇮",
        "code": "isn",
        "region": "Central America",
        "active_users": 3000,
        "difficulty": "Hard"
    },
    "VGT": {
        "name": "Flemish Sign Language",
        "country": "Belgium",
        "flag": "🇧🇪",
        "code": "vgt",
        "region": "Europe",
        "active_users": 5000,
        "difficulty": "Medium"
    },
    "SSL": {
        "name": "Swedish Sign Language",
        "country": "Sweden",
        "flag": "🇸🇪",
        "code": "ssl",
        "region": "Europe",
        "active_users": 8000,
        "difficulty": "Medium"
    },
    "NSL": {
        "name": "Norwegian Sign Language",
        "country": "Norway",
        "flag": "🇳🇴",
        "code": "nsl",
        "region": "Europe", 
        "active_users": 5000,
        "difficulty": "Medium"
    },
    "DSL": {
        "name": "Danish Sign Language",
        "country": "Denmark",
        "flag": "🇩🇰",
        "code": "dsl",
        "region": "Europe",
        "active_users": 4000,
        "difficulty": "Medium"
    },
    "FSL": {
        "name": "Finnish Sign Language",
        "country": "Finland",
        "flag": "🇫🇮",
        "code": "fsl",
        "region": "Europe",
        "active_users": 5000,
        "difficulty": "Medium"
    },
    "KSL": {
        "name": "Korean Sign Language",
        "country": "South Korea",
        "flag": "🇰🇷",
        "code": "ksl",
        "region": "Asia",
        "active_users": 300000,
        "difficulty": "Hard"
    }
}

# UI Configuration
UI_CONFIG = {
    "theme": {
        "primary_color": "#2E8B57",  # Sea Green
        "secondary_color": "#4682B4",  # Steel Blue
        "accent_color": "#FF6347",  # Tomato
        "background_color": "#F8F9FA",  # Light Gray
        "text_color": "#2C3E50",  # Dark Blue Gray
        "success_color": "#28A745",  # Green
        "warning_color": "#FFC107",  # Amber
        "error_color": "#DC3545",  # Red
        "info_color": "#17A2B8"  # Cyan
    },
    "fonts": {
        "primary": "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
        "secondary": "'Arial', sans-serif",
        "monospace": "'Courier New', monospace"
    },
    "layout": {
        "sidebar_width": 280,
        "content_padding": 20,
        "border_radius": 8,
        "box_shadow": "0 2px 4px rgba(0,0,0,0.1)"
    },
    "animations": {
        "transition_speed": "0.3s",
        "hover_scale": 1.05,
        "fade_duration": "0.5s"
    }
}

# Model Configuration
MODEL_CONFIG = {
    "hand_tracking": {
        "model_complexity": 1,
        "min_detection_confidence": 0.5,
        "min_tracking_confidence": 0.5,
        "max_num_hands": 2
    },
    "sign_recognition": {
        "model_name": "MobileNetV3",
        "input_shape": (224, 224, 3),
        "num_classes": 1000,  # Will be updated based on selected language
        "confidence_threshold": 0.6,
        "batch_size": 32
    },
    "preprocessing": {
        "image_size": (224, 224),
        "normalization_mean": [0.485, 0.456, 0.406],
        "normalization_std": [0.229, 0.224, 0.225]
    }
}

# Learning Configuration
LEARNING_CONFIG = {
    "skill_levels": {
        "Beginner": {
            "required_accuracy": 70,
            "signs_to_complete": 50,
            "practice_time_hours": 10
        },
        "Intermediate": {
            "required_accuracy": 80,
            "signs_to_complete": 150, 
            "practice_time_hours": 30
        },
        "Advanced": {
            "required_accuracy": 90,
            "signs_to_complete": 300,
            "practice_time_hours": 60
        }
    },
    "daily_goals": {
        "signs_practice": 5,
        "accuracy_target": 85,
        "practice_minutes": 15,
        "streak_bonus": 10
    },
    "gamification": {
        "xp_per_sign": 10,
        "xp_per_accuracy_percent": 1,
        "daily_bonus": 50,
        "streak_multiplier": 1.5,
        "achievement_xp": 100
    }
}

# Camera Configuration
CAMERA_CONFIG = {
    "default_resolution": (1280, 720),
    "fps": 30,
    "buffer_size": 1,
    "flip_horizontal": True,
    "codec": "MJPG"
}

# Database Configuration
DATABASE_CONFIG = {
    "firebase": {
        "project_id": "sign-language-platform",
        "collections": {
            "users": "users",
            "progress": "user_progress",
            "lessons": "lessons",
            "signs": "sign_vocabulary",
            "feedback": "user_feedback"
        }
    }
}

# API Configuration
API_CONFIG = {
    "fastapi": {
        "host": "localhost",
        "port": 8000,
        "reload": True,
        "workers": 1
    },
    "endpoints": {
        "predict": "/api/v1/predict",
        "feedback": "/api/v1/feedback", 
        "progress": "/api/v1/progress",
        "translate": "/api/v1/translate"
    }
}

# File Paths
PATHS = {
    "models": "src/models/",
    "data": "data/",
    "assets": "assets/",
    "logs": "logs/",
    "temp": "temp/",
    "exports": "exports/"
}

# Logging Configuration
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "logs/app.log",
    "max_bytes": 10485760,  # 10MB
    "backup_count": 5
}

# Security Configuration
SECURITY_CONFIG = {
    "jwt_secret": "your-secret-key-here",  # Should be environment variable
    "jwt_algorithm": "HS256",
    "jwt_expiration_hours": 24,
    "bcrypt_rounds": 12,
    "max_login_attempts": 5,
    "lockout_duration_minutes": 30
}

# Feature Flags
FEATURE_FLAGS = {
    "real_time_feedback": True,
    "multi_language_support": True,
    "progress_analytics": True,
    "social_features": False,
    "advanced_statistics": True,
    "export_data": True,
    "offline_mode": False
}
