"""
Daily Challenges System for Sign Language Learning
Provides interactive puzzles and challenges for daily practice
"""

import streamlit as st
import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import logging
import json

logger = logging.getLogger(__name__)

class DailyChallengesSystem:
    """Manages daily challenges and puzzles for sign language learning"""
    
    def __init__(self, quiz_database, progress_manager):
        """Initialize daily challenges system"""
        self.quiz_database = quiz_database
        self.progress_manager = progress_manager
        self.challenge_types = [
            "sequence_memory",
            "speed_signing", 
            "pattern_matching",
            "sign_scramble",
            "rapid_fire"
        ]
        
    def render_daily_challenges_interface(self) -> None:
        """Render the main daily challenges interface"""
        st.markdown("## 🎮 Daily Challenges")
        
        # Challenge overview
        self.render_challenge_overview()
        
        # Current daily challenge
        self.render_daily_challenge()
        
        # Additional mini challenges
        self.render_mini_challenges()
        
        # Challenge history and stats
        self.render_challenge_statistics()
    
    def render_challenge_overview(self) -> None:
        """Render challenge overview section"""
        st.markdown("### 🌟 Today's Challenge Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            streak = self.get_daily_streak()
            st.metric("🔥 Daily Streak", f"{streak} days")
        
        with col2:
            completed_today = self.get_challenges_completed_today()
            st.metric("✅ Completed Today", completed_today)
        
        with col3:
            total_xp_today = self.get_xp_earned_today()
            st.metric("🎁 XP Today", f"+{total_xp_today}")
        
        with col4:
            next_reset = self.get_next_reset_time()
            st.metric("⏰ Reset In", next_reset)
    
    def render_daily_challenge(self) -> None:
        """Render the main daily challenge"""
        st.markdown("### 🎯 Daily Challenge")
        
        daily_challenge = self.get_daily_challenge()
        
        if daily_challenge:
            # Challenge card
            with st.container():
                st.markdown(f"#### {daily_challenge['title']}")
                st.markdown(daily_challenge['description'])
                
                # Challenge progress
                progress = self.get_challenge_progress(daily_challenge['id'])
                if progress['completed']:
                    st.success("✅ Challenge Completed!")
                    st.markdown(f"**Reward:** +{daily_challenge['xp_reward']} XP")
                else:
                    # Progress bar
                    progress_percentage = (progress['current'] / progress['target']) * 100
                    st.progress(progress_percentage / 100)
                    st.markdown(f"Progress: {progress['current']}/{progress['target']}")
                    
                    # Start challenge button
                    if st.button("🚀 Start Daily Challenge", type="primary", key="start_daily_challenge"):
                        self.start_challenge(daily_challenge)
        else:
            st.info("Daily challenge will be available soon!")
    
    def render_mini_challenges(self) -> None:
        """Render mini challenges section"""
        st.markdown("### 🎲 Mini Challenges")
        
        mini_challenges = self.get_available_mini_challenges()
        
        if mini_challenges:
            cols = st.columns(min(len(mini_challenges), 3))
            
            for idx, challenge in enumerate(mini_challenges[:3]):
                with cols[idx % 3]:
                    with st.container():
                        st.markdown(f"**{challenge['title']}**")
                        st.markdown(challenge['description'])
                        st.markdown(f"⏱️ {challenge['duration']}")
                        st.markdown(f"🎁 +{challenge['xp_reward']} XP")
                        
                        if st.button(f"Start", key=f"mini_challenge_{challenge['id']}"):
                            self.start_mini_challenge(challenge)
        else:
            st.info("No mini challenges available right now. Check back later!")
    
    def render_challenge_statistics(self) -> None:
        """Render challenge statistics and history"""
        with st.expander("📊 Challenge Statistics"):
            stats = self.get_challenge_statistics()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**This Week:**")
                st.metric("Challenges Completed", stats['week']['completed'])
                st.metric("XP Earned", f"+{stats['week']['xp']}")
                st.metric("Best Streak", f"{stats['week']['best_streak']} days")
            
            with col2:
                st.markdown("**All Time:**")
                st.metric("Total Challenges", stats['all_time']['completed'])
                st.metric("Total XP", f"+{stats['all_time']['xp']}")
                st.metric("Longest Streak", f"{stats['all_time']['best_streak']} days")
    
    def get_daily_challenge(self) -> Optional[Dict[str, Any]]:
        """Get today's daily challenge"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Check if we have a cached challenge for today
        if 'daily_challenge' not in st.session_state or st.session_state.get('challenge_date') != today:
            challenge = self.generate_daily_challenge()
            st.session_state.daily_challenge = challenge
            st.session_state.challenge_date = today
        
        return st.session_state.daily_challenge
    
    def generate_daily_challenge(self) -> Dict[str, Any]:
        """Generate a new daily challenge"""
        challenge_type = random.choice(self.challenge_types)
        current_language = st.session_state.get('current_language', 'ASL')
        
        challenges = {
            "sequence_memory": {
                "id": "sequence_memory",
                "title": "🧠 Sequence Memory",
                "description": "Remember and perform a sequence of signs in the correct order",
                "type": "sequence_memory",
                "target": 5,
                "xp_reward": 50,
                "duration": "5 minutes",
                "signs": random.sample(self.quiz_database.get_practice_questions(10), 5)
            },
            "speed_signing": {
                "id": "speed_signing",
                "title": "⚡ Speed Signing",
                "description": "Perform 10 signs as quickly and accurately as possible",
                "type": "speed_signing", 
                "target": 10,
                "xp_reward": 40,
                "duration": "3 minutes",
                "signs": random.sample(self.quiz_database.get_practice_questions(15), 10)
            },
            "pattern_matching": {
                "id": "pattern_matching",
                "title": "🔍 Pattern Matching",
                "description": "Identify and perform signs that match given patterns",
                "type": "pattern_matching",
                "target": 8,
                "xp_reward": 45,
                "duration": "4 minutes",
                "patterns": self.generate_sign_patterns()
            },
            "sign_scramble": {
                "id": "sign_scramble",
                "title": "🔤 Sign Scramble",
                "description": "Unscramble the letters to form sign names, then perform them",
                "type": "sign_scramble",
                "target": 6,
                "xp_reward": 35,
                "duration": "4 minutes",
                "scrambled_signs": self.generate_scrambled_signs()
            },
            "rapid_fire": {
                "id": "rapid_fire",
                "title": "🔥 Rapid Fire",
                "description": "Quickly respond to random sign prompts",
                "type": "rapid_fire",
                "target": 15,
                "xp_reward": 60,
                "duration": "2 minutes",
                "signs": random.sample(self.quiz_database.get_practice_questions(20), 15)
            }
        }
        
        return challenges[challenge_type]
    
    def get_available_mini_challenges(self) -> List[Dict[str, Any]]:
        """Get available mini challenges"""
        mini_challenges = [
            {
                "id": "quick_practice",
                "title": "Quick Practice",
                "description": "5 random signs",
                "duration": "2 min",
                "xp_reward": 15,
                "signs_count": 5
            },
            {
                "id": "alphabet_drill",
                "title": "Alphabet Drill", 
                "description": "Sign the alphabet",
                "duration": "3 min",
                "xp_reward": 20,
                "type": "alphabet"
            },
            {
                "id": "number_challenge",
                "title": "Number Challenge",
                "description": "Sign numbers 1-10",
                "duration": "2 min", 
                "xp_reward": 15,
                "type": "numbers"
            }
        ]
        
        # Filter out completed challenges
        available = []
        for challenge in mini_challenges:
            if not self.is_mini_challenge_completed_today(challenge['id']):
                available.append(challenge)
        
        return available
    
    def start_challenge(self, challenge: Dict[str, Any]) -> None:
        """Start a daily challenge"""
        try:
            st.session_state.active_challenge = {
                "challenge": challenge,
                "start_time": time.time(),
                "current_step": 0,
                "score": 0,
                "completed_signs": [],
                "type": "daily"
            }
            
            if challenge['type'] == 'sequence_memory':
                self.start_sequence_memory_challenge(challenge)
            elif challenge['type'] == 'speed_signing':
                self.start_speed_signing_challenge(challenge)
            elif challenge['type'] == 'pattern_matching':
                self.start_pattern_matching_challenge(challenge)
            elif challenge['type'] == 'sign_scramble':
                self.start_sign_scramble_challenge(challenge)
            elif challenge['type'] == 'rapid_fire':
                self.start_rapid_fire_challenge(challenge)
            
            st.rerun()
            
        except Exception as e:
            st.error(f"Error starting challenge: {str(e)}")
            logger.error(f"Challenge start error: {str(e)}")
    
    def start_mini_challenge(self, challenge: Dict[str, Any]) -> None:
        """Start a mini challenge"""
        try:
            st.session_state.active_challenge = {
                "challenge": challenge,
                "start_time": time.time(),
                "current_step": 0,
                "score": 0,
                "completed_signs": [],
                "type": "mini"
            }
            
            if challenge['id'] == 'quick_practice':
                signs = random.sample(self.quiz_database.get_practice_questions(10), 5)
                st.session_state.active_challenge['signs'] = signs
            elif challenge['id'] == 'alphabet_drill':
                alphabet_signs = [{'sign': chr(i)} for i in range(ord('A'), ord('Z')+1)]
                st.session_state.active_challenge['signs'] = alphabet_signs
            elif challenge['id'] == 'number_challenge':
                number_signs = [{'sign': str(i)} for i in range(1, 11)]
                st.session_state.active_challenge['signs'] = number_signs
            
            st.success(f"🚀 {challenge['title']} started!")
            st.rerun()
            
        except Exception as e:
            st.error(f"Error starting mini challenge: {str(e)}")
            logger.error(f"Mini challenge start error: {str(e)}")
    
    def start_sequence_memory_challenge(self, challenge: Dict[str, Any]) -> None:
        """Start sequence memory challenge"""
        st.markdown("## 🧠 Sequence Memory Challenge")
        st.info("Memorize the sequence of signs, then perform them in order!")
        
        # Show sequence for memorization
        st.markdown("### Memorize this sequence:")
        
        sequence = challenge['signs'][:5]  # Take first 5 signs
        for i, sign_data in enumerate(sequence, 1):
            st.markdown(f"{i}. **{sign_data['sign'].upper()}**")
        
        # Timer for memorization
        memorization_time = 30  # 30 seconds
        if st.button("I've memorized it - Start signing!", type="primary"):
            st.session_state.challenge_phase = "signing"
            st.session_state.sequence_to_sign = sequence
            st.rerun()
    
    def start_speed_signing_challenge(self, challenge: Dict[str, Any]) -> None:
        """Start speed signing challenge"""
        st.markdown("## ⚡ Speed Signing Challenge")
        st.info("Sign as many signs as possible quickly and accurately!")
        
        if 'challenge_phase' not in st.session_state:
            st.session_state.challenge_phase = "ready"
        
        if st.session_state.challenge_phase == "ready":
            st.markdown("### Ready to start?")
            if st.button("🚀 Start Speed Challenge!", type="primary"):
                st.session_state.challenge_phase = "active"
                st.session_state.speed_challenge_start = time.time()
                st.session_state.current_sign_index = 0
                st.rerun()
        
        elif st.session_state.challenge_phase == "active":
            self.render_active_speed_challenge(challenge)
    
    def start_pattern_matching_challenge(self, challenge: Dict[str, Any]) -> None:
        """Start pattern matching challenge"""
        st.markdown("## 🔍 Pattern Matching Challenge")
        st.info("Find and perform signs that match the given patterns!")
        
        patterns = challenge.get('patterns', [])
        if patterns:
            current_pattern = patterns[0] if patterns else None
            if current_pattern:
                st.markdown(f"### Find signs that: {current_pattern['description']}")
                st.markdown("**Examples:** " + ", ".join(current_pattern['examples']))
        
        if st.button("Start Pattern Challenge!", type="primary"):
            st.session_state.challenge_phase = "active"
            st.rerun()
    
    def start_sign_scramble_challenge(self, challenge: Dict[str, Any]) -> None:
        """Start sign scramble challenge"""
        st.markdown("## 🔤 Sign Scramble Challenge")
        st.info("Unscramble the letters to form sign names, then perform them!")
        
        scrambled = challenge.get('scrambled_signs', [])
        if scrambled:
            current_scramble = scrambled[0] if scrambled else None
            if current_scramble:
                st.markdown(f"### Unscramble: **{current_scramble['scrambled']}**")
                
                user_answer = st.text_input("Your answer:", key="scramble_answer")
                
                if st.button("Submit Answer"):
                    if user_answer.lower() == current_scramble['original'].lower():
                        st.success("Correct! Now perform the sign.")
                        st.session_state.challenge_phase = "perform_sign"
                        st.session_state.current_sign = current_scramble['original']
                    else:
                        st.error("Try again!")
    
    def start_rapid_fire_challenge(self, challenge: Dict[str, Any]) -> None:
        """Start rapid fire challenge"""
        st.markdown("## 🔥 Rapid Fire Challenge")
        st.info("Quickly respond to sign prompts as they appear!")
        
        if st.button("Start Rapid Fire!", type="primary"):
            st.session_state.challenge_phase = "active"
            st.session_state.rapid_fire_start = time.time()
            st.session_state.current_prompt_index = 0
            st.rerun()
    
    def render_active_speed_challenge(self, challenge: Dict[str, Any]) -> None:
        """Render active speed signing challenge"""
        current_index = st.session_state.get('current_sign_index', 0)
        signs = challenge['signs']
        
        if current_index < len(signs):
            current_sign = signs[current_index]['sign']
            
            # Time remaining
            elapsed = time.time() - st.session_state.speed_challenge_start
            time_limit = 180  # 3 minutes
            remaining = max(0, time_limit - elapsed)
            
            st.markdown(f"### Current Sign: **{current_sign.upper()}**")
            st.markdown(f"⏱️ Time Remaining: {int(remaining)}s")
            st.markdown(f"Progress: {current_index + 1}/{len(signs)}")
            
            # Progress bar
            progress = (current_index + 1) / len(signs)
            st.progress(progress)
            
            if remaining <= 0:
                self.complete_speed_challenge(challenge, current_index)
            else:
                if st.button("✅ Signed it!", key=f"speed_sign_{current_index}"):
                    st.session_state.current_sign_index += 1
                    if st.session_state.current_sign_index >= len(signs):
                        self.complete_speed_challenge(challenge, len(signs))
                    st.rerun()
        else:
            self.complete_speed_challenge(challenge, len(signs))
    
    def complete_speed_challenge(self, challenge: Dict[str, Any], completed_signs: int) -> None:
        """Complete speed signing challenge"""
        elapsed = time.time() - st.session_state.speed_challenge_start
        
        st.balloons()
        st.success("🎉 Speed Challenge Completed!")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Signs Completed", completed_signs)
        with col2:
            st.metric("Time Taken", f"{elapsed:.1f}s")
        with col3:
            signs_per_minute = (completed_signs / elapsed) * 60 if elapsed > 0 else 0
            st.metric("Signs/Minute", f"{signs_per_minute:.1f}")
        
        # Award XP
        base_xp = challenge['xp_reward']
        bonus_xp = max(0, (challenge['target'] - completed_signs) * 5)
        total_xp = base_xp + bonus_xp
        
        st.success(f"🎁 +{total_xp} XP earned!")
        
        # Mark challenge as completed
        self.mark_challenge_completed(challenge['id'], {
            'completed_signs': completed_signs,
            'time_taken': elapsed,
            'xp_earned': total_xp
        })
        
        # Clear session state
        if 'active_challenge' in st.session_state:
            del st.session_state.active_challenge
        if 'challenge_phase' in st.session_state:
            del st.session_state.challenge_phase
    
    def generate_sign_patterns(self) -> List[Dict[str, Any]]:
        """Generate sign patterns for pattern matching"""
        patterns = [
            {
                "description": "contain the letter 'A'",
                "examples": ["Apple", "Water", "Amazing"],
                "criteria": lambda sign: 'a' in sign.lower()
            },
            {
                "description": "start with a consonant",
                "examples": ["Book", "Cat", "Dog"],
                "criteria": lambda sign: sign[0].lower() not in 'aeiou'
            },
            {
                "description": "have 4 or more letters",
                "examples": ["House", "Computer", "Happy"],
                "criteria": lambda sign: len(sign) >= 4
            }
        ]
        return patterns
    
    def generate_scrambled_signs(self) -> List[Dict[str, str]]:
        """Generate scrambled signs for word puzzle"""
        signs = ["HELLO", "THANK", "WATER", "HAPPY", "HOUSE", "APPLE"]
        scrambled = []
        
        for sign in signs:
            scrambled_letters = list(sign)
            random.shuffle(scrambled_letters)
            scrambled.append({
                "original": sign,
                "scrambled": "".join(scrambled_letters)
            })
        
        return scrambled
    
    def get_daily_streak(self) -> int:
        """Get current daily streak"""
        # Implement streak calculation based on completion history
        return st.session_state.get('daily_streak', 0)
    
    def get_challenges_completed_today(self) -> int:
        """Get number of challenges completed today"""
        today = datetime.now().strftime("%Y-%m-%d")
        completed_today = st.session_state.get(f'challenges_completed_{today}', 0)
        return completed_today
    
    def get_xp_earned_today(self) -> int:
        """Get XP earned today from challenges"""
        today = datetime.now().strftime("%Y-%m-%d")
        xp_today = st.session_state.get(f'challenge_xp_{today}', 0)
        return xp_today
    
    def get_next_reset_time(self) -> str:
        """Get time until next daily reset"""
        now = datetime.now()
        tomorrow = now + timedelta(days=1)
        next_reset = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
        time_diff = next_reset - now
        
        hours = time_diff.seconds // 3600
        minutes = (time_diff.seconds % 3600) // 60
        
        return f"{hours}h {minutes}m"
    
    def get_challenge_progress(self, challenge_id: str) -> Dict[str, Any]:
        """Get progress for a specific challenge"""
        today = datetime.now().strftime("%Y-%m-%d")
        progress_key = f"challenge_progress_{challenge_id}_{today}"
        
        default_progress = {"current": 0, "target": 1, "completed": False}
        return st.session_state.get(progress_key, default_progress)
    
    def get_challenge_statistics(self) -> Dict[str, Any]:
        """Get challenge statistics"""
        # Mock statistics - implement with real data storage
        return {
            "week": {
                "completed": 5,
                "xp": 250,
                "best_streak": 3
            },
            "all_time": {
                "completed": 45,
                "xp": 2250,
                "best_streak": 7
            }
        }
    
    def is_mini_challenge_completed_today(self, challenge_id: str) -> bool:
        """Check if mini challenge is completed today"""
        today = datetime.now().strftime("%Y-%m-%d")
        completed_key = f"mini_challenge_{challenge_id}_{today}"
        return st.session_state.get(completed_key, False)
    
    def mark_challenge_completed(self, challenge_id: str, results: Dict[str, Any]) -> None:
        """Mark a challenge as completed"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Mark challenge as completed
        progress_key = f"challenge_progress_{challenge_id}_{today}"
        st.session_state[progress_key] = {
            "current": results.get('completed_signs', 1),
            "target": 1,
            "completed": True
        }
        
        # Update daily totals
        challenges_key = f'challenges_completed_{today}'
        st.session_state[challenges_key] = st.session_state.get(challenges_key, 0) + 1
        
        xp_key = f'challenge_xp_{today}'
        st.session_state[xp_key] = st.session_state.get(xp_key, 0) + results.get('xp_earned', 0)
        
        # Update streak
        self.update_daily_streak()
    
    def update_daily_streak(self) -> None:
        """Update the daily streak counter"""
        today = datetime.now().strftime("%Y-%m-%d")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        # Check if completed yesterday
        yesterday_completed = st.session_state.get(f'challenges_completed_{yesterday}', 0) > 0
        
        if yesterday_completed:
            st.session_state['daily_streak'] = st.session_state.get('daily_streak', 0) + 1
        else:
            st.session_state['daily_streak'] = 1  # Start new streak
