"""
Reusable Streamlit UI components and widgets for EduGenie.
Featuring an interactive, functional sidebar equipped with:
- Module Navigation
- One-Click Quick Launchers (Auto-load topics into any module)
- Live Study Session Tracker (Questions answered, notes reviewed, concepts learned)
- API Connection Badge & Cache Reset
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
    Renders a fully interactive, functional sidebar:
    1. App Identity Card with live API status
    2. Primary Study Tool Navigation
    3. Quick Topic Launchers (loads topic directly into the selected tool)
    4. Live Study Progress & Session Metrics
    5. Action toolbar (Reset Session, Documentation)
    """
    api_key = resolve_api_key()
    model_name = "gemini-3.8-flash"

    # Initialize study session counters in session_state
    if "concepts_explored" not in st.session_state:
        st.session_state.concepts_explored = 0
    if "quizzes_completed" not in st.session_state:
        st.session_state.quizzes_completed = 0
    if "doubts_resolved" not in st.session_state:
        st.session_state.doubts_resolved = 0

    with st.sidebar:
        # 1. App Identity Card
        st.markdown("""
        <div class="sidebar-brand-card">
            <div class="brand-icon">🎓</div>
            <div>
                <div class="brand-title">EduGenie</div>
                <div class="brand-subtitle">Gemini AI Study Suite</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 2. Primary Navigation
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

        # 3. Interactive Quick Subject Presets
        with st.container(border=True):
            st.markdown("<div style='font-weight: 700; font-size: 0.88rem; color: #f1f5f9; margin-bottom: 6px;'>⚡ Quick Subject Presets</div>", unsafe_allow_html=True)
            st.caption("Click to automatically load a topic into your active tool:")

            col_q1, col_q2 = st.columns(2)
            with col_q1:
                if st.button("🧬 Biology", key="side_preset_bio", use_container_width=True):
                    st.session_state["concept_topic_input"] = "Photosynthesis & Cellular Respiration"
                    st.session_state["quiz_topic_input"] = "Cellular Biology & Genetics"
                    st.rerun()
                if st.button("⚛️ Physics", key="side_preset_phy", use_container_width=True):
                    st.session_state["concept_topic_input"] = "Quantum Mechanics & Superposition"
                    st.session_state["quiz_topic_input"] = "Newtonian Mechanics & Laws of Motion"
                    st.rerun()
            with col_q2:
                if st.button("💻 CompSci", key="side_preset_cs", use_container_width=True):
                    st.session_state["concept_topic_input"] = "Transformer Neural Networks"
                    st.session_state["quiz_topic_input"] = "Data Structures & Algorithms"
                    st.rerun()
                if st.button("📐 Math", key="side_preset_math", use_container_width=True):
                    st.session_state["concept_topic_input"] = "Bayes' Theorem & Conditional Probability"
                    st.session_state["quiz_topic_input"] = "Calculus & Linear Algebra"
                    st.rerun()

        # 4. Live Session Activity Tracker
        with st.container(border=True):
            st.markdown("<div style='font-weight: 700; font-size: 0.88rem; color: #f1f5f9; margin-bottom: 6px;'>📊 Live Session Metrics</div>", unsafe_allow_html=True)
            
            # Count active session activities
            c_count = 1 if st.session_state.get("explainer_output") else 0
            q_count = len(st.session_state.get("quiz_data", []))
            d_count = len(st.session_state.get("chat_messages", [])) // 2

            st.markdown(f"""
            <div style="font-size: 0.8rem; color: #94a3b8; line-height: 1.8;">
                <div>• 💡 Concepts Explained: <b style="color: #38bdf8;">{c_count}</b></div>
                <div>• ✍️ Active Questions: <b style="color: #a78bfa;">{q_count}</b></div>
                <div>• 💬 Doubts Discussed: <b style="color: #34d399;">{d_count}</b></div>
            </div>
            """, unsafe_allow_html=True)

        # 5. Session Actions & Status
        st.markdown("<div style='margin-top: 6px;'></div>", unsafe_allow_html=True)
        col_side_rst, col_side_status = st.columns([1.2, 1])
        with col_side_rst:
            if st.button("🔄 Reset Workspace", key="side_clear_all", use_container_width=True):
                st.session_state.explainer_output = None
                st.session_state.explainer_audio = None
                st.session_state.quiz_data = None
                st.session_state.user_quiz_answers = {}
                st.session_state.quiz_submitted = False
                st.session_state.flashcards_data = None
                st.session_state.summarizer_output = None
                st.session_state.summarizer_audio = None
                st.session_state.chat_messages = []
                st.rerun()
        with col_side_status:
            if api_key:
                st.markdown('<div style="text-align: right; padding-top: 6px;"><span class="badge-tag badge-green">🟢 Active</span></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div style="text-align: right; padding-top: 6px;"><span class="badge-tag badge-amber">⚠️ No Key</span></div>', unsafe_allow_html=True)

    return api_key, model_name, selected_module


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
