"""
View controller for Module 2: Smart Quiz & Flashcard Deck Generator.
"""

import streamlit as st
from backend.services import generate_quiz, generate_flashcards


def render_quiz_view(api_key: str, model_name: str):
    """Renders the quiz and flashcard generator module."""
    st.subheader("❓ Smart Quiz & Interactive Flashcard Generator")
    st.caption("Reinforce knowledge with interactive auto-graded questions or high-yield active recall flashcards.")

    tab_quiz, tab_flashcards = st.tabs(["📝 Multiple-Choice Quiz", "🗂️ Interactive Flashcard Deck"])

    with tab_quiz:
        col_q1, col_q2, col_q3 = st.columns([2, 1, 1])
        with col_q1:
            quiz_topic = st.text_input("Quiz Topic / Subject Area:", placeholder="e.g., Cellular Respiration, Operating Systems, Machine Learning")
        with col_q2:
            num_questions = st.selectbox("Number of Questions", [3, 5, 10], index=1)
        with col_q3:
            difficulty = st.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"], index=1)

        create_quiz_btn = st.button("🎯 Generate Dynamic Quiz", type="primary")

        if create_quiz_btn:
            if not api_key:
                st.error("🔑 Please enter a valid Gemini API Key.")
                return

            if not quiz_topic.strip():
                st.warning("Please enter a quiz topic.")
                return

            with st.spinner("Generating quiz questions with Gemini..."):
                result = generate_quiz(
                    api_key=api_key,
                    model_name=model_name,
                    topic=quiz_topic,
                    num_questions=num_questions,
                    difficulty=difficulty
                )

                if result["success"]:
                    st.session_state.quiz_data = result["data"]
                    st.session_state.user_quiz_answers = {}
                    st.session_state.quiz_submitted = False
                    st.success(f"Generated {len(result['data'])} interactive questions!")
                else:
                    st.error(result["error"])

        # Render Quiz Deck
        if st.session_state.get("quiz_data"):
            st.markdown("---")
            st.subheader("✍️ Answer the Questions:")

            for idx, q in enumerate(st.session_state.quiz_data):
                st.markdown(f"""
                <div class="glass-card">
                    <div class="glass-card-header">
                        <span class="badge-tag badge-blue">Q{idx + 1}</span>
                        <span>{q['question']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                selected_opt = st.radio(
                    f"Select answer for Q{idx + 1}:",
                    options=q["options"],
                    key=f"quiz_q_{idx}",
                    index=None,
                    label_visibility="collapsed"
                )
                st.session_state.user_quiz_answers[idx] = selected_opt
                st.write("")

            col_sub, col_reset = st.columns([1, 4])
            with col_sub:
                if st.button("📊 Submit & Grade Quiz", type="primary", use_container_width=True):
                    st.session_state.quiz_submitted = True

            if st.session_state.get("quiz_submitted"):
                score = 0
                total = len(st.session_state.quiz_data)
                
                st.markdown("---")
                st.subheader("📈 Assessment & Detailed Breakdown:")

                for idx, q in enumerate(st.session_state.quiz_data):
                    user_ans = st.session_state.user_quiz_answers.get(idx)
                    correct_ans = q["correct_answer"]
                    is_correct = (user_ans == correct_ans)

                    if is_correct:
                        score += 1
                        st.success(f"**Q{idx + 1}: Correct!** ✅ (Your Answer: {user_ans})")
                    else:
                        st.error(f"**Q{idx + 1}: Incorrect** ❌ | Your Answer: `{user_ans or 'Unanswered'}` | Correct: `{correct_ans}`")

                    st.info(f"💡 **Explanation:** {q.get('explanation', 'No explanation provided.')}")
                    st.write("")

                percentage = score / total
                st.progress(percentage)
                st.metric(label="🏆 Final Score", value=f"{score}/{total} ({percentage*100:.1f}%)")

                if percentage >= 0.8:
                    st.balloons()
                    st.markdown('<span class="badge-tag badge-green">🌟 Mastery Achieved - Outstanding Work!</span>', unsafe_allow_html=True)
                elif percentage >= 0.5:
                    st.markdown('<span class="badge-tag badge-amber">👍 Solid Effort - Review explanations to close gaps.</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="badge-tag badge-purple">📚 Needs Revision - Try re-explaining the topic in Module 1.</span>', unsafe_allow_html=True)

    with tab_flashcards:
        col_f1, col_f2 = st.columns([3, 1])
        with col_f1:
            fc_topic = st.text_input("Flashcards Topic / Subject Area:", placeholder="e.g., Machine Learning Metrics, Mitosis Phases, Python Dunder Methods", key="fc_topic_input")
        with col_f2:
            fc_count = st.selectbox("Number of Cards", [5, 8, 12], index=0)

        create_fc_btn = st.button("🗂️ Generate Flashcard Deck", type="primary")

        if create_fc_btn:
            if not api_key:
                st.error("🔑 Please enter a valid Gemini API Key.")
                return

            if not fc_topic.strip():
                st.warning("Please enter a flashcard topic.")
                return

            with st.spinner("Generating flashcards..."):
                result = generate_flashcards(
                    api_key=api_key,
                    model_name=model_name,
                    topic=fc_topic,
                    count=fc_count
                )

                if result["success"]:
                    st.session_state.flashcards_data = result["data"]
                    st.success(f"Generated {len(result['data'])} flashcards!")
                else:
                    st.error(result["error"])

        if st.session_state.get("flashcards_data"):
            st.markdown("---")
            st.subheader("💡 Flip & Review Flashcards:")
            for idx, card in enumerate(st.session_state.flashcards_data):
                with st.expander(f"📌 Card #{idx+1}: {card.get('front')}", expanded=False):
                    st.markdown(f"""
                    <div class="flashcard-box">
                        <div class="flashcard-front">❓ {card.get('front')}</div>
                        <div class="flashcard-back">💡 {card.get('back')}</div>
                    </div>
                    """, unsafe_allow_html=True)
