"""
View controller for Module 4: Socratic Instant Doubt Clarifier (Interactive Chat).
"""

import streamlit as st
from backend.services import chat_doubt_solver


def render_chat_view(api_key: str, model_name: str):
    """Renders the interactive chat-based doubt solver."""
    st.subheader("💬 Instant 24/7 AI Tutor & Doubt Clarifier")
    st.caption("Ask questions, request simpler explanations, or debug homework problems with persistent multi-turn conversational context.")

    col_chat_h, col_chat_clear = st.columns([5, 1])
    with col_chat_clear:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_messages = []
            st.rerun()

    st.markdown("""
    <div style="margin-bottom: 12px;">
        <span style="font-size: 0.8rem; color: #94a3b8; margin-right: 6px;">Quick Prompts:</span>
        <span class="chip-btn">💡 Give an intuitive analogy</span>
        <span class="chip-btn">📐 Step-by-step example</span>
        <span class="chip-btn">⚠️ What are common mistakes?</span>
        <span class="chip-btn">🎯 Test my understanding</span>
    </div>
    """, unsafe_allow_html=True)

    # Display chat history
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User Input
    if user_doubt := st.chat_input("Ask a doubt, paste code, or request an explanation..."):
        if not api_key:
            st.error("🔑 Please enter a valid Gemini API Key in the sidebar.")
            return

        st.session_state.chat_messages.append({"role": "user", "content": user_doubt})
        with st.chat_message("user"):
            st.markdown(user_doubt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            with st.spinner("EduGenie is thinking..."):
                history_to_send = st.session_state.chat_messages[:-1]
                result = chat_doubt_solver(
                    api_key=api_key,
                    model_name=model_name,
                    conversation_history=history_to_send,
                    user_query=user_doubt
                )

                if result["success"]:
                    bot_reply = result["reply"]
                    message_placeholder.markdown(bot_reply)
                    st.session_state.chat_messages.append({"role": "assistant", "content": bot_reply})
                else:
                    error_msg = result["error"]
                    message_placeholder.error(error_msg)
                    st.session_state.chat_messages.append({"role": "assistant", "content": error_msg})
