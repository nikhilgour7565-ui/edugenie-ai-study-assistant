"""
EduGenie: Autonomous Google Gemini Powered Learning Assistant
Main Application Entry Point and Dynamic View Router.
"""

import streamlit as st
from dotenv import load_dotenv

# Load local environment variables
load_dotenv()

# --- STREAMLIT PAGE CONFIGURATION ---
st.set_page_config(
    page_title="EduGenie | AI Learning Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- IMPORT FRONTEND COMPONENTS & STYLES ---
from frontend.styles import apply_custom_styles
from frontend.components import render_hero_banner, render_sidebar
from frontend.views.auth_view import render_auth_view
from frontend.views.home_view import render_home_view
from frontend.views.explainer_view import render_explainer_view
from frontend.views.quiz_view import render_quiz_view
from frontend.views.summarizer_view import render_summarizer_view
from frontend.views.chat_view import render_chat_view
from frontend.views.learning_plan_view import render_learning_plan_view

# Apply Design System & Glassmorphic CSS
apply_custom_styles()

# Check Authentication Status
if "authenticated_user" not in st.session_state or st.session_state.authenticated_user is None:
    render_auth_view()
else:
    # Render Top Hero Banner
    render_hero_banner()

    # Render Sidebar Navigation & API Controls
    api_key, model_name, selected_module = render_sidebar()

    # --- MODULE VIEW ROUTING ---
    if selected_module == "🏠 Home & Overview":
        render_home_view()

    elif selected_module == "🎓 Concept Explainer":
        render_explainer_view(api_key, model_name)

    elif selected_module == "❓ Quiz & Flashcards":
        render_quiz_view(api_key, model_name)

    elif selected_module == "📝 Notes Summarizer":
        render_summarizer_view(api_key, model_name)

    elif selected_module == "💬 Doubt Clarifier":
        render_chat_view(api_key, model_name)

    elif selected_module == "🗺️ Learning Plan":
        render_learning_plan_view(api_key, model_name)
