"""
View controller for Module 1: Adaptive Concept Explainer & Multimodal Tutor.
Implements unified glassmorphic input cards, compact file dropzone, and responsive tabbed output.
"""

import time
import streamlit as st
from backend.services import generate_explanation, generate_tts_audio
from backend.parsers import extract_delimited_section
from frontend.components import render_export_buttons


def render_explainer_view(api_key: str, model_name: str):
    """Renders the concept explainer module with clean SaaS layout."""
    st.markdown("""
    <div style="margin-bottom: 18px;">
        <h2 style="margin: 0; display: flex; align-items: center; gap: 8px; font-size: 1.4rem;">
            <span>🎓</span> Adaptive Concept Explainer
        </h2>
        <div style="color: #94a3b8; font-size: 0.88rem; margin-top: 2px;">
            Deconstruct difficult STEM and humanities topics with calibrated depth, real-world analogies, and audio playback.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_input, col_output = st.columns([1, 1.4], gap="large")

    with col_input:
        with st.container(border=True):
            st.markdown("<div style='font-weight: 700; font-size: 0.95rem; color: #f8fafc; margin-bottom: 10px;'>⚙️ Learning Parameters</div>", unsafe_allow_html=True)

            topic = st.text_input(
                "Concept / Topic Name",
                placeholder="e.g., Backpropagation, Photosynthesis, Bayes Theorem",
                key="concept_topic_input"
            )

            col_sub1, col_sub2 = st.columns(2)
            with col_sub1:
                audience_level = st.selectbox(
                    "Audience Depth",
                    [
                        "Explain Like I'm 5 (ELI5)",
                        "Beginner / High School",
                        "Undergraduate / University",
                        "Advanced / Industry Professional"
                    ],
                    index=1,
                    key="concept_audience_select"
                )
            with col_sub2:
                output_style = st.selectbox(
                    "Learning Focus",
                    [
                        "Balanced & Structured",
                        "Story & Analogy Driven",
                        "Real-World Applications",
                        "Concise Bullet Cheatsheet"
                    ],
                    index=0,
                    key="concept_style_select"
                )

            uploaded_file = st.file_uploader(
                "📎 Attach Diagram or Document (.png, .jpg, .pdf, .txt)",
                type=["png", "jpg", "jpeg", "pdf", "txt"],
                key="explainer_file_uploader"
            )

            generate_btn = st.button("🚀 Explain Concept & Process Attachments", type="primary", use_container_width=True, key="explainer_submit_btn")

        if generate_btn:
            if not api_key:
                st.error("🔑 Please provide a valid Gemini API Key in the sidebar or `.env` file.")
            elif not topic.strip() and not uploaded_file:
                st.warning("Please enter a concept name or upload a document/diagram.")
            else:
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

    with col_output:
        if st.session_state.get("explainer_output"):
            exp_data = st.session_state.explainer_output
            raw_text = exp_data["content"]

            # Output Header Toolbar
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; flex-wrap: wrap; gap: 8px;">
                <div style="display: flex; gap: 6px; align-items: center;">
                    <span class="badge-tag badge-purple">Topic: {exp_data['topic']}</span>
                    <span class="badge-tag badge-blue">{exp_data['level']}</span>
                </div>
                <span class="badge-tag badge-cyan">⏱️ Generated in {exp_data['time']}s</span>
            </div>
            """, unsafe_allow_html=True)

            # Audio Player Toolbar
            with st.container(border=True):
                col_audio_btn, col_audio_status = st.columns([1, 1.5])
                with col_audio_btn:
                    if st.button("🔊 Listen to Audio Lesson", key="play_explainer_tts", use_container_width=True):
                        with st.spinner("Generating audio..."):
                            try:
                                audio_stream = generate_tts_audio(raw_text)
                                st.audio(audio_stream, format="audio/mp3")
                            except Exception as err:
                                st.warning(f"Audio generation unavailable: {str(err)}")

            # Structured Tabs
            tab_intuition, tab_deep, tab_analogy, tab_apps, tab_quiz, tab_full = st.tabs([
                "💡 Intuition", "🔍 Deep Dive", "🌟 Analogy", "🛠️ Applications", "❓ Self-Check", "📑 Full Note"
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

            # Export Buttons
            render_export_buttons(exp_data["topic"], raw_text, key_prefix="explainer_export")
        else:
            # Empty state placeholder
            st.markdown("""
            <div style="background: rgba(18, 24, 38, 0.4); border: 1px dashed rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 42px 20px; text-align: center; color: #64748b;">
                <div style="font-size: 2.2rem; margin-bottom: 8px;">📖</div>
                <div style="font-size: 1rem; font-weight: 600; color: #94a3b8; margin-bottom: 4px;">Explanation Workspace Ready</div>
                <div style="font-size: 0.84rem;">Configure parameters on the left and click <b>Explain Concept</b> to generate tabbed lessons and audio.</div>
            </div>
            """, unsafe_allow_html=True)
