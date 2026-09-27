"""
View controller for Login & Registration screens in EduGenie.
Provides glassmorphic authentication cards, guest access mode, and validation.
"""

import streamlit as st
from backend.auth import authenticate_user, register_user


def render_auth_view():
    """Renders login and registration portal."""
    st.markdown("""
    <div style="text-align: center; margin-top: 10px; margin-bottom: 25px;">
        <div style="font-size: 3rem; margin-bottom: 6px;">🎓</div>
        <h1 style="font-size: 2.2rem; font-weight: 800; background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 50%, #f472b6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 4px;">
            Welcome to EduGenie AI
        </h1>
        <div style="color: #94a3b8; font-size: 1rem; max-width: 540px; margin: 0 auto;">
            Your autonomous AI study companion for calibrated concept breakdowns, dynamic quizzes, exam cheat-sheets, and personalized learning plans.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_center1, col_center2, col_center3 = st.columns([1, 1.8, 1])

    with col_center2:
        auth_tab_login, auth_tab_register = st.tabs(["🔐 Sign In", "📝 Create Account"])

        with auth_tab_login:
            with st.container(border=True):
                st.markdown("<h4 style='margin: 0 0 14px 0; color: #f8fafc;'>Sign in to your Study Account</h4>", unsafe_allow_html=True)
                
                login_email = st.text_input("Email Address", placeholder="scholar@edugenie.ai", key="auth_login_email")
                login_pwd = st.text_input("Password", type="password", placeholder="••••••••", key="auth_login_pwd")

                col_btn1, col_btn2 = st.columns([1.2, 1])
                with col_btn1:
                    if st.button("🚀 Sign In", type="primary", use_container_width=True, key="auth_submit_login"):
                        success, user_data, msg = authenticate_user(login_email, login_pwd)
                        if success:
                            st.session_state.authenticated_user = user_data
                            st.success(f"Welcome back, {user_data['name']}!")
                            st.rerun()
                        else:
                            st.error(msg)

                with col_btn2:
                    if st.button("⚡ Quick Guest Login", use_container_width=True, key="auth_guest_login"):
                        st.session_state.authenticated_user = {"email": "guest@edugenie.ai", "name": "Guest Scholar"}
                        st.success("Logged in as Guest!")
                        st.rerun()

                st.markdown("""
                <div style="margin-top: 14px; font-size: 0.82rem; color: #64748b; text-align: center;">
                    💡 Default Demo Account: <code>student@edugenie.ai</code> | Password: <code>edugenie123</code>
                </div>
                """, unsafe_allow_html=True)

        with auth_tab_register:
            with st.container(border=True):
                st.markdown("<h4 style='margin: 0 0 14px 0; color: #f8fafc;'>New Student Registration</h4>", unsafe_allow_html=True)
                
                reg_name = st.text_input("Full Name", placeholder="Alex Morgan", key="auth_reg_name")
                reg_email = st.text_input("Email Address", placeholder="alex@university.edu", key="auth_reg_email")
                reg_pwd = st.text_input("Create Password", type="password", placeholder="At least 6 characters", key="auth_reg_pwd")

                if st.button("✨ Create Free Account", type="primary", use_container_width=True, key="auth_submit_register"):
                    success, msg = register_user(reg_email, reg_name, reg_pwd)
                    if success:
                        st.success(msg + " You can now switch to Sign In.")
                    else:
                        st.error(msg)
