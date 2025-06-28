"""
ProgressTracker for monitoring user learning progress and generating insights
"""

import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import logging

logger = logging.getLogger(__name__)

class ProgressTracker:
    """Tracks and analyzes user learning progress"""
    
    def __init__(self):
        """Initialize the progress tracker"""
        self.session_data = {}
        self.progress_history = {}
        
    def start_session(self, user_id: str, session_type: str = "practice") -> str:
        """
        Start a new learning session
        
        Args:
            user_id: User identifier
            session_type: Type of session (practice, lesson, challenge)
            
        Returns:
            Session ID
        """
        session_id = f"{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.session_data[session_id] = {
            "user_id": user_id,
            "session_type": session_type,
            "start_time": datetime.now(),
            "end_time": None,
            "signs_attempted": [],
            "signs_correct": [],
            "accuracy_scores": [],
            "total_attempts": 0,
            "total_correct": 0,
            "session_accuracy": 0.0,
            "duration_minutes": 0
        }
        
        logger.info(f"Session started: {session_id}")
        return session_id
    
    def end_session(self, session_id: str) -> Dict[str, Any]:
        """
        End a learning session and calculate final metrics
        
        Args:
            session_id: Session identifier
            
        Returns:
            Session summary data
        """
        if session_id not in self.session_data:
            return {}
        
        session = self.session_data[session_id]
        session["end_time"] = datetime.now()
        
        # Calculate session duration
        duration = session["end_time"] - session["start_time"]
        session["duration_minutes"] = round(duration.total_seconds() / 60, 1)
        
        # Calculate final accuracy
        if session["total_attempts"] > 0:
            session["session_accuracy"] = session["total_correct"] / session["total_attempts"]
        
        # Store in progress history
        user_id = session["user_id"]
        if user_id not in self.progress_history:
            self.progress_history[user_id] = []
        
        self.progress_history[user_id].append(session.copy())
        
        logger.info(f"Session ended: {session_id}")
        return self._get_session_summary(session)
    
    def record_sign_attempt(self, session_id: str, sign: str, is_correct: bool, confidence: float) -> bool:
        """
        Record a sign attempt within a session
        
        Args:
            session_id: Session identifier
            sign: Sign that was attempted
            is_correct: Whether the attempt was correct
            confidence: Confidence score (0-1)
            
        Returns:
            True if recorded successfully
        """
        if session_id not in self.session_data:
            return False
        
        session = self.session_data[session_id]
        
        # Record attempt data
        session["signs_attempted"].append(sign)
        session["accuracy_scores"].append(confidence)
        session["total_attempts"] += 1
        
        if is_correct:
            session["signs_correct"].append(sign)
            session["total_correct"] += 1
        
        logger.debug(f"Sign attempt recorded: {sign} ({'correct' if is_correct else 'incorrect'})")
        return True
    
    def get_current_session_stats(self, session_id: str) -> Dict[str, Any]:
        """
        Get current session statistics
        
        Args:
            session_id: Session identifier
            
        Returns:
            Current session statistics
        """
        if session_id not in self.session_data:
            return {}
        
        session = self.session_data[session_id]
        
        current_accuracy = 0.0
        if session["total_attempts"] > 0:
            current_accuracy = session["total_correct"] / session["total_attempts"]
        
        # Calculate current session duration
        current_time = datetime.now()
        duration = current_time - session["start_time"]
        current_duration = round(duration.total_seconds() / 60, 1)
        
        return {
            "total_attempts": session["total_attempts"],
            "total_correct": session["total_correct"],
            "current_accuracy": round(current_accuracy * 100, 1),
            "duration_minutes": current_duration,
            "unique_signs": len(set(session["signs_attempted"])),
            "average_confidence": round(np.mean(session["accuracy_scores"]) * 100, 1) if session["accuracy_scores"] else 0
        }
    
    def _get_session_summary(self, session: Dict[str, Any]) -> Dict[str, Any]:
        """Generate session summary"""
        unique_signs = set(session["signs_attempted"])
        signs_learned = len(set(session["signs_correct"]))
        
        return {
            "session_type": session["session_type"],
            "duration_minutes": session["duration_minutes"],
            "total_attempts": session["total_attempts"],
            "total_correct": session["total_correct"],
            "session_accuracy": round(session["session_accuracy"] * 100, 1),
            "unique_signs_attempted": len(unique_signs),
            "signs_learned": signs_learned,
            "average_confidence": round(np.mean(session["accuracy_scores"]) * 100, 1) if session["accuracy_scores"] else 0,
            "start_time": session["start_time"].isoformat(),
            "end_time": session["end_time"].isoformat()
        }
    
    def get_user_progress_overview(self, user_id: str, days: int = 30) -> Dict[str, Any]:
        """
        Get comprehensive progress overview for a user
        
        Args:
            user_id: User identifier
            days: Number of days to analyze
            
        Returns:
            Progress overview data
        """
        if user_id not in self.progress_history:
            return self._empty_progress_overview()
        
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_sessions = [
            session for session in self.progress_history[user_id]
            if session["start_time"] >= cutoff_date
        ]
        
        if not recent_sessions:
            return self._empty_progress_overview()
        
        # Calculate aggregate statistics
        total_sessions = len(recent_sessions)
        total_practice_time = sum(session["duration_minutes"] for session in recent_sessions)
        total_attempts = sum(session["total_attempts"] for session in recent_sessions)
        total_correct = sum(session["total_correct"] for session in recent_sessions)
        
        # Calculate averages
        avg_accuracy = (total_correct / total_attempts * 100) if total_attempts > 0 else 0
        avg_session_duration = total_practice_time / total_sessions if total_sessions > 0 else 0
        
        # Calculate unique signs
        all_signs_attempted = set()
        all_signs_learned = set()
        
        for session in recent_sessions:
            all_signs_attempted.update(session["signs_attempted"])
            all_signs_learned.update(session["signs_correct"])
        
        # Calculate progress trends
        accuracy_trend = self._calculate_accuracy_trend(recent_sessions)
        practice_trend = self._calculate_practice_trend(recent_sessions, days)
        
        return {
            "period_days": days,
            "total_sessions": total_sessions,
            "total_practice_minutes": round(total_practice_time, 1),
            "total_attempts": total_attempts,
            "total_correct": total_correct,
            "average_accuracy": round(avg_accuracy, 1),
            "average_session_duration": round(avg_session_duration, 1),
            "unique_signs_attempted": len(all_signs_attempted),
            "unique_signs_learned": len(all_signs_learned),
            "accuracy_trend": accuracy_trend,
            "practice_trend": practice_trend,
            "streak_info": self._calculate_streak_info(recent_sessions),
            "improvement_areas": self._identify_improvement_areas(recent_sessions)
        }
    
    def _empty_progress_overview(self) -> Dict[str, Any]:
        """Return empty progress overview for new users"""
        return {
            "period_days": 0,
            "total_sessions": 0,
            "total_practice_minutes": 0,
            "total_attempts": 0,
            "total_correct": 0,
            "average_accuracy": 0,
            "average_session_duration": 0,
            "unique_signs_attempted": 0,
            "unique_signs_learned": 0,
            "accuracy_trend": "stable",
            "practice_trend": "stable",
            "streak_info": {"current_streak": 0, "best_streak": 0},
            "improvement_areas": []
        }
    
    def _calculate_accuracy_trend(self, sessions: List[Dict[str, Any]]) -> str:
        """Calculate accuracy trend over sessions"""
        if len(sessions) < 3:
            return "stable"
        
        # Get accuracy for each session
        accuracies = [session["session_accuracy"] for session in sessions[-10:]]  # Last 10 sessions
        
        # Calculate trend using linear regression slope
        x = np.arange(len(accuracies))
        slope = np.polyfit(x, accuracies, 1)[0]
        
        if slope > 0.05:
            return "improving"
        elif slope < -0.05:
            return "declining"
        else:
            return "stable"
    
    def _calculate_practice_trend(self, sessions: List[Dict[str, Any]], days: int) -> str:
        """Calculate practice frequency trend"""
        if days < 7:
            return "stable"
        
        # Split sessions into two halves
        mid_point = len(sessions) // 2
        first_half = sessions[:mid_point]
        second_half = sessions[mid_point:]
        
        if not first_half or not second_half:
            return "stable"
        
        first_avg = len(first_half) / (days // 2)
        second_avg = len(second_half) / (days // 2)
        
        if second_avg > first_avg * 1.2:
            return "increasing"
        elif second_avg < first_avg * 0.8:
            return "decreasing"
        else:
            return "stable"
    
    def _calculate_streak_info(self, sessions: List[Dict[str, Any]]) -> Dict[str, int]:
        """Calculate practice streak information"""
        if not sessions:
            return {"current_streak": 0, "best_streak": 0}
        
        # Group sessions by date
        session_dates = set()
        for session in sessions:
            date = session["start_time"].date()
            session_dates.add(date)
        
        # Calculate current streak
        current_streak = 0
        today = datetime.now().date()
        
        for i in range(30):  # Check last 30 days
            check_date = today - timedelta(days=i)
            if check_date in session_dates:
                current_streak += 1
            else:
                break
        
        # Calculate best streak (simplified)
        best_streak = max(current_streak, len(session_dates) // 2)  # Rough estimate
        
        return {"current_streak": current_streak, "best_streak": best_streak}
    
    def _identify_improvement_areas(self, sessions: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Identify areas where user can improve"""
        if not sessions:
            return []
        
        improvement_areas = []
        
        # Check overall accuracy
        total_attempts = sum(session["total_attempts"] for session in sessions)
        total_correct = sum(session["total_correct"] for session in sessions)
        overall_accuracy = (total_correct / total_attempts) if total_attempts > 0 else 0
        
        if overall_accuracy < 0.7:
            improvement_areas.append({
                "area": "accuracy",
                "suggestion": "Focus on proper hand positioning and finger placement",
                "priority": "high"
            })
        
        # Check session consistency
        avg_duration = np.mean([session["duration_minutes"] for session in sessions])
        if avg_duration < 10:
            improvement_areas.append({
                "area": "practice_time",
                "suggestion": "Try to practice for at least 15 minutes per session",
                "priority": "medium"
            })
        
        # Check variety of signs
        all_signs = set()
        for session in sessions:
            all_signs.update(session["signs_attempted"])
        
        if len(all_signs) < 10:
            improvement_areas.append({
                "area": "vocabulary",
                "suggestion": "Practice a wider variety of signs to expand your vocabulary",
                "priority": "medium"
            })
        
        return improvement_areas
    
    def generate_weekly_report(self, user_id: str) -> Dict[str, Any]:
        """
        Generate a comprehensive weekly progress report
        
        Args:
            user_id: User identifier
            
        Returns:
            Weekly report data
        """
        overview = self.get_user_progress_overview(user_id, days=7)
        
        # Add weekly-specific insights
        weekly_report = overview.copy()
        weekly_report.update({
            "report_type": "weekly",
            "generated_at": datetime.now().isoformat(),
            "achievements_this_week": self._get_weekly_achievements(user_id),
            "recommended_focus": self._get_weekly_recommendations(overview),
            "next_week_goals": self._suggest_next_week_goals(overview)
        })
        
        return weekly_report
    
    def _get_weekly_achievements(self, user_id: str) -> List[Dict[str, str]]:
        """Get achievements earned this week"""
        # Simplified achievement detection
        overview = self.get_user_progress_overview(user_id, days=7)
        achievements = []
        
        if overview["total_sessions"] >= 5:
            achievements.append({
                "name": "Consistent Learner",
                "description": "Practiced 5 or more times this week"
            })
        
        if overview["average_accuracy"] >= 85:
            achievements.append({
                "name": "Accuracy Master",
                "description": "Maintained 85%+ accuracy this week"
            })
        
        if overview["total_practice_minutes"] >= 60:
            achievements.append({
                "name": "Dedicated Practitioner",
                "description": "Practiced for over 1 hour this week"
            })
        
        return achievements
    
    def _get_weekly_recommendations(self, overview: Dict[str, Any]) -> List[str]:
        """Get recommendations based on weekly performance"""
        recommendations = []
        
        if overview["accuracy_trend"] == "declining":
            recommendations.append("Review basic signs and focus on proper hand positioning")
        
        if overview["total_sessions"] < 3:
            recommendations.append("Try to practice at least 3 times per week for better retention")
        
        if overview["average_session_duration"] < 10:
            recommendations.append("Increase session length to 15-20 minutes for better learning")
        
        if not recommendations:
            recommendations.append("Great progress! Continue with your current practice routine")
        
        return recommendations
    
    def _suggest_next_week_goals(self, overview: Dict[str, Any]) -> List[str]:
        """Suggest goals for next week"""
        goals = []
        
        # Accuracy goal
        current_accuracy = overview["average_accuracy"]
        if current_accuracy < 80:
            goals.append(f"Improve accuracy to {min(85, current_accuracy + 10)}%")
        else:
            goals.append("Maintain accuracy above 80%")
        
        # Practice frequency goal
        if overview["total_sessions"] < 5:
            goals.append("Practice at least 5 times next week")
        else:
            goals.append("Continue consistent daily practice")
        
        # Vocabulary goal
        signs_learned = overview["unique_signs_learned"]
        goals.append(f"Learn {max(3, signs_learned // 2)} new signs")
        
        return goals
