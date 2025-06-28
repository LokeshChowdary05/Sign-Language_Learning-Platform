import streamlit as st
import pandas as pd
import time
import random
from typing import Dict, List, Any

# Import custom modules
from quiz_database import QuizDatabase
from daily_challenges import DailyChallenges
from camera_manager import CameraManager, CameraInterface

# Configure Streamlit page
st.set_page_config(
    page_title="Sign Language Learning Platform",
    page_icon="🤟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
def initialize_session_state():
    """Initialize all session state variables."""
    if 'user_progress' not in st.session_state:
        st.session_state.user_progress = {
            'total_xp': 0,
            'daily_streak': 0,
            'completed_modules': [],
            'quiz_scores': {},
            'current_level': 1
        }
    
    if 'current_quiz' not in st.session_state:
        st.session_state.current_quiz = None
    
    if 'quiz_active' not in st.session_state:
        st.session_state.quiz_active = False
    
    if 'camera_manager' not in st.session_state:
        st.session_state.camera_manager = CameraManager()
    
    if 'selected_language' not in st.session_state:
        st.session_state.selected_language = "ASL"
    
    if 'selected_module' not in st.session_state:
        st.session_state.selected_module = "Basics"

def main():
    """Main application function."""
    # Initialize session state
    initialize_session_state()
    
    # Initialize components
    quiz_db = QuizDatabase()
    daily_challenges = DailyChallenges(quiz_db)
    camera_interface = CameraInterface(st.session_state.camera_manager)
    
    # Sidebar navigation
    with st.sidebar:
        st.title("🤟 Sign Language Learning")
        st.markdown("---")
        
        # Navigation menu
        page = st.selectbox(
            "Navigate to:",
            ["🏠 Home", "📚 Learn Signs", "📚 Course", "🎯 Practice \u0026 Quiz", "🏆 Daily Challenges", "📊 Progress"],
            index=0
        )
        
        st.markdown("---")
        
        # User stats sidebar
        st.subheader("👤 Your Stats")
        progress = st.session_state.user_progress
        st.metric("XP", progress['total_xp'])
        st.metric("Streak", f"{progress['daily_streak']} days")
        st.metric("Level", progress['current_level'])
        
        # Quick settings
        st.markdown("---")
        st.subheader("⚙️ Quick Settings")
        
        # Language selection
        languages = quiz_db.get_available_languages()
        selected_lang = st.selectbox("Language:", languages, 
                                   index=languages.index(st.session_state.selected_language))
        if selected_lang != st.session_state.selected_language:
            st.session_state.selected_language = selected_lang
            st.rerun()
        
        # Camera controls
        st.markdown("**Camera Controls:**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📷 Start", use_container_width=True):
                st.session_state.camera_manager.start_camera()
                st.rerun()
        with col2:
            if st.button("⏹️ Stop", use_container_width=True):
                st.session_state.camera_manager.stop_camera()
                st.rerun()
    
    # Main content area
    if page == "🏠 Home":
        show_home_page(quiz_db, camera_interface)
    elif page == "📚 Learn Signs":
        show_learn_page(quiz_db, camera_interface)
    elif page == "🎯 Practice \u0026 Quiz":
        show_practice_page(quiz_db, camera_interface)
    elif page == "🏆 Daily Challenges":
        daily_challenges.show_interface()
    elif page == "📊 Progress":
        show_progress_page(quiz_db)
    elif page == "📚 Course":
        show_course_page()

def show_home_page(quiz_db, camera_interface):
    """Display the home page."""
    st.title("🤟 Welcome to Sign Language Learning Platform")
    st.markdown("### Learn sign language through interactive lessons and real-time practice!")
    
    # Hero section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        #### 🌟 Features:
        - **Real-time Sign Recognition** - Practice with your camera
        - **Multiple Languages** - ASL, BSL, FSL and more
        - **Interactive Quizzes** - Test your knowledge
        - **Daily Challenges** - Keep your skills sharp
        - **Progress Tracking** - Monitor your improvement
        
        #### 🚀 Getting Started:
        1. Select your preferred sign language
        2. Start with the basics module
        3. Practice signs using your camera
        4. Take quizzes to test your knowledge
        5. Complete daily challenges for extra XP
        """)
        
        # Quick start buttons
        st.markdown("#### ⚡ Quick Start:")
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            if st.button("📚 Start Learning", type="primary", use_container_width=True):
                st.session_state.selected_page = "📚 Learn Signs"
                st.rerun()
        
        with col_b:
            if st.button("🎯 Take Quiz", use_container_width=True):
                st.session_state.selected_page = "🎯 Practice & Quiz"
                st.rerun()
        
        with col_c:
            if st.button("🏆 Daily Challenge", use_container_width=True):
                st.session_state.selected_page = "🏆 Daily Challenges"
                st.rerun()
    
    with col2:
        st.subheader("📸 Camera Preview")
        # Camera preview
        try:
            camera_interface.display_camera()
        except:
            st.info("📷 Start camera to see preview")
        
        # Recent activity
        st.subheader("📈 Recent Activity")
        if st.session_state.user_progress['completed_modules']:
            for module in st.session_state.user_progress['completed_modules'][-3:]:
                st.success(f"✅ Completed: {module}")
        else:
            st.info("No completed modules yet. Start learning!")

def show_learn_page(quiz_db, camera_interface):
    """Display the learning page with modules and lessons."""
    st.title("📚 Learn Sign Language")
    
    # Language and module selection
    col1, col2 = st.columns(2)
    
    with col1:
        languages = quiz_db.get_available_languages()
        selected_language = st.selectbox(
            "Select Language:",
            languages,
            index=languages.index(st.session_state.selected_language)
        )
        st.session_state.selected_language = selected_language
    
    with col2:
        modules = quiz_db.get_modules_for_language(selected_language)
        selected_module = st.selectbox(
            "Select Module:",
            modules,
            index=modules.index(st.session_state.selected_module) if st.session_state.selected_module in modules else 0
        )
        st.session_state.selected_module = selected_module
    
    # Module content
    st.markdown("---")
    
    # Get signs for the selected module
    signs = quiz_db.get_quiz_questions(selected_language, selected_module, num_questions=20)
    
    if not signs:
        st.error("No signs available for this module.")
        return
    
    # Display module overview
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(f"📖 {selected_module} Module")
        
        # Signs grid
        st.write(f"**Available Signs ({len(signs)}):**")
        
        # Create tabs for different categories
        categories = list(set(sign['category'] for sign in signs))
        if len(categories) > 1:
            tabs = st.tabs(categories)
            for i, category in enumerate(categories):
                with tabs[i]:
                    category_signs = [sign for sign in signs if sign['category'] == category]
                    display_signs_grid(category_signs, camera_interface)
        else:
            display_signs_grid(signs, camera_interface)
        
        # Practice all button
        st.markdown("---")
        col_a, col_b = st.columns(2)
        
        with col_a:
            if st.button("🎯 Practice All Signs", type="primary", use_container_width=True):
                start_practice_session(selected_language, selected_module, signs)
        
        with col_b:
            if st.button("📝 Take Module Quiz", use_container_width=True):
                start_quiz(selected_language, selected_module, quiz_db)
    
    with col2:
        st.subheader("📸 Practice Area")
        try:
            camera_interface.display_camera()
        except:
            st.info("📷 Start camera to practice")
        
        # Module progress
        st.subheader("📊 Module Progress")
        module_key = f"{selected_language}_{selected_module}"
        
        if module_key in st.session_state.user_progress['quiz_scores']:
            score = st.session_state.user_progress['quiz_scores'][module_key]
            st.metric("Best Quiz Score", f"{score:.1f}%")
            
            if score >= 70:
                st.success("✅ Module Completed!")
            else:
                st.info("🎯 Complete with 70%+ to finish module")
        else:
            st.info("📝 Take the quiz to track progress")

def display_signs_grid(signs, camera_interface):
    """Display signs in a grid layout."""
    cols_per_row = 3
    for i in range(0, len(signs), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, sign in enumerate(signs[i:i+cols_per_row]):
            with cols[j]:
                with st.container():
                    # Difficulty indicator
                    difficulty_stars = "⭐" * sign['difficulty']
                    st.markdown(f"**{sign['sign']}** {difficulty_stars}")
                    st.caption(f"Category: {sign['category'].title()}")
                    
                    if st.button(f"Practice {sign['sign']}", key=f"practice_{sign['sign']}_{i}_{j}"):
                        st.info(f"🎯 Practice: **{sign['sign']}**")
                        st.write("Show this sign to the camera!")

def start_practice_session(language, module, signs):
    """Start a practice session for all signs in the module."""
    st.session_state.practice_session = {
        'language': language,
        'module': module,
        'signs': [sign['sign'] for sign in signs],
        'current_index': 0,
        'completed': [],
        'start_time': time.time()
    }
    st.success(f"🎯 Started practice session for {module}!")
    st.rerun()

def start_quiz(language, module, quiz_db):
    """Start a quiz for the selected module."""
    quiz_questions = quiz_db.get_quiz_questions(language, module, num_questions=10)
    
    if not quiz_questions:
        st.error("No quiz questions available for this module.")
        return
    
    st.session_state.current_quiz = {
        'language': language,
        'module': module,
        'questions': quiz_questions,
        'current_question': 0,
        'score': 0,
        'start_time': time.time(),
        'answers': []
    }
    st.session_state.quiz_active = True
    st.success(f"📝 Started quiz for {module}!")
    st.rerun()

def show_practice_page(quiz_db, camera_interface):
    """Display the practice and quiz page."""
    st.title("🎯 Practice & Quiz")
    
    # Check if there's an active quiz
    if st.session_state.quiz_active and st.session_state.current_quiz:
        show_quiz_interface(quiz_db, camera_interface)
        return
    
    # Check if there's an active practice session
    if 'practice_session' in st.session_state:
        show_practice_session(camera_interface)
        return
    
    # Main practice interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎯 Quick Practice")
        
        # Practice options
        languages = quiz_db.get_available_languages()
        selected_language = st.selectbox("Choose Language:", languages)
        
        difficulty = st.select_slider(
            "Difficulty Level:",
            options=[1, 2, 3],
            value=1,
            format_func=lambda x: f"{'⭐' * x} Level {x}"
        )
        
        # Get practice questions
        practice_signs = quiz_db.get_practice_questions(selected_language, difficulty)
        
        if practice_signs:
            st.write(f"**Available Signs ({len(practice_signs)}):**")
            
            # Display practice signs
            for i, sign in enumerate(practice_signs[:6]):  # Show first 6
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.write(f"**{sign['sign']}** ({'⭐' * sign['difficulty']})")
                with col_b:
                    if st.button("Practice", key=f"practice_btn_{i}"):
                        st.info(f"🎯 Show the sign for: **{sign['sign']}**")
        
        # Quiz section
        st.markdown("---")
        st.subheader("📝 Take a Quiz")
        
        quiz_language = st.selectbox("Quiz Language:", languages, key="quiz_lang")
        modules = quiz_db.get_modules_for_language(quiz_language)
        quiz_module = st.selectbox("Quiz Module:", modules)
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            num_questions = st.slider("Number of Questions:", 5, 20, 10)
        
        with col_b:
            if st.button("🚀 Start Quiz", type="primary", use_container_width=True):
                start_quiz(quiz_language, quiz_module, quiz_db)
    
    with col2:
        st.subheader("📸 Camera Practice")
        try:
            camera_interface.display_camera()
        except:
            st.info("📷 Start camera for practice")
        
        # Quick practice signs
        st.subheader("⚡ Quick Practice")
        quick_signs = ["Hello", "Thank You", "Please", "Sorry", "Yes", "No"]
        
        for sign in quick_signs:
            if st.button(f"Practice: {sign}", key=f"quick_{sign}", use_container_width=True):
                st.info(f"🎯 Show: **{sign}**")

def show_practice_session(camera_interface):
    """Display an active practice session."""
    session = st.session_state.practice_session
    
    st.subheader(f"🎯 Practice Session: {session['module']}")
    
    # Progress
    total_signs = len(session['signs'])
    completed = len(session['completed'])
    progress = completed / total_signs if total_signs > 0 else 0
    
    st.progress(progress)
    st.write(f"Progress: {completed}/{total_signs} signs completed")
    
    # Current sign
    if session['current_index'] < total_signs:
        current_sign = session['signs'][session['current_index']]
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.info(f"🎯 **Practice Sign:** {current_sign}")
            
            # Camera area
            try:
                camera_interface.display_camera()
            except:
                st.info("📷 Camera not available")
            
            # Practice controls
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                if st.button("✅ Completed", type="primary"):
                    session['completed'].append(current_sign)
                    session['current_index'] += 1
                    st.rerun()
            
            with col_b:
                if st.button("⏭️ Skip"):
                    session['current_index'] += 1
                    st.rerun()
            
            with col_c:
                if st.button("🏠 End Session"):
                    del st.session_state.practice_session
                    st.rerun()
        
        with col2:
            st.subheader("📊 Session Stats")
            elapsed_time = time.time() - session['start_time']
            st.metric("Time Elapsed", f"{elapsed_time/60:.1f} min")
            st.metric("Signs/Min", f"{completed/(elapsed_time/60):.1f}" if elapsed_time > 0 else "0")
            
            # Completed signs
            if session['completed']:
                st.write("**Completed:**")
                for sign in session['completed'][-5:]:  # Show last 5
                    st.success(f"✅ {sign}")
    else:
        # Session completed
        st.success("🎉 Practice session completed!")
        
        elapsed_time = time.time() - session['start_time']
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Time", f"{elapsed_time/60:.1f} min")
        
        with col2:
            st.metric("Signs Completed", completed)
        
        with col3:
            st.metric("Average Speed", f"{completed/(elapsed_time/60):.1f} signs/min" if elapsed_time > 0 else "0")
        
        # Award XP
        xp_earned = completed * 5
        st.session_state.user_progress['total_xp'] += xp_earned
        st.info(f"🎉 You earned {xp_earned} XP!")
        
        if st.button("🏠 Return to Practice"):
            del st.session_state.practice_session
            st.rerun()

def show_quiz_interface(quiz_db, camera_interface):
    """Display the quiz interface."""
    quiz = st.session_state.current_quiz
    
    st.subheader(f"📝 Quiz: {quiz['module']} ({quiz['language']})")
    
    # Quiz progress
    total_questions = len(quiz['questions'])
    current_q_num = quiz['current_question'] + 1
    progress = quiz['current_question'] / total_questions if total_questions > 0 else 0
    
    st.progress(progress)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Question", f"{current_q_num}/{total_questions}")
    
    with col2:
        st.metric("Score", f"{quiz['score']}/{quiz['current_question']}" if quiz['current_question'] > 0 else "0/0")
    
    with col3:
        elapsed_time = time.time() - quiz['start_time']
        st.metric("Time", f"{elapsed_time/60:.1f} min")
    
    # Current question
    if quiz['current_question'] < total_questions:
        current_question = quiz['questions'][quiz['current_question']]
        
        st.markdown("---")
        st.info(f"🎯 **Show the sign for:** {current_question['sign']}")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Camera area
            try:
                camera_interface.display_camera()
            except:
                st.info("📷 Camera not available - using manual mode")
            
            # Manual answer options for testing
            st.write("**For testing - Select your answer:**")
            answer_options = [current_question['sign']] + random.sample(
                [q['sign'] for q in quiz['questions'] if q != current_question], 
                min(3, len(quiz['questions']) - 1)
            )
            random.shuffle(answer_options)
            
            selected_answer = st.radio("Choose your answer:", answer_options, key=f"q_{quiz['current_question']}")
            
            if st.button("Submit Answer", type="primary"):
                # Check answer
                if selected_answer == current_question['sign']:
                    quiz['score'] += 1
                    st.success("✅ Correct!")
                else:
                    st.error(f"❌ Incorrect. The answer was: {current_question['sign']}")
                
                quiz['answers'].append({
                    'question': current_question['sign'],
                    'user_answer': selected_answer,
                    'correct': selected_answer == current_question['sign']
                })
                
                quiz['current_question'] += 1
                
                # Check if quiz is complete
                if quiz['current_question'] >= total_questions:
                    complete_quiz(quiz_db)
                else:
                    st.session_state.current_quiz = quiz
                    time.sleep(1)  # Brief pause to show result
                    st.rerun()
        
        with col2:
            st.subheader("🎮 Quiz Controls")
            
            if st.button("⏭️ Skip Question"):
                quiz['current_question'] += 1
                if quiz['current_question'] >= total_questions:
                    complete_quiz(quiz_db)
                else:
                    st.rerun()
            
            if st.button("🏠 End Quiz"):
                st.session_state.quiz_active = False
                st.session_state.current_quiz = None
                st.rerun()
            
            # Show quiz progress
            st.write("**Progress:**")
            for i in range(total_questions):
                if i < quiz['current_question']:
                    st.write(f"✅ Question {i+1}")
                elif i == quiz['current_question']:
                    st.write(f"📍 Question {i+1} (current)")
                else:
                    st.write(f"⏸️ Question {i+1}")

def complete_quiz(quiz_db):
    """Complete the current quiz and show results."""
    quiz = st.session_state.current_quiz
    
    # Calculate final score
    total_questions = len(quiz['questions'])
    score = quiz['score']
    percentage = (score / total_questions) * 100 if total_questions > 0 else 0
    
    # Update user progress
    module_key = f"{quiz['language']}_{quiz['module']}"
    st.session_state.user_progress['quiz_scores'][module_key] = percentage
    
    # Award XP and check module completion
    if percentage >= 70:  # Passing score
        if quiz['module'] not in st.session_state.user_progress['completed_modules']:
            st.session_state.user_progress['completed_modules'].append(quiz['module'])
        
        # Award XP
        xp_earned = int(percentage / 10) * 10  # 10 XP per 10%
        st.session_state.user_progress['total_xp'] += xp_earned
        
        st.balloons()
        st.success(f"🎉 Quiz Completed! Score: {score}/{total_questions} ({percentage:.1f}%)")
        st.success(f"✅ Module completed! You earned {xp_earned} XP!")
    else:
        st.success(f"📝 Quiz Completed! Score: {score}/{total_questions} ({percentage:.1f}%)")
        st.info("💪 Keep practicing! You need 70% to complete the module.")
    
    # Show detailed results
    st.subheader("📊 Quiz Results")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Final Score", f"{score}/{total_questions}")
    
    with col2:
        st.metric("Percentage", f"{percentage:.1f}%")
    
    with col3:
        elapsed_time = time.time() - quiz['start_time']
        st.metric("Time Taken", f"{elapsed_time/60:.1f} min")
    
    # Show answer breakdown
    if quiz['answers']:
        st.write("**Answer Breakdown:**")
        for i, answer in enumerate(quiz['answers']):
            icon = "✅" if answer['correct'] else "❌"
            st.write(f"{icon} Q{i+1}: {answer['question']} - Your answer: {answer['user_answer']}")
    
    # Reset quiz state
    st.session_state.quiz_active = False
    st.session_state.current_quiz = None
    
    if st.button("🏠 Back to Practice"):
        st.rerun()

def show_course_page():
    """Display the comprehensive course page."""
    st.title("📚 Comprehensive Sign Language Course")
    st.markdown("### 🌟 **Most Viewed Course** - Master Sign Language from Basics to Advanced")
    
    # Course overview with tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📖 Course Overview", "📹 Video Lessons", "📝 Interactive Exercises", "🏆 Certification"])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("🎯 What You'll Learn")
            st.markdown("""
            **Module 1: Introduction to Sign Language**
            - History and importance of sign language
            - Different sign language systems worldwide
            - Basic principles and etiquette
            
            **Module 2: Alphabet and Numbers**
            - Complete fingerspelling alphabet
            - Numbers 1-100 and beyond
            - Practice exercises and games
            
            **Module 3: Common Phrases and Expressions**
            - Greetings and farewells
            - Daily conversation starters
            - Polite expressions and questions
            
            **Module 4: Grammar and Syntax**
            - Sign language sentence structure
            - Facial expressions and body language
            - Time concepts and tenses
            
            **Module 5: Advanced Communication**
            - Complex conversations
            - Professional and academic vocabulary
            - Regional variations and dialects
            """)
        
        with col2:
            st.subheader("📊 Course Stats")
            st.metric("👀 Views", "2.5M+")
            st.metric("⭐ Rating", "4.9/5")
            st.metric("🎓 Students", "150K+")
            st.metric("⏱️ Duration", "40 hours")
            
            st.info("🏆 **#1 Most Popular Course** \nJoin thousands of successful learners!")
    
    with tab2:
        st.subheader("📹 Interactive Video Lessons")
        
        lessons = [
            {
                "title": "Getting Started with Sign Language", 
                "duration": "15 min", 
                "level": "Beginner",
                "youtube_id": "Bqzh6ZQ9UzI",  # ASL Basics video
                "description": "Learn the fundamentals of sign language communication"
            },
            {
                "title": "Mastering the Alphabet", 
                "duration": "25 min", 
                "level": "Beginner",
                "youtube_id": "tkMg8g8vVUo",  # ASL Alphabet video
                "description": "Complete guide to fingerspelling the alphabet"
            },
            {
                "title": "Essential Daily Phrases", 
                "duration": "30 min", 
                "level": "Intermediate",
                "youtube_id": "ianXgNJT7jY",  # Basic phrases video
                "description": "Common phrases for everyday conversations"
            },
            {
                "title": "Advanced Grammar Concepts", 
                "duration": "45 min", 
                "level": "Advanced",
                "youtube_id": "2Euof4PnjDk",  # ASL Grammar video
                "description": "Understanding sign language sentence structure"
            },
            {
                "title": "Professional Sign Language", 
                "duration": "35 min", 
                "level": "Advanced",
                "youtube_id": "F8d_XFnmIeE",  # Professional signs video
                "description": "Workplace and formal communication in sign language"
            }
        ]
        
        # Add session state for video tracking
        if 'current_video' not in st.session_state:
            st.session_state.current_video = None
        
        for i, lesson in enumerate(lessons):
            with st.expander(f"Lesson {i+1}: {lesson['title']}", expanded=(st.session_state.current_video == i)):
                # Lesson info
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"⏱️ Duration: {lesson['duration']}")
                with col2:
                    level_color = {"Beginner": "🟢", "Intermediate": "🟡", "Advanced": "🔴"}
                    st.write(f"{level_color[lesson['level']]} Level: {lesson['level']}")
                with col3:
                    watch_button = st.button(f"▶️ Watch Video", key=f"lesson_{i}")
                
                # Description
                st.write(f"📝 {lesson['description']}")
                
                # Video player
                if watch_button or st.session_state.current_video == i:
                    st.session_state.current_video = i
                    st.markdown("---")
                    st.markdown(f"**🎬 Now Playing: {lesson['title']}**")
                    
                    # YouTube video link
                    youtube_watch_url = f"https://www.youtube.com/watch?v={lesson['youtube_id']}"
                    
                    # Create a more prominent YouTube link
                    st.markdown(
                        f"""
                        <div style="text-align: center; padding: 20px; background-color: #ff0000; border-radius: 10px; margin: 10px 0;">
                            <a href="{youtube_watch_url}" target="_blank" style="color: white; text-decoration: none; font-size: 18px; font-weight: bold;">
                                ▶️ WATCH VIDEO ON YOUTUBE
                            </a>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    st.success(f"🎥 Click the red button above to watch '{lesson['title']}' on YouTube!")
                    st.info("💡 The video will open in a new tab so you can continue learning here.")
                    
                    # Video controls
                    st.markdown("---")
                    col_a, col_b, col_c = st.columns(3)
                    
                    with col_a:
                        if st.button("📝 Take Notes", key=f"notes_{i}"):
                            st.info("✏️ Note-taking feature - Write your thoughts about this lesson!")
                    
                    with col_b:
                        if st.button("✅ Mark Complete", key=f"complete_{i}"):
                            st.success(f"🎉 Lesson {i+1} marked as complete!")
                            # Update user progress
                            if 'completed_lessons' not in st.session_state.user_progress:
                                st.session_state.user_progress['completed_lessons'] = []
                            if i not in st.session_state.user_progress['completed_lessons']:
                                st.session_state.user_progress['completed_lessons'].append(i)
                                st.session_state.user_progress['total_xp'] += 25  # Award XP
                    
                    with col_c:
                        if st.button("🔗 Open in YouTube", key=f"youtube_{i}"):
                            youtube_watch_url = f"https://www.youtube.com/watch?v={lesson['youtube_id']}"
                            st.markdown(f"[🔗 Watch on YouTube]({youtube_watch_url})")
                            st.info("Click the link above to open in YouTube app or new tab")
                
                # Show completion status
                if 'completed_lessons' in st.session_state.user_progress and i in st.session_state.user_progress['completed_lessons']:
                    st.success("✅ Completed")
    
    with tab3:
        st.subheader("📝 Interactive Practice Exercises")
        
        exercise_types = [
            {"name": "Alphabet Practice", "description": "Master fingerspelling with interactive exercises", "icon": "🔤"},
            {"name": "Vocabulary Builder", "description": "Learn essential signs with spaced repetition", "icon": "📖"},
            {"name": "Conversation Practice", "description": "Practice real-world conversations", "icon": "💬"},
            {"name": "Speed Recognition", "description": "Improve your sign recognition speed", "icon": "⚡"},
            {"name": "Grammar Exercises", "description": "Master sign language grammar rules", "icon": "📝"}
        ]
        
        cols = st.columns(2)
        for i, exercise in enumerate(exercise_types):
            with cols[i % 2]:
                with st.container():
                    st.markdown(f"### {exercise['icon']} {exercise['name']}")
                    st.write(exercise['description'])
                    if st.button(f"Start {exercise['name']}", key=f"exercise_{i}"):
                        st.info(f"Starting {exercise['name']}...")
    
    with tab4:
        st.subheader("🏆 Course Certification")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 📜 Get Certified!
            
            Complete the comprehensive course and receive:
            
            ✅ **Official Certificate of Completion**
            ✅ **Digital Badge for LinkedIn**
            ✅ **Downloadable PDF Certificate**
            ✅ **Lifetime Access to Course Materials**
            
            **Requirements:**
            - Complete all 5 modules
            - Pass final assessment with 80%+
            - Submit practice video portfolio
            """)
        
        with col2:
            st.info("📊 **Your Progress** \n\n🎯 Modules Completed: 0/5 \n📝 Assessments Passed: 0/5 \n🎥 Videos Submitted: 0/3")
            
            st.success("🚀 Ready to start your certification journey?")
    
    # Call-to-action section
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🚀 Ready to Start Learning?")
        
        if st.button("🎯 Start Course Now", type="primary", use_container_width=True):
            st.balloons()
            st.success("🎉 Welcome to the course! Let's begin your sign language journey!")
            st.info("💡 Tip: Start with Module 1 in the 'Learn Signs' section")
        
        st.markdown("---")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            if st.button("📚 Go to Learn Signs", use_container_width=True):
                st.info("Redirecting to Learn Signs page...")
        
        with col_b:
            if st.button("🎯 Take Practice Quiz", use_container_width=True):
                st.info("Redirecting to Practice & Quiz page...")

def show_progress_page(quiz_db):
    """Display the progress tracking page."""
    st.title("📊 Your Learning Progress")
    
    progress = st.session_state.user_progress
    
    # Overall stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total XP", progress['total_xp'])
    
    with col2:
        st.metric("Current Level", progress['current_level'])
    
    with col3:
        st.metric("Daily Streak", f"{progress['daily_streak']} days")
    
    with col4:
        st.metric("Modules Completed", len(progress['completed_modules']))
    
    # Progress details
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("✅ Completed Modules")
        if progress['completed_modules']:
            for module in progress['completed_modules']:
                st.success(f"✅ {module}")
        else:
            st.info("No modules completed yet. Keep learning!")
        
        # Recent achievements
        st.subheader("🏆 Recent Achievements")
        achievements = [
            "🎯 First Quiz Completed",
            "📚 Module Master",
            "🔥 Week Streak",
            "⚡ Speed Learner"
        ]
        
        for achievement in achievements:
            st.write(f"🏅 {achievement}")
    
    with col2:
        st.subheader("📈 Quiz Scores")
        
        if progress['quiz_scores']:
            # Create dataframe for quiz scores
            quiz_data = []
            for module_key, score in progress['quiz_scores'].items():
                language, module = module_key.split('_', 1)
                quiz_data.append({
                    'Language': language,
                    'Module': module,
                    'Score': f"{score:.1f}%",
                    'Status': "✅ Passed" if score >= 70 else "📝 Practice More"
                })
            
            df = pd.DataFrame(quiz_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No quiz scores yet. Take a quiz to see your progress!")
        
        # Learning statistics
        st.subheader("📊 Learning Statistics")
        
        # Mock statistics - in real app, these would be calculated
        stats = {
            "Signs Learned": random.randint(50, 200),
            "Practice Sessions": random.randint(10, 50),
            "Average Session": "12 min",
            "Favorite Category": "Greetings"
        }
        
        for stat_name, stat_value in stats.items():
            st.metric(stat_name, stat_value)

if __name__ == "__main__":
    main()
