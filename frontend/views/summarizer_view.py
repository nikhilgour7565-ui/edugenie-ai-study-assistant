"""
View controller for Module 3: Multimodal Notes Summarizer & Cheat-Sheet Generator.
Implements dual-column split layout (Input Dropzone vs. Structured Cheat-Sheet Tabs & Audio).
"""

import streamlit as st
from backend.services import generate_summary, generate_tts_audio
from backend.parsers import extract_text_from_pdf, extract_delimited_section
from frontend.components import render_export_buttons


def render_summarizer_view(api_key: str, model_name: str):
    """Renders the study notes summarizer and cheat-sheet module."""
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h2 style="margin: 0; display: flex; align-items: center; gap: 10px;">
            <span>📝</span> Notes Summarizer & Exam Cheat-Sheet
        </h2>
        <div style="color: #94a3b8; font-size: 0.95rem; margin-top: 4px;">
            Condense lengthy lecture transcripts, research papers, and textbook chapters into executive summaries and 1-page cheat sheets.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_input, col_output = st.columns([1, 1.3], gap="large")

    with col_input:
        with st.container(border=True):
            st.markdown("##### 📥 Study Material Dropzone")

            notes_text = st.text_area(
                "Paste notes, transcript, or article:",
                height=160,
                placeholder="Paste lecture transcript, reading material, or bullet notes here...",
                key="summarizer_text_input"
            )

            uploaded_doc = st.file_uploader(
                "📎 Or attach document (.pdf, .txt):",
                type=["pdf", "txt"],
                key="summarizer_doc_uploader"
            )

            # Live Stats
            active_text = notes_text
            if uploaded_doc is not None and not active_text.strip():
                if "pdf" in uploaded_doc.type:
                    active_text = extract_text_from_pdf(uploaded_doc.getvalue())
                else:
                    active_text = uploaded_doc.getvalue().decode("utf-8", errors="ignore")

            word_count = len(active_text.split()) if active_text.strip() else 0
            char_count = len(active_text)
            st.markdown(f'<div style="margin-bottom: 12px;"><span class="stat-pill">📊 {word_count} words | {char_count} chars</span></div>', unsafe_allow_html=True)

            summary_depth = st.radio(
                "Summary Detail Level:",
                ["Executive Overview (Fast Revision)", "In-Depth Structured Notes", "High-Yield Exam Cheat-Sheet"],
                index=1,
                key="summarizer_depth_radio"
            )

            summarize_btn = st.button("⚡ Condense & Extract Cheat-Sheet", type="primary", use_container_width=True, key="summarizer_submit_btn")

        if summarize_btn:
            if not api_key:
                st.error("🔑 Please enter a valid Gemini API Key in the sidebar.")
            elif not active_text.strip():
                st.warning("Please paste text or upload a document to summarize.")
            else:
                with st.spinner("Analyzing and condensing notes with Gemini..."):
                    result = generate_summary(
                        api_key=api_key,
                        model_name=model_name,
                        text_content=active_text,
                        summary_depth=summary_depth
                    )

                    if result["success"]:
                        st.session_state.summarizer_output = result["content"]
                    else:
                        st.error(result["error"])

    with col_output:
        if st.session_state.get("summarizer_output"):
            raw_summary = st.session_state.summarizer_output

            # Audio Recap Bar
            with st.container(border=True):
                col_audio, col_status = st.columns([1, 1.5])
                with col_audio:
                    if st.button("🔊 Listen to Audio Recap", key="play_summary_tts", use_container_width=True):
                        with st.spinner("Synthesizing audio recap..."):
                            try:
                                audio_stream = generate_tts_audio(raw_summary)
                                st.audio(audio_stream, format="audio/mp3")
                            except Exception as err:
                                st.warning(f"Audio generation unavailable: {str(err)}")

            # Tabbed Sections
            tab_sum1, tab_sum2, tab_sum3, tab_sum4 = st.tabs([
                "📌 Overview", "🔑 Glossary", "📑 Structured Notes", "🚀 1-Page Cheat Sheet"
            ])

            with tab_sum1:
                st.markdown(extract_delimited_section(raw_summary, "Overview") or raw_summary)
            with tab_sum2:
                st.markdown(extract_delimited_section(raw_summary, "Key Glossary") or "See Structured Notes tab.")
            with tab_sum3:
                st.markdown(extract_delimited_section(raw_summary, "Structured Notes") or "See Overview tab.")
            with tab_sum4:
                st.markdown(extract_delimited_section(raw_summary, "One-Page Cheat-Sheet") or "See Overview tab.")

            # Export Buttons
            render_export_buttons("Study Notes & Cheat-Sheet", raw_summary, key_prefix="summary_export")
        else:
            # Empty state placeholder
            st.markdown("""
            <div style="background: rgba(19, 27, 46, 0.5); border: 2px dashed rgba(255, 255, 255, 0.1); border-radius: 14px; padding: 48px 24px; text-align: center; color: #64748b;">
                <div style="font-size: 2.5rem; margin-bottom: 10px;">📑</div>
                <div style="font-size: 1.1rem; font-weight: 600; color: #94a3b8; margin-bottom: 6px;">Summarizer Workspace Ready</div>
                <div style="font-size: 0.88rem;">Paste notes or upload a PDF on the left and click <b>Condense & Extract</b> to generate structured revision materials.</div>
            </div>
            """, unsafe_allow_html=True)
