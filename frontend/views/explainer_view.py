"""
View controller for Module 1: Adaptive Concept Explainer & Multimodal Tutor.
"""

import time
import streamlit as st
from backend.services import generate_explanation, generate_tts_audio
from backend.parsers import extract_delimited_section
from frontend.components import render_export_buttons


def render_explainer_view(api_key: str, model_name: str):
    """Renders the concept explainer module."""
    st.subheader("🎓 Adaptive Concept Explainer & Multimodal Tutor")
    st.caption("Learn any topic or upload diagrams, textbook pages, and PDFs for structured breakdowns and audio playback.")

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        topic = st.text_input(
            "Concept or Topic Name:",
            placeholder="e.g., Backpropagation, Photosynthesis, Bayes Theorem, TCP/IP Handshake",
            key="concept_topic_input"
        )
    with col2:
        audience_level = st.selectbox(
            "Audience Level",
            [
                "Explain Like I'm 5 (ELI5)",
                "Beginner / High School",
                "Undergraduate / University",
                "Advanced / Industry Professional"
            ],
            index=1
        )
    with col3:
        output_style = st.selectbox(
            "Learning Style",
            [
                "Balanced & Structured",
                "Story & Analogy Driven",
                "Real-World Industry Applications",
                "Concise Bullet Cheatsheet"
            ],
            index=0
        )

    # Multimodal File Ingestion
    uploaded_file = st.file_uploader(
        "📎 Optional: Upload Diagram, Textbook Page, or PDF (.png, .jpg, .pdf, .txt)",
        type=["png", "jpg", "jpeg", "pdf", "txt"],
        key="explainer_file_uploader"
    )

    generate_btn = st.button("🚀 Explain Concept & Process Attachments", type="primary", use_container_width=True)

    if generate_btn:
        if not api_key:
            st.error("🔑 Please provide a valid Gemini API Key in the sidebar or `.env` file.")
            return

        if not topic.strip() and not uploaded_file:
            st.warning("Please enter a concept name or upload a document/diagram.")
            return

        start_time = time.time()
        with st.spinner("Analyzing concept and synthesizing structured explanation..."):
            file_bytes = uploaded_file.getvalue() if uploaded_file else None
            file_type = uploaded_file.type if uploaded_file else None

            result = generate_explanation(
                api_key=api_key,
                model_name=model_name,
                topic=topic,
                audience_level=audience_level,
                output_style=output_style,
                uploaded_file_bytes=file_bytes,
                file_type=file_type
            )

            if result["success"]:
                elapsed = round(time.time() - start_time, 2)
                st.session_state.explainer_output = {
                    "topic": topic if topic else "Uploaded Document Analysis",
                    "content": result["content"],
                    "time": elapsed,
                    "level": audience_level
                }
            else:
                st.error(result["error"])

    # Render Explainer Output
    if st.session_state.get("explainer_output"):
        exp_data = st.session_state.explainer_output
        st.markdown("---")
        
        # Meta Header
        st.markdown(f"""
        <div style="display: flex; gap: 8px; align-items: center; margin-bottom: 14px;">
            <span class="badge-tag badge-purple">Topic: {exp_data['topic']}</span>
            <span class="badge-tag badge-blue">Level: {exp_data['level']}</span>
            <span class="stat-pill">⏱️ Generated in {exp_data['time']}s</span>
        </div>
        """, unsafe_allow_html=True)

        raw_text = exp_data["content"]
        
        # Audio Player
        if st.button("🔊 Listen to Audio Explanation", key="play_explainer_tts"):
            with st.spinner("Synthesizing audio..."):
                try:
                    audio_stream = generate_tts_audio(raw_text)
                    st.audio(audio_stream, format="audio/mp3")
                except Exception as err:
                    st.warning(f"Audio generation unavailable: {str(err)}")

        # Tabbed Sections
        tab_intuition, tab_deep, tab_analogy, tab_apps, tab_quiz, tab_full = st.tabs([
            "💡 Intuition", "🔍 Deep Breakdown", "🌟 Analogy", "🛠️ Applications", "❓ Self-Check", "📑 Full Note"
        ])

        with tab_intuition:
            content = extract_delimited_section(raw_text, "Core Intuition") or raw_text
            st.markdown(content)
        with tab_deep:
            content = extract_delimited_section(raw_text, "Deep Breakdown") or "See Full Note tab."
            st.markdown(content)
        with tab_analogy:
            content = extract_delimited_section(raw_text, "Real-World Analogy") or "See Full Note tab."
            st.markdown(content)
        with tab_apps:
            content = extract_delimited_section(raw_text, "Industry Applications") or "See Full Note tab."
            st.markdown(content)
        with tab_quiz:
            content = extract_delimited_section(raw_text, "Self-Check Quiz") or "See Full Note tab."
            st.markdown(content)
        with tab_full:
            st.markdown(raw_text)

        # Download Buttons
        render_export_buttons(exp_data["topic"], raw_text, key_prefix="explainer_export")
