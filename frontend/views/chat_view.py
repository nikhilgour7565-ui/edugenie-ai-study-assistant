"""
View controller for Module 4: Socratic Instant Doubt Clarifier (Interactive Chat).
Answers doubts, explains solutions, and debugs code with optional reference document context.
"""

import streamlit as st
from backend.services import chat_doubt_solver
from backend.parsers import extract_text_from_pdf


def render_chat_view(api_key: str, model_name: str):
    """Renders the interactive chat-based doubt solver."""
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h2 style="margin: 0; display: flex; align-items: center; gap: 10px;">
            <span>💬</span> Instant Socratic AI Tutor
        </h2>
        <div style="color: #94a3b8; font-size: 0.95rem; margin-top: 4px;">
            Ask clarifying questions, debug code, or attach notes for contextual doubt resolution.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Initialize chat messages if not present
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    # Optional Context Attachment & Session Controls
    with st.expander("📎 Optional: Attach Subject Material / Reference Document for Context", expanded=False):
        chat_doc = st.file_uploader(
            "Upload lecture notes, assignment, or chapter (.pdf, .txt):",
            type=["pdf", "txt"],
            key="chat_context_doc"
        )
        if chat_doc is not None:
            if "pdf" in chat_doc.type:
                st.session_state.chat_context_text = extract_text_from_pdf(chat_doc.getvalue())
            else:
                st.session_state.chat_context_text = chat_doc.getvalue().decode("utf-8", errors="ignore")
            st.success(f"Attached context from '{chat_doc.name}' ({len(st.session_state.chat_context_text)} chars).")

    # Clickable Starter Prompt Chips
    st.markdown("""
    <div style="margin-bottom: 8px;">
        <span style="font-size: 0.8rem; color: #94a3b8;">Suggested Doubts to Explore:</span>
    </div>
    """, unsafe_allow_html=True)

    col_p1, col_p2, col_p3, col_p4 = st.columns(4)
    sample_queries = [
        "Why is quicksort O(n^2) worst case?",
        "Explain backpropagation step-by-step",
        "What is the difference between TCP and UDP?",
        "How does attention mechanism work in LLMs?"
    ]

    selected_prompt = None
    for idx, (c, q_text) in enumerate(zip([col_p1, col_p2, col_p3, col_p4], sample_queries)):
        with c:
            if st.button(f"💡 {q_text[:28]}...", key=f"chat_chip_{idx}", use_container_width=True, help=q_text):
                selected_prompt = q_text

    # Top Toolbar
    col_chat_h, col_chat_clear = st.columns([5, 1.2])
    with col_chat_clear:
        if st.button("🗑️ Clear Session", use_container_width=True, key="chat_clear_btn"):
            st.session_state.chat_messages = []
            st.session_state.chat_context_text = None
            st.rerun()

    # Empty State Welcome Card
    if not st.session_state.chat_messages:
        st.markdown("""
        <div style="background: rgba(19, 27, 46, 0.4); border: 1px dashed rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 32px 20px; text-align: center; color: #64748b; margin-bottom: 20px;">
            <div style="font-size: 2rem; margin-bottom: 6px;">🧞</div>
            <div style="font-weight: 600; color: #cbd5e1; font-size: 1rem;">EduGenie Socratic Tutor is Ready</div>
            <div style="font-size: 0.85rem; margin-top: 4px;">Type your doubt, question, or code snippet in the input bar below to start your real-time learning session.</div>
        </div>
        """, unsafe_allow_html=True)

    # Render Chat History
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Determine Active Input (from input box or clicked chip)
    user_input = st.chat_input("Ask a doubt, paste code, or request an explanation...")
    active_query = user_input or selected_prompt

    if active_query:
        if not api_key:
            st.error("🔑 Please enter a valid Gemini API Key in the sidebar or `.env` file.")
            return

        st.session_state.chat_messages.append({"role": "user", "content": active_query})
        with st.chat_message("user"):
            st.markdown(active_query)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            with st.spinner("EduGenie is analyzing and preparing a structured response..."):
                history_to_send = st.session_state.chat_messages[:-1]
                context_to_send = st.session_state.get("chat_context_text")
                result = chat_doubt_solver(
                    api_key=api_key,
                    model_name=model_name,
                    conversation_history=history_to_send,
                    user_query=active_query,
                    context_text=context_to_send
                )

                if result["success"]:
                    bot_reply = result["reply"]
                    message_placeholder.markdown(bot_reply)
                    st.session_state.chat_messages.append({"role": "assistant", "content": bot_reply})
                    st.rerun()
                else:
                    error_msg = result["error"]
                    message_placeholder.error(error_msg)
                    st.session_state.chat_messages.append({"role": "assistant", "content": error_msg})
