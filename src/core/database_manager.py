"""
Database Manager for Sign Language Learning Platform
Handles user accounts, progress tracking, and session management using SQLite
"""

import sqlite3
import hashlib
import uuid
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Comprehensive database manager for user data and platform analytics"""
    
    def __init__(self, db_path: str = "data/platform.db"):
        """Initialize database connection and create tables"""
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    name TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1,
                    profile_data TEXT
                )
            """)
            
            # User sessions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_sessions (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    device_info TEXT,
                    ip_address TEXT,
                    session_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    session_end TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)
            
            # User progress table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    language TEXT NOT NULL,
                    signs_learned INTEGER DEFAULT 0,
                    accuracy_score REAL DEFAULT 0.0,
                    practice_time INTEGER DEFAULT 0,
                    level TEXT DEFAULT 'Beginner',
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)
            
            # Activity tracking table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS activity_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    activity_type TEXT NOT NULL,
                    activity_data TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    FOREIGN KEY (session_id) REFERENCES user_sessions (id)
                )
            """)
            
            # Practice sessions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS practice_sessions (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    language TEXT NOT NULL,
                    session_type TEXT NOT NULL,
                    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    end_time TIMESTAMP,
                    signs_practiced INTEGER DEFAULT 0,
                    correct_signs INTEGER DEFAULT 0,
                    total_attempts INTEGER DEFAULT 0,
                    average_confidence REAL DEFAULT 0.0,
                    session_data TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)
            
            # Quiz results table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS quiz_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    language TEXT NOT NULL,
                    quiz_id TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    total_questions INTEGER NOT NULL,
                    time_taken INTEGER,
                    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    answers TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)
            
            # Daily challenges table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS daily_challenges (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    challenge_id TEXT NOT NULL,
                    language TEXT NOT NULL,
                    completed BOOLEAN DEFAULT 0,
                    score INTEGER DEFAULT 0,
                    completed_at TIMESTAMP,
                    challenge_date DATE DEFAULT CURRENT_DATE,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)
            
            # Sign recognition attempts
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sign_attempts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    language TEXT NOT NULL,
                    target_sign TEXT NOT NULL,
                    predicted_sign TEXT,
                    confidence REAL,
                    is_correct BOOLEAN,
                    attempt_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    feedback TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    FOREIGN KEY (session_id) REFERENCES practice_sessions (id)
                )
            """)
            
            conn.commit()
            logger.info("Database initialized successfully")
    
    def hash_password(self, password: str) -> str:
        """Hash password with salt"""
        salt = "sign_lang_platform_salt"
        return hashlib.sha256((password + salt).encode()).hexdigest()
    
    def create_user(self, email: str, password: str, name: str) -> Optional[str]:
        """Create new user account"""
        try:
            user_id = str(uuid.uuid4())
            password_hash = self.hash_password(password)
            
            profile_data = {
                "skill_level": "Beginner",
                "preferred_language": "ASL",
                "daily_goal": 15,
                "difficulty": "Easy",
                "achievements": [],
                "streak_count": 0
            }
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO users (id, email, password_hash, name, profile_data)
                    VALUES (?, ?, ?, ?, ?)
                """, (user_id, email, password_hash, name, json.dumps(profile_data)))
                
                # Initialize progress for default language
                cursor.execute("""
                    INSERT INTO user_progress (user_id, language)
                    VALUES (?, ?)
                """, (user_id, "ASL"))
                
                conn.commit()
                logger.info(f"User created: {email}")
                return user_id
                
        except sqlite3.IntegrityError:
            logger.error(f"User already exists: {email}")
            return None
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            return None
    
    def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user and return user data"""
        try:
            password_hash = self.hash_password(password)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, email, name, profile_data, created_at
                    FROM users 
                    WHERE email = ? AND password_hash = ? AND is_active = 1
                """, (email, password_hash))
                
                result = cursor.fetchone()
                if result:
                    user_data = {
                        "user_id": result[0],
                        "email": result[1],
                        "name": result[2],
                        "profile": json.loads(result[3]) if result[3] else {},
                        "created_at": result[4]
                    }
                    
                    # Update last login
                    cursor.execute("""
                        UPDATE users SET last_login = CURRENT_TIMESTAMP
                        WHERE id = ?
                    """, (result[0],))
                    conn.commit()
                    
                    return user_data
                    
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            
        return None
    
    def create_session(self, user_id: str, device_info: str, ip_address: str = None) -> str:
        """Create new user session"""
        session_id = str(uuid.uuid4())
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO user_sessions (id, user_id, device_info, ip_address)
                    VALUES (?, ?, ?, ?)
                """, (session_id, user_id, device_info, ip_address))
                conn.commit()
                
            return session_id
            
        except Exception as e:
            logger.error(f"Error creating session: {str(e)}")
            return session_id
    
    def end_session(self, session_id: str):
        """End user session"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE user_sessions 
                    SET session_end = CURRENT_TIMESTAMP, is_active = 0
                    WHERE id = ?
                """, (session_id,))
                conn.commit()
                
        except Exception as e:
            logger.error(f"Error ending session: {str(e)}")
    
    def log_activity(self, user_id: str, session_id: str, activity_type: str, activity_data: Dict[str, Any]):
        """Log user activity"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO activity_logs (user_id, session_id, activity_type, activity_data)
                    VALUES (?, ?, ?, ?)
                """, (user_id, session_id, activity_type, json.dumps(activity_data)))
                conn.commit()
                
        except Exception as e:
            logger.error(f"Error logging activity: {str(e)}")
    
    def update_user_progress(self, user_id: str, language: str, signs_learned: int = None, 
                           accuracy_score: float = None, practice_time: int = None, level: str = None):
        """Update user progress for specific language"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if progress exists
                cursor.execute("""
                    SELECT id FROM user_progress 
                    WHERE user_id = ? AND language = ?
                """, (user_id, language))
                
                if cursor.fetchone():
                    # Update existing progress
                    updates = []
                    params = []
                    
                    if signs_learned is not None:
                        updates.append("signs_learned = signs_learned + ?")
                        params.append(signs_learned)
                    
                    if accuracy_score is not None:
                        updates.append("accuracy_score = ?")
                        params.append(accuracy_score)
                    
                    if practice_time is not None:
                        updates.append("practice_time = practice_time + ?")
                        params.append(practice_time)
                    
                    if level is not None:
                        updates.append("level = ?")
                        params.append(level)
                    
                    if updates:
                        updates.append("last_updated = CURRENT_TIMESTAMP")
                        params.extend([user_id, language])
                        
                        cursor.execute(f"""
                            UPDATE user_progress 
                            SET {', '.join(updates)}
                            WHERE user_id = ? AND language = ?
                        """, params)
                else:
                    # Create new progress entry
                    cursor.execute("""
                        INSERT INTO user_progress (user_id, language, signs_learned, accuracy_score, practice_time, level)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (user_id, language, signs_learned or 0, accuracy_score or 0.0, practice_time or 0, level or 'Beginner'))
                
                conn.commit()
                
        except Exception as e:
            logger.error(f"Error updating progress: {str(e)}")
    
    def get_user_progress(self, user_id: str, language: str = None) -> Dict[str, Any]:
        """Get user progress data"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                if language:
                    cursor.execute("""
                        SELECT language, signs_learned, accuracy_score, practice_time, level, last_updated
                        FROM user_progress 
                        WHERE user_id = ? AND language = ?
                    """, (user_id, language))
                    result = cursor.fetchone()
                    
                    if result:
                        return {
                            "language": result[0],
                            "signs_learned": result[1],
                            "accuracy_score": result[2],
                            "practice_time": result[3],
                            "level": result[4],
                            "last_updated": result[5]
                        }
                else:
                    # Get all progress
                    cursor.execute("""
                        SELECT language, signs_learned, accuracy_score, practice_time, level, last_updated
                        FROM user_progress 
                        WHERE user_id = ?
                    """, (user_id,))
                    results = cursor.fetchall()
                    
                    progress = {}
                    for result in results:
                        progress[result[0]] = {
                            "signs_learned": result[1],
                            "accuracy_score": result[2],
                            "practice_time": result[3],
                            "level": result[4],
                            "last_updated": result[5]
                        }
                    return progress
                    
        except Exception as e:
            logger.error(f"Error getting progress: {str(e)}")
            
        return {}
    
    def get_recent_activity(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent user activity"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT activity_type, activity_data, timestamp
                    FROM activity_logs 
                    WHERE user_id = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                """, (user_id, limit))
                
                activities = []
                for result in cursor.fetchall():
                    activities.append({
                        "activity_type": result[0],
                        "activity_data": json.loads(result[1]) if result[1] else {},
                        "timestamp": result[2]
                    })
                
                return activities
                
        except Exception as e:
            logger.error(f"Error getting recent activity: {str(e)}")
            return []
    
    def save_quiz_result(self, user_id: str, language: str, quiz_id: str, score: int, 
                        total_questions: int, time_taken: int, answers: Dict[str, Any]):
        """Save quiz result"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO quiz_results (user_id, language, quiz_id, score, total_questions, time_taken, answers)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (user_id, language, quiz_id, score, total_questions, time_taken, json.dumps(answers)))
                conn.commit()
                
        except Exception as e:
            logger.error(f"Error saving quiz result: {str(e)}")
    
    def get_user_stats(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive user statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get total progress across all languages
                cursor.execute("""
                    SELECT 
                        SUM(signs_learned) as total_signs,
                        AVG(accuracy_score) as avg_accuracy,
                        SUM(practice_time) as total_time
                    FROM user_progress 
                    WHERE user_id = ?
                """, (user_id,))
                progress_stats = cursor.fetchone()
                
                # Get quiz stats
                cursor.execute("""
                    SELECT 
                        COUNT(*) as quizzes_taken,
                        AVG(score * 1.0 / total_questions) as avg_quiz_score
                    FROM quiz_results 
                    WHERE user_id = ?
                """, (user_id,))
                quiz_stats = cursor.fetchone()
                
                # Get practice sessions count
                cursor.execute("""
                    SELECT COUNT(*) FROM practice_sessions 
                    WHERE user_id = ? AND end_time IS NOT NULL
                """, (user_id,))
                sessions_count = cursor.fetchone()[0]
                
                # Calculate streak
                cursor.execute("""
                    SELECT DISTINCT DATE(timestamp) as practice_date
                    FROM activity_logs 
                    WHERE user_id = ? AND activity_type IN ('practice_session', 'quiz_completed')
                    ORDER BY practice_date DESC
                    LIMIT 30
                """, (user_id,))
                practice_dates = [row[0] for row in cursor.fetchall()]
                
                streak = self._calculate_streak(practice_dates)
                
                return {
                    "total_signs_learned": progress_stats[0] or 0,
                    "average_accuracy": round((progress_stats[1] or 0) * 100, 1),
                    "total_practice_time": progress_stats[2] or 0,
                    "quizzes_completed": quiz_stats[0] or 0,
                    "average_quiz_score": round((quiz_stats[1] or 0) * 100, 1),
                    "practice_sessions": sessions_count,
                    "current_streak": streak,
                    "practice_dates": practice_dates[:7]  # Last 7 days
                }
                
        except Exception as e:
            logger.error(f"Error getting user stats: {str(e)}")
            return {}
    
    def _calculate_streak(self, practice_dates: List[str]) -> int:
        """Calculate current practice streak"""
        if not practice_dates:
            return 0
        
        today = datetime.now().date()
        streak = 0
        
        for i, date_str in enumerate(practice_dates):
            practice_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            expected_date = today - timedelta(days=i)
            
            if practice_date == expected_date:
                streak += 1
            else:
                break
        
        return streak
    
    def record_sign_attempt(self, user_id: str, session_id: str, language: str, 
                          target_sign: str, predicted_sign: str, confidence: float, 
                          is_correct: bool, feedback: str = None):
        """Record sign recognition attempt"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO sign_attempts (user_id, session_id, language, target_sign, 
                                             predicted_sign, confidence, is_correct, feedback)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (user_id, session_id, language, target_sign, predicted_sign, 
                     confidence, is_correct, feedback))
                conn.commit()
                
        except Exception as e:
            logger.error(f"Error recording sign attempt: {str(e)}")
    
    def get_language_stats(self, user_id: str) -> Dict[str, Dict[str, Any]]:
        """Get statistics per language for the user"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT 
                        language,
                        COUNT(*) as attempts,
                        AVG(confidence) as avg_confidence,
                        SUM(CASE WHEN is_correct = 1 THEN 1 ELSE 0 END) as correct_attempts
                    FROM sign_attempts 
                    WHERE user_id = ?
                    GROUP BY language
                """, (user_id,))
                
                stats = {}
                for result in cursor.fetchall():
                    language = result[0]
                    stats[language] = {
                        "total_attempts": result[1],
                        "average_confidence": round((result[2] or 0) * 100, 1),
                        "accuracy_rate": round((result[3] / result[1]) * 100, 1) if result[1] > 0 else 0,
                        "correct_attempts": result[3]
                    }
                
                return stats
                
        except Exception as e:
            logger.error(f"Error getting language stats: {str(e)}")
            return {}
