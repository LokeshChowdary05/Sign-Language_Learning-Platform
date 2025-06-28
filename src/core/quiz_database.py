"""
Comprehensive Quiz Database for Sign Language Learning Platform
Contains quiz questions for all supported languages and modules
"""

import random
from typing import Dict, List, Any

class QuizDatabase:
    """Database of quiz questions for all languages and modules"""
    
    def __init__(self):
        """Initialize quiz database with questions for all languages"""
        self.quiz_data = {
            "ASL": {
                "module_1": {
                    "title": "Basic Greetings & Common Signs",
                    "duration": 600,  # 10 minutes
                    "questions": [
                        {"sign": "hello", "description": "Basic greeting - wave your hand"},
                        {"sign": "thank_you", "description": "Show gratitude - touch chin and move forward"},
                        {"sign": "please", "description": "Polite request - flat hand on chest, circular motion"},
                        {"sign": "sorry", "description": "Apology - fist on chest, circular motion"},
                        {"sign": "yes", "description": "Affirmation - nod fist up and down"},
                        {"sign": "no", "description": "Negation - index and middle finger tap thumb"},
                        {"sign": "good_morning", "description": "Morning greeting - 'good' + 'morning'"},
                        {"sign": "good_night", "description": "Evening farewell - 'good' + 'night'"},
                        {"sign": "welcome", "description": "Greeting gesture - open arms welcoming"},
                        {"sign": "goodbye", "description": "Farewell - wave hand"},
                        {"sign": "nice", "description": "Pleasant - flat hand slide over other palm"},
                        {"sign": "help", "description": "Assistance - one hand supports the other"},
                        {"sign": "water", "description": "Drink - W handshape at mouth"},
                        {"sign": "food", "description": "Eating - fingers to mouth repeatedly"},
                        {"sign": "more", "description": "Additional - fingertips together, tap twice"}
                    ]
                },
                "module_2": {
                    "title": "Numbers 1-15",
                    "duration": 600,  # 10 minutes
                    "questions": [
                        {"sign": "one", "description": "Number 1 - index finger up"},
                        {"sign": "two", "description": "Number 2 - index and middle finger up"},
                        {"sign": "three", "description": "Number 3 - thumb, index, middle finger up"},
                        {"sign": "four", "description": "Number 4 - four fingers up, thumb tucked"},
                        {"sign": "five", "description": "Number 5 - all fingers spread open"},
                        {"sign": "six", "description": "Number 6 - thumb and pinky touch"},
                        {"sign": "seven", "description": "Number 7 - thumb and ring finger touch"},
                        {"sign": "eight", "description": "Number 8 - thumb and middle finger touch"},
                        {"sign": "nine", "description": "Number 9 - thumb and index finger touch"},
                        {"sign": "ten", "description": "Number 10 - thumb up, shake"},
                        {"sign": "eleven", "description": "Number 11 - flick index finger twice"},
                        {"sign": "twelve", "description": "Number 12 - flick index and middle finger"},
                        {"sign": "thirteen", "description": "Number 13 - flick index finger and wiggle"},
                        {"sign": "fourteen", "description": "Number 14 - flick index, middle, ring finger"},
                        {"sign": "fifteen", "description": "Number 15 - flick all fingers except thumb"}
                    ]
                },
                "module_3": {
                    "title": "Family & Relationships",
                    "duration": 600,  # 10 minutes
                    "questions": [
                        {"sign": "mother", "description": "Parent - thumb to chin"},
                        {"sign": "father", "description": "Parent - thumb to forehead"},
                        {"sign": "sister", "description": "Female sibling - L handshape to jaw, then index fingers"},
                        {"sign": "brother", "description": "Male sibling - L handshape to forehead, then index fingers"},
                        {"sign": "grandmother", "description": "Female grandparent - mother sign moved forward"},
                        {"sign": "grandfather", "description": "Male grandparent - father sign moved forward"},
                        {"sign": "aunt", "description": "Female relative - A handshape near jaw"},
                        {"sign": "uncle", "description": "Male relative - U handshape near forehead"},
                        {"sign": "cousin", "description": "Extended family - C handshape at temple"},
                        {"sign": "family", "description": "Related group - F handshapes circle around"},
                        {"sign": "baby", "description": "Infant - rock arms like holding baby"},
                        {"sign": "child", "description": "Young person - pat air downward"},
                        {"sign": "friend", "description": "Companion - hook index fingers together"},
                        {"sign": "love", "description": "Affection - cross arms over chest"},
                        {"sign": "home", "description": "Residence - fingertips to mouth, then to cheek"}
                    ]
                }
            },
            "BSL": {
                "module_1": {
                    "title": "Basic Greetings & Common Signs",
                    "duration": 600,
                    "questions": [
                        {"sign": "hello", "description": "British greeting - flat hand to forehead"},
                        {"sign": "thank_you", "description": "Gratitude - fingertips to chin, forward"},
                        {"sign": "please", "description": "Request - flat hand circles on chest"},
                        {"sign": "sorry", "description": "Apology - S handshape on chest"},
                        {"sign": "yes", "description": "Agreement - nod with fist"},
                        {"sign": "no", "description": "Disagreement - index finger wag"},
                        {"sign": "good_morning", "description": "Morning greeting"},
                        {"sign": "good_evening", "description": "Evening greeting"},
                        {"sign": "welcome", "description": "Welcoming gesture"},
                        {"sign": "goodbye", "description": "Farewell wave"},
                        {"sign": "nice", "description": "Pleasant feeling"},
                        {"sign": "help", "description": "Assistance request"},
                        {"sign": "water", "description": "Drink gesture"},
                        {"sign": "food", "description": "Eating motion"},
                        {"sign": "more", "description": "Additional request"}
                    ]
                },
                "module_2": {
                    "title": "Numbers 1-15",
                    "duration": 600,
                    "questions": [
                        {"sign": "one", "description": "One finger extended"},
                        {"sign": "two", "description": "Two fingers in V shape"},
                        {"sign": "three", "description": "Three fingers extended"},
                        {"sign": "four", "description": "Four fingers up"},
                        {"sign": "five", "description": "Open hand palm out"},
                        {"sign": "six", "description": "Six with thumb and pinky"},
                        {"sign": "seven", "description": "Seven finger pattern"},
                        {"sign": "eight", "description": "Eight finger configuration"},
                        {"sign": "nine", "description": "Nine finger position"},
                        {"sign": "ten", "description": "Ten with both hands"},
                        {"sign": "eleven", "description": "Eleven finger pattern"},
                        {"sign": "twelve", "description": "Twelve configuration"},
                        {"sign": "thirteen", "description": "Thirteen pattern"},
                        {"sign": "fourteen", "description": "Fourteen finger setup"},
                        {"sign": "fifteen", "description": "Fifteen hand position"}
                    ]
                },
                "module_3": {
                    "title": "Family & Relationships",
                    "duration": 600,
                    "questions": [
                        {"sign": "mother", "description": "Female parent sign"},
                        {"sign": "father", "description": "Male parent sign"},
                        {"sign": "sister", "description": "Female sibling"},
                        {"sign": "brother", "description": "Male sibling"},
                        {"sign": "grandmother", "description": "Female grandparent"},
                        {"sign": "grandfather", "description": "Male grandparent"},
                        {"sign": "aunt", "description": "Female relative"},
                        {"sign": "uncle", "description": "Male relative"},
                        {"sign": "cousin", "description": "Extended family member"},
                        {"sign": "family", "description": "Family unit"},
                        {"sign": "baby", "description": "Young child"},
                        {"sign": "child", "description": "Young person"},
                        {"sign": "friend", "description": "Close companion"},
                        {"sign": "love", "description": "Deep affection"},
                        {"sign": "home", "description": "Place of residence"}
                    ]
                }
            },
            "FSL": {
                "module_1": {
                    "title": "Salutations de Base et Signes Communs",
                    "duration": 600,
                    "questions": [
                        {"sign": "bonjour", "description": "Salutation française"},
                        {"sign": "merci", "description": "Expression de gratitude"},
                        {"sign": "s_il_vous_plait", "description": "Demande polie"},
                        {"sign": "pardon", "description": "Excuses"},
                        {"sign": "oui", "description": "Affirmation"},
                        {"sign": "non", "description": "Négation"},
                        {"sign": "bonsoir", "description": "Salutation du soir"},
                        {"sign": "bonne_nuit", "description": "Adieu nocturne"},
                        {"sign": "bienvenue", "description": "Accueil"},
                        {"sign": "au_revoir", "description": "Adieu"},
                        {"sign": "bien", "description": "Bon/agréable"},
                        {"sign": "aide", "description": "Assistance"},
                        {"sign": "eau", "description": "Liquide à boire"},
                        {"sign": "nourriture", "description": "Aliment"},
                        {"sign": "plus", "description": "Davantage"}
                    ]
                },
                "module_2": {
                    "title": "Nombres 1-15",
                    "duration": 600,
                    "questions": [
                        {"sign": "un", "description": "Chiffre 1"},
                        {"sign": "deux", "description": "Chiffre 2"},
                        {"sign": "trois", "description": "Chiffre 3"},
                        {"sign": "quatre", "description": "Chiffre 4"},
                        {"sign": "cinq", "description": "Chiffre 5"},
                        {"sign": "six", "description": "Chiffre 6"},
                        {"sign": "sept", "description": "Chiffre 7"},
                        {"sign": "huit", "description": "Chiffre 8"},
                        {"sign": "neuf", "description": "Chiffre 9"},
                        {"sign": "dix", "description": "Chiffre 10"},
                        {"sign": "onze", "description": "Chiffre 11"},
                        {"sign": "douze", "description": "Chiffre 12"},
                        {"sign": "treize", "description": "Chiffre 13"},
                        {"sign": "quatorze", "description": "Chiffre 14"},
                        {"sign": "quinze", "description": "Chiffre 15"}
                    ]
                },
                "module_3": {
                    "title": "Famille et Relations",
                    "duration": 600,
                    "questions": [
                        {"sign": "mere", "description": "Parent féminin"},
                        {"sign": "pere", "description": "Parent masculin"},
                        {"sign": "soeur", "description": "Sœur"},
                        {"sign": "frere", "description": "Frère"},
                        {"sign": "grand_mere", "description": "Grand-mère"},
                        {"sign": "grand_pere", "description": "Grand-père"},
                        {"sign": "tante", "description": "Tante"},
                        {"sign": "oncle", "description": "Oncle"},
                        {"sign": "cousin", "description": "Cousin/cousine"},
                        {"sign": "famille", "description": "Unité familiale"},
                        {"sign": "bebe", "description": "Jeune enfant"},
                        {"sign": "enfant", "description": "Jeune personne"},
                        {"sign": "ami", "description": "Compagnon proche"},
                        {"sign": "amour", "description": "Affection profonde"},
                        {"sign": "maison", "description": "Lieu de résidence"}
                    ]
                }
            }
        }
        
        # Add similar structures for other languages
        self._add_other_languages()
    
    def _add_other_languages(self):
        """Add quiz data for other supported languages"""
        # Add similar quiz structures for GSL, JSL, CSL, ISL, PSL, SSL, RSL
        other_languages = ["GSL", "JSL", "CSL", "ISL", "PSL", "SSL", "RSL"]
        
        for lang in other_languages:
            self.quiz_data[lang] = {
                "module_1": {
                    "title": f"{lang} Basic Greetings & Common Signs",
                    "duration": 600,
                    "questions": [
                        {"sign": "hello", "description": f"{lang} greeting"},
                        {"sign": "thank_you", "description": f"{lang} gratitude"},
                        {"sign": "please", "description": f"{lang} polite request"},
                        {"sign": "sorry", "description": f"{lang} apology"},
                        {"sign": "yes", "description": f"{lang} affirmation"},
                        {"sign": "no", "description": f"{lang} negation"},
                        {"sign": "good_morning", "description": f"{lang} morning greeting"},
                        {"sign": "good_night", "description": f"{lang} night farewell"},
                        {"sign": "welcome", "description": f"{lang} welcoming"},
                        {"sign": "goodbye", "description": f"{lang} farewell"},
                        {"sign": "nice", "description": f"{lang} pleasant"},
                        {"sign": "help", "description": f"{lang} assistance"},
                        {"sign": "water", "description": f"{lang} drink"},
                        {"sign": "food", "description": f"{lang} eating"},
                        {"sign": "more", "description": f"{lang} additional"}
                    ]
                },
                "module_2": {
                    "title": f"{lang} Numbers 1-15",
                    "duration": 600,
                    "questions": [
                        {"sign": f"one", "description": f"{lang} number 1"},
                        {"sign": f"two", "description": f"{lang} number 2"},
                        {"sign": f"three", "description": f"{lang} number 3"},
                        {"sign": f"four", "description": f"{lang} number 4"},
                        {"sign": f"five", "description": f"{lang} number 5"},
                        {"sign": f"six", "description": f"{lang} number 6"},
                        {"sign": f"seven", "description": f"{lang} number 7"},
                        {"sign": f"eight", "description": f"{lang} number 8"},
                        {"sign": f"nine", "description": f"{lang} number 9"},
                        {"sign": f"ten", "description": f"{lang} number 10"},
                        {"sign": f"eleven", "description": f"{lang} number 11"},
                        {"sign": f"twelve", "description": f"{lang} number 12"},
                        {"sign": f"thirteen", "description": f"{lang} number 13"},
                        {"sign": f"fourteen", "description": f"{lang} number 14"},
                        {"sign": f"fifteen", "description": f"{lang} number 15"}
                    ]
                },
                "module_3": {
                    "title": f"{lang} Family & Relationships",
                    "duration": 600,
                    "questions": [
                        {"sign": "mother", "description": f"{lang} female parent"},
                        {"sign": "father", "description": f"{lang} male parent"},
                        {"sign": "sister", "description": f"{lang} female sibling"},
                        {"sign": "brother", "description": f"{lang} male sibling"},
                        {"sign": "grandmother", "description": f"{lang} female grandparent"},
                        {"sign": "grandfather", "description": f"{lang} male grandparent"},
                        {"sign": "aunt", "description": f"{lang} female relative"},
                        {"sign": "uncle", "description": f"{lang} male relative"},
                        {"sign": "cousin", "description": f"{lang} extended family"},
                        {"sign": "family", "description": f"{lang} family unit"},
                        {"sign": "baby", "description": f"{lang} young child"},
                        {"sign": "child", "description": f"{lang} young person"},
                        {"sign": "friend", "description": f"{lang} companion"},
                        {"sign": "love", "description": f"{lang} affection"},
                        {"sign": "home", "description": f"{lang} residence"}
                    ]
                }
            }
    
    def get_quiz_questions(self, language: str, module: str, count: int = 15) -> List[Dict[str, Any]]:
        """Get quiz questions for specific language and module"""
        try:
            if language in self.quiz_data and module in self.quiz_data[language]:
                questions = self.quiz_data[language][module]["questions"]
                # Randomize and limit to requested count
                selected_questions = random.sample(questions, min(count, len(questions)))
                return selected_questions
            else:
                # Return default questions if language/module not found
                return self._get_default_questions(count)
        except Exception as e:
            print(f"Error getting quiz questions: {e}")
            return self._get_default_questions(count)
    
    def _get_default_questions(self, count: int = 15) -> List[Dict[str, Any]]:
        """Return default questions when specific language/module not available"""
        default_questions = [
            {"sign": "hello", "description": "Basic greeting"},
            {"sign": "thank_you", "description": "Expression of gratitude"},
            {"sign": "please", "description": "Polite request"},
            {"sign": "sorry", "description": "Apology"},
            {"sign": "yes", "description": "Affirmation"},
            {"sign": "no", "description": "Negation"},
            {"sign": "help", "description": "Request for assistance"},
            {"sign": "water", "description": "Basic need"},
            {"sign": "food", "description": "Basic need"},
            {"sign": "more", "description": "Additional request"},
            {"sign": "good", "description": "Positive expression"},
            {"sign": "bad", "description": "Negative expression"},
            {"sign": "one", "description": "Number 1"},
            {"sign": "two", "description": "Number 2"},
            {"sign": "three", "description": "Number 3"}
        ]
        return random.sample(default_questions, min(count, len(default_questions)))
    
    def get_practice_questions(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get random questions for practice mode"""
        practice_signs = [
            {"sign": "hello", "description": "Basic greeting"},
            {"sign": "thank_you", "description": "Show gratitude"},
            {"sign": "please", "description": "Polite request"},
            {"sign": "sorry", "description": "Apology"},
            {"sign": "yes", "description": "Affirmation"},
            {"sign": "no", "description": "Negation"},
            {"sign": "help", "description": "Request assistance"},
            {"sign": "water", "description": "Basic need"},
            {"sign": "food", "description": "Sustenance"},
            {"sign": "more", "description": "Additional request"},
            {"sign": "good", "description": "Positive"},
            {"sign": "bad", "description": "Negative"},
            {"sign": "one", "description": "Number 1"},
            {"sign": "two", "description": "Number 2"},
            {"sign": "five", "description": "Number 5"}
        ]
        return random.sample(practice_signs, min(count, len(practice_signs)))
    
    def get_daily_challenge_puzzles(self, count: int = 3) -> List[Dict[str, Any]]:
        """Get daily challenge puzzles"""
        puzzles = [
            {
                "title": "Morning Warm-up",
                "description": "Practice 5 basic greetings",
                "signs": ["hello", "good_morning", "welcome", "nice", "thank_you"],
                "difficulty": "Easy",
                "reward": "10 XP",
                "time_limit": 300  # 5 minutes
            },
            {
                "title": "Number Master",
                "description": "Sign numbers 1-10 with 90% accuracy",
                "signs": ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"],
                "difficulty": "Medium",
                "reward": "25 XP",
                "time_limit": 420  # 7 minutes
            },
            {
                "title": "Family Signs Challenge",
                "description": "Learn 8 family-related signs",
                "signs": ["mother", "father", "sister", "brother", "family", "baby", "child", "love"],
                "difficulty": "Hard",
                "reward": "50 XP",
                "time_limit": 600  # 10 minutes
            },
            {
                "title": "Quick Response",
                "description": "Sign as many words as possible in 2 minutes",
                "signs": ["yes", "no", "help", "water", "food", "more", "good", "bad"],
                "difficulty": "Medium",
                "reward": "30 XP",
                "time_limit": 120  # 2 minutes
            },
            {
                "title": "Perfect Practice",
                "description": "Achieve 95% accuracy in basic signs",
                "signs": ["hello", "thank_you", "please", "sorry", "goodbye"],
                "difficulty": "Hard",
                "reward": "40 XP",
                "time_limit": 300  # 5 minutes
            }
        ]
        return random.sample(puzzles, min(count, len(puzzles)))
