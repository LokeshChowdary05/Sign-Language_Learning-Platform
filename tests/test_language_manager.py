"""
Unit tests for the LanguageManager module
"""

import pytest
from src.core.language_manager import LanguageManager

class TestLanguageManager:
    """Test cases for LanguageManager class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.manager = LanguageManager()
    
    def test_get_all_languages(self):
        """Test getting all supported languages"""
        languages = self.manager.get_all_languages()
        
        assert isinstance(languages, dict)
        assert len(languages) >= 20  # Should have 20+ languages
        assert 'ASL' in languages
        assert 'BSL' in languages
        assert 'LSP' in languages
    
    def test_get_language_details_valid(self):
        """Test getting details for a valid language"""
        details = self.manager.get_language_details('ASL')
        
        assert isinstance(details, dict)
        assert details['name'] == 'American Sign Language'
        assert details['country'] == 'United States'
        assert details['flag'] == '🇺🇸'
        assert details['code'] == 'asl'
    
    def test_get_language_details_invalid(self):
        """Test getting details for an invalid language"""
        details = self.manager.get_language_details('INVALID')
        
        assert details == {}
    
    def test_language_exists_valid(self):
        """Test checking existence of valid language"""
        assert self.manager.language_exists('ASL') is True
        assert self.manager.language_exists('BSL') is True
        assert self.manager.language_exists('LSP') is True
    
    def test_language_exists_invalid(self):
        """Test checking existence of invalid language"""
        assert self.manager.language_exists('INVALID') is False
        assert self.manager.language_exists('') is False
        assert self.manager.language_exists('XYZ') is False
    
    def test_language_exists_case_insensitive(self):
        """Test case insensitive language checking"""
        assert self.manager.language_exists('asl') is True
        assert self.manager.language_exists('bsl') is True
        assert self.manager.language_exists('lsp') is True

if __name__ == "__main__":
    pytest.main([__file__])
