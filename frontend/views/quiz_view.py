"""
View controller for Module 2: Smart Quiz & Flashcard Deck Generator.
Generates dynamic quizzes and active recall flashcards strictly from the user's
specified topic or uploaded notes/documents (.pdf, .txt).
"""

import streamlit as st
from backend.services import generate_quiz, generate_flashcards
from backend.parsers import extract_text_from_pdf


def render_quiz_view(api_key: str, model_name: str):
    """Renders the quiz and flashcard generator module."""
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h2 style="margin: 0; display: flex; align-items: center; gap: 10px;">
            <span>❓</span> Smart Quiz & Flashcard Suite
        </h2>
        <div style="color: #94a3b8; font-size: 0.95rem; margin-top: 4px;">
            Generate real, calibrated AI quizzes and active-recall flashcards directly from your topic or uploaded study material.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Initialize state keys if not set
    if "quiz_data" not in st.session_state:
        st.session_state.quiz_data = None
        st.session_state.user_quiz_answers = {}
        st.session_state.quiz_submitted = False

    if "flashcards_data" not in st.session_state:
        st.session_state.flashcards_data = None

    # Quick Practice Preset Chips
    st.markdown("""
    <div style="margin-bottom: 12px; display: flex; align-items: center; gap: 6px; flex-wrap: wrap;">
        <span style="font-size: 0.8rem; color: #94a3b8;">Quick Topic Suggestions:</span>
    </div>
    """, unsafe_allow_html=True)

    col_c1, col_c2, col_c3, col_c4 = st.columns(4)
    quick_topics = ["Python & OOP", "Cell Biology & DNA", "Data Structures & Algos", "World History"]
    for idx, (c, topic_name) in enumerate(zip([col_c1, col_c2, col_c3, col_c4], quick_topics)):
        with c:
            if st.button(f"🎯 {topic_name}", key=f"quiz_quick_{idx}", use_container_width=True):
                st.session_state["quiz_topic_input"] = topic_name
                st.session_state["fc_topic_input"] = topic_name
                if api_key:
                    with st.spinner(f"Generating real quiz for '{topic_name}' with Gemini..."):
                        res = generate_quiz(api_key=api_key, model_name=model_name, topic=topic_name, num_questions=3, difficulty="Medium")
                        if res["success"]:
                            st.session_state.quiz_data = res["data"]
                            st.session_state.user_quiz_answers = {}
                            st.session_state.quiz_submitted = False
                            st.rerun()

    tab_quiz, tab_flashcards = st.tabs(["📝 Interactive Quiz Engine", "🗂️ Active Recall Flashcard Deck"])

    with tab_quiz:
        # Top Control Ribbon
        with st.container(border=True):
            col_q1, col_q2, col_q3 = st.columns([2.5, 1, 1], gap="medium")
            with col_q1:
                quiz_topic = st.text_input(
                    "Quiz Topic / Subject:",
                    placeholder="e.g., Cellular Respiration, Operating Systems, Machine Learning",
                    key="quiz_topic_input"
                )
            with col_q2:
                num_questions = st.selectbox("Questions:", [3, 5, 10], index=1, key="quiz_num_select")
            with col_q3:
                difficulty = st.selectbox("Difficulty:", ["Easy", "Medium", "Hard"], index=1, key="quiz_diff_select")

            quiz_file = st.file_uploader(
                "📎 Optional: Upload study document (.pdf, .txt) to generate questions directly from its content:",
                type=["pdf", "txt"],
                key="quiz_doc_uploader"
            )

            create_quiz_btn = st.button("🚀 Generate Quiz from Topic / Document", type="primary", use_container_width=True, key="quiz_generate_btn")

        if create_quiz_btn:
            if not api_key:
                st.error("🔑 Please enter a valid Gemini API Key in the sidebar or `.env` file.")
            elif not quiz_topic.strip() and not quiz_file:
                st.warning("Please enter a subject name or upload a document to generate quiz questions.")
            else:
                extracted_context = None
                if quiz_file is not None:
                    if "pdf" in quiz_file.type:
                        extracted_context = extract_text_from_pdf(quiz_file.getvalue())
                    else:
                        extracted_context = quiz_file.getvalue().decode("utf-8", errors="ignore")

                with st.spinner("Synthesizing dynamic quiz questions with Gemini..."):
                    result = generate_quiz(
                        api_key=api_key,
                        model_name=model_name,
                        topic=quiz_topic,
                        num_questions=num_questions,
                        difficulty=difficulty,
                        text_context=extracted_context
                    )

                    if result["success"]:
                        st.session_state.quiz_data = result["data"]
                        st.session_state.user_quiz_answers = {}
                        st.session_state.quiz_submitted = False
                        st.success(f"Generated {len(result['data'])} real questions for '{quiz_topic or quiz_file.name}'!")
                        st.rerun()
                    else:
                        st.error(result["error"])

        # Render Numbered Question Cards
        if st.session_state.get("quiz_data"):
            st.markdown("---")
            st.markdown("#### ✍️ Answer the Questions Below:")

            for idx, q in enumerate(st.session_state.quiz_data):
                st.markdown(f"""
                <div class="glass-card">
                    <div class="glass-card-header">
                        <span class="badge-tag badge-cyan">Question {idx + 1}</span>
                        <span>{q['question']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                selected_opt = st.radio(
                    f"Select answer for Question {idx + 1}:",
                    options=q["options"],
                    key=f"quiz_q_{idx}",
                    index=None,
                    label_visibility="collapsed"
                )
                st.session_state.user_quiz_answers[idx] = selected_opt
                st.write("")

            col_sub, col_reset = st.columns([1.5, 4])
            with col_sub:
                if st.button("📊 Submit & Grade Quiz", type="primary", use_container_width=True, key="quiz_grade_btn"):
                    st.session_state.quiz_submitted = True

            # Score Card & Breakdown
            if st.session_state.get("quiz_submitted"):
                score = 0
                total = len(st.session_state.quiz_data)
                
                st.markdown("---")
                st.markdown("#### 📈 Assessment & Detailed Rationale:")

                for idx, q in enumerate(st.session_state.quiz_data):
                    user_ans = st.session_state.user_quiz_answers.get(idx)
                    correct_ans = q["correct_answer"]
                    is_correct = (user_ans == correct_ans)

                    if is_correct:
                        score += 1
                        st.success(f"**Q{idx + 1}: Correct!** ✅ (Your Answer: `{user_ans}`)")
                    else:
                        st.error(f"**Q{idx + 1}: Incorrect** ❌ | Your Answer: `{user_ans or 'Unanswered'}` | Correct: `{correct_ans}`")

                    st.info(f"💡 **Explanation:** {q.get('explanation', 'No explanation provided.')}")
                    st.write("")

                percentage = score / total if total > 0 else 0
                st.progress(percentage)
                st.metric(label="🏆 Final Score", value=f"{score}/{total} ({percentage*100:.1f}%)")

                if percentage >= 0.8:
                    st.balloons()
                    st.markdown('<span class="badge-tag badge-green" style="font-size: 0.9rem;">🌟 Mastery Achieved - Outstanding Work!</span>', unsafe_allow_html=True)
                elif percentage >= 0.5:
                    st.markdown('<span class="badge-tag badge-amber" style="font-size: 0.9rem;">👍 Solid Effort - Review explanations to close gaps.</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="badge-tag badge-purple" style="font-size: 0.9rem;">📚 Needs Revision - Try re-explaining the topic in Module 1.</span>', unsafe_allow_html=True)
        else:
            # Empty State
            st.markdown("""
            <div style="background: rgba(18, 24, 38, 0.4); border: 1px dashed rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 42px 20px; text-align: center; color: #64748b; margin-top: 16px;">
                <div style="font-size: 2.2rem; margin-bottom: 8px;">🎯</div>
                <div style="font-size: 1rem; font-weight: 600; color: #94a3b8; margin-bottom: 4px;">Quiz Engine Ready</div>
                <div style="font-size: 0.84rem;">Enter your topic or upload a study document above and click <b>Generate Quiz</b> to synthesize real AI practice questions.</div>
            </div>
            """, unsafe_allow_html=True)

    with tab_flashcards:
        with st.container(border=True):
            col_f1, col_f2 = st.columns([3, 1], gap="medium")
            with col_f1:
                fc_topic = st.text_input(
                    "Flashcard Topic / Subject:",
                    placeholder="e.g., Key ML Metrics, Mitosis Phases, Python Dunder Methods",
                    key="fc_topic_input"
                )
            with col_f2:
                fc_count = st.selectbox("Deck Size:", [3, 5, 8, 12], index=1, key="fc_count_select")

            fc_file = st.file_uploader(
                "📎 Optional: Upload study document (.pdf, .txt) to extract flashcards directly from source:",
                type=["pdf", "txt"],
                key="fc_doc_uploader"
            )

            create_fc_btn = st.button("🗂️ Build Deck from Topic / Document", type="primary", use_container_width=True, key="fc_generate_btn")

        if create_fc_btn:
            if not api_key:
                st.error("🔑 Please enter a valid Gemini API Key in the sidebar or `.env` file.")
            elif not fc_topic.strip() and not fc_file:
                st.warning("Please enter a flashcard topic or upload a document.")
            else:
                fc_context = None
                if fc_file is not None:
                    if "pdf" in fc_file.type:
                        fc_context = extract_text_from_pdf(fc_file.getvalue())
                    else:
                        fc_context = fc_file.getvalue().decode("utf-8", errors="ignore")

                with st.spinner("Synthesizing high-yield flashcard deck with Gemini..."):
                    result = generate_flashcards(
                        api_key=api_key,
                        model_name=model_name,
                        topic=fc_topic,
                        count=fc_count,
                        text_context=fc_context
                    )

                    if result["success"]:
                        st.session_state.flashcards_data = result["data"]
                        st.success(f"Generated {len(result['data'])} active-recall flashcards for '{fc_topic or fc_file.name}'!")
                        st.rerun()
                    else:
                        st.error(result["error"])

        if st.session_state.get("flashcards_data"):
            st.markdown("---")
            st.markdown("#### 💡 Flip & Review Flashcards:")
            for idx, card in enumerate(st.session_state.flashcards_data):
                with st.expander(f"📌 Card #{idx+1}: {card.get('front')}", expanded=False):
                    st.markdown(f"""
                    <div class="flashcard-box">
                        <div class="flashcard-front">❓ Question / Concept</div>
                        <div style="font-size: 1.05rem; font-weight: 600; color: #f8fafc; margin-bottom: 8px;">{card.get('front')}</div>
                        <div class="flashcard-back"><b>💡 Answer / Key Definition:</b><br>{card.get('back')}</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            # Empty State
            st.markdown("""
            <div style="background: rgba(18, 24, 38, 0.4); border: 1px dashed rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 42px 20px; text-align: center; color: #64748b; margin-top: 16px;">
                <div style="font-size: 2.2rem; margin-bottom: 8px;">🗂️</div>
                <div style="font-size: 1rem; font-weight: 600; color: #94a3b8; margin-bottom: 4px;">Flashcard Deck Ready</div>
                <div style="font-size: 0.84rem;">Enter a subject or upload notes above and click <b>Build Deck</b> to generate interactive active-recall flashcards.</div>
            </div>
            """, unsafe_allow_html=True)
