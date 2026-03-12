"""Legal pages for MathBlitz"""
import streamlit as st

from frontend.styles.css import custom_css


def render_privacy_policy_page() -> None:
    """
    Render the Privacy Policy page
    """
    custom_css()
    
    st.markdown('<div class="legal-page-card">', unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="legal-page-header">
        <h1 class="legal-page-title">📜 Privacy Policy</h1>
        <p class="legal-last-updated">Last Updated: January 2025</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Content sections
    st.markdown('<div class="legal-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="legal-section-title">Overview</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="legal-content">
        MathBlitz ("we," "our," or "us") is committed to protecting your privacy. This Privacy Policy explains how your personal information is collected, used, and disclosed by MathBlitz.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="legal-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="legal-section-title">Information We Collect</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="legal-content">
        <strong>Information You Provide:</strong>
        <ul>
            <li><strong>Account Information:</strong> When you register, we collect your username and password.</li>
            <li><strong>Progress Data:</strong> We store your practice progress, scores, and achievements.</li>
            <li><strong>Settings:</strong> We save your preferences (sound settings, default difficulty, etc.)</li>
        </ul>
        <strong>Automatically Collected Information:</strong>
        <ul>
            <li><strong>Usage Data:</strong> We collect information about how you use the app (exercises completed, time spent, etc.)</li>
            <li><strong>Device Information:</strong> Basic device information for app functionality</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="legal-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="legal-section-title">How We Use Your Information</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="legal-content">
        We use your information to:
        <ul>
            <li>Provide and improve our math practice services</li>
            <li>Track your progress and achievements</li>
            <li>Maintain leaderboard rankings</li>
            <li>Save your preferences and settings</li>
            <li>Communicate important updates</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="legal-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="legal-section-title">Data Storage</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="legal-content">
        <ul>
            <li>All user data is stored locally on your device</li>
            <li>Progress data is saved as CSV files in your local <code>data/progress</code> folder</li>
            <li>User credentials are stored in <code>data/users.json</code></li>
            <li>We do not sell or share your personal information with third parties</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="legal-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="legal-section-title">Data Security</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="legal-content">
        We implement appropriate security measures to protect your personal information:
        <ul>
            <li>Passwords are stored securely</li>
            <li>Local data storage is protected by your device's security</li>
            <li>No sensitive payment information is collected</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="legal-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="legal-section-title">Your Rights</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="legal-content">
        You have the right to:
        <ul>
            <li>Access your personal data</li>
            <li>Delete your account and associated data</li>
            <li>Reset your progress at any time</li>
            <li>Export your data in CSV format</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="legal-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="legal-section-title">Children\'s Privacy</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="legal-content">
        MathBlitz is designed for general audiences, including children. We do not knowingly collect personal information from children under 13 without parental consent.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="legal-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="legal-section-title">Changes to This Policy</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="legal-content">
        We may update this Privacy Policy from time to time. We will notify you of any changes by posting the new policy on this page.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="legal-footer">
        <p class="legal-footer-text">By using MathBlitz, you agree to the terms outlined in this Privacy Policy.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Back button with enhanced styling
    st.markdown('<div class="fade-in-up">', unsafe_allow_html=True)
    if st.button("🔙 Back to Login", use_container_width=True, type="primary"):
        st.session_state.show_privacy_policy = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


def render_terms_of_service_page() -> None:
    """
    Render the Terms of Service page
    """
    custom_css()
    
    st.markdown('<div class="legal-page-card">', unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="legal-page-header">
        <h1 class="legal-page-title">📋 Terms of Service</h1>
        <p class="legal-last-updated">Last Updated: January 2025</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Content sections
    st.markdown('<div class="legal-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="legal-section-title">Acceptance of Terms</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="legal-content">
        By accessing and using MathBlitz ("the App"), you accept and agree to be bound by the terms and provision of this agreement.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="legal-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="legal-section-title">Description of Service</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="legal-content">
        MathBlitz is an interactive math practice application that provides:
        <ul>
            <li>11 different math exercise types</li>
            <li>Gamification features including scoring and streaks</li>
            <li>World leaderboard rankings</li>
            <li>User progress tracking</li>
            <li>Multiple difficulty levels</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="legal-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="legal-section-title">User Accounts</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="legal-content">
        <strong>Registration:</strong>
        <ul>
            <li>You must provide accurate and complete registration information</li>
            <li>You are responsible for maintaining the security of your account</li>
            <li>You must be at least 13 years old to create an account</li>
        </ul>
        <strong>Account Responsibilities:</strong>
        <ul>
            <li>You are solely responsible for all activities under your account</li>
            <li>You must notify us immediately of any unauthorized use</li>
            <li>You agree not to share your account credentials with others</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="legal-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="legal-section-title">Acceptable Use</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="legal-content">
        You agree not to:
        <ul>
            <li>Use the app for any unlawful purpose</li>
            <li>Attempt to gain unauthorized access to any part of the app</li>
            <li>Interfere with the proper operation of the app</li>
            <li>Submit false or misleading information</li>
            <li>Create multiple accounts to manipulate leaderboards</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="legal-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="legal-section-title">Intellectual Property</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="legal-content">
        <ul>
            <li>All content and materials in MathBlitz are owned by us</li>
            <li>You may not copy, modify, or distribute our content without permission</li>
            <li>The "MathBlitz" name and logo are our trademarks</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="legal-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="legal-section-title">User-Generated Content</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="legal-content">
        You retain ownership of any progress data you generate while using the app. By using the app, you grant us the right to display your username and scores on the leaderboard.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="legal-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="legal-section-title">Disclaimers</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="legal-content">
        THE APP IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND. WE DO NOT GUARANTEE THAT THE APP WILL BE UNINTERRUPTED OR ERROR-FREE.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="legal-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="legal-section-title">Limitation of Liability</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="legal-content">
        We shall not be liable for any indirect, incidental, or consequential damages arising from your use of the app.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="legal-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="legal-section-title">Termination</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="legal-content">
        We reserve the right to terminate or suspend your account at any time for violation of these terms.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="legal-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="legal-section-title">Changes to Terms</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="legal-content">
        We may modify these terms at any time. Continued use of the app constitutes acceptance of updated terms.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="legal-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="legal-section-title">Governing Law</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="legal-content">
        These terms shall be governed by and construed in accordance with applicable laws.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="legal-footer">
        <p class="legal-footer-text">By using MathBlitz, you acknowledge that you have read and understood these Terms of Service and agree to be bound by them.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Back button with enhanced styling
    st.markdown('<div class="fade-in-up">', unsafe_allow_html=True)
    if st.button("🔙 Back to Login", use_container_width=True, type="primary"):
        st.session_state.show_terms_of_service = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

