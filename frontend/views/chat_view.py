"""
View controller for Module 4: Socratic Instant Doubt Clarifier (Interactive Chat).
Implements floating prompt chips, custom styled user vs AI bubbles, and clear chat toolbars.
"""

import streamlit as st
from backend.services import chat_doubt_solver


def render_chat_view(api_key: str, model_name: str):
    """Renders the interactive chat-based doubt solver."""
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h2 style="margin: 0; display: flex; align-items: center; gap: 10px;">
            <span>💬</span> Instant Socratic AI Tutor
        </h2>
        <div style="color: #94a3b8; font-size: 0.95rem; margin-top: 4px;">
            Ask clarifying questions, debug code, or work through tricky homework problems with multi-turn conversational memory.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Top Toolbar
    col_chat_h, col_chat_clear = st.columns([5, 1.2])
    with col_chat_h:
        # Prompt Suggestion Chips
        st.markdown("""
        <div style="margin-bottom: 12px; display: flex; flex-wrap: wrap; gap: 6px; align-items: center;">
            <span style="font-size: 0.8rem; color: #94a3b8; margin-right: 4px;">Quick Prompts:</span>
            <span class="chip-btn">💡 Give an intuitive analogy</span>
            <span class="chip-btn">📐 Step-by-step example</span>
            <span class="chip-btn">⚠️ What are common mistakes?</span>
            <span class="chip-btn">🎯 Test my understanding</span>
        </div>
        """, unsafe_allow_html=True)
    with col_chat_clear:
        if st.button("🗑️ Clear Session", use_container_width=True, key="chat_clear_btn"):
            st.session_state.chat_messages = []
            st.rerun()

    # Display Chat History
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    if not st.session_state.chat_messages:
        st.markdown("""
        <div style="background: rgba(19, 27, 46, 0.4); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 14px; padding: 32px 20px; text-align: center; color: #64748b; margin-bottom: 20px;">
            <div style="font-size: 2rem; margin-bottom: 6px;">🧞</div>
            <div style="font-weight: 600; color: #cbd5e1; font-size: 1rem;">EduGenie Tutor is Online</div>
            <div style="font-size: 0.85rem; margin-top: 4px;">Type any question below or pick a prompt to start your learning session.</div>
        </div>
        """, unsafe_allow_html=True)

    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat Input Box
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
