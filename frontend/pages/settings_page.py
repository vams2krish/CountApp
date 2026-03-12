"""Settings page for MathBlitz - Modern Clean Design"""
import streamlit as st

from frontend.styles.css import custom_css
from database import user_db, progress_db
from config.settings import EXERCISE_NAMES


def render_settings_page() -> None:
    """
    Render the settings page
    """
    custom_css()
    
    # Page title
    st.markdown(
        '<h2 class="page-title fade-in-up">⚙️ Settings</h2>',
        unsafe_allow_html=True
    )
    
    # Get current settings
    username = st.session_state.username
    current_settings = user_db.get_user_settings(username)
    
    # Settings sections with enhanced styling
    st.markdown('<div class="settings-section fade-in-up">', unsafe_allow_html=True)
    st.markdown('<div class="settings-section-title"><span class="icon">🎮</span> Practice Preferences</div>', unsafe_allow_html=True)
    
    # Sound toggle with enhanced styling
    sound = st.toggle(
        "🔊 Sound Effects",
        value=current_settings.get("sound_enabled", True),
        help="Enable or disable sound effects during practice"
    )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('<div class="settings-section fade-in-up">', unsafe_allow_html=True)
    st.markdown('<div class="settings-section-title"><span class="icon">📊</span> Default Settings</div>', unsafe_allow_html=True)
    
    # Default difficulty
    diff = st.selectbox(
        "Default Difficulty",
        ["Easy", "Medium", "Hard"],
        index=["Easy", "Medium", "Hard"].index(
            current_settings.get("default_difficulty", "Medium")
        ),
        help="Set your preferred difficulty level"
    )
    
    # Default exercise
    default_ex = current_settings.get("default_exercise", "Cash Counting")
    ex_idx = EXERCISE_NAMES.index(default_ex) if default_ex in EXERCISE_NAMES else 0
    ex = st.selectbox(
        "Default Exercise",
        EXERCISE_NAMES,
        index=ex_idx,
        help="Set your preferred exercise type"
    )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Action buttons with enhanced styling
    st.markdown('<div class="settings-actions-enhanced fade-in-up">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💾 Save Settings", use_container_width=True, type="primary"):
            new_settings = {
                "sound_enabled": sound,
                "default_difficulty": diff,
                "default_exercise": ex
            }
            user_db.save_user_settings(username, new_settings)
            st.session_state.settings = new_settings
            st.success("✅ Settings saved successfully!")
    
    with col2:
        if st.button("🗑️ Reset Progress", use_container_width=True):
            progress_db.reset_progress(username)
            st.session_state.score = 0
            st.session_state.streak = 0
            st.success("✅ Progress reset successfully!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Account info with enhanced styling
    st.markdown('<div class="settings-section fade-in-up">', unsafe_allow_html=True)
    st.markdown('<div class="settings-section-title"><span class="icon">👤</span> Account Information</div>', unsafe_allow_html=True)
    
    # Display account stats with enhanced card
    user_score = st.session_state.get("score", 0)
    user_streak = st.session_state.get("streak", 0)
    
    # Get first letter for avatar
    initial = username[0].upper() if username else "?"
    
    st.markdown(f'''
    <div class="settings-account-card">
        <div class="settings-account-header">
            <div class="settings-account-avatar">{initial}</div>
            <div class="settings-account-name">{username}</div>
        </div>
        <div class="settings-account-stats">
            <div style="text-align: center; padding: 12px; background: rgba(255,255,255,0.5); border-radius: 12px;">
                <div style="font-size: 1.5rem; font-weight: 800; color: #0066CC; font-family: 'JetBrains Mono', monospace;">{user_score}</div>
                <div style="font-size: 0.75rem; color: #64748B; font-weight: 600; text-transform: uppercase;">Total Score</div>
            </div>
            <div style="text-align: center; padding: 12px; background: rgba(255,255,255,0.5); border-radius: 12px;">
                <div style="font-size: 1.5rem; font-weight: 800; color: #F59E0B; font-family: 'JetBrains Mono', monospace;">{user_streak}</div>
                <div style="font-size: 0.75rem; color: #64748B; font-weight: 600; text-transform: uppercase;">Current Streak</div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

