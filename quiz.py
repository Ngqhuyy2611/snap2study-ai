import streamlit as st


def display_quiz(quiz):

    if not quiz:
        st.warning("Chưa có câu hỏi Quiz.")
        return

    # =========================================================
    # CSS
    # =========================================================

    st.markdown(
        """
<style>

/* =========================================================
   QUIZ
   ========================================================= */

.snap-quiz-title {
    text-align: center;

    color: #101828;

    font-size: 29px;
    font-weight: 800;

    margin-top: 30px;
    margin-bottom: 5px;
}

.snap-quiz-subtitle {
    text-align: center;

    color: #667085;

    font-size: 14px;

    margin-bottom: 24px;
}


/* =========================================================
   QUESTION CARD
   ========================================================= */

.snap-quiz-card {
    background:
        radial-gradient(
            circle at top right,
            rgba(129, 140, 248, 0.14),
            transparent 32%
        ),
        linear-gradient(
            135deg,
            #ffffff 0%,
            #f8f7ff 100%
        );

    border: 1px solid #dfdcff;

    border-radius: 22px;

    padding: 27px 30px;

    margin: 18px 0 10px 0;

    box-shadow:
        0 12px 30px rgba(67, 56, 202, 0.09),
        0 4px 12px rgba(16, 24, 40, 0.05);
}


/* =========================================================
   QUESTION NUMBER
   ========================================================= */

.snap-quiz-number {
    display: inline-block;

    padding: 6px 12px;

    border-radius: 999px;

    background: #eeecff;

    color: #5146d8;

    font-size: 12px;

    font-weight: 800;

    letter-spacing: 0.6px;

    margin-bottom: 13px;
}


/* =========================================================
   QUESTION TEXT
   ========================================================= */

.snap-quiz-question {
    color: #101828;

    font-size: 17px;

    line-height: 1.6;

    font-weight: 700;
}


/* =========================================================
   RESULT CARD
   ========================================================= */

.snap-result-card {
    background:
        linear-gradient(
            135deg,
            #f8f7ff 0%,
            #eef4ff 100%
        );

    border: 1px solid #d8d4ff;

    border-radius: 25px;

    padding: 30px;

    margin: 25px 0;

    text-align: center;

    box-shadow:
        0 16px 38px rgba(67, 56, 202, 0.11);
}


/* =========================================================
   SCORE
   ========================================================= */

.snap-score {
    color: #5146d8;

    font-size: 46px;

    font-weight: 850;

    line-height: 1;

    margin: 12px 0;
}


/* =========================================================
   SCORE LABEL
   ========================================================= */

.snap-score-label {
    color: #667085;

    font-size: 14px;

    font-weight: 600;
}


/* =========================================================
   DETAIL
   ========================================================= */

.snap-quiz-detail {
    border-radius: 17px;

    padding: 18px 20px;

    margin: 12px 0;

    font-size: 14px;

    line-height: 1.55;
}


/* =========================================================
   MOBILE
   ========================================================= */

@media (max-width: 768px) {

    .snap-quiz-card {
        padding: 22px 18px;
        border-radius: 18px;
    }

    .snap-quiz-question {
        font-size: 16px;
    }

    .snap-score {
        font-size: 40px;
    }
}

</style>
        """,
        unsafe_allow_html=True
    )

    # =========================================================
    # TITLE
    # =========================================================

    st.markdown(
        '<div class="snap-quiz-title">❓ Quiz</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="snap-quiz-subtitle">'
        'Kiểm tra mức độ hiểu bài của bạn'
        '</div>',
        unsafe_allow_html=True
    )

    # =========================================================
    # SESSION STATE
    # =========================================================

    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False

    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0

    if "quiz_total" not in st.session_state:
        st.session_state.quiz_total = len(quiz)

    if "quiz_percentage" not in st.session_state:
        st.session_state.quiz_percentage = 0

    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = []

    # =========================================================
    # QUIZ FORM
    # =========================================================

    with st.form("snap2study_quiz_form"):

        answers = []

        for i, question in enumerate(quiz):

            question_text = str(
                question.get(
                    "question",
                    "Không có câu hỏi."
                )
            )

            options = question.get(
                "options",
                []
            )

            # -------------------------------------------------
            # FLOATING QUESTION CARD
            # -------------------------------------------------

            question_html = (
                '<div class="snap-quiz-card">'
                f'<div class="snap-quiz-number">'
                f'CÂU {i + 1}'
                '</div>'
                f'<div class="snap-quiz-question">'
                f'{question_text}'
                '</div>'
                '</div>'
            )

            st.markdown(
                question_html,
                unsafe_allow_html=True
            )

            selected = st.radio(
                "Chọn đáp án:",
                options,
                index=None,
                key=f"snap_quiz_answer_{i}",
                label_visibility="visible"
            )

            answers.append(selected)

        st.write("")

        submitted = st.form_submit_button(
            "📝  Nộp bài",
            use_container_width=True,
            type="primary"
        )

    # =========================================================
    # CALCULATE RESULT
    # =========================================================

    if submitted:

        score = 0

        wrong_questions = []

        for i, question in enumerate(quiz):

            selected = answers[i]

            correct_letter = str(
                question.get(
                    "answer",
                    ""
                )
            ).strip().upper()

            correct_text = str(
                question.get(
                    "correct_answer",
                    correct_letter
                )
            )

            if selected:

                selected_text = str(
                    selected
                ).strip()

                # Lấy chữ A/B/C/D ở đầu option
                selected_letter = (
                    selected_text[0].upper()
                    if selected_text
                    else ""
                )

                if selected_letter == correct_letter:

                    score += 1

                else:

                    wrong_questions.append({
                        "question": question.get(
                            "question",
                            ""
                        ),
                        "answer": correct_text,
                        "difficulty": "Cần ôn lại"
                    })

            else:

                wrong_questions.append({
                    "question": question.get(
                        "question",
                        ""
                    ),
                    "answer": correct_text,
                    "difficulty": "Cần ôn lại"
                })

        total = len(quiz)

        percentage = (
            int(score / total * 100)
            if total
            else 0
        )

        # Save
        st.session_state.quiz_submitted = True
        st.session_state.quiz_score = score
        st.session_state.quiz_total = total
        st.session_state.quiz_percentage = percentage
        st.session_state.quiz_answers = answers

        # Review cards
        st.session_state.review_cards = (
            wrong_questions
        )

    # =========================================================
    # RESULT
    # =========================================================

    if st.session_state.quiz_submitted:

        score = st.session_state.quiz_score
        total = st.session_state.quiz_total
        percentage = st.session_state.quiz_percentage

        # -----------------------------------------------------
        # SCORE CARD
        # -----------------------------------------------------

        result_html = (
            '<div class="snap-result-card">'
            '<div class="snap-score-label">'
            '🎯 KẾT QUẢ CỦA BẠN'
            '</div>'
            f'<div class="snap-score">'
            f'{score} / {total}'
            '</div>'
            f'<div class="snap-score-label">'
            f'Độ chính xác: {percentage}%'
            '</div>'
            '</div>'
        )

        st.markdown(
            result_html,
            unsafe_allow_html=True
        )

        st.progress(
            percentage / 100,
            text=f"📊 {percentage}% chính xác"
        )

        # -----------------------------------------------------
        # FEEDBACK
        # -----------------------------------------------------

        if percentage >= 80:

            st.success(
                "🎉 Xuất sắc! Bạn đã nắm khá tốt kiến thức."
            )

        elif percentage >= 50:

            st.info(
                "👍 Khá tốt! Hãy ôn thêm những phần còn chưa chắc."
            )

        else:

            st.warning(
                "📖 Đừng lo! Hãy xem lại bài và thử lại nhé."
            )

        # -----------------------------------------------------
        # REVIEW SUGGESTION
        # -----------------------------------------------------

        wrong_questions = (
            st.session_state.review_cards
        )

        if wrong_questions:

            with st.container(border=True):

                st.markdown(
                    "### 🔁 Ôn lại phần chưa chắc"
                )

                st.write(
                    f"Bạn có **{len(wrong_questions)} "
                    f"câu cần ôn lại**."
                )

                st.caption(
                    "Các câu này sẽ được chuyển thành "
                    "Flashcard ở phần bên dưới."
                )

        else:

            st.success(
                "🏆 Tuyệt vời! Bạn đã trả lời đúng tất cả."
            )

        # -----------------------------------------------------
        # DETAIL
        # -----------------------------------------------------

        st.markdown(
            "### 📋 Kết quả chi tiết"
        )

        saved_answers = (
            st.session_state.quiz_answers
        )

        for i, question in enumerate(quiz):

            selected = (
                saved_answers[i]
                if i < len(saved_answers)
                else None
            )

            correct_letter = str(
                question.get(
                    "answer",
                    ""
                )
            ).strip().upper()

            correct_text = str(
                question.get(
                    "correct_answer",
                    correct_letter
                )
            )

            if selected:

                selected_text = str(
                    selected
                ).strip()

                selected_letter = (
                    selected_text[0].upper()
                    if selected_text
                    else ""
                )

                if selected_letter == correct_letter:

                    st.success(
                        f"**Câu {i + 1}**  ·  ✅ Chính xác"
                    )

                else:

                    st.error(
                        f"**Câu {i + 1}**  ·  ❌ Chưa đúng  \n"
                        f"Đáp án đúng: **{correct_text}**"
                    )

            else:

                st.warning(
                    f"**Câu {i + 1}**  ·  ⚪ Chưa trả lời  \n"
                    f"Đáp án đúng: **{correct_text}**"
                )
