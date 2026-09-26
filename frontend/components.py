"""
Reusable Streamlit UI components and widgets for EduGenie.
"""

from typing import Tuple
import streamlit as st
from backend.gemini_client import resolve_api_key
from backend.parsers import generate_export_document


def render_hero_banner():
    """Renders the top promotional hero banner."""
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">🧞 EduGenie: AI Learning Companion</div>
        <div class="hero-subtitle">Supercharge your studies with multimodal document ingestion, audio revision, interactive quizzes, active recall flashcards, and 24/7 instant doubt clarification powered by Google Gemini.</div>
        <div class="pill-container">
            <span class="feature-pill">📄 PDF & Diagram Multimodal Intake</span>
            <span class="feature-pill">🔊 Audio Text-to-Speech</span>
            <span class="feature-pill">🎓 Adaptive Explanations</span>
            <span class="feature-pill">❓ Smart MCQs & Scoring</span>
            <span class="feature-pill">🗂️ Flip Flashcards</span>
            <span class="feature-pill">📝 Exam Cheat-Sheets</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar() -> Tuple[str, str, str]:
    """Renders sidebar controls and returns (api_key, model_name, selected_module)."""
    with st.sidebar:
        st.markdown("### ⚙️ Engine Settings")

        # Resolve API Key
        default_key = resolve_api_key()
        user_api_key = st.text_input(
            "🔑 Gemini API Key",
            value=default_key,
            type="password",
            help="Provide your Google Gemini API key. Pre-configured secrets will auto-populate here."
        )
        selected_api_key = user_api_key.strip() if user_api_key else default_key

        # Model Selection
        selected_model = st.selectbox(
            "⚡ Gemini Model",
            options=["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash-exp"],
            index=0,
            help="`gemini-1.5-flash` provides ultra-fast, reliable multimodal reasoning."
        )

        st.markdown("---")
        st.markdown("### 📚 Navigation")
        selected_module = st.radio(
            "Choose Learning Tool:",
            options=[
                "🎓 Concept Explainer",
                "❓ Smart Quiz & Flashcards",
                "📝 Notes Summarizer & Cheat-Sheet",
                "💬 Instant Doubt Clarifier"
            ],
            index=0
        )

        st.markdown("---")
        if selected_api_key:
            st.markdown('<span class="badge-tag badge-green">● API Key Connected</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="badge-tag badge-amber">⚠️ API Key Required</span>', unsafe_allow_html=True)

        st.markdown("---")
        st.caption("Powered by Google GenAI SDK & Streamlit")

    return selected_api_key, selected_model, selected_module


def render_export_buttons(title: str, markdown_content: str, key_prefix: str = "export"):
    """Renders 3-column export download buttons (.md, .txt, .html)."""
    st.markdown("##### 📥 Export Study Package:")
    col_d1, col_d2, col_d3 = st.columns(3)
    
    file_slug = title.lower().replace(" ", "_")[:30]

    with col_d1:
        st.download_button(
            label="📄 Download Markdown (.md)",
            data=markdown_content,
            file_name=f"{file_slug}_notes.md",
            mime="text/markdown",
            key=f"{key_prefix}_md",
            use_container_width=True
        )
    with col_d2:
        plain_text = generate_export_document(title, markdown_content, doc_format="txt")
        st.download_button(
            label="📝 Download Plain Text (.txt)",
            data=plain_text,
            file_name=f"{file_slug}_notes.txt",
            mime="text/plain",
            key=f"{key_prefix}_txt",
            use_container_width=True
        )
    with col_d3:
        html_doc = generate_export_document(title, markdown_content, doc_format="html")
        st.download_button(
            label="🌐 Download Printable HTML",
            data=html_doc,
            file_name=f"{file_slug}_notes.html",
            mime="text/html",
            key=f"{key_prefix}_html",
            use_container_width=True
        )
