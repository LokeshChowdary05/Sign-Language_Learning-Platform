import random
from typing import Dict, List, Any

class QuizDatabase:
    """
    Comprehensive quiz database for multiple sign languages.
    Organized by language and modules with various difficulty levels.
    """
    
    def __init__(self):
        self.quiz_data = {
            "ASL": {
                "Basics": [
                    {"sign": "Hello", "difficulty": 1, "category": "greetings"},
                    {"sign": "Thank You", "difficulty": 1, "category": "greetings"},
                    {"sign": "Please", "difficulty": 1, "category": "greetings"},
                    {"sign": "Sorry", "difficulty": 1, "category": "greetings"},
                    {"sign": "Yes", "difficulty": 1, "category": "responses"},
                    {"sign": "No", "difficulty": 1, "category": "responses"},
                    {"sign": "Good Morning", "difficulty": 2, "category": "greetings"},
                    {"sign": "Good Night", "difficulty": 2, "category": "greetings"},
                    {"sign": "How are you", "difficulty": 2, "category": "questions"},
                    {"sign": "Fine", "difficulty": 1, "category": "responses"}
                ],
                "Numbers": [
                    {"sign": "One", "difficulty": 1, "category": "numbers"},
                    {"sign": "Two", "difficulty": 1, "category": "numbers"},
                    {"sign": "Three", "difficulty": 1, "category": "numbers"},
                    {"sign": "Four", "difficulty": 1, "category": "numbers"},
                    {"sign": "Five", "difficulty": 1, "category": "numbers"},
                    {"sign": "Six", "difficulty": 2, "category": "numbers"},
                    {"sign": "Seven", "difficulty": 2, "category": "numbers"},
                    {"sign": "Eight", "difficulty": 2, "category": "numbers"},
                    {"sign": "Nine", "difficulty": 2, "category": "numbers"},
                    {"sign": "Ten", "difficulty": 2, "category": "numbers"}
                ],
                "Colors": [
                    {"sign": "Red", "difficulty": 1, "category": "colors"},
                    {"sign": "Blue", "difficulty": 1, "category": "colors"},
                    {"sign": "Green", "difficulty": 1, "category": "colors"},
                    {"sign": "Yellow", "difficulty": 1, "category": "colors"},
                    {"sign": "Black", "difficulty": 2, "category": "colors"},
                    {"sign": "White", "difficulty": 2, "category": "colors"},
                    {"sign": "Orange", "difficulty": 2, "category": "colors"},
                    {"sign": "Purple", "difficulty": 2, "category": "colors"},
                    {"sign": "Pink", "difficulty": 3, "category": "colors"},
                    {"sign": "Brown", "difficulty": 3, "category": "colors"}
                ],
                "Family": [
                    {"sign": "Mother", "difficulty": 1, "category": "family"},
                    {"sign": "Father", "difficulty": 1, "category": "family"},
                    {"sign": "Sister", "difficulty": 2, "category": "family"},
                    {"sign": "Brother", "difficulty": 2, "category": "family"},
                    {"sign": "Family", "difficulty": 2, "category": "family"},
                    {"sign": "Grandmother", "difficulty": 3, "category": "family"},
                    {"sign": "Grandfather", "difficulty": 3, "category": "family"},
                    {"sign": "Aunt", "difficulty": 3, "category": "family"},
                    {"sign": "Uncle", "difficulty": 3, "category": "family"},
                    {"sign": "Cousin", "difficulty": 3, "category": "family"}
                ],
                "Animals": [
                    {"sign": "Cat", "difficulty": 1, "category": "animals"},
                    {"sign": "Dog", "difficulty": 1, "category": "animals"},
                    {"sign": "Bird", "difficulty": 2, "category": "animals"},
                    {"sign": "Fish", "difficulty": 2, "category": "animals"},
                    {"sign": "Horse", "difficulty": 2, "category": "animals"},
                    {"sign": "Elephant", "difficulty": 3, "category": "animals"},
                    {"sign": "Lion", "difficulty": 3, "category": "animals"},
                    {"sign": "Monkey", "difficulty": 3, "category": "animals"},
                    {"sign": "Tiger", "difficulty": 3, "category": "animals"},
                    {"sign": "Bear", "difficulty": 3, "category": "animals"}
                ]
            },
            "BSL": {
                "Basics": [
                    {"sign": "Hello", "difficulty": 1, "category": "greetings"},
                    {"sign": "Goodbye", "difficulty": 1, "category": "greetings"},
                    {"sign": "Please", "difficulty": 1, "category": "greetings"},
                    {"sign": "Thank You", "difficulty": 1, "category": "greetings"},
                    {"sign": "Yes", "difficulty": 1, "category": "responses"},
                    {"sign": "No", "difficulty": 1, "category": "responses"},
                    {"sign": "Sorry", "difficulty": 2, "category": "greetings"},
                    {"sign": "Excuse Me", "difficulty": 2, "category": "greetings"},
                    {"sign": "Nice to Meet You", "difficulty": 3, "category": "greetings"},
                    {"sign": "How are you", "difficulty": 2, "category": "questions"}
                ],
                "Numbers": [
                    {"sign": "One", "difficulty": 1, "category": "numbers"},
                    {"sign": "Two", "difficulty": 1, "category": "numbers"},
                    {"sign": "Three", "difficulty": 1, "category": "numbers"},
                    {"sign": "Four", "difficulty": 1, "category": "numbers"},
                    {"sign": "Five", "difficulty": 1, "category": "numbers"},
                    {"sign": "Six", "difficulty": 2, "category": "numbers"},
                    {"sign": "Seven", "difficulty": 2, "category": "numbers"},
                    {"sign": "Eight", "difficulty": 2, "category": "numbers"},
                    {"sign": "Nine", "difficulty": 2, "category": "numbers"},
                    {"sign": "Ten", "difficulty": 2, "category": "numbers"}
                ]
            },
            "FSL": {
                "Basics": [
                    {"sign": "Bonjour", "difficulty": 1, "category": "greetings"},
                    {"sign": "Merci", "difficulty": 1, "category": "greetings"},
                    {"sign": "S'il vous plait", "difficulty": 2, "category": "greetings"},
                    {"sign": "Au revoir", "difficulty": 1, "category": "greetings"},
                    {"sign": "Oui", "difficulty": 1, "category": "responses"},
                    {"sign": "Non", "difficulty": 1, "category": "responses"},
                    {"sign": "Pardon", "difficulty": 2, "category": "greetings"},
                    {"sign": "Bonsoir", "difficulty": 2, "category": "greetings"},
                    {"sign": "Comment allez-vous", "difficulty": 3, "category": "questions"},
                    {"sign": "Ca va bien", "difficulty": 2, "category": "responses"}
                ]
            }
        }
        
        self.daily_challenges = [
            {"type": "speed", "signs": ["Hello", "Thank You", "Please", "Sorry"], "time_limit": 30},
            {"type": "sequence", "signs": ["One", "Two", "Three", "Four", "Five"], "time_limit": 45},
            {"type": "scramble", "signs": ["Red", "Blue", "Green", "Yellow"], "time_limit": 60},
            {"type": "rapid_fire", "signs": ["Yes", "No", "Hello", "Goodbye"], "time_limit": 20},
            {"type": "pattern", "signs": ["Cat", "Dog", "Bird", "Fish"], "time_limit": 40}
        ]
    
    def get_available_languages(self) -> List[str]:
        """Get list of available sign languages."""
        return list(self.quiz_data.keys())
    
    def get_modules_for_language(self, language: str) -> List[str]:
        """Get available modules for a specific language."""
        return list(self.quiz_data.get(language, {}).keys())
    
    def get_quiz_questions(self, language: str, module: str, num_questions: int = 10) -> List[Dict[str, Any]]:
        """Get quiz questions for specified language and module."""
        if language not in self.quiz_data or module not in self.quiz_data[language]:
            return []
        
        all_questions = self.quiz_data[language][module]
        
        # If requesting more questions than available, return all
        if num_questions >= len(all_questions):
            return random.sample(all_questions, len(all_questions))
        
        return random.sample(all_questions, num_questions)
    
    def get_practice_questions(self, language: str, difficulty: int = None) -> List[Dict[str, Any]]:
        """Get practice questions, optionally filtered by difficulty."""
        if language not in self.quiz_data:
            return []
        
        all_questions = []
        for module in self.quiz_data[language].values():
            all_questions.extend(module)
        
        if difficulty is not None:
            all_questions = [q for q in all_questions if q["difficulty"] == difficulty]
        
        return random.sample(all_questions, min(20, len(all_questions)))
    
    def get_daily_challenge(self) -> Dict[str, Any]:
        """Get a random daily challenge."""
        return random.choice(self.daily_challenges)
    
    def get_signs_by_category(self, language: str, category: str) -> List[Dict[str, Any]]:
        """Get all signs of a specific category."""
        if language not in self.quiz_data:
            return []
        
        signs = []
        for module in self.quiz_data[language].values():
            signs.extend([q for q in module if q["category"] == category])
        
        return signs
    
    def search_signs(self, language: str, search_term: str) -> List[Dict[str, Any]]:
        """Search for signs containing the search term."""
        if language not in self.quiz_data:
            return []
        
        results = []
        search_term = search_term.lower()
        
        for module in self.quiz_data[language].values():
            for question in module:
                if search_term in question["sign"].lower():
                    results.append(question)
        
        return results
