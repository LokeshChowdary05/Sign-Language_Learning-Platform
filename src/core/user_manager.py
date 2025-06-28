"""
UserManager for handling user authentication, profiles, and data management
"""

import json
import hashlib
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)

class UserManager:
    """Manager for user authentication and profile data"""
    
    def __init__(self):
        """Initialize the user manager"""
        self.users_data = {}
        self.current_user = None
        
        # Load demo users for testing
        self._load_demo_users()
    
    def _load_demo_users(self):
        """Load demo users for testing purposes"""
        demo_users = {
            "demo_user": {
                "user_id": "demo_user",
                "name": "Demo User",
                "email": "demo@example.com",
                "created_at": datetime.now().isoformat(),
                "last_login": datetime.now().isoformat(),
                "profile": {
                    "skill_level": "Beginner",
                    "preferred_languages": ["ASL", "BSL"],
                    "daily_goal_minutes": 15,
                    "preferred_difficulty": "Easy"
                },
                "statistics": {
                    "total_signs_learned": 12,
                    "total_practice_time": 180,  # minutes
                    "current_streak": 3,
                    "best_streak": 7,
                    "accuracy_average": 0.78,
                    "sessions_completed": 8
                },
                "achievements": [
                    {
                        "id": "first_sign",
                        "name": "First Sign",
                        "description": "Learned your first sign",
                        "earned_at": (datetime.now() - timedelta(days=5)).isoformat()
                    },
                    {
                        "id": "week_streak",
                        "name": "Week Warrior",
                        "description": "Practiced for 7 days straight",
                        "earned_at": (datetime.now() - timedelta(days=1)).isoformat()
                    }
                ]
            }
        }
        
        self.users_data = demo_users
    
    def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Authenticate user with email and password
        
        Args:
            email: User email
            password: User password
            
        Returns:
            User data if authentication successful, None otherwise
        """
        try:
            # For demo purposes, accept any email/password combination
            if email and password:
                # Use demo user or create new one
                if email == "demo@example.com":
                    user_data = self.users_data["demo_user"]
                else:
                    user_data = self._create_user(email, password)
                
                # Update last login
                user_data["last_login"] = datetime.now().isoformat()
                self.current_user = user_data
                
                logger.info(f"User authenticated: {email}")
                return user_data
            
            return None
            
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return None
    
    def _create_user(self, email: str, password: str) -> Dict[str, Any]:
        """Create a new user account"""
        user_id = str(uuid.uuid4())
        
        user_data = {
            "user_id": user_id,
            "name": email.split("@")[0].title(),
            "email": email,
            "created_at": datetime.now().isoformat(),
            "last_login": datetime.now().isoformat(),
            "profile": {
                "skill_level": "Beginner",
                "preferred_languages": ["ASL"],
                "daily_goal_minutes": 15,
                "preferred_difficulty": "Easy"
            },
            "statistics": {
                "total_signs_learned": 0,
                "total_practice_time": 0,
                "current_streak": 0,
                "best_streak": 0,
                "accuracy_average": 0.0,
                "sessions_completed": 0
            },
            "achievements": []
        }
        
        self.users_data[user_id] = user_data
        logger.info(f"New user created: {email}")
        
        return user_data
    
    def get_user_data(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user data by user ID"""
        return self.users_data.get(user_id)
    
    def update_user_profile(self, user_id: str, profile_data: Dict[str, Any]) -> bool:
        """
        Update user profile information
        
        Args:
            user_id: User identifier
            profile_data: Profile data to update
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if user_id in self.users_data:
                self.users_data[user_id]["profile"].update(profile_data)
                logger.info(f"Profile updated for user: {user_id}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error updating profile: {str(e)}")
            return False
    
    def update_user_statistics(self, user_id: str, session_data: Dict[str, Any]) -> bool:
        """
        Update user learning statistics
        
        Args:
            user_id: User identifier
            session_data: Session data including signs learned, time, accuracy
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if user_id not in self.users_data:
                return False
            
            stats = self.users_data[user_id]["statistics"]
            
            # Update statistics
            stats["total_signs_learned"] += session_data.get("signs_learned", 0)
            stats["total_practice_time"] += session_data.get("practice_time", 0)
            stats["sessions_completed"] += 1
            
            # Update accuracy average
            current_accuracy = session_data.get("accuracy", 0)
            if stats["sessions_completed"] == 1:
                stats["accuracy_average"] = current_accuracy
            else:
                # Weighted average
                total_sessions = stats["sessions_completed"]
                stats["accuracy_average"] = (
                    (stats["accuracy_average"] * (total_sessions - 1) + current_accuracy) / total_sessions
                )
            
            # Update streak
            last_session = session_data.get("date", datetime.now().date())
            yesterday = datetime.now().date() - timedelta(days=1)
            today = datetime.now().date()
            
            if last_session == today:
                stats["current_streak"] += 1
            elif last_session != yesterday:
                stats["current_streak"] = 1 if last_session == today else 0
            
            # Update best streak
            if stats["current_streak"] > stats["best_streak"]:
                stats["best_streak"] = stats["current_streak"]
            
            logger.info(f"Statistics updated for user: {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating statistics: {str(e)}")
            return False
    
    def add_achievement(self, user_id: str, achievement: Dict[str, Any]) -> bool:
        """
        Add an achievement to user's profile
        
        Args:
            user_id: User identifier
            achievement: Achievement data
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if user_id not in self.users_data:
                return False
            
            # Check if achievement already exists
            existing_achievements = [a["id"] for a in self.users_data[user_id]["achievements"]]
            
            if achievement["id"] not in existing_achievements:
                achievement["earned_at"] = datetime.now().isoformat()
                self.users_data[user_id]["achievements"].append(achievement)
                logger.info(f"Achievement '{achievement['name']}' added for user: {user_id}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error adding achievement: {str(e)}")
            return False
    
    def get_user_progress(self, user_id: str) -> Dict[str, Any]:
        """
        Get comprehensive user progress data
        
        Args:
            user_id: User identifier
            
        Returns:
            Dictionary containing progress information
        """
        try:
            if user_id not in self.users_data:
                return {}
            
            user_data = self.users_data[user_id]
            stats = user_data["statistics"]
            profile = user_data["profile"]
            
            # Calculate progress metrics
            skill_levels = ["Beginner", "Intermediate", "Advanced"]
            current_level_index = skill_levels.index(profile["skill_level"])
            
            # Signs needed for next level (arbitrary thresholds)
            level_thresholds = [0, 50, 150, 300]
            signs_for_next_level = level_thresholds[min(current_level_index + 1, len(level_thresholds) - 1)]
            
            progress_data = {
                "current_level": profile["skill_level"],
                "signs_learned": stats["total_signs_learned"],
                "signs_for_next_level": signs_for_next_level,
                "level_progress_percentage": min(100, (stats["total_signs_learned"] / signs_for_next_level) * 100) if signs_for_next_level > 0 else 100,
                "total_practice_hours": round(stats["total_practice_time"] / 60, 1),
                "average_accuracy": round(stats["accuracy_average"] * 100, 1),
                "current_streak": stats["current_streak"],
                "best_streak": stats["best_streak"],
                "total_achievements": len(user_data["achievements"]),
                "sessions_completed": stats["sessions_completed"]
            }
            
            return progress_data
            
        except Exception as e:
            logger.error(f"Error getting user progress: {str(e)}")
            return {}
    
    def export_user_data(self, user_id: str) -> Optional[str]:
        """
        Export user data as JSON string
        
        Args:
            user_id: User identifier
            
        Returns:
            JSON string of user data or None if error
        """
        try:
            if user_id in self.users_data:
                user_data = self.users_data[user_id].copy()
                # Remove sensitive information
                user_data.pop("password_hash", None)
                
                return json.dumps(user_data, indent=2, default=str)
            
            return None
            
        except Exception as e:
            logger.error(f"Error exporting user data: {str(e)}")
            return None
    
    def delete_user_account(self, user_id: str) -> bool:
        """
        Delete user account and all associated data
        
        Args:
            user_id: User identifier
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if user_id in self.users_data:
                del self.users_data[user_id]
                logger.info(f"User account deleted: {user_id}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error deleting user account: {str(e)}")
            return False
    
    def get_leaderboard(self, metric: str = "signs_learned", limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get leaderboard data for specified metric
        
        Args:
            metric: Metric to rank by (signs_learned, accuracy_average, current_streak)
            limit: Number of top users to return
            
        Returns:
            List of user data sorted by metric
        """
        try:
            leaderboard = []
            
            for user_data in self.users_data.values():
                stats = user_data["statistics"]
                
                entry = {
                    "name": user_data["name"],
                    "value": stats.get(metric, 0),
                    "level": user_data["profile"]["skill_level"]
                }
                
                # Format value based on metric
                if metric == "accuracy_average":
                    entry["value"] = round(entry["value"] * 100, 1)
                elif metric == "total_practice_time":
                    entry["value"] = round(entry["value"] / 60, 1)  # Convert to hours
                
                leaderboard.append(entry)
            
            # Sort by value (descending)
            leaderboard.sort(key=lambda x: x["value"], reverse=True)
            
            return leaderboard[:limit]
            
        except Exception as e:
            logger.error(f"Error getting leaderboard: {str(e)}")
            return []
    
    def check_daily_goal(self, user_id: str) -> Dict[str, Any]:
        """
        Check if user has met their daily goal
        
        Args:
            user_id: User identifier
            
        Returns:
            Dictionary with daily goal status
        """
        try:
            if user_id not in self.users_data:
                return {"met_goal": False, "progress": 0}
            
            user_data = self.users_data[user_id]
            daily_goal = user_data["profile"]["daily_goal_minutes"]
            
            # For demo purposes, assume some practice time today
            today_practice_time = 12  # minutes (this would come from session tracking)
            
            progress_percentage = min(100, (today_practice_time / daily_goal) * 100)
            
            return {
                "met_goal": today_practice_time >= daily_goal,
                "progress": round(progress_percentage, 1),
                "today_minutes": today_practice_time,
                "goal_minutes": daily_goal
            }
            
        except Exception as e:
            logger.error(f"Error checking daily goal: {str(e)}")
            return {"met_goal": False, "progress": 0}
