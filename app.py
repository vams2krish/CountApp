"""
MathBlitz - Production-Ready Practice App
=========================================
A modular and scalable math practice application built with Streamlit.

Architecture:
- config/       : Application configuration and settings
- database/     : Data persistence layer (users, leaderboard, progress)
- services/     : Business logic layer (auth, exercises, etc.)
- frontend/     : UI layer (pages, components, styles)
"""

import streamlit as st

# Import configuration
from config.settings import PAGE_CONFIG

# Import database layer
from database import user_db, progress_db

# Import frontend pages
from frontend.pages import (
    render_login_page,
    render_practice_page,
    render_progress_page,
    render_settings_page
)
from frontend.components import render_sidebar
from frontend.styles import custom_css


def configure_page():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title=PAGE_CONFIG["page_title"],
        page_icon=PAGE_CONFIG["page_icon"],
        layout=PAGE_CONFIG["layout"],
        menu_items=PAGE_CONFIG["menu_items"]
    )


def initialize_session_state():
    """Initialize session state variables"""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    if "username" not in st.session_state:
        st.session_state.username = ""
    
    if "score" not in st.session_state:
        st.session_state.score = 0
    
    if "streak" not in st.session_state:
        st.session_state.streak = 0
    
    if "settings" not in st.session_state:
        st.session_state.settings = {}
    
    # Default page selection - track which page user wants to see
    if "selected_page" not in st.session_state:
        st.session_state.selected_page = "practice"


def load_user_session(username: str):
    """Load user data into session state"""
    st.session_state.logged_in = True
    st.session_state.username = username
    st.session_state.score = progress_db.get_total_score(username)
    st.session_state.streak = progress_db.get_current_streak(username)
    st.session_state.settings = user_db.get_user_settings(username)
    # Reset to default page on login
    st.session_state.selected_page = "practice"


def render_main_app():
    """Render the main application after login"""
    username = st.session_state.username
    
    # Load settings if not already loaded
    if not st.session_state.settings:
        st.session_state.settings = user_db.get_user_settings(username)
    
    # Render sidebar and get selected page
    try:
        selected = render_sidebar(
            username=username,
            score=st.session_state.score,
            streak=st.session_state.streak
        )
        
        # Update selected page based on sidebar selection
        if selected:
            if "practice" in selected.lower() or "🎮" in selected:
                st.session_state.selected_page = "practice"
            elif "progress" in selected.lower() or "📊" in selected:
                st.session_state.selected_page = "progress"
            elif "settings" in selected.lower() or "⚙️" in selected:
                st.session_state.selected_page = "settings"
    except Exception as e:
        st.error(f"Error rendering sidebar: {e}")
        st.session_state.selected_page = "practice"
    
    # Route to appropriate page based on stored selection
    try:
        if st.session_state.selected_page == "practice":
            render_practice_page()
        elif st.session_state.selected_page == "progress":
            render_progress_page()
        elif st.session_state.selected_page == "settings":
            render_settings_page()
        else:
            render_practice_page()
    except Exception as e:
        st.error(f"Error rendering page: {e}")
        st.markdown("### ⚠️ An error occurred. Please try refreshing the page.")
        if st.button("Go to Practice"):
            st.session_state.selected_page = "practice"
            st.rerun()


def handle_login():
    """Handle the login/routing logic"""
    if not st.session_state.logged_in:
        render_login_page()
        return
    
    # User is logged in - render main app
    render_main_app()


def main():
    """Main entry point for the application"""
    # Configure page
    configure_page()
    
    # Apply custom CSS
    custom_css()
    
    # Initialize session state
    initialize_session_state()
    
    # Handle routing
    handle_login()


if __name__ == "__main__":
    main()

