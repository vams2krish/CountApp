"""Card components for MathBlitz - Modern Clean Design"""
import streamlit as st
from typing import Dict, Any, List


def render_card(content: str, class_name: str = "card") -> None:
    """
    Render a styled card container
    
    Args:
        content: HTML content inside the card
        class_name: CSS class for styling
    """
    st.markdown(f'<div class="{class_name}">{content}</div>', unsafe_allow_html=True)


def render_stat_card(icon: str, value: str, label: str, color: str = "#0066CC") -> None:
    """
    Render a statistics card
    
    Args:
        icon: Emoji icon
        value: The value to display
        label: The label for the value
        color: The color for the value
    """
    st.markdown(f'''<div class="stat-card">
        <div class="stat-icon">{icon}</div>
        <div class="stat-value" style="color: {color};">{value}</div>
        <div class="stat-label">{label}</div>
    </div>''', unsafe_allow_html=True)


def render_leaderboard_card(
    entries: List[Dict[str, Any]],
    current_username: str,
    max_entries: int = 10
) -> None:
    """
    Render a leaderboard card
    
    Args:
        entries: List of leaderboard entries
        current_username: Current user's username
        max_entries: Maximum number of entries to show
    """
    st.markdown('<div class="leaderboard-card">', unsafe_allow_html=True)
    st.markdown('<div class="leaderboard-title">🌍 World Leaderboard</div>', unsafe_allow_html=True)
    
    for i, entry in enumerate(entries[:max_entries]):
        rank_class = f"top-{i+1}" if i < 3 else ""
        is_current = entry["username"] == current_username
        name_display = entry["username"] + " (You)" if is_current else entry["username"]
        name_class = "you" if is_current else ""
        
        st.markdown(f'''<div class="leaderboard-item {rank_class}">
            <span class="lb-rank">#{i+1}</span>
            <span class="lb-name {name_class}">{name_display}</span>
            <span class="lb-score">{entry["score"]}</span>
        </div>''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


def render_formula_box(
    icon: str,
    formula: str,
    example: str,
    tip: str
) -> None:
    """
    Render a formula information box
    
    Args:
        icon: Emoji icon
        formula: The formula text
        example: Example calculation
        tip: Tip for solving
    """
    st.markdown(f'''<div class="formula-box">
        <div class="formula-title">📐 {icon} Formula</div>
        <div class="formula-text">{formula}</div>
        <div class="formula-example">💡 Example: {example}</div>
        <div class="formula-tip">✨ {tip}</div>
    </div>''', unsafe_allow_html=True)


def render_timer(time_remaining: float, difficulty: str = "Medium") -> None:
    """
    Render a timer display
    
    Args:
        time_remaining: Seconds remaining
        difficulty: Current difficulty level
    """
    if time_remaining > 20:
        timer_class = "timer-easy"
    elif time_remaining > 10:
        timer_class = "timer-medium"
    else:
        timer_class = "timer-hard"
    
    st.markdown(
        f'<div class="timer-display {timer_class}">⏱️ {int(time_remaining)}s</div>',
        unsafe_allow_html=True
    )


def render_success_message(points: int) -> None:
    """
    Render a success message
    
    Args:
        points: Points earned
    """
    st.markdown(
        f'<div class="success-message">🎉 Correct! +{points} points!</div>',
        unsafe_allow_html=True
    )


def render_error_message(correct_answer: Any) -> None:
    """
    Render an error message
    
    Args:
        correct_answer: The correct answer
    """
    st.markdown(
        f'<div class="error-message">❌ Incorrect<br>Correct answer: {correct_answer}</div>',
        unsafe_allow_html=True
    )


def render_task_display(
    icon: str,
    exercise_name: str,
    question_html: str,
    key: int = 0
) -> None:
    """
    Render a task display box
    
    Args:
        icon: Exercise icon emoji
        exercise_name: Name of the exercise
        question_html: HTML for the question content
        key: Unique key for animation
    """
    st.markdown(
        f'<div class="task-display fade-in" key="task_{key}">'
        f'<span class="exercise-icon">{icon}</span>'
        f'<div class="exercise-name">{exercise_name}</div>'
        f'</div>',
        unsafe_allow_html=True
    )
    st.markdown(question_html, unsafe_allow_html=True)

