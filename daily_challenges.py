import streamlit as st
import time
import random
from typing import Dict, List, Any
from datetime import datetime, timedelta

class DailyChallenges:
    """
    Manages daily challenges and mini-challenges for sign language learning.
    Provides various challenge types with scoring and progress tracking.
    """
    
    def __init__(self, quiz_db):
        self.quiz_db = quiz_db
        self.challenge_types = {
            "speed_signing": {
                "name": "Speed Signing",
                "description": "Sign as many words as possible in the time limit",
                "icon": "⚡",
                "time_limit": 60,
                "scoring": "signs_per_minute"
            },
            "sequence_memory": {
                "name": "Sequence Memory",
                "description": "Remember and repeat the sequence of signs",
                "icon": "🧠",
                "time_limit": 120,
                "scoring": "sequence_length"
            },
            "pattern_matching": {
                "name": "Pattern Matching",
                "description": "Match the pattern shown with correct signs",
                "icon": "🔄",
                "time_limit": 90,
                "scoring": "patterns_completed"
            },
            "sign_scramble": {
                "name": "Sign Scramble",
                "description": "Unscramble the letters to form sign words",
                "icon": "🔤",
                "time_limit": 180,
                "scoring": "words_unscrambled"
            },
            "rapid_fire": {
                "name": "Rapid Fire",
                "description": "Quick fire questions with immediate signing",
                "icon": "🔥",
                "time_limit": 45,
                "scoring": "correct_signs"
            }
        }
        
        # Initialize session state for challenges
        if 'daily_challenge_completed' not in st.session_state:
            st.session_state.daily_challenge_completed = False
        if 'challenge_stats' not in st.session_state:
            st.session_state.challenge_stats = {
                'total_completed': 0,
                'best_scores': {},
                'streak': 0,
                'last_completed': None
            }
        if 'current_challenge' not in st.session_state:
            st.session_state.current_challenge = None
    
    def show_interface(self):
        """Main interface for daily challenges."""
        st.title("🏆 Daily Challenges")
        
        # Show daily challenge status
        self._show_daily_status()
        
        # Navigation tabs
        tab1, tab2, tab3, tab4 = st.tabs(["Today's Challenge", "Mini Challenges", "Leaderboard", "Statistics"])
        
        with tab1:
            self._show_daily_challenge()
        
        with tab2:
            self._show_mini_challenges()
        
        with tab3:
            self._show_leaderboard()
        
        with tab4:
            self._show_statistics()
    
    def _show_daily_status(self):
        """Display daily challenge completion status."""
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.session_state.daily_challenge_completed:
                st.success("✅ Today's Challenge Complete!")
            else:
                st.info("🎯 Daily Challenge Available")
        
        with col2:
            streak = st.session_state.challenge_stats['streak']
            st.metric("🔥 Current Streak", f"{streak} days")
        
        with col3:
            total = st.session_state.challenge_stats['total_completed']
            st.metric("🏆 Total Completed", total)
    
    def _show_daily_challenge(self):
        """Show the main daily challenge."""
        st.subheader("🌟 Today's Featured Challenge")
        
        if st.session_state.daily_challenge_completed:
            st.success("🎉 You've already completed today's challenge! Come back tomorrow for a new one.")
            self._show_challenge_results()
            return
        
        # Get today's challenge
        today_challenge = self._get_todays_challenge()
        
        # Display challenge info
        challenge_info = self.challenge_types[today_challenge['type']]
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"""
            ### {challenge_info['icon']} {challenge_info['name']}
            
            **Description:** {challenge_info['description']}
            
            **Time Limit:** {challenge_info['time_limit']} seconds
            
            **Scoring:** {challenge_info['scoring'].replace('_', ' ').title()}
            """)
        
        with col2:
            if st.button("🚀 Start Challenge", type="primary", use_container_width=True):
                st.session_state.current_challenge = today_challenge
                st.rerun()
        
        # Run active challenge
        if st.session_state.current_challenge:
            self._run_challenge(st.session_state.current_challenge)
    
    def _show_mini_challenges(self):
        """Show quick mini-challenges."""
        st.subheader("⚡ Quick Mini Challenges")
        st.write("Perfect for a quick practice session!")
        
        # Create mini challenges grid
        col1, col2 = st.columns(2)
        
        mini_challenges = [
            {"name": "5-Sign Sprint", "type": "speed_signing", "duration": 30, "target": 5},
            {"name": "Number Sequence", "type": "sequence_memory", "duration": 45, "target": "1-10"},
            {"name": "Color Match", "type": "pattern_matching", "duration": 60, "target": "colors"},
            {"name": "Family Signs", "type": "rapid_fire", "duration": 30, "target": "family"}
        ]
        
        for i, challenge in enumerate(mini_challenges):
            with col1 if i % 2 == 0 else col2:
                with st.container():
                    st.markdown(f"**{challenge['name']}**")
                    st.write(f"⏱️ {challenge['duration']}s | 🎯 {challenge['target']}")
                    
                    if st.button(f"Start {challenge['name']}", key=f"mini_{i}"):
                        self._start_mini_challenge(challenge)
    
    def _show_leaderboard(self):
        """Show challenge leaderboard."""
        st.subheader("🏅 Challenge Leaderboard")
        
        # Mock leaderboard data
        leaderboard_data = [
            {"rank": 1, "name": "SignMaster", "score": 2850, "streak": 15},
            {"rank": 2, "name": "HandsUp", "score": 2720, "streak": 12},
            {"rank": 3, "name": "QuickSigns", "score": 2680, "streak": 8},
            {"rank": 4, "name": "You", "score": st.session_state.challenge_stats.get('total_score', 2400), "streak": st.session_state.challenge_stats['streak']},
            {"rank": 5, "name": "GestureGuru", "score": 2350, "streak": 5}
        ]
        
        for entry in leaderboard_data:
            col1, col2, col3, col4 = st.columns([1, 3, 2, 2])
            
            with col1:
                if entry["rank"] <= 3:
                    medal = ["🥇", "🥈", "🥉"][entry["rank"] - 1]
                    st.write(f"{medal}")
                else:
                    st.write(f"#{entry['rank']}")
            
            with col2:
                style = "**" if entry["name"] == "You" else ""
                st.write(f"{style}{entry['name']}{style}")
            
            with col3:
                st.write(f"🏆 {entry['score']}")
            
            with col4:
                st.write(f"🔥 {entry['streak']}")
    
    def _show_statistics(self):
        """Show detailed challenge statistics."""
        st.subheader("📊 Your Challenge Statistics")
        
        stats = st.session_state.challenge_stats
        
        # Overall stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Challenges Completed", stats['total_completed'])
        
        with col2:
            st.metric("Best Streak", stats.get('best_streak', stats['streak']))
        
        with col3:
            avg_score = stats.get('average_score', 0)
            st.metric("Average Score", f"{avg_score:.0f}")
        
        with col4:
            completion_rate = stats.get('completion_rate', 0)
            st.metric("Completion Rate", f"{completion_rate:.1%}")
        
        # Best scores by challenge type
        st.subheader("🏆 Best Scores by Challenge Type")
        
        if stats['best_scores']:
            for challenge_type, score in stats['best_scores'].items():
                challenge_info = self.challenge_types.get(challenge_type, {})
                icon = challenge_info.get('icon', '🏆')
                name = challenge_info.get('name', challenge_type.title())
                st.write(f"{icon} **{name}:** {score}")
        else:
            st.info("Complete some challenges to see your best scores!")
    
    def _get_todays_challenge(self) -> Dict[str, Any]:
        """Get today's featured challenge based on the date."""
        # Use date as seed for consistent daily challenge
        today = datetime.now().date()
        random.seed(int(today.strftime("%Y%m%d")))
        
        challenge_type = random.choice(list(self.challenge_types.keys()))
        challenge_signs = self._get_challenge_signs(challenge_type)
        
        return {
            "type": challenge_type,
            "signs": challenge_signs,
            "date": today,
            "difficulty": random.choice([1, 2, 3])
        }
    
    def _get_challenge_signs(self, challenge_type: str) -> List[str]:
        """Get appropriate signs for a challenge type."""
        # Get signs from quiz database
        languages = self.quiz_db.get_available_languages()
        language = random.choice(languages)
        
        if challenge_type == "speed_signing":
            signs = self.quiz_db.get_practice_questions(language, difficulty=1)
        elif challenge_type == "sequence_memory":
            signs = self.quiz_db.get_signs_by_category(language, "numbers")
        elif challenge_type == "pattern_matching":
            signs = self.quiz_db.get_signs_by_category(language, "colors")
        elif challenge_type == "sign_scramble":
            signs = self.quiz_db.get_practice_questions(language, difficulty=2)
        else:  # rapid_fire
            signs = self.quiz_db.get_signs_by_category(language, "greetings")
        
        # Extract sign names
        sign_names = [sign["sign"] for sign in signs[:10]]
        return sign_names if sign_names else ["Hello", "Thank You", "Please", "Sorry", "Yes"]
    
    def _run_challenge(self, challenge: Dict[str, Any]):
        """Run an active challenge."""
        challenge_info = self.challenge_types[challenge['type']]
        
        st.markdown("---")
        st.subheader(f"🎮 {challenge_info['name']} - In Progress")
        
        # Initialize challenge state
        if 'challenge_start_time' not in st.session_state:
            st.session_state.challenge_start_time = time.time()
            st.session_state.challenge_score = 0
            st.session_state.challenge_completed_signs = []
        
        # Calculate remaining time
        elapsed_time = time.time() - st.session_state.challenge_start_time
        remaining_time = max(0, challenge_info['time_limit'] - elapsed_time)
        
        # Display timer and score
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("⏱️ Time Left", f"{remaining_time:.0f}s")
        
        with col2:
            st.metric("🏆 Score", st.session_state.challenge_score)
        
        with col3:
            st.metric("✅ Completed", len(st.session_state.challenge_completed_signs))
        
        if remaining_time > 0:
            # Run specific challenge logic
            if challenge['type'] == "speed_signing":
                self._run_speed_signing(challenge)
            elif challenge['type'] == "sequence_memory":
                self._run_sequence_memory(challenge)
            elif challenge['type'] == "pattern_matching":
                self._run_pattern_matching(challenge)
            elif challenge['type'] == "sign_scramble":
                self._run_sign_scramble(challenge)
            elif challenge['type'] == "rapid_fire":
                self._run_rapid_fire(challenge)
        else:
            # Challenge completed
            self._complete_challenge(challenge)
    
    def _run_speed_signing(self, challenge: Dict[str, Any]):
        """Run speed signing challenge."""
        st.write("🎯 **Show the following signs as quickly as possible:**")
        
        current_sign_index = len(st.session_state.challenge_completed_signs)
        
        if current_sign_index < len(challenge['signs']):
            current_sign = challenge['signs'][current_sign_index]
            st.info(f"**Current Sign:** {current_sign}")
            
            # Mock sign detection - in real app, this would use camera
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Sign Completed", key="sign_done"):
                    st.session_state.challenge_completed_signs.append(current_sign)
                    st.session_state.challenge_score += 10
                    st.rerun()
            
            with col2:
                if st.button("⏭️ Skip Sign", key="skip_sign"):
                    st.session_state.challenge_completed_signs.append(f"{current_sign} (skipped)")
                    st.rerun()
        else:
            st.success("🎉 All signs completed! Waiting for time to end...")
    
    def _run_sequence_memory(self, challenge: Dict[str, Any]):
        """Run sequence memory challenge."""
        st.write("🧠 **Remember this sequence, then repeat it:**")
        
        sequence = challenge['signs'][:5]  # Use first 5 signs
        st.write(" → ".join(sequence))
        
        st.write("**Now repeat the sequence:**")
        user_sequence = st.text_input("Enter the sequence (comma-separated):")
        
        if st.button("Submit Sequence"):
            user_signs = [s.strip() for s in user_sequence.split(',')]
            if user_signs == sequence:
                st.session_state.challenge_score += 50
                st.success("✅ Correct sequence!")
            else:
                st.error("❌ Incorrect sequence. Try again!")
    
    def _run_pattern_matching(self, challenge: Dict[str, Any]):
        """Run pattern matching challenge."""
        st.write("🔄 **Match the pattern:**")
        
        pattern = challenge['signs'][:4]
        st.write(f"Pattern: {' → '.join(pattern)}")
        
        # Create options for matching
        options = pattern + random.sample(challenge['signs'], 2)
        random.shuffle(options)
        
        selected = st.multiselect("Select signs in the correct order:", options)
        
        if st.button("Check Pattern"):
            if selected == pattern:
                st.session_state.challenge_score += 30
                st.success("✅ Pattern matched!")
            else:
                st.error("❌ Pattern doesn't match. Try again!")
    
    def _run_sign_scramble(self, challenge: Dict[str, Any]):
        """Run sign scramble challenge."""
        st.write("🔤 **Unscramble these sign words:**")
        
        if 'scrambled_words' not in st.session_state:
            st.session_state.scrambled_words = []
            for sign in challenge['signs'][:3]:
                letters = list(sign.replace(' ', ''))
                random.shuffle(letters)
                st.session_state.scrambled_words.append(''.join(letters))
        
        for i, scrambled in enumerate(st.session_state.scrambled_words):
            st.write(f"**Word {i+1}:** {scrambled}")
            answer = st.text_input(f"Unscrambled word {i+1}:", key=f"unscramble_{i}")
            
            if answer.lower().replace(' ', '') == challenge['signs'][i].lower().replace(' ', ''):
                st.success(f"✅ Correct! The word is: {challenge['signs'][i]}")
    
    def _run_rapid_fire(self, challenge: Dict[str, Any]):
        """Run rapid fire challenge."""
        st.write("🔥 **Quick! Show these signs one after another:**")
        
        signs_remaining = challenge['signs'][len(st.session_state.challenge_completed_signs):]
        
        if signs_remaining:
            current_sign = signs_remaining[0]
            st.info(f"**Show:** {current_sign}")
            
            if st.button("✅ Done!", key="rapid_done"):
                st.session_state.challenge_completed_signs.append(current_sign)
                st.session_state.challenge_score += 5
                st.rerun()
    
    def _complete_challenge(self, challenge: Dict[str, Any]):
        """Complete the current challenge and update stats."""
        st.markdown("---")
        st.subheader("🎉 Challenge Completed!")
        
        final_score = st.session_state.challenge_score
        
        # Update stats
        stats = st.session_state.challenge_stats
        stats['total_completed'] += 1
        
        # Update best score for this challenge type
        challenge_type = challenge['type']
        if challenge_type not in stats['best_scores'] or final_score > stats['best_scores'][challenge_type]:
            stats['best_scores'][challenge_type] = final_score
        
        # Update streak
        today = datetime.now().date()
        if stats['last_completed'] == today - timedelta(days=1):
            stats['streak'] += 1
        else:
            stats['streak'] = 1
        stats['last_completed'] = today
        
        # Show results
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("🏆 Final Score", final_score)
        
        with col2:
            st.metric("✅ Signs Completed", len(st.session_state.challenge_completed_signs))
        
        with col3:
            efficiency = (final_score / max(1, len(challenge['signs']))) * 100
            st.metric("⚡ Efficiency", f"{efficiency:.0f}%")
        
        # Mark daily challenge as completed
        if challenge.get('is_daily', True):
            st.session_state.daily_challenge_completed = True
        
        # Reset challenge state
        if st.button("🏠 Return to Challenges"):
            st.session_state.current_challenge = None
            for key in ['challenge_start_time', 'challenge_score', 'challenge_completed_signs', 'scrambled_words']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    def _show_challenge_results(self):
        """Show results of completed daily challenge."""
        st.subheader("📊 Today's Results")
        
        # Mock results - in real app, this would come from stored data
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("🏆 Your Score", "850")
        
        with col2:
            st.metric("🎯 Accuracy", "92%")
        
        with col3:
            st.metric("⚡ Speed", "15 signs/min")
        
        st.info("🎉 Great job! You earned 50 XP and maintained your streak!")
    
    def _start_mini_challenge(self, challenge: Dict[str, Any]):
        """Start a mini challenge."""
        st.session_state.current_challenge = {
            **challenge,
            'signs': self._get_challenge_signs(challenge['type']),
            'is_daily': False
        }
        st.rerun()
