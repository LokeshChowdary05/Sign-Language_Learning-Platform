"""
Real-time Quiz System for Sign Language Learning
Handles timed quizzes, scoring, and progress tracking
"""

import time
import random
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import logging
import streamlit as st
from .quiz_database import QuizDatabase

logger = logging.getLogger(__name__)

class QuizSystem:
    """Real-time quiz system for sign language learning"""
    
    def __init__(self, hand_tracker, model_predictor):
        """Initialize quiz system"""
        self.hand_tracker = hand_tracker
        self.model_predictor = model_predictor
        self.current_quiz = None
        self.quiz_results = []
        self.quiz_active = False
        self.quiz_database = QuizDatabase()
        
        # Quiz configurations
        self.quiz_configs = {
            "practice": {
                "duration": 180,  # 3 minutes
                "signs_count": 10,
                "difficulty": "easy",
                "passing_score": 70
            },
            "module_1": {
                "duration": 600,  # 10 minutes
                "signs_count": 15,
                "difficulty": "easy",
                "passing_score": 80
            },
            "module_2": {
                "duration": 600,  # 10 minutes
                "signs_count": 15,
                "difficulty": "medium", 
                "passing_score": 85
            },
            "module_3": {
                "duration": 600,  # 10 minutes
                "signs_count": 15,
                "difficulty": "hard",
                "passing_score": 90
            }
        }
    
    def start_quiz(self, quiz_type: str, language: str = "ASL") -> Dict[str, Any]:
        """Start a new quiz session with language-specific questions"""
        try:
            if quiz_type not in self.quiz_configs:
                return {"error": "Invalid quiz type"}
            
            config = self.quiz_configs[quiz_type]
            
            # Get questions from database based on quiz type and language
            if quiz_type == "practice":
                quiz_questions = self.quiz_database.get_practice_questions(config["signs_count"])
            else:
                quiz_questions = self.quiz_database.get_quiz_questions(
                    language, quiz_type, config["signs_count"]
                )
            
            # Extract signs from questions
            quiz_signs = [q["sign"] for q in quiz_questions]
            
            self.current_quiz = {
                "quiz_type": quiz_type,
                "language": language,
                "config": config,
                "signs": quiz_signs,
                "questions": quiz_questions,
                "current_sign_index": 0,
                "start_time": datetime.now(),
                "end_time": datetime.now() + timedelta(seconds=config["duration"]),
                "score": 0,
                "attempts": [],
                "completed": False,
                "time_remaining": config["duration"]
            }
            
            self.quiz_active = True
            logger.info(f"Started {quiz_type} quiz for {language} with {len(quiz_signs)} signs")
            
            return {
                "success": True,
                "quiz_id": f"{quiz_type}_{language}_{int(time.time())}",
                "duration": config["duration"],
                "signs_count": len(quiz_signs),
                "first_sign": quiz_signs[0] if quiz_signs else None,
                "questions": quiz_questions
            }
            
        except Exception as e:
            logger.error(f"Error starting quiz: {str(e)}")
            return {"error": str(e)}
    
    def get_current_sign(self) -> Optional[str]:
        """Get the current sign to practice"""
        if not self.quiz_active or not self.current_quiz:
            return None
        
        if self.current_quiz["current_sign_index"] < len(self.current_quiz["signs"]):
            return self.current_quiz["signs"][self.current_quiz["current_sign_index"]]
        
        return None
    
    def validate_sign_attempt(self, predicted_sign: str, confidence: float) -> Dict[str, Any]:
        """Validate a sign attempt during quiz"""
        if not self.quiz_active or not self.current_quiz:
            return {"error": "No active quiz"}
        
        current_sign = self.get_current_sign()
        if not current_sign:
            return {"error": "No current sign"}
        
        # Check if time is up
        if datetime.now() > self.current_quiz["end_time"]:
            self.end_quiz()
            return {"error": "Quiz time expired"}
        
        # Validate the sign
        is_correct = predicted_sign.lower() == current_sign.lower()
        min_confidence = 0.7  # Minimum confidence for acceptance
        
        attempt_result = {
            "sign": current_sign,
            "predicted": predicted_sign,
            "confidence": confidence,
            "is_correct": is_correct and confidence >= min_confidence,
            "timestamp": datetime.now().isoformat(),
            "time_taken": (datetime.now() - self.current_quiz["start_time"]).total_seconds()
        }
        
        self.current_quiz["attempts"].append(attempt_result)
        
        result = {
            "is_correct": attempt_result["is_correct"],
            "confidence": confidence,
            "current_sign": current_sign,
            "predicted_sign": predicted_sign,
            "feedback": self._get_feedback(attempt_result),
            "progress": self._get_quiz_progress()
        }
        
        # If correct, move to next sign
        if attempt_result["is_correct"]:
            self.current_quiz["score"] += 1
            self.current_quiz["current_sign_index"] += 1
            
            # Check if quiz is complete
            if self.current_quiz["current_sign_index"] >= len(self.current_quiz["signs"]):
                self.end_quiz()
                result["quiz_completed"] = True
                result["final_results"] = self.get_quiz_results()
            else:
                result["next_sign"] = self.get_current_sign()
        
        return result
    
    def _get_feedback(self, attempt: Dict[str, Any]) -> Dict[str, str]:
        """Generate feedback for an attempt"""
        if attempt["is_correct"]:
            if attempt["confidence"] >= 0.9:
                return {
                    "type": "excellent",
                    "message": "🎉 Excellent! Perfect sign recognition!",
                    "color": "success"
                }
            else:
                return {
                    "type": "good",
                    "message": "✅ Good job! Sign recognized correctly.",
                    "color": "success"
                }
        else:
            if attempt["confidence"] < 0.3:
                return {
                    "type": "low_confidence",
                    "message": "❌ Sign not clearly detected. Please adjust your position and try again.",
                    "color": "error"
                }
            else:
                return {
                    "type": "wrong_sign",
                    "message": f"❌ Incorrect. Expected '{attempt['sign']}', got '{attempt['predicted']}'.",
                    "color": "error"
                }
    
    def _get_quiz_progress(self) -> Dict[str, Any]:
        """Get current quiz progress"""
        if not self.current_quiz:
            return {}
        
        total_signs = len(self.current_quiz["signs"])
        current_index = self.current_quiz["current_sign_index"]
        time_remaining = max(0, (self.current_quiz["end_time"] - datetime.now()).total_seconds())
        
        return {
            "current_sign_index": current_index,
            "total_signs": total_signs,
            "progress_percentage": (current_index / total_signs) * 100,
            "score": self.current_quiz["score"],
            "accuracy": (self.current_quiz["score"] / max(1, current_index)) * 100 if current_index > 0 else 0,
            "time_remaining": int(time_remaining),
            "time_remaining_formatted": self._format_time(int(time_remaining))
        }
    
    def _format_time(self, seconds: int) -> str:
        """Format time in MM:SS format"""
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"
    
    def end_quiz(self) -> Dict[str, Any]:
        """End the current quiz and calculate results"""
        if not self.current_quiz:
            return {"error": "No active quiz"}
        
        self.quiz_active = False
        self.current_quiz["completed"] = True
        self.current_quiz["end_time"] = datetime.now()
        
        results = self.get_quiz_results()
        self.quiz_results.append(results)
        
        return results
    
    def get_quiz_results(self) -> Dict[str, Any]:
        """Get comprehensive quiz results"""
        if not self.current_quiz:
            return {"error": "No quiz data"}
        
        total_signs = len(self.current_quiz["signs"])
        correct_signs = self.current_quiz["score"]
        total_attempts = len(self.current_quiz["attempts"])
        
        accuracy = (correct_signs / total_signs) * 100 if total_signs > 0 else 0
        passing_score = self.current_quiz["config"]["passing_score"]
        passed = accuracy >= passing_score
        
        # Calculate XP and level progress
        xp_earned = self._calculate_xp(correct_signs, accuracy, self.current_quiz["config"]["difficulty"])
        
        results = {
            "quiz_type": self.current_quiz["quiz_type"],
            "total_signs": total_signs,
            "correct_signs": correct_signs,
            "total_attempts": total_attempts,
            "accuracy": round(accuracy, 1),
            "passing_score": passing_score,
            "passed": passed,
            "xp_earned": xp_earned,
            "duration": self.current_quiz["config"]["duration"],
            "time_taken": (self.current_quiz["end_time"] - self.current_quiz["start_time"]).total_seconds(),
            "attempts": self.current_quiz["attempts"],
            "grade": self._calculate_grade(accuracy),
            "feedback": self._get_final_feedback(accuracy, passed),
            "timestamp": datetime.now().isoformat()
        }
        
        return results
    
    def _calculate_xp(self, correct_signs: int, accuracy: float, difficulty: str) -> int:
        """Calculate XP earned from quiz"""
        base_xp = correct_signs * 10  # 10 XP per correct sign
        
        # Difficulty multiplier
        difficulty_multipliers = {"easy": 1.0, "medium": 1.5, "hard": 2.0}
        multiplier = difficulty_multipliers.get(difficulty, 1.0)
        
        # Accuracy bonus
        if accuracy >= 95:
            accuracy_bonus = 50
        elif accuracy >= 90:
            accuracy_bonus = 30
        elif accuracy >= 80:
            accuracy_bonus = 20
        else:
            accuracy_bonus = 0
        
        total_xp = int((base_xp * multiplier) + accuracy_bonus)
        return total_xp
    
    def _calculate_grade(self, accuracy: float) -> str:
        """Calculate letter grade based on accuracy"""
        if accuracy >= 95:
            return "A+"
        elif accuracy >= 90:
            return "A"
        elif accuracy >= 85:
            return "B+"
        elif accuracy >= 80:
            return "B"
        elif accuracy >= 75:
            return "C+"
        elif accuracy >= 70:
            return "C"
        elif accuracy >= 65:
            return "D+"
        elif accuracy >= 60:
            return "D"
        else:
            return "F"
    
    def _get_final_feedback(self, accuracy: float, passed: bool) -> Dict[str, str]:
        """Get final feedback for quiz completion"""
        if passed:
            if accuracy >= 95:
                return {
                    "title": "🏆 Outstanding Performance!",
                    "message": "You've mastered these signs with exceptional accuracy!",
                    "color": "success"
                }
            elif accuracy >= 85:
                return {
                    "title": "🎉 Excellent Work!",
                    "message": "Great job! You're showing strong progress in sign language.",
                    "color": "success"
                }
            else:
                return {
                    "title": "✅ Well Done!",
                    "message": "You passed! Keep practicing to improve your accuracy.",
                    "color": "success"
                }
        else:
            return {
                "title": "📚 Keep Practicing!",
                "message": "Don't worry! Practice makes perfect. Review the signs and try again.",
                "color": "warning"
            }
    
    def get_quiz_status(self) -> Dict[str, Any]:
        """Get current quiz status"""
        if not self.quiz_active or not self.current_quiz:
            return {"active": False}
        
        return {
            "active": True,
            "current_sign": self.get_current_sign(),
            "progress": self._get_quiz_progress(),
            "quiz_type": self.current_quiz["quiz_type"]
        }
    
    def pause_quiz(self) -> bool:
        """Pause the current quiz"""
        if self.quiz_active and self.current_quiz:
            self.quiz_active = False
            return True
        return False
    
    def resume_quiz(self) -> bool:
        """Resume a paused quiz"""
        if not self.quiz_active and self.current_quiz and not self.current_quiz["completed"]:
            # Adjust end time to account for pause
            pause_duration = datetime.now() - self.current_quiz.get("pause_start", datetime.now())
            self.current_quiz["end_time"] += pause_duration
            self.quiz_active = True
            return True
        return False
    
    def skip_current_sign(self) -> Dict[str, Any]:
        """Skip the current sign (counts as incorrect)"""
        if not self.quiz_active or not self.current_quiz:
            return {"error": "No active quiz"}
        
        current_sign = self.get_current_sign()
        if not current_sign:
            return {"error": "No current sign"}
        
        # Record as skipped attempt
        attempt_result = {
            "sign": current_sign,
            "predicted": "SKIPPED",
            "confidence": 0.0,
            "is_correct": False,
            "timestamp": datetime.now().isoformat(),
            "time_taken": (datetime.now() - self.current_quiz["start_time"]).total_seconds(),
            "skipped": True
        }
        
        self.current_quiz["attempts"].append(attempt_result)
        self.current_quiz["current_sign_index"] += 1
        
        # Check if quiz is complete
        if self.current_quiz["current_sign_index"] >= len(self.current_quiz["signs"]):
            self.end_quiz()
            return {
                "skipped": True,
                "quiz_completed": True,
                "final_results": self.get_quiz_results()
            }
        
        return {
            "skipped": True,
            "next_sign": self.get_current_sign(),
            "progress": self._get_quiz_progress()
        }
    
    def get_quiz_history(self) -> List[Dict[str, Any]]:
        """Get history of completed quizzes"""
        return self.quiz_results.copy()
    
    def clear_quiz_history(self) -> bool:
        """Clear quiz history"""
        self.quiz_results.clear()
        return True
