"""Practice page for MathBlitz - Modern Clean Design"""
import streamlit as st
import time
from typing import Dict, Any

from frontend.styles.css import custom_css
from frontend.components.cards import render_formula_box
from frontend.components.modals import render_calculation_breakdown, render_share_buttons, render_timer_display
from services import ExerciseService, ProgressService, LeaderboardService, SoundService
from config.settings import EXERCISE_NAMES, DIFFICULTY_SETTINGS


def render_practice_page() -> None:
    """
    Render the main practice page
    """
    custom_css()
    
    # Initialize services
    exercise_service = ExerciseService()
    progress_service = ProgressService()
    leaderboard_service = LeaderboardService()
    sound_service = SoundService()
    
    # Get settings
    settings = st.session_state.get("settings", {})
    sound_enabled = settings.get("sound_enabled", True)
    
    # Header section
    st.markdown('<h2 class="page-title">🎮 Activity - Math Games</h2>', unsafe_allow_html=True)
    
    # Exercise and difficulty selectors
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        default_exercise = settings.get("default_exercise", "Cash Counting")
        exercise_idx = EXERCISE_NAMES.index(default_exercise) if default_exercise in EXERCISE_NAMES else 0
        exercise = st.selectbox(
            "🎯 Exercise",
            EXERCISE_NAMES,
            index=exercise_idx,
            label_visibility="collapsed"
        )
    
    with col2:
        default_difficulty = settings.get("default_difficulty", "Medium")
        difficulty_idx = ["Easy", "Medium", "Hard"].index(default_difficulty)
        difficulty = st.selectbox(
            "📊 Difficulty",
            ["Easy", "Medium", "Hard"],
            index=difficulty_idx,
            label_visibility="collapsed"
        )
    
    with col3:
        time_limit = DIFFICULTY_SETTINGS[difficulty]["time_limit"]
        if "start_time" in st.session_state:
            elapsed = time.time() - st.session_state.start_time
            remaining = max(0, time_limit - elapsed)
            render_timer_display(remaining, difficulty)
            
            # Handle timeout
            if remaining <= 0 and not st.session_state.get("task_submitted", False):
                _handle_timeout(progress_service, sound_enabled)
                st.rerun()
    
    st.markdown("---")
    
    # Show formula
    formula = exercise_service.get_formula(exercise)
    if formula:
        render_formula_box(
            icon=formula.get("icon", "📐"),
            formula=formula.get("formula", ""),
            example=formula.get("example", ""),
            tip=formula.get("tip", "")
        )
    
    # New Task button
    if not st.session_state.get("current_task") or not st.session_state.get("task_submitted", False):
        if st.button("✨ New Task", type="primary", use_container_width=True):
            _generate_new_task(exercise_service, sound_service, sound_enabled, exercise, difficulty)
            st.rerun()
    
    # Handle result display and auto-advance
    if st.session_state.get("show_result", False):
        _handle_result_display(
            exercise_service,
            progress_service,
            leaderboard_service,
            sound_enabled,
            exercise,
            difficulty
        )
    
    # Show current task
    if st.session_state.get("current_task"):
        _render_current_task(
            exercise_service,
            progress_service,
            sound_service,
            sound_enabled,
            exercise,
            difficulty
        )


def _generate_new_task(
    exercise_service: ExerciseService,
    sound_service: SoundService,
    sound_enabled: bool,
    exercise: str,
    difficulty: str
) -> None:
    """Generate a new task"""
    st.session_state.task_key = st.session_state.get("task_key", 0) + 1
    st.session_state.current_task = exercise_service.generate_task(exercise, difficulty)
    st.session_state.start_time = time.time()
    st.session_state.task_submitted = False
    st.session_state.show_result = False
    sound_service.play_new_task(sound_enabled)


def _handle_timeout(
    progress_service: ProgressService,
    sound_enabled: bool
) -> None:
    """Handle timeout when time runs out"""
    from datetime import datetime
    
    # Create timeout entry
    entry = {
        "Timestamp": datetime.now().isoformat(),
        "Mode": st.session_state.get("current_task", {}).get("exercise", "Unknown"),
        "Exercise": st.session_state.get("current_task", {}).get("exercise", "Unknown"),
        "Difficulty": st.session_state.get("selected_difficulty", "Medium"),
        "UserAnswer": 0,
        "CorrectAnswer": 0,
        "Status": "Timeout",
        "TimeTaken": DIFFICULTY_SETTINGS.get(st.session_state.get("selected_difficulty", "Medium"), {}).get("time_limit", 45),
        "Points": 0
    }
    progress_service.save_exercise_result(
        username=st.session_state.username,
        exercise=entry["Exercise"],
        difficulty=entry["Difficulty"],
        user_answer=0,
        correct_answer=0,
        is_correct=False,
        time_taken=entry["TimeTaken"],
        points_earned=0
    )


