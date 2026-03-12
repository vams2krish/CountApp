"""Authentication pages for MathBlitz - Modern Clean Design"""
import streamlit as st

from frontend.styles.css import custom_css
from services import AuthService
from database import user_db, progress_db


def render_login_page() -> None:
    """
    Render the login/registration page
    """
    custom_css()
    
    # Check if showing legal pages
    if st.session_state.get("show_privacy_policy"):
        from frontend.pages.legal_pages import render_privacy_policy_page
        render_privacy_policy_page()
        return
    
    if st.session_state.get("show_terms_of_service"):
        from frontend.pages.legal_pages import render_terms_of_service_page
        render_terms_of_service_page()
        return
    
    # Page title
    st.markdown('<p class="main-title">MathBlitz</p>', unsafe_allow_html=True)
    st.markdown(
        '<p style="text-align:center; color: #64748B; font-size: 1.1rem; margin-bottom: 2rem;">'
        'Master math skills with interactive exercises!</p>',
        unsafe_allow_html=True
    )
    
    # Auth form container
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        
        # Custom tab system
        if "auth_tab" not in st.session_state:
            st.session_state.auth_tab = "login"
        
        # Tab buttons
        tab_col1, tab_col2 = st.columns(2)
        
        with tab_col1:
            if st.button(
                "🔑 Login",
                use_container_width=True,
                type="primary" if st.session_state.auth_tab == "login" else "secondary"
            ):
                st.session_state.auth_tab = "login"
                st.rerun()
        
        with tab_col2:
            if st.button(
                "✨ Register",
                use_container_width=True,
                type="primary" if st.session_state.auth_tab == "register" else "secondary"
            ):
                st.session_state.auth_tab = "register"
                st.rerun()
        
        st.markdown("<hr style='margin: 1.5rem 0;'>", unsafe_allow_html=True)
        
        # Render appropriate form
        if st.session_state.auth_tab == "login":
            _render_login_form()
        else:
            _render_register_form()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Legal links at bottom
    _render_legal_links()


def _render_login_form() -> None:
    """Render the login form"""
    auth_service = AuthService()
    
    with st.form("login"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        st.markdown('<div class="auth-submit">', unsafe_allow_html=True)
        submit = st.form_submit_button("🚀 Login", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if submit:
            if auth_service.login(username, password):
                # Set session state
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.score = progress_db.get_total_score(username)
                st.session_state.streak = progress_db.get_current_streak(username)
                st.session_state.settings = user_db.get_user_settings(username)
                st.rerun()
            else:
                st.error("Invalid credentials. Please try again.")


def _render_register_form() -> None:
    """Render the registration form"""
    auth_service = AuthService()
    
    with st.form("register"):
        new_user = st.text_input("Username", placeholder="Choose a username")
        new_pass = st.text_input("Password", type="password", placeholder="Choose a password")
        confirm = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
        
        st.markdown('<div class="auth-submit">', unsafe_allow_html=True)
        submit = st.form_submit_button("✨ Create Account", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if submit:
            if not new_user or not new_pass:
                st.error("Please fill in all fields.")
            elif new_pass != confirm:
                st.error("Passwords do not match.")
            elif len(new_user) < 3:
                st.error("Username must be at least 3 characters.")
            elif len(new_pass) < 4:
                st.error("Password must be at least 4 characters.")
            else:
                success, msg = auth_service.register(new_user, new_pass, confirm)
                
                if success:
                    st.success("🎉 Registration successful! Please login.")
                    st.session_state.auth_tab = "login"
                    st.rerun()
                else:
                    st.error(msg)


def _render_legal_links() -> None:
    """Render legal page links at bottom"""
    st.markdown("<hr style='margin-top: 2rem;'>", unsafe_allow_html=True)
    
    col_legal1, col_legal2, col_legal3 = st.columns([1, 2, 1])
    
    with col_legal2:
        c1, c2 = st.columns(2)
        
        with c1:
            if st.button("📜 Privacy Policy", key="priv_btn", use_container_width=True):
                st.session_state.show_privacy_policy = True
                st.rerun()
        
        with c2:
            if st.button("📝 Terms of Service", key="tos_btn", use_container_width=True):
                st.session_state.show_terms_of_service = True
                st.rerun()

