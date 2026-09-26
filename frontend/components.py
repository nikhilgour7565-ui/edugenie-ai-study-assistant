"""
Reusable Streamlit UI components and widgets for EduGenie.
Implements the refined SaaS sidebar cards, compact status dots,
and slim hero banners.
"""

from typing import Tuple
import streamlit as st
from backend.gemini_client import resolve_api_key
from backend.parsers import generate_export_document


def render_hero_banner():
    """Renders the refined subtle glass hero header."""
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-top-row">
            <h1 class="hero-title">
                <span>🎓 EduGenie</span>
                <span style="font-size: 0.72rem; color: #38bdf8; font-weight: 600; padding: 2px 8px; background: rgba(56, 189, 248, 0.12); border-radius: 12px; border: 1px solid rgba(56, 189, 248, 0.3);">Pro AI Study Suite</span>
            </h1>
            <div class="pill-container" style="margin-top: 0;">
                <span class="feature-pill">📄 PDF & Diagram Intake</span>
                <span class="feature-pill">🔊 Audio Lessons</span>
                <span class="feature-pill">❓ Smart MCQs</span>
                <span class="feature-pill">📝 Exam Cheat-Sheets</span>
            </div>
        </div>
        <div class="hero-subtitle">
            Calibrated concept explanations, interactive active-recall quizzes, and 24/7 doubt clarification powered by Google Gemini.
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar() -> Tuple[str, str, str]:
    """
    Renders the modern SaaS sidebar:
    1. Compact App Identity Card
    2. Settings Card with compact status dot (🟢 / 🔴)
    3. Navigation Menu Card with active highlight pills
    4. Minimal footer
    """
    with st.sidebar:
        # 1. Compact App Identity Card
        st.markdown("""
        <div class="sidebar-brand-card">
            <div class="brand-icon">🎓</div>
            <div>
                <div class="brand-title">EduGenie</div>
                <div class="brand-subtitle">Gemini AI Study Suite</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 2. Settings & Engine Card
        with st.container(border=True):
            default_key = resolve_api_key()
            
            # Compact Status Dot Header
            if default_key:
                status_html = '<span title="API Key Connected & Active" style="display: flex; align-items: center; gap: 6px; font-size: 0.82rem; font-weight: 600; color: #86efac;"><span style="height: 8px; width: 8px; background-color: #22c55e; border-radius: 50%; display: inline-block; box-shadow: 0 0 6px #22c55e;"></span> Connected</span>'
            else:
                status_html = '<span title="API Key Required" style="display: flex; align-items: center; gap: 6px; font-size: 0.82rem; font-weight: 600; color: #f87171;"><span style="height: 8px; width: 8px; background-color: #ef4444; border-radius: 50%; display: inline-block; box-shadow: 0 0 6px #ef4444;"></span> Key Missing</span>'

            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-weight: 700; font-size: 0.88rem; color: #f1f5f9;">⚙️ Engine Settings</span>
                {status_html}
            </div>
            """, unsafe_allow_html=True)

            user_api_key = st.text_input(
                "Gemini API Key",
                value=default_key,
                type="password",
                placeholder="AIzaSy...",
                help="Provide your Google Gemini API key. Pre-configured environment keys auto-populate here.",
                key="sidebar_api_key_input",
                label_visibility="collapsed"
            )
            selected_api_key = user_api_key.strip() if user_api_key else default_key

            selected_model = st.selectbox(
                "Model",
                options=["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash-exp"],
                index=0,
                help="`gemini-1.5-flash` provides fast, responsive multimodal reasoning.",
                key="sidebar_model_select"
            )

        # 3. Navigation Menu Card
        with st.container(border=True):
            st.markdown("<div style='font-weight: 700; font-size: 0.88rem; color: #f1f5f9; margin-bottom: 8px;'>📚 Study Tools</div>", unsafe_allow_html=True)
            
            selected_module = st.radio(
                "Navigation:",
                options=[
                    "🎓 Concept Explainer",
                    "❓ Quiz & Flashcards",
                    "📝 Notes Summarizer",
                    "💬 Doubt Clarifier"
                ],
                index=0,
                label_visibility="collapsed",
                key="sidebar_module_nav"
            )

        # 4. Minimal Footer
        st.caption("⚡ Powered by Google GenAI & Streamlit")

    return selected_api_key, selected_model, selected_module


def render_export_buttons(title: str, markdown_content: str, key_prefix: str = "export"):
    """Renders 3-column export download buttons (.md, .txt, .html)."""
    st.markdown("##### 📥 Export Study Package:")
    col_d1, col_d2, col_d3 = st.columns(3)
    
    file_slug = title.lower().replace(" ", "_")[:30]

    with col_d1:
        st.download_button(
            label="📄 Markdown Note (.md)",
            data=markdown_content,
            file_name=f"{file_slug}_notes.md",
            mime="text/markdown",
            key=f"{key_prefix}_md",
            use_container_width=True
        )
    with col_d2:
        plain_text = generate_export_document(title, markdown_content, doc_format="txt")
        st.download_button(
            label="📝 Text File (.txt)",
            data=plain_text,
            file_name=f"{file_slug}_notes.txt",
            mime="text/plain",
            key=f"{key_prefix}_txt",
            use_container_width=True
        )
    with col_d3:
        html_doc = generate_export_document(title, markdown_content, doc_format="html")
        st.download_button(
            label="🌐 Printable HTML (.html)",
            data=html_doc,
            file_name=f"{file_slug}_notes.html",
            mime="text/html",
            key=f"{key_prefix}_html",
            use_container_width=True
        )
