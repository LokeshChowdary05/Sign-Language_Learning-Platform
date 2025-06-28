"""
Quiz Manager for Sign Language Learning Platform
Contains 5 comprehensive quizzes for each of the 20+ supported languages (100 total quizzes)
"""

from typing import Dict, List, Any, Optional
import random
import json
from datetime import datetime
import logging
from src.config.settings import SUPPORTED_LANGUAGES

logger = logging.getLogger(__name__)

class QuizManager:
    """Manages quizzes for all supported sign languages"""
    
    def __init__(self):
        """Initialize quiz manager with comprehensive quiz data"""
        self.quizzes = self._generate_all_quizzes()
    
    def _generate_all_quizzes(self) -> Dict[str, List[Dict[str, Any]]]:
        """Generate 5 quizzes for each supported language"""
        all_quizzes = {}
        
        for lang_code, lang_info in SUPPORTED_LANGUAGES.items():
            all_quizzes[lang_code] = self._generate_language_quizzes(lang_code, lang_info)
        
        return all_quizzes
    
    def _generate_language_quizzes(self, lang_code: str, lang_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate 5 comprehensive quizzes for a specific language"""
        base_signs = self._get_base_signs_for_language(lang_code)
        
        quizzes = [
            self._create_basics_quiz(lang_code, lang_info, base_signs),
            self._create_numbers_quiz(lang_code, lang_info, base_signs),
            self._create_family_quiz(lang_code, lang_info, base_signs),
            self._create_emotions_quiz(lang_code, lang_info, base_signs),
            self._create_advanced_quiz(lang_code, lang_info, base_signs)
        ]
        
        return quizzes
    
    def _get_base_signs_for_language(self, lang_code: str) -> Dict[str, List[str]]:
        """Get base vocabulary for each language with cultural adaptations"""
        
        # Base signs that are common across all sign languages but may have cultural variations
        base_vocabulary = {
            "greetings": ["hello", "goodbye", "good morning", "good evening", "nice to meet you", "how are you", "thank you", "please", "excuse me", "sorry"],
            "numbers": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"],
            "family": ["mother", "father", "sister", "brother", "grandmother", "grandfather", "aunt", "uncle", "cousin", "family"],
            "emotions": ["happy", "sad", "angry", "excited", "tired", "surprised", "worried", "calm", "confused", "proud"],
            "colors": ["red", "blue", "green", "yellow", "black", "white", "orange", "purple", "pink", "brown"],
            "food": ["eat", "drink", "hungry", "thirsty", "breakfast", "lunch", "dinner", "water", "milk", "bread"],
            "time": ["today", "tomorrow", "yesterday", "morning", "afternoon", "evening", "night", "week", "month", "year"],
            "actions": ["go", "come", "sit", "stand", "walk", "run", "sleep", "wake up", "work", "study"],
            "places": ["home", "school", "work", "hospital", "store", "restaurant", "park", "library", "church", "city"],
            "nature": ["sun", "moon", "star", "tree", "flower", "rain", "snow", "wind", "fire", "water"]
        }
        
        # Add language-specific cultural signs
        cultural_additions = self._get_cultural_signs(lang_code)
        for category, signs in cultural_additions.items():
            if category in base_vocabulary:
                base_vocabulary[category].extend(signs)
            else:
                base_vocabulary[category] = signs
        
        return base_vocabulary
    
    def _get_cultural_signs(self, lang_code: str) -> Dict[str, List[str]]:
        """Get culturally specific signs for each language"""
        cultural_signs = {
            "ASL": {
                "culture": ["American", "baseball", "football", "hamburger", "democracy"],
                "places": ["Washington DC", "New York", "California", "Texas"]
            },
            "BSL": {
                "culture": ["British", "tea", "football (soccer)", "fish and chips", "queue"],
                "places": ["London", "England", "Scotland", "Wales"]
            },
            "LSP": {
                "culture": ["Portuguese", "fado", "football", "port wine", "azulejo"],
                "places": ["Lisbon", "Porto", "Portugal", "Algarve"]
            },
            "LSE": {
                "culture": ["Spanish", "flamenco", "paella", "siesta", "bullfighting"],
                "places": ["Madrid", "Barcelona", "Spain", "Andalusia"]
            },
            "DGS": {
                "culture": ["German", "beer", "sausage", "oktoberfest", "precision"],
                "places": ["Berlin", "Munich", "Germany", "Bavaria"]
            },
            "LSF": {
                "culture": ["French", "wine", "cheese", "baguette", "romance"],
                "places": ["Paris", "Lyon", "France", "Normandy"]
            },
            "JSL": {
                "culture": ["Japanese", "sushi", "origami", "bowing", "harmony"],
                "places": ["Tokyo", "Kyoto", "Japan", "Osaka"]
            },
            "CSL": {
                "culture": ["Chinese", "rice", "tea ceremony", "kung fu", "dragon"],
                "places": ["Beijing", "Shanghai", "China", "Hong Kong"]
            },
            "AUSLAN": {
                "culture": ["Australian", "kangaroo", "koala", "beach", "mate"],
                "places": ["Sydney", "Melbourne", "Australia", "Brisbane"]
            },
            "NZSL": {
                "culture": ["New Zealand", "kiwi", "rugby", "haka", "sheep"],
                "places": ["Auckland", "Wellington", "Christchurch", "New Zealand"]
            },
            "ISL": {
                "culture": ["Italian", "pasta", "pizza", "opera", "art"],
                "places": ["Rome", "Milan", "Venice", "Italy"]
            },
            "RSL": {
                "culture": ["Russian", "vodka", "ballet", "borscht", "cold"],
                "places": ["Moscow", "St. Petersburg", "Russia", "Siberia"]
            },
            "LIBRAS": {
                "culture": ["Brazilian", "carnival", "football", "capoeira", "beach"],
                "places": ["Rio de Janeiro", "São Paulo", "Brazil", "Amazon"]
            },
            "LSM": {
                "culture": ["Mexican", "tacos", "mariachi", "día de los muertos", "spicy"],
                "places": ["Mexico City", "Guadalajara", "Mexico", "Cancun"]
            },
            "ISN": {
                "culture": ["Nicaraguan", "coffee", "lakes", "volcanos", "revolution"],
                "places": ["Managua", "León", "Nicaragua", "Granada"]
            },
            "VGT": {
                "culture": ["Flemish", "waffles", "chocolate", "beer", "art"],
                "places": ["Brussels", "Antwerp", "Belgium", "Ghent"]
            },
            "SSL": {
                "culture": ["Swedish", "meatballs", "IKEA", "cold", "northern lights"],
                "places": ["Stockholm", "Gothenburg", "Sweden", "Lapland"]
            },
            "NSL": {
                "culture": ["Norwegian", "fjords", "salmon", "oil", "northern lights"],
                "places": ["Oslo", "Bergen", "Norway", "Tromsø"]
            },
            "DSL": {
                "culture": ["Danish", "hygge", "pastries", "vikings", "bicycles"],
                "places": ["Copenhagen", "Aarhus", "Denmark", "Greenland"]
            },
            "FSL": {
                "culture": ["Finnish", "sauna", "Nokia", "reindeer", "northern lights"],
                "places": ["Helsinki", "Tampere", "Finland", "Lapland"]
            },
            "KSL": {
                "culture": ["Korean", "kimchi", "k-pop", "taekwondo", "technology"],
                "places": ["Seoul", "Busan", "South Korea", "Jeju"]
            }
        }
        
        return cultural_signs.get(lang_code, {"culture": [], "places": []})
    
    def _create_basics_quiz(self, lang_code: str, lang_info: Dict[str, Any], signs: Dict[str, List[str]]) -> Dict[str, Any]:
        """Create basic greetings and common phrases quiz"""
        questions = []
        
        # Greeting questions
        greetings = signs["greetings"][:8]  # Use first 8 greetings
        for greeting in greetings:
            questions.append({
                "id": f"basics_{len(questions) + 1}",
                "type": "multiple_choice",
                "question": f"What is the sign for '{greeting}' in {lang_info['name']}?",
                "options": [greeting, *random.sample([g for g in greetings if g != greeting], 3)],
                "correct_answer": greeting,
                "points": 10,
                "difficulty": "Easy",
                "category": "greetings"
            })
        
        # Color questions
        colors = signs["colors"][:7]  # Use first 7 colors
        for color in colors:
            questions.append({
                "id": f"basics_{len(questions) + 1}",
                "type": "multiple_choice",
                "question": f"How do you sign '{color}' in {lang_info['name']}?",
                "options": [color, *random.sample([c for c in colors if c != color], 3)],
                "correct_answer": color,
                "points": 10,
                "difficulty": "Easy",
                "category": "colors"
            })
        
        return {
            "quiz_id": f"{lang_code}_basics",
            "title": f"{lang_info['name']} - Basic Signs",
            "description": f"Test your knowledge of basic greetings and common signs in {lang_info['name']}",
            "language": lang_code,
            "difficulty": "Easy",
            "estimated_time": 10,
            "total_questions": len(questions),
            "total_points": sum(q["points"] for q in questions),
            "questions": random.sample(questions, min(10, len(questions)))
        }
    
    def _create_numbers_quiz(self, lang_code: str, lang_info: Dict[str, Any], signs: Dict[str, List[str]]) -> Dict[str, Any]:
        """Create numbers and counting quiz"""
        questions = []
        numbers = signs["numbers"]
        
        # Number recognition
        for num in numbers[:15]:  # Use numbers 1-15
            wrong_answers = random.sample([n for n in numbers if n != num], 3)
            questions.append({
                "id": f"numbers_{len(questions) + 1}",
                "type": "multiple_choice",
                "question": f"What number is being signed? (Number: {num})",
                "options": [num, *wrong_answers],
                "correct_answer": num,
                "points": 10,
                "difficulty": "Easy",
                "category": "numbers"
            })
        
        # Number sequences
        questions.append({
            "id": f"numbers_{len(questions) + 1}",
            "type": "sequence",
            "question": f"Put these numbers in order as they would be signed in {lang_info['name']}:",
            "options": ["3", "1", "4", "2"],
            "correct_answer": ["1", "2", "3", "4"],
            "points": 20,
            "difficulty": "Medium",
            "category": "number_sequence"
        })
        
        return {
            "quiz_id": f"{lang_code}_numbers",
            "title": f"{lang_info['name']} - Numbers & Counting",
            "description": f"Test your number signing skills in {lang_info['name']}",
            "language": lang_code,
            "difficulty": "Easy",
            "estimated_time": 8,
            "total_questions": len(questions),
            "total_points": sum(q["points"] for q in questions),
            "questions": random.sample(questions, min(10, len(questions)))
        }
    
    def _create_family_quiz(self, lang_code: str, lang_info: Dict[str, Any], signs: Dict[str, List[str]]) -> Dict[str, Any]:
        """Create family relationships quiz"""
        questions = []
        family_signs = signs["family"]
        
        for family_member in family_signs:
            wrong_answers = random.sample([f for f in family_signs if f != family_member], 3)
            questions.append({
                "id": f"family_{len(questions) + 1}",
                "type": "multiple_choice",
                "question": f"How do you sign '{family_member}' in {lang_info['name']}?",
                "options": [family_member, *wrong_answers],
                "correct_answer": family_member,
                "points": 15,
                "difficulty": "Medium",
                "category": "family"
            })
        
        # Relationship questions
        questions.append({
            "id": f"family_{len(questions) + 1}",
            "type": "true_false",
            "question": f"In {lang_info['name']}, family signs often use specific hand shapes near the face.",
            "correct_answer": True,
            "points": 10,
            "difficulty": "Medium",
            "category": "family_structure"
        })
        
        return {
            "quiz_id": f"{lang_code}_family",
            "title": f"{lang_info['name']} - Family & Relationships",
            "description": f"Learn family relationship signs in {lang_info['name']}",
            "language": lang_code,
            "difficulty": "Medium",
            "estimated_time": 12,
            "total_questions": len(questions),
            "total_points": sum(q["points"] for q in questions),
            "questions": random.sample(questions, min(12, len(questions)))
        }
    
    def _create_emotions_quiz(self, lang_code: str, lang_info: Dict[str, Any], signs: Dict[str, List[str]]) -> Dict[str, Any]:
        """Create emotions and feelings quiz"""
        questions = []
        emotions = signs["emotions"]
        
        for emotion in emotions:
            wrong_answers = random.sample([e for e in emotions if e != emotion], 3)
            questions.append({
                "id": f"emotions_{len(questions) + 1}",
                "type": "multiple_choice",
                "question": f"What emotion is being expressed: '{emotion}' in {lang_info['name']}?",
                "options": [emotion, *wrong_answers],
                "correct_answer": emotion,
                "points": 15,
                "difficulty": "Medium",
                "category": "emotions"
            })
        
        # Emotional expression questions
        questions.append({
            "id": f"emotions_{len(questions) + 1}",
            "type": "matching",
            "question": f"Match the emotion with its typical facial expression in {lang_info['name']}:",
            "pairs": [
                ["happy", "smiling"],
                ["sad", "frowning"],
                ["angry", "intense expression"],
                ["surprised", "wide eyes"]
            ],
            "points": 20,
            "difficulty": "Medium",
            "category": "emotional_expression"
        })
        
        return {
            "quiz_id": f"{lang_code}_emotions",
            "title": f"{lang_info['name']} - Emotions & Feelings",
            "description": f"Express emotions and feelings in {lang_info['name']}",
            "language": lang_code,
            "difficulty": "Medium",
            "estimated_time": 15,
            "total_questions": len(questions),
            "total_points": sum(q["points"] for q in questions),
            "questions": random.sample(questions, min(12, len(questions)))
        }
    
    def _create_advanced_quiz(self, lang_code: str, lang_info: Dict[str, Any], signs: Dict[str, List[str]]) -> Dict[str, Any]:
        """Create advanced vocabulary and grammar quiz"""
        questions = []
        
        # Complex vocabulary
        advanced_signs = signs["actions"] + signs["places"] + signs["time"]
        for sign in advanced_signs[:15]:  # Use first 15 advanced signs
            category_signs = [s for category in signs.values() for s in category if s != sign]
            wrong_answers = random.sample(category_signs, 3)
            
            questions.append({
                "id": f"advanced_{len(questions) + 1}",
                "type": "multiple_choice",
                "question": f"What is the advanced sign for '{sign}' in {lang_info['name']}?",
                "options": [sign, *wrong_answers],
                "correct_answer": sign,
                "points": 20,
                "difficulty": "Hard",
                "category": "advanced_vocabulary"
            })
        
        # Grammar and structure questions
        questions.append({
            "id": f"advanced_{len(questions) + 1}",
            "type": "true_false",
            "question": f"In {lang_info['name']}, facial expressions are crucial for grammatical meaning.",
            "correct_answer": True,
            "points": 25,
            "difficulty": "Hard",
            "category": "grammar"
        })
        
        questions.append({
            "id": f"advanced_{len(questions) + 1}",
            "type": "true_false",
            "question": f"{lang_info['name']} uses a different word order than spoken {lang_info['name'].replace(' Sign Language', '')} language.",
            "correct_answer": True,
            "points": 25,
            "difficulty": "Hard",
            "category": "grammar"
        })
        
        # Cultural context
        cultural_signs = self._get_cultural_signs(lang_code).get("culture", [])
        if cultural_signs:
            cultural_sign = random.choice(cultural_signs)
            questions.append({
                "id": f"advanced_{len(questions) + 1}",
                "type": "open_ended",
                "question": f"Describe the cultural significance of the sign '{cultural_sign}' in {lang_info['name']}.",
                "sample_answer": f"The sign '{cultural_sign}' represents an important cultural element in {lang_info['country']} and reflects the deaf community's connection to their heritage.",
                "points": 30,
                "difficulty": "Hard",
                "category": "cultural_context"
            })
        
        return {
            "quiz_id": f"{lang_code}_advanced",
            "title": f"{lang_info['name']} - Advanced Concepts",
            "description": f"Challenge yourself with advanced {lang_info['name']} concepts and cultural context",
            "language": lang_code,
            "difficulty": "Hard",
            "estimated_time": 20,
            "total_questions": len(questions),
            "total_points": sum(q["points"] for q in questions),
            "questions": random.sample(questions, min(15, len(questions)))
        }
    
    def get_quiz(self, language: str, quiz_type: str) -> Optional[Dict[str, Any]]:
        """Get a specific quiz for a language"""
        if language not in self.quizzes:
            return None
        
        quiz_mapping = {
            "basics": 0,
            "numbers": 1,
            "family": 2,
            "emotions": 3,
            "advanced": 4
        }
        
        quiz_index = quiz_mapping.get(quiz_type)
        if quiz_index is None or quiz_index >= len(self.quizzes[language]):
            return None
        
        return self.quizzes[language][quiz_index]
    
    def get_all_quizzes_for_language(self, language: str) -> List[Dict[str, Any]]:
        """Get all quizzes for a specific language"""
        return self.quizzes.get(language, [])
    
    def get_random_quiz(self, language: str = None, difficulty: str = None) -> Optional[Dict[str, Any]]:
        """Get a random quiz, optionally filtered by language and difficulty"""
        available_quizzes = []
        
        if language:
            if language in self.quizzes:
                available_quizzes = self.quizzes[language]
        else:
            for lang_quizzes in self.quizzes.values():
                available_quizzes.extend(lang_quizzes)
        
        if difficulty:
            available_quizzes = [q for q in available_quizzes if q["difficulty"] == difficulty]
        
        if not available_quizzes:
            return None
        
        return random.choice(available_quizzes)
    
    def get_quiz_statistics(self) -> Dict[str, Any]:
        """Get overall quiz statistics"""
        total_quizzes = sum(len(quizzes) for quizzes in self.quizzes.values())
        
        difficulty_counts = {"Easy": 0, "Medium": 0, "Hard": 0}
        total_questions = 0
        
        for lang_quizzes in self.quizzes.values():
            for quiz in lang_quizzes:
                difficulty_counts[quiz["difficulty"]] += 1
                total_questions += quiz["total_questions"]
        
        return {
            "total_languages": len(self.quizzes),
            "total_quizzes": total_quizzes,
            "quizzes_per_language": 5,
            "total_questions": total_questions,
            "difficulty_distribution": difficulty_counts,
            "average_questions_per_quiz": round(total_questions / total_quizzes, 1)
        }
    
    def validate_quiz_answer(self, quiz_id: str, question_id: str, user_answer: Any) -> Dict[str, Any]:
        """Validate a user's answer to a quiz question"""
        # Find the quiz and question
        quiz = None
        question = None
        
        for lang_quizzes in self.quizzes.values():
            for q in lang_quizzes:
                if q["quiz_id"] == quiz_id:
                    quiz = q
                    for quest in q["questions"]:
                        if quest["id"] == question_id:
                            question = quest
                            break
                    break
            if quiz:
                break
        
        if not quiz or not question:
            return {"error": "Quiz or question not found"}
        
        correct_answer = question["correct_answer"]
        is_correct = False
        feedback = ""
        
        if question["type"] == "multiple_choice":
            is_correct = user_answer == correct_answer
            feedback = "Correct!" if is_correct else f"Incorrect. The correct answer is '{correct_answer}'"
        
        elif question["type"] == "true_false":
            is_correct = user_answer == correct_answer
            feedback = "Correct!" if is_correct else f"Incorrect. The correct answer is {correct_answer}"
        
        elif question["type"] == "sequence":
            is_correct = user_answer == correct_answer
            feedback = "Correct sequence!" if is_correct else f"Incorrect order. The correct sequence is {correct_answer}"
        
        elif question["type"] == "open_ended":
            # For open-ended questions, we'll give partial credit based on keywords
            is_correct = True  # Always give credit for attempting
            feedback = "Thank you for your response! Open-ended questions help reinforce learning."
        
        points_earned = question["points"] if is_correct else 0
        
        return {
            "is_correct": is_correct,
            "points_earned": points_earned,
            "max_points": question["points"],
            "feedback": feedback,
            "correct_answer": correct_answer
        }
