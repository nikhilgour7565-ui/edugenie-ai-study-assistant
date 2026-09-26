"""
View controller for Module 2: Smart Quiz & Flashcard Deck Generator.
Implements pre-loaded practice questions, top control ribbon, numbered MCQ cards,
grading score card, and interactive active recall flashcard flip-deck.
"""

import streamlit as st
from backend.services import generate_quiz, generate_flashcards

DEFAULT_PRACTICE_QUIZ = [
    {
        "id": 1,
        "question": "Which component in an Artificial Neural Network introduces non-linearity to the model?",
        "options": ["Activation Function", "Loss Function", "Learning Rate", "Weight Matrix"],
        "correct_answer": "Activation Function",
        "explanation": "Activation functions (like ReLU, Sigmoid) introduce non-linear properties to neural networks, allowing them to learn complex patterns beyond simple linear combinations."
    },
    {
        "id": 2,
        "question": "In Object-Oriented Programming, what principle refers to bundling data and the methods that operate on that data into a single unit?",
        "options": ["Inheritance", "Encapsulation", "Polymorphism", "Abstraction"],
        "correct_answer": "Encapsulation",
        "explanation": "Encapsulation is the bundling of data and the methods that act on that data, restricting direct access to some of an object's components to prevent unintended modifications."
    },
    {
        "id": 3,
        "question": "What is the primary product formed during the light-dependent reactions of photosynthesis that powers the Calvin Cycle?",
        "options": ["Glucose and Water", "ATP and NADPH", "Carbon Dioxide and Oxygen", "Pyruvate and Acetyl-CoA"],
        "correct_answer": "ATP and NADPH",
        "explanation": "Light reactions produce ATP and NADPH (chemical energy carriers), which are subsequently used in the light-independent Calvin Cycle to fix CO2 into sugar."
    }
]

DEFAULT_FLASHCARDS = [
    {
        "front": "Overfitting vs. Underfitting",
        "back": "Overfitting occurs when a model learns noise in training data and performs poorly on unseen data. Underfitting occurs when a model is too simple to capture underlying patterns."
    },
    {
        "front": "Big O: Time Complexity of Binary Search",
        "back": "O(log n) — because the search space is halved at each comparison step in a sorted array."
    },
    {
        "front": "Mitochondria Function",
        "back": "The 'powerhouse of the cell' responsible for generating most of the cell's supply of adenosine triphosphate (ATP) through cellular respiration."
    }
]


def render_quiz_view(api_key: str, model_name: str):
    """Renders the quiz and flashcard generator module."""
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h2 style="margin: 0; display: flex; align-items: center; gap: 10px;">
            <span>❓</span> Smart Quiz & Flashcard Suite
        </h2>
        <div style="color: #94a3b8; font-size: 0.95rem; margin-top: 4px;">
            Practice immediately with pre-loaded questions or generate custom AI quizzes on any topic without uploading files.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Initialize default practice questions if session is empty
    if "quiz_data" not in st.session_state or st.session_state.quiz_data is None:
        st.session_state.quiz_data = DEFAULT_PRACTICE_QUIZ
        st.session_state.user_quiz_answers = {}
        st.session_state.quiz_submitted = False

    if "flashcards_data" not in st.session_state or st.session_state.flashcards_data is None:
        st.session_state.flashcards_data = DEFAULT_FLASHCARDS

    # Quick Practice Preset Chips
    st.markdown("""
    <div style="margin-bottom: 12px; display: flex; align-items: center; gap: 6px; flex-wrap: wrap;">
        <span style="font-size: 0.8rem; color: #94a3b8;">Generate on Quick Topics:</span>
    </div>
    """, unsafe_allow_html=True)

    col_c1, col_c2, col_c3, col_c4 = st.columns(4)
    quick_topics = ["Python & OOP", "Cell Biology & DNA", "Data Structures & Algos", "World History"]
    for idx, (c, topic_name) in enumerate(zip([col_c1, col_c2, col_c3, col_c4], quick_topics)):
        with c:
            if st.button(f"🎯 {topic_name}", key=f"quiz_quick_{idx}", use_container_width=True):
                if api_key:
                    with st.spinner(f"Generating quiz on '{topic_name}'..."):
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
            col_q1, col_q2, col_q3, col_q4 = st.columns([2.5, 1, 1, 1.2], gap="medium")
            with col_q1:
                quiz_topic = st.text_input(
                    "Topic / Subject Name:",
                    placeholder="e.g., Cellular Respiration, Operating Systems, Machine Learning",
                    key="quiz_topic_input"
                )
            with col_q2:
                num_questions = st.selectbox("Questions:", [3, 5, 10], index=0, key="quiz_num_select")
            with col_q3:
                difficulty = st.selectbox("Difficulty:", ["Easy", "Medium", "Hard"], index=1, key="quiz_diff_select")
            with col_q4:
                st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
                create_quiz_btn = st.button("🚀 Generate Quiz", type="primary", use_container_width=True, key="quiz_generate_btn")

        if create_quiz_btn:
            if not api_key:
                st.error("🔑 Please enter a valid Gemini API Key in the sidebar or `.env` file.")
            elif not quiz_topic.strip():
                st.warning("Please enter a subject or topic name.")
            else:
                with st.spinner("Synthesizing dynamic quiz questions with Gemini..."):
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

                percentage = score / total
                st.progress(percentage)
                st.metric(label="🏆 Final Score", value=f"{score}/{total} ({percentage*100:.1f}%)")

                if percentage >= 0.8:
                    st.balloons()
                    st.markdown('<span class="badge-tag badge-green" style="font-size: 0.9rem;">🌟 Mastery Achieved - Outstanding Work!</span>', unsafe_allow_html=True)
                elif percentage >= 0.5:
                    st.markdown('<span class="badge-tag badge-amber" style="font-size: 0.9rem;">👍 Solid Effort - Review explanations to close gaps.</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="badge-tag badge-purple" style="font-size: 0.9rem;">📚 Needs Revision - Try re-explaining the topic in Module 1.</span>', unsafe_allow_html=True)

    with tab_flashcards:
        with st.container(border=True):
            col_f1, col_f2, col_f3 = st.columns([3, 1, 1.2], gap="medium")
            with col_f1:
                fc_topic = st.text_input(
                    "Flashcard Topic / Subject:",
                    placeholder="e.g., Key ML Metrics, Mitosis Phases, Python Dunder Methods",
                    key="fc_topic_input"
                )
            with col_f2:
                fc_count = st.selectbox("Deck Size:", [3, 5, 8], index=0, key="fc_count_select")
            with col_f3:
                st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
                create_fc_btn = st.button("🗂️ Build Deck", type="primary", use_container_width=True, key="fc_generate_btn")

        if create_fc_btn:
            if not api_key:
                st.error("🔑 Please enter a valid Gemini API Key.")
            elif not fc_topic.strip():
                st.warning("Please enter a flashcard topic.")
            else:
                with st.spinner("Synthesizing high-yield flashcard deck..."):
                    result = generate_flashcards(
                        api_key=api_key,
                        model_name=model_name,
                        topic=fc_topic,
                        count=fc_count
                    )

                    if result["success"]:
                        st.session_state.flashcards_data = result["data"]
                        st.success(f"Generated {len(result['data'])} active-recall flashcards!")
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