def _handle_result_display(
    exercise_service: ExerciseService,
    progress_service: ProgressService,
    leaderboard_service: LeaderboardService,
    sound_enabled: bool,
    exercise: str,
    difficulty: str
) -> None:
    """Handle displaying the result and auto-advancing"""
    if "result_time" not in st.session_state:
        st.session_state.result_time = time.time()
    
    elapsed = time.time() - st.session_state.result_time
    
    if elapsed >= 2:
        # Generate new task after 2 seconds
        _generate_new_task(exercise_service, SoundService(), sound_enabled, exercise, difficulty)
        st.rerun()
    else:
        remaining = 2 - elapsed
        st.info(f"⏳ New task in {int(remaining)}s...")


def _render_current_task(
    exercise_service: ExerciseService,
    progress_service: ProgressService,
    sound_service: SoundService,
    sound_enabled: bool,
    exercise: str,
    difficulty: str
) -> None:
    """Render the current task and handle submission"""
    task = st.session_state.current_task
    
    # Check if already submitted
    if st.session_state.get("task_submitted", False):
        user_ans = st.session_state.get("user_answer", 0)
        correct_ans = task["correct_answer"]
        
        # Determine task display class based on answer
        task_class = "task-display task-display-correct" if user_ans == correct_ans else "task-display task-display-incorrect"
        
        if user_ans == correct_ans:
            from frontend.components.cards import render_success_message
            render_success_message(st.session_state.get("last_points", 0))
            SoundService().play_correct(sound_enabled)
            LeaderboardService().update_score(
                st.session_state.username,
                st.session_state.score
            )
        else:
            from frontend.components.cards import render_error_message
            render_error_message(correct_ans)
            SoundService().play_wrong(sound_enabled)
        
        # Show calculation breakdown
        render_calculation_breakdown(task)
        
        # Next Task button
        if st.button("Next Task ➡️", type="primary", use_container_width=True):
            _generate_new_task(exercise_service, sound_service, sound_enabled, exercise, difficulty)
            st.rerun()
        
        # Show share buttons
        render_share_buttons(
            st.session_state.score,
            st.session_state.streak
        )
        
        st.session_state.show_result = True
        return
    
    # Render task question
    _render_task_question(task, st.session_state.get("task_key", 0))
    
    # Handle answer submission
    user_input = _render_answer_input(task)
    
    if st.button("✅ Submit Answer", type="primary", use_container_width=True):
        _process_answer(
            progress_service,
            task,
            difficulty,
            user_input,
            exercise_service
        )
        st.rerun()


