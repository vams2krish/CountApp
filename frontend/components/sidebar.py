"""Sidebar component for MathBlitz - Modern Clean Design"""
import streamlit as st

from frontend.styles.css import custom_css
from services import leaderboard_service


def render_sidebar(username: str, score: int, streak: int) -> str:
    """
    Render the sidebar with user info and navigation buttons
    
    Args:
        username: The current username
        score: Current score
        streak: Current streak
        
    Returns:
        Selected menu option
    """
    custom_css()
    
    # Initialize selected page if not exists
    if "selected_page" not in st.session_state:
        st.session_state.selected_page = "practice"
    
    with st.sidebar:
        # User header
        st.markdown(f'''
        <div class="sidebar-header">
            <div class="sidebar-user">
                <div class="sidebar-avatar">{username[0].upper()}</div>
                <div class="sidebar-username">{username}</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Score and streak
        st.markdown(f'''
        <div class="sidebar-score-container">
            <div class="sidebar-score-item">
                <div class="sidebar-score-value">🏆 {score}</div>
                <div class="sidebar-score-label">Score</div>
            </div>
            <div class="sidebar-score-item">
                <div class="sidebar-score-value">🔥 {streak}</div>
                <div class="sidebar-score-label">Streak</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Navigation Menu - Beautiful Button Style
        st.markdown('<div class="nav-section">', unsafe_allow_html=True)
        st.markdown('<div class="nav-title">📍 Navigation</div>', unsafe_allow_html=True)
        
        # Practice Button
        practice_active = "active" if st.session_state.selected_page == "practice" else ""
        if st.button(
            "🎮  Activity - Math Games",
            key="nav_practice",
            use_container_width=True,
            type="primary" if practice_active else "secondary"
        ):
            st.session_state.selected_page = "practice"
            st.rerun()
        
        # Progress Button
        progress_active = "active" if st.session_state.selected_page == "progress" else ""
        if st.button(
            "📊  Progress",
            key="nav_progress",
            use_container_width=True,
            type="primary" if progress_active else "secondary"
        ):
            st.session_state.selected_page = "progress"
            st.rerun()
        
        # Settings Button
        settings_active = "active" if st.session_state.selected_page == "settings" else ""
        if st.button(
            "⚙️  Settings",
            key="nav_settings",
            use_container_width=True,
            type="primary" if settings_active else "secondary"
        ):
            st.session_state.selected_page = "settings"
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Leaderboard
        st.markdown('<div class="leaderboard-card"><div class="leaderboard-title">🌍 World Leaderboard</div>', unsafe_allow_html=True)
        
        try:
            leaderboard = leaderboard_service.get_top_players(10)
            for i, entry in enumerate(leaderboard):
                rank_class = f"top-{i+1}" if i < 3 else ""
                is_current = entry["username"] == username
                name_display = entry["username"] + " (You)" if is_current else entry["username"]
                name_class = "you" if is_current else ""
                rank_display = f"gold" if i == 0 else ("silver" if i == 1 else ("bronze" if i == 2 else ""))
                
                st.markdown(f'''<div class="leaderboard-item {rank_class}">
                    <span class="lb-rank {rank_display}">#{i+1}</span>
                    <span class="lb-name {name_class}">{name_display}</span>
                    <span class="lb-score">{entry["score"]}</span>
                </div>''', unsafe_allow_html=True)
        except Exception as e:
            st.markdown('<p style="text-align:center;color:#64748B;">No leaderboard data</p>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Delete Account section
        _render_delete_account_section(username)
        
        st.markdown("---")
        
        # Logout button - styled nicely
        if st.button("🚪  Logout", key="logout_btn", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()
        
        return st.session_state.selected_page


def _render_delete_account_section(username: str) -> None:
    """Render the delete account section with confirmation"""
    if "delete_confirm" not in st.session_state:
        st.session_state.delete_confirm = False
    
    if st.session_state.delete_confirm:
        # Show confirmation
        st.markdown('<div class="danger-zone">', unsafe_allow_html=True)
        st.markdown('<div class="danger-title">⚠️ Delete Account</div>', unsafe_allow_html=True)
        st.markdown(f'<p class="danger-text">Type "{username}" to confirm:</p>', unsafe_allow_html=True)
        
        confirm_text = st.text_input(
            "Confirm username",
            key="confirm_delete_input",
            placeholder="Enter username"
        )
        
        col_del1, col_del2 = st.columns(2)
        
        with col_del1:
            if st.button("✅ Confirm Delete", key="confirm_del", use_container_width=True, type="primary"):
                if confirm_text == username:
                    from database import user_db, progress_db
                    from services import leaderboard_service
                    
                    user_db.delete_user(username)
                    progress_db.delete_progress(username)
                    leaderboard_service.remove_user(username)
                    
                    st.session_state.logged_in = False
                    st.session_state.delete_confirm = False
                    st.success("Account deleted!")
                    st.rerun()
                else:
                    st.error("Username doesn't match!")
        
        with col_del2:
            if st.button("❌ Cancel", key="cancel_del", use_container_width=True):
                st.session_state.delete_confirm = False
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        if st.button("🗑️  Delete Account", key="delete_acc_btn", use_container_width=True):
            st.session_state.delete_confirm = True
            st.rerun()

