"""Pages module for MathBlitz"""
from .auth_pages import render_login_page
from .practice_page import render_practice_page
from .progress_page import render_progress_page
from .settings_page import render_settings_page
from .legal_pages import render_privacy_policy_page, render_terms_of_service_page

__all__ = [
    "render_login_page",
    "render_practice_page",
    "render_progress_page",
    "render_settings_page",
    "render_privacy_policy_page",
    "render_terms_of_service_page"
]