def _render_task_question(task: Dict[str, Any], key: int) -> None:
    """Render the task question"""
    task_type = task.get("type", "")
    
    question_html = ""
    
    if task_type == "cash":
        question_html = f'''<p class="task-question">
            🧾 Price: <span class="highlight">${task["price"]}</span><br>
            💰 Paid: <span class="highlight">${task["paid"]}</span></p>'''
    
    elif task_type == "billing":
        question_html = f'''<p class="task-question">
            📋 {task["service"]}<br>
            📅 {task["total_days"]} days<br>
            ❌ Missed: {task["missed_days"]}<br>
            💰 ₹{task["daily_cost"]}/day</p>'''
    
    elif task_type == "tip":
        question_html = f'''<p class="task-question">
            💵 Bill: <span class="highlight">${task["bill"]}</span><br>
            💝 Tip: <span class="accent">{task["tip_percent"]}%</span></p>'''
    
    elif task_type == "discount":
        question_html = f'''<p class="task-question">
            💰 Price: <span class="highlight">${task["original_price"]}</span><br>
            📉 Discount: <span class="accent">{task["discount_percent"]}%</span></p>'''
    
    elif task_type == "tax":
        question_html = f'''<p class="task-question">
            💵 Price: <span class="highlight">${task["price"]}</span><br>
            📊 Tax: <span class="accent">{task["tax_rate"]}%</span></p>'''
    
    elif task_type == "split":
        question_html = f'''<p class="task-question">
            💵 Total: <span class="highlight">${task["total"]}</span><br>
            👥 People: {task["people"]}<br>
            💝 Tip: {task["tip"]}%</p>'''
    
    elif task_type == "profit":
        question_html = f'''<p class="task-question">
            💰 Cost: <span class="highlight">${task["cost_price"]}</span><br>
            📈 Markup: <span class="accent">{task["markup_percent"]}%</span></p>'''
    
    elif task_type == "unit":
        question_html = f'''<p class="task-question">
            🛒 Option 1: ${task["price1"]} for {task["qty1"]} = ${task["unit1"]}/item<br>
            🛒 Option 2: ${task["price2"]} for {task["qty2"]} = ${task["unit2"]}/item</p>'''
    
    elif task_type == "percent":
        question_html = f'''<p class="task-question">
            🔢 What is <span class="accent">{task["percent"]}%</span> of <span class="highlight">{task["number"]}</span>?</p>'''
    
    elif task_type == "currency":
        question_html = f'''<p style="color: #64748B; font-size: 0.9rem;">💡 Rate: 1 {task["from_currency"]} = {task["rate"]} {task["to_currency"]}</p>
            <p class="task-question">💱 Convert {task["from_currency"]} {task["amount"]} to {task["to_currency"]}</p>'''
    
    elif task_type == "interest":
        question_html = f'''<p class="task-question">
            💰 Principal: <span class="highlight">${task["principal"]}</span><br>
            📊 Rate: <span class="accent">{task["rate"]}%</span><br>
            📅 Years: <span class="highlight">{task["years"]}</span></p>'''
    
    elif task_type == "compound_interest":
        question_html = f'''<p class="task-question">
            💰 Principal: <span class="highlight">${task["principal"]}</span><br>
            📊 Rate: <span class="accent">{task["rate"]}%</span> (compounded annually)<br>
            📅 Time: <span class="highlight">{task["years"]} year(s)</span></p>
            <p style="color: #64748B; font-size: 0.9rem;">💡 Find the final amount (A = P(1 + r/100)^t)</p>'''
    
    elif task_type == "multiplication":
        question_html = f'''<p class="task-question">
            ✖️ <span class="highlight">{task["number1"]}</span> × <span class="accent">{task["number2"]}</span> = ?</p>'''
    
    # Render the task display
    st.markdown(
        f'<div class="task-display fade-in" key="task_{key}">'
        f'<span class="exercise-icon">{task["icon"]}</span>'
        f'<div class="exercise-name">{task["exercise"]}</div>'
        f'</div>',
        unsafe_allow_html=True
    )
    st.markdown(question_html, unsafe_allow_html=True)


def _render_answer_input(task: Dict[str, Any]):
    """Render the answer input widget based on task type"""
    task_type = task.get("type", "")
    
    if task_type == "unit":
        return st.selectbox("👍 Better option:", [1, 2], key="ans")
    elif task_type == "multiplication":
        return st.number_input(
            "✖️ Answer:",
            min_value=0,
            step=1,
            key="ans"
        )
    else:
        return st.number_input(
            "💵 Answer:",
            min_value=0.0,
            step=0.01,
            key="ans"
        )


def _process_answer(
    progress_service: ProgressService,
    task: Dict[str, Any],
    difficulty: str,
    user_input,
    exercise_service: ExerciseService
) -> None:
    """Process the user's answer"""
    correct = task["correct_answer"]
    time_taken = time.time() - st.session_state.start_time
    
    is_correct = user_input == correct
    
    if is_correct:
        points = exercise_service.calculate_points(difficulty, time_taken)
        st.session_state.score += points
        st.session_state.streak += 1
        st.session_state.last_points = points
    else:
        st.session_state.streak = 0
        points = 0
    
    # Save progress
    progress_service.save_exercise_result(
        username=st.session_state.username,
        exercise=task["exercise"],
        difficulty=difficulty,
        user_answer=user_input,
        correct_answer=correct,
        is_correct=is_correct,
        time_taken=time_taken,
        points_earned=points
    )
    
    # Update session state
    st.session_state.user_answer = user_input
    st.session_state.task_submitted = True

