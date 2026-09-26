"""
View controller for Module 3: Multimodal Notes Summarizer & Cheat-Sheet Generator.
Implements pre-loaded sample notes, quick summary buttons, audio player, and instant exports.
"""

import streamlit as st
from backend.services import generate_summary, generate_tts_audio
from backend.parsers import extract_text_from_pdf, extract_delimited_section
from frontend.components import render_export_buttons

SAMPLE_NOTES = """# Artificial Intelligence & Machine Learning Overview

## 1. Fundamental Paradigms
- Supervised Learning: Algorithms learn from labeled training pairs (Input X -> Label Y). Common models include Linear Regression, Support Vector Machines, and Convolutional Neural Networks.
- Unsupervised Learning: Discovers hidden patterns in unlabeled data. Key methods include K-Means Clustering and Principal Component Analysis (PCA).
- Reinforcement Learning: An agent learns through trial-and-error by taking actions in an environment to maximize cumulative reward signals.

## 2. Deep Learning Architecture
Neural networks consist of stacked layers of interconnected nodes (neurons). Each connection has a learnable weight. During training, the network uses:
1. Forward Propagation: Calculates output predictions from inputs.
2. Loss Function: Measures discrepancy between predicted and ground-truth values.
3. Backpropagation: Uses the chain rule of calculus to compute gradient of loss with respect to every weight.
4. Optimizer (SGD, Adam): Updates weights in the opposite direction of the gradient to minimize loss.

## 3. Key Formulas & Rules of Thumb
- Mean Squared Error (MSE): Loss = (1/n) * sum((y_pred - y_true)^2)
- Gradient Descent Update: W_new = W_old - (learning_rate * gradient)
- Activation Rule: ReLU(x) = max(0, x) is preferred for deep hidden layers to avoid vanishing gradients.
"""


def render_summarizer_view(api_key: str, model_name: str):
    """Renders the study notes summarizer and cheat-sheet module."""
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h2 style="margin: 0; display: flex; align-items: center; gap: 10px;">
            <span>📝</span> Notes Summarizer & Exam Cheat-Sheet
        </h2>
        <div style="color: #94a3b8; font-size: 0.95rem; margin-top: 4px;">
            Condense lengthy study materials or test immediately with built-in sample notes — no file upload required!
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Initialize sample notes into session if empty
    if "summarizer_text_input" not in st.session_state:
        st.session_state["summarizer_text_input"] = ""

    # Quick Sample Load Button
    col_s_top1, col_s_top2 = st.columns([1.2, 4])
    with col_s_top1:
        if st.button("📋 Load Sample AI Notes", key="summarizer_load_sample_btn", use_container_width=True):
            st.session_state["summarizer_text_input"] = SAMPLE_NOTES
            st.rerun()

    col_input, col_output = st.columns([1, 1.3], gap="large")

    with col_input:
        with st.container(border=True):
            st.markdown("##### 📥 Study Material Input")

            notes_text = st.text_area(
                "Paste notes or type lecture text:",
                value=st.session_state.get("summarizer_text_input", ""),
                height=180,
                placeholder="Paste lecture transcript, reading material, or bullet notes here...",
                key="summarizer_text_input_field"
            )

            uploaded_doc = st.file_uploader(
                "📎 Optional: Attach document (.pdf, .txt):",
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
                st.error("🔑 Please enter a valid Gemini API Key in the sidebar or `.env` file.")
            elif not active_text.strip():
                st.warning("Please paste text, load sample notes, or upload a document to summarize.")
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
                        # Pre-generate Audio Stream
                        try:
                            audio_stream = generate_tts_audio(result["content"])
                            st.session_state.summarizer_audio = audio_stream.getvalue()
                        except Exception:
                            st.session_state.summarizer_audio = None
                        st.rerun()
                    else:
                        st.error(result["error"])

    with col_output:
        if st.session_state.get("summarizer_output"):
            raw_summary = st.session_state.summarizer_output

            # Audio Player Bar
            if st.session_state.get("summarizer_audio"):
                st.audio(st.session_state.summarizer_audio, format="audio/mp3")
            else:
                if st.button("🔊 Generate Summary Audio Recap", key="play_summary_tts", use_container_width=True):
                    with st.spinner("Synthesizing audio recap..."):
                        try:
                            audio_stream = generate_tts_audio(raw_summary)
                            st.session_state.summarizer_audio = audio_stream.getvalue()
                            st.rerun()
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
            <div style="background: rgba(18, 24, 38, 0.4); border: 1px dashed rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 42px 20px; text-align: center; color: #64748b;">
                <div style="font-size: 2.2rem; margin-bottom: 8px;">📑</div>
                <div style="font-size: 1rem; font-weight: 600; color: #94a3b8; margin-bottom: 4px;">Summarizer Workspace Ready</div>
                <div style="font-size: 0.84rem;">Click <b>Load Sample AI Notes</b> above or paste your study material to instantly generate cheat-sheets and audio recaps.</div>
            </div>
            """, unsafe_allow_html=True)
