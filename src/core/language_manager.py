"""
Language Manager for Sign Language Learning Platform
Handles language selection, metadata, and multilingual support
"""

from typing import Dict, List, Optional, Any
import json
import logging

logger = logging.getLogger(__name__)

class LanguageManager:
    """Manages supported sign languages and their metadata"""
    
    def __init__(self):
        """Initialize the language manager with supported languages"""
        self.supported_languages = {
            "ASL": {
                "name": "American Sign Language",
                "flag": "🇺🇸",
                "region": "North America", 
                "difficulty": "Medium",
                "users": "500,000+",
                "description": "The primary sign language of deaf communities in the United States and Canada."
            },
            "BSL": {
                "name": "British Sign Language",
                "flag": "🇬🇧", 
                "region": "Europe",
                "difficulty": "Medium",
                "users": "150,000+",
                "description": "The sign language used in the United Kingdom and Northern Ireland."
            },
            "LSF": {
                "name": "French Sign Language",
                "flag": "🇫🇷",
                "region": "Europe", 
                "difficulty": "Medium",
                "users": "100,000+",
                "description": "The sign language of the deaf community in France."
            },
            "DGS": {
                "name": "German Sign Language",
                "flag": "🇩🇪",
                "region": "Europe",
                "difficulty": "Hard",
                "users": "80,000+", 
                "description": "The sign language of the deaf community in Germany."
            },
            "JSL": {
                "name": "Japanese Sign Language",
                "flag": "🇯🇵",
                "region": "Asia",
                "difficulty": "Hard",
                "users": "320,000+",
                "description": "The sign language of the deaf community in Japan."
            },
            "CSL": {
                "name": "Chinese Sign Language", 
                "flag": "🇨🇳",
                "region": "Asia",
                "difficulty": "Hard",
                "users": "20M+",
                "description": "The sign language used by the deaf community in China."
            },
            "LIBRAS": {
                "name": "Brazilian Sign Language",
                "flag": "🇧🇷", 
                "region": "South America",
                "difficulty": "Medium",
                "users": "5M+",
                "description": "The sign language of the deaf community in Brazil."
            },
            "LSE": {
                "name": "Spanish Sign Language",
                "flag": "🇪🇸",
                "region": "Europe",
                "difficulty": "Medium", 
                "users": "120,000+",
                "description": "The sign language used in Spain."
            },
            "LSP": {
                "name": "Portuguese Sign Language",
                "flag": "🇵🇹",
                "region": "Europe",
                "difficulty": "Medium",
                "users": "60,000+",
                "description": "The sign language of the deaf community in Portugal."
            },
            "AUSLAN": {
                "name": "Australian Sign Language",
                "flag": "🇦🇺",
                "region": "Oceania",
                "difficulty": "Medium",
                "users": "16,000+",
                "description": "The sign language of the Australian deaf community."
            },
            "ISL": {
                "name": "Indian Sign Language",
                "flag": "🇮🇳", 
                "region": "Asia",
                "difficulty": "Medium",
                "users": "2.7M+",
                "description": "The sign language used by the deaf community in India."
            },
            "RSL": {
                "name": "Russian Sign Language",
                "flag": "🇷🇺",
                "region": "Europe/Asia",
                "difficulty": "Hard",
                "users": "120,000+",
                "description": "The sign language of the deaf community in Russia."
            },
            "TSL": {
                "name": "Thai Sign Language",
                "flag": "🇹🇭",
                "region": "Asia", 
                "difficulty": "Medium",
                "users": "56,000+",
                "description": "The sign language used in Thailand."
            },
            "KSL": {
                "name": "Korean Sign Language",
                "flag": "🇰🇷",
                "region": "Asia",
                "difficulty": "Hard",
                "users": "300,000+",
                "description": "The sign language of the deaf community in South Korea."
            },
            "NZSL": {
                "name": "New Zealand Sign Language",
                "flag": "🇳🇿",
                "region": "Oceania",
                "difficulty": "Medium", 
                "users": "24,000+",
                "description": "The sign language of New Zealand's deaf community."
            },
            "SASL": {
                "name": "South African Sign Language",
                "flag": "🇿🇦",
                "region": "Africa",
                "difficulty": "Medium",
                "users": "600,000+",
                "description": "The sign language used in South Africa."
            },
            "FinSL": {
                "name": "Finnish Sign Language",
                "flag": "🇫🇮",
                "region": "Europe",
                "difficulty": "Hard",
                "users": "14,000+",
                "description": "The sign language of the Finnish deaf community."
            },
            "SSL": {
                "name": "Swedish Sign Language", 
                "flag": "🇸🇪",
                "region": "Europe",
                "difficulty": "Medium",
                "users": "35,000+",
                "description": "The sign language used in Sweden."
            },
            "DSL": {
                "name": "Danish Sign Language",
                "flag": "🇩🇰",
                "region": "Europe",
                "difficulty": "Medium",
                "users": "5,000+",
                "description": "The sign language of the Danish deaf community."
            },
            "NSL": {
                "name": "Norwegian Sign Language",
                "flag": "🇳🇴",
                "region": "Europe", 
                "difficulty": "Medium",
                "users": "5,000+",
                "description": "The sign language used in Norway."
            }
        }
        
        self.current_language = "ASL"
        
    def get_supported_languages(self) -> Dict[str, Dict[str, str]]:
        """Get all supported languages with metadata"""
        return self.supported_languages
    
    def get_language_info(self, language_code: str) -> Optional[Dict[str, str]]:
        """Get information about a specific language"""
        return self.supported_languages.get(language_code)
    
    def get_language_names(self) -> List[str]:
        """Get list of language names"""
        return [lang["name"] for lang in self.supported_languages.values()]
    
    def get_language_codes(self) -> List[str]:
        """Get list of language codes"""
        return list(self.supported_languages.keys())
    
    def set_current_language(self, language_code: str) -> bool:
        """Set the current active language"""
        if language_code in self.supported_languages:
            self.current_language = language_code
            logger.info(f"Language changed to: {language_code}")
            return True
        else:
            logger.warning(f"Unsupported language code: {language_code}")
            return False
    
    def get_current_language(self) -> str:
        """Get the current active language code"""
        return self.current_language
    
    def get_current_language_info(self) -> Dict[str, str]:
        """Get information about the current language"""
        return self.supported_languages[self.current_language]
