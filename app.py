"""
EduGenie: Google Gemini Powered Learning Assistant
Main Application Entry Point and View Router.
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
from frontend.views.explainer_view import render_explainer_view
from frontend.views.quiz_view import render_quiz_view
from frontend.views.summarizer_view import render_summarizer_view
from frontend.views.chat_view import render_chat_view

# Apply Design System & Glassmorphism
apply_custom_styles()

# Render Top Hero Banner
render_hero_banner()

# Render Sidebar Navigation & API Controls
api_key, model_name, selected_module = render_sidebar()

# --- MODULE VIEW ROUTING ---
if selected_module == "🎓 Concept Explainer":
    render_explainer_view(api_key, model_name)

elif selected_module == "❓ Quiz & Flashcards":
    render_quiz_view(api_key, model_name)

elif selected_module == "📝 Notes Summarizer":
    render_summarizer_view(api_key, model_name)

elif selected_module == "💬 Doubt Clarifier":
    render_chat_view(api_key, model_name)
