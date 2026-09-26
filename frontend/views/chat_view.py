"""
View controller for Module 4: Socratic Instant Doubt Clarifier (Interactive Chat).
Implements clickable prompt chips, pre-loaded starter conversations, and styled chat messages.
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
            Ask clarifying questions, debug code, or pick a sample question below to start a learning session immediately!
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Initialize chat messages if not present
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    # Clickable Starter Prompt Chips
    st.markdown("""
    <div style="margin-bottom: 8px;">
        <span style="font-size: 0.8rem; color: #94a3b8;">Click a Sample Question to Ask:</span>
    </div>
    """, unsafe_allow_html=True)

    col_p1, col_p2, col_p3, col_p4 = st.columns(4)
    sample_queries = [
        "Why is quicksort O(n^2) worst case?",
        "Explain backpropagation using a simple chain rule example",
        "What is the difference between TCP and UDP?",
        "How do transformers use self-attention?"
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
            st.rerun()

    # Empty State Welcome Card
    if not st.session_state.chat_messages:
        st.markdown("""
        <div style="background: rgba(19, 27, 46, 0.4); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 14px; padding: 32px 20px; text-align: center; color: #64748b; margin-bottom: 20px;">
            <div style="font-size: 2rem; margin-bottom: 6px;">🧞</div>
            <div style="font-weight: 600; color: #cbd5e1; font-size: 1rem;">EduGenie Socratic Tutor is Online</div>
            <div style="font-size: 0.85rem; margin-top: 4px;">Click any sample question above or type your own question in the input bar below.</div>
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
                result = chat_doubt_solver(
                    api_key=api_key,
                    model_name=model_name,
                    conversation_history=history_to_send,
                    user_query=active_query
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
