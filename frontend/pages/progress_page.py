"""Progress page for MathBlitz - Modern Clean Design"""
import streamlit as st

from frontend.styles.css import custom_css
from frontend.components.cards import render_stat_card
from services import ProgressService
from database import progress_db


def render_progress_page() -> None:
    """
    Render the progress/analytics page
    """
    custom_css()
    
    progress_service = ProgressService()
    username = st.session_state.username
    
    # Page title
    st.markdown(
        '<h2 class="page-title fade-in-up">📊 Your Progress</h2>',
        unsafe_allow_html=True
    )
    
    # Load progress data
    progress = progress_db.load_progress(username)
    
    if progress.empty:
        st.markdown(
            '<div class="card card-gradient fade-in-up"><p style="text-align: center; color: #64748B; font-size: 1.1rem;">'
            'No exercises yet. Start practicing! 🎮</p></div>',
            unsafe_allow_html=True
        )
        return
    
    # Calculate stats
    total = len(progress)
    correct = len(progress[progress["Status"] == "Correct"])
    accuracy = (correct / total * 100) if total > 0 else 0
    total_points = int(progress["Points"].sum())
    avg_time = progress["TimeTaken"].mean() if not progress.empty else 0
    
    # Display stats with enhanced cards
    st.markdown('<div class="progress-stats-grid fade-in-up">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    stats_data = [
        ("📝", total, "Exercises", "accent-blue"),
        ("✅", f"{accuracy:.0f}%", "Accuracy", "accent-green"),
        ("🏆", total_points, "Points", "accent-purple"),
        ("⏱️", f"{avg_time:.1f}s", "Avg Time", "accent-orange")
    ]
    
    for i, (icon, value, label, accent_class) in enumerate(stats_data):
        with eval(f"col{i+1}"):
            st.markdown(f'''
            <div class="progress-stat-card {accent_class}">
                <span class="stat-icon">{icon}</span>
                <span class="stat-value">{value}</span>
                <span class="stat-label">{label}</span>
            </div>
            ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Show detailed analytics if enough data
    if len(progress) > 1:
        st.markdown("---")
        
        tab1, tab2, tab3 = st.tabs(["📈 Accuracy Trend", "⏱️ Time Analysis", "🎯 By Exercise"])
        
        with tab1:
            _render_accuracy_trend(progress)
        
        with tab2:
            _render_time_analysis(progress)
        
        with tab3:
            _render_exercise_stats(progress)
    
    st.markdown("---")
    
    # Recent activity with enhanced styling
    st.markdown('''
    <div class="progress-activity-header fade-in-up">
        <h3 class="progress-activity-title">📝 Recent Activity</h3>
    </div>
    ''', unsafe_allow_html=True)
    
    # Style the dataframe with custom classes
    st.markdown('<div class="progress-table fade-in-up">', unsafe_allow_html=True)
    
    recent = progress.tail(10)[["Timestamp", "Exercise", "Difficulty", "Status", "Points"]]
    
    # Create styled dataframe
    st.dataframe(
        recent,
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Export button with enhanced styling
    st.markdown('<div class="fade-in-up">', unsafe_allow_html=True)
    csv_data = progress.to_csv(index=False).encode('utf-8')
    st.download_button(
        "⬇️ Download Progress Log",
        csv_data,
        f"{username}_progress.csv",
        "text/csv",
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)


def _render_accuracy_trend(progress) -> None:
    """Render accuracy trend chart"""
    progress = progress.copy()
    progress["StatusNum"] = (progress["Status"] == "Correct").astype(int)
    progress["Rolling"] = progress["StatusNum"].rolling(5).mean() * 100
    
    st.markdown('''
    <div class="progress-chart-enhanced fade-in">
        <div class="progress-chart-header">
            <span class="progress-chart-title">Accuracy Trend</span>
            <span class="progress-chart-badge">Last 5 Exercises</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    st.line_chart(progress["Rolling"].dropna(), use_container_width=True)


def _render_time_analysis(progress) -> None:
    """Render time analysis chart"""
    st.markdown('''
    <div class="progress-chart-enhanced fade-in">
        <div class="progress-chart-header">
            <span class="progress-chart-title">Time Analysis</span>
            <span class="progress-chart-badge">Performance</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    st.line_chart(progress["TimeTaken"], use_container_width=True)


def _render_exercise_stats(progress) -> None:
    """Render exercise statistics"""
    stats = progress.groupby("Exercise").agg({
        "Status": lambda x: (x == "Correct").mean() * 100,
        "Points": "sum"
    }).round(1)
    
    stats.columns = ["Accuracy %", "Points"]
    
    st.markdown('''
    <div class="progress-chart-enhanced fade-in">
        <div class="progress-chart-header">
            <span class="progress-chart-title">Performance by Exercise</span>
            <span class="progress-chart-badge">Breakdown</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    st.dataframe(stats, use_container_width=True)

