"""
Reusable Streamlit UI components and widgets for EduGenie.
Implements the redesigned vertical sidebar hierarchy, hero banners,
and multi-format export buttons.
"""

from typing import Tuple
import streamlit as st
from backend.gemini_client import resolve_api_key
from backend.parsers import generate_export_document


def render_hero_banner():
    """Renders the top promotional hero banner."""
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">🧞 EduGenie <span style="font-size: 1.1rem; color: #a5f3fc; font-weight: 600; padding: 2px 10px; background: rgba(6, 182, 212, 0.2); border-radius: 20px; border: 1px solid rgba(6, 182, 212, 0.4);">v1.0 Pro</span></div>
        <div class="hero-subtitle">Adaptive AI study companion powered by Google Gemini. Transform dense textbooks, diagrams, and lecture notes into interactive explanations, audio lessons, and active-recall quizzes.</div>
        <div class="pill-container">
            <span class="feature-pill">📄 Multimodal PDF/Diagram Intake</span>
            <span class="feature-pill">🔊 Text-to-Speech Audio</span>
            <span class="feature-pill">🎓 Calibrated Explanations</span>
            <span class="feature-pill">❓ Dynamic MCQs & Grading</span>
            <span class="feature-pill">🗂️ Active Recall Flashcards</span>
            <span class="feature-pill">📝 1-Page Exam Cheat Sheets</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar() -> Tuple[str, str, str]:
    """
    Renders the redesigned vertical visual sidebar:
    1. App Identity Card
    2. API & Model Configuration Card (bordered container)
    3. Navigation Menu
    4. Sidebar Footer (stats & links)
    """
    with st.sidebar:
        # 1. App Identity Card
        st.markdown("""
        <div class="sidebar-brand-card">
            <div class="brand-icon-wrapper">🎓</div>
            <div class="brand-title">EduGenie</div>
            <div class="brand-subtitle">Google Gemini AI Study Suite</div>
        </div>
        """, unsafe_allow_html=True)

        # 2. API & Model Configuration Card
        with st.container(border=True):
            st.markdown("##### ⚡ Engine & Auth")

            default_key = resolve_api_key()
            
            # API Status Pill
            if default_key:
                st.markdown('<div style="margin-bottom: 8px;"><span class="badge-tag badge-green">● Gemini API Active</span></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div style="margin-bottom: 8px;"><span class="badge-tag badge-amber">⚠️ Key Required</span></div>', unsafe_allow_html=True)

            user_api_key = st.text_input(
                "API Key",
                value=default_key,
                type="password",
                placeholder="AIzaSy...",
                help="Provide your Google Gemini API key. Pre-configured environment keys will auto-populate.",
                key="sidebar_api_key_input"
            )
            selected_api_key = user_api_key.strip() if user_api_key else default_key

            selected_model = st.selectbox(
                "Model Version",
                options=["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash-exp"],
                index=0,
                help="`gemini-1.5-flash` provides ultra-fast reasoning and low latency.",
                key="sidebar_model_select"
            )

        st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)

        # 3. Navigation Menu
        st.markdown("##### 📚 Study Modules")
        selected_module = st.radio(
            "Select Module:",
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

        st.markdown("---")

        # 4. Sidebar Footer
        st.markdown("""
        <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 10px; padding: 12px 14px; font-size: 0.78rem; color: #94a3b8;">
            <div style="font-weight: 700; color: #e2e8f0; margin-bottom: 4px;">🚀 Study Suite Status</div>
            <div>• Engine: Google GenAI</div>
            <div>• Latency: Sub-second Flash</div>
            <div>• Multimodal: PDF / Image / Text</div>
        </div>
        """, unsafe_allow_html=True)

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
