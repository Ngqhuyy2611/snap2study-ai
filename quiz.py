import streamlit as st


def display_quiz(quiz):

    if not quiz:
        st.warning("Chưa có câu hỏi Quiz.")
        return

    # =====================================================
    # CSS
    # =====================================================

    st.markdown(
        """
<style>

.quiz-title {
    text-align: center;

    color: #101828;

    font-size: 28px;
    font-weight: 800;

    margin-top: 25px;
    margin-bottom: 5px;
}

.quiz-subtitle {
    text-align: center;

    color: #667085;

    font-size: 14px;

    margin-bottom: 25px;
}

.quiz-question-card {
    background:
        linear-gradient(
            135deg,
            #F8F7FF 0%,
            #F2F6FF 100%
        );

    border: 1px solid #DDD9FF;

    border-radius: 20px;

    padding: 22px 24px;

    margin: 18px 0 10px 0;

    box-shadow:
        0 8px 25px rgba(16, 24, 40, 0.07);
}

.quiz-number {
    display: inline-block;

    padding: 6px 13px;

    border-radius: 999px;

    background: #E9E7FF;

    color: #5146D8;

    font-size: 12px;
    font-weight: 800;

    margin-bottom: 12px;
}

.quiz-question-text {
    color: #101828;

    font-size: 18px;
    font-weight: 700;

    line-height: 1.55;
}

.quiz-result-card {
    background:
        linear-gradient(
            135deg,
            #F5F3FF,
            #EEF4FF
        );

    border: 1px solid #DDD9FF;

    border-radius: 24px;

    padding: 30px;

    text-align: center;

    margin: 25px 0;

    box-shadow:
        0 12px 35px rgba(16, 24, 40, 0.08);
}

.quiz-result-label {
    color: #667085;

    font-size: 14px;
    font-weight: 700;
}

.quiz-score {
    color: #5146D8;

    font-size: 50px;
    font-weight: 900;

    margin: 5px 0;
}

.quiz-percent {
    color: #344054;

    font-size: 17px;
    font-weight: 700;
}

.quiz-detail-title {
    color: #101828;

    font-size: 20px;
    font-weight: 800;

    margin-top: 25px;
    margin-bottom: 15px;
}

</style>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # HEADER
    # =====================================================

    st.markdown(
        """
<div class="quiz-title">
    ❓ Quiz
</div>

<div class="quiz-subtitle">
    Kiểm tra mức độ hiểu bài của bạn
</div>
        """,
        unsafe_allow_html=True
    )

    st.progress(
        0,
        text=f"📝 {len(quiz)} câu hỏi"
    )

    # =====================================================
    # FORM
    # =====================================================

    with st.form("quiz_form"):

        answers = []

        for i, question in enumerate(quiz):

            question_text = str(
                question.get(
                    "question",
                    "Không có câu hỏi."
                )
            )

            st.markdown(
                f"""
<div class="quiz-question-card">

<div class="quiz-number">
❓ CÂU {i + 1}
</div>

<div class="quiz-question-text">
{question_text}
</div>

</div>
                """,
                unsafe_allow_html=True
            )

            options = question.get(
                "options",
                []
            )

            selected = st.radio(
                "Chọn đáp án:",
                options,
                key=f"quiz_{i}",
                index=None
            )

            answers.append(selected)

        st.write("")

        submitted = st.form_submit_button(
            "📝  Nộp bài",
            use_container_width=True,
            type="primary"
        )

    # =====================================================
    # RESULT
    # =====================================================

    if submitted:

        score = 0

        wrong_questions = []

        # =================================================
        # CHECK ANSWERS
        # =================================================

        for i, question in enumerate(quiz):

            selected = answers[i]

            correct = str(
                question.get(
                    "answer",
                    ""
                )
            ).strip().upper()

            if selected:

                selected_letter = (
                    str(selected)[0]
                    .upper()
                )

                if selected_letter == correct:

                    score += 1

                else:

                    wrong_questions.append({

                        "question": question.get(
                            "question",
                            ""
                        ),

                        "answer": question.get(
                            "correct_answer",
                            correct
                        ),

                        "difficulty": "Cần ôn lại"

                    })

            else:

                wrong_questions.append({

                    "question": question.get(
                        "question",
                        ""
                    ),

                    "answer": question.get(
                        "correct_answer",
                        correct
                    ),

                    "difficulty": "Cần ôn lại"

                })

        total = len(quiz)

        percentage = int(
            score / total * 100
        )

        # =================================================
        # SAVE RESULT
        # =================================================

        st.session_state.quiz_score = score

        st.session_state.quiz_total = total

        st.session_state.quiz_percentage = percentage

        st.session_state.review_cards = wrong_questions

        # =================================================
        # RESULT CARD
        # =================================================

        st.markdown(
            f"""
<div class="quiz-result-card">

<div class="quiz-result-label">
🎯 KẾT QUẢ CỦA BẠN
</div>

<div class="quiz-score">
{score} / {total}
</div>

<div class="quiz-percent">
{percentage}% chính xác
</div>

</div>
            """,
            unsafe_allow_html=True
        )

        # =================================================
        # MESSAGE
        # =================================================

        if percentage >= 80:

            st.success(
                "🎉 Xuất sắc! Bạn đã nắm khá tốt kiến thức."
            )

        elif percentage >= 50:

            st.warning(
                "👍 Khá tốt! Hãy ôn thêm những phần còn chưa chắc."
            )

        else:

            st.error(
                "📖 Đừng lo! Hãy xem lại bài và thử lại nhé."
            )

        st.progress(
            percentage / 100,
            text=f"📊 Độ chính xác: {percentage}%"
        )

        # =================================================
        # REVIEW
        # =================================================

        if wrong_questions:

            st.markdown(
                """
<div class="quiz-detail-title">
💡 Gợi ý ôn lại
</div>
                """,
                unsafe_allow_html=True
            )

            st.info(
                f"Bạn có **{len(wrong_questions)} câu cần ôn lại**."
            )

            st.success(
                "🃏 Những câu chưa đúng đã được chuyển "
                "thành Flashcard để bạn ôn lại bên dưới."
            )

        else:

            st.success(
                "🏆 Tuyệt vời! Bạn không có câu sai."
            )

        # =================================================
        # DETAIL
        # =================================================

        st.markdown(
            """
<div class="quiz-detail-title">
📋 Kết quả chi tiết
</div>
            """,
            unsafe_allow_html=True
        )

        for i, question in enumerate(quiz):

            selected = answers[i]

            correct = str(
                question.get(
                    "answer",
                    ""
                )
            ).strip().upper()

            if selected:

                selected_letter = (
                    str(selected)[0]
                    .upper()
                )

                if selected_letter == correct:

                    st.success(
                        f"Câu {i + 1}: ✅ Chính xác"
                    )

                else:

                    correct_text = question.get(
                        "correct_answer",
                        correct
                    )

                    st.error(
                        f"Câu {i + 1}: ❌ Sai — "
                        f"Đáp án đúng: {correct_text}"
                    )

            else:

                correct_text = question.get(
                    "correct_answer",
                    correct
                )

                st.warning(
                    f"Câu {i + 1}: ⚪ Chưa trả lời — "
                    f"Đáp án đúng: {correct_text}"
                )
