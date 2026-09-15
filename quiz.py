import streamlit as st


def display_quiz(quiz):

    if not quiz:

        st.warning(
            "Chưa có câu hỏi Quiz."
        )

        return

    # =====================================================
    # HEADER
    # =====================================================

    st.markdown("## ❓ Quiz")

    st.caption(
        "Kiểm tra mức độ hiểu bài của bạn."
    )

    # =====================================================
    # QUIZ STATE
    # =====================================================

    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False

    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0

    if "quiz_total" not in st.session_state:
        st.session_state.quiz_total = len(quiz)

    if "quiz_percentage" not in st.session_state:
        st.session_state.quiz_percentage = 0

    # =====================================================
    # FORM
    # =====================================================

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

            # Khung câu hỏi
            with st.container(border=True):

                st.markdown(
                    f"### 🟣 Câu {i + 1}"
                )

                st.markdown(
                    f"**{question_text}**"
                )

                st.write("")

                selected = st.radio(
                    "Chọn đáp án:",
                    options,
                    key=f"snap_quiz_{i}",
                    index=None
                )

                answers.append(selected)

            st.write("")

        submitted = st.form_submit_button(
            "📝 Nộp bài",
            use_container_width=True,
            type="primary"
        )

    # =====================================================
    # CALCULATE RESULT
    # =====================================================

    if submitted:

        score = 0
        wrong_questions = []

        for i, question in enumerate(quiz):

            selected = answers[i]

            correct = str(
                question.get(
                    "answer",
                    ""
                )
            ).strip().upper()

            correct_text = str(
                question.get(
                    "correct_answer",
                    correct
                )
            )

            if selected:

                selected_letter = (
                    str(selected).strip()[0].upper()
                )

                if selected_letter == correct:

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

        percentage = int(
            score / total * 100
        ) if total else 0

        # Lưu kết quả
        st.session_state.quiz_submitted = True
        st.session_state.quiz_score = score
        st.session_state.quiz_total = total
        st.session_state.quiz_percentage = percentage
        st.session_state.review_cards = wrong_questions

        st.session_state.quiz_answers = answers

    # =====================================================
    # SHOW RESULT
    # =====================================================

    if st.session_state.quiz_submitted:

        score = st.session_state.quiz_score
        total = st.session_state.quiz_total
        percentage = st.session_state.quiz_percentage

        st.write("")

        # Điểm
        with st.container(border=True):

            st.markdown(
                "### 🎯 Kết quả của bạn"
            )

            st.markdown(
                f"# {score} / {total}"
            )

            st.progress(
                percentage / 100,
                text=f"📊 Độ chính xác: {percentage}%"
            )

        # =================================================
        # MESSAGE
        # =================================================

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

        # =================================================
        # REVIEW
        # =================================================

        wrong_questions = (
            st.session_state.review_cards
        )

        if wrong_questions:

            st.write("")

            with st.container(border=True):

                st.markdown(
                    "### 🔁 Gợi ý ôn lại"
                )

                st.write(
                    f"Bạn có **{len(wrong_questions)} "
                    f"câu cần ôn lại**."
                )

                st.info(
                    "🃏 Những câu chưa đúng sẽ được "
                    "chuyển thành Flashcard ở phần "
                    "**Ôn lại phần chưa chắc**."
                )

        else:

            st.success(
                "🏆 Tuyệt vời! Bạn không có câu sai."
            )

        # =================================================
        # DETAILED RESULT
        # =================================================

        st.write("")

        st.markdown(
            "### 📋 Kết quả chi tiết"
        )

        saved_answers = st.session_state.get(
            "quiz_answers",
            []
        )

        for i, question in enumerate(quiz):

            selected = (
                saved_answers[i]
                if i < len(saved_answers)
                else None
            )

            correct = str(
                question.get(
                    "answer",
                    ""
                )
            ).strip().upper()

            correct_text = str(
                question.get(
                    "correct_answer",
                    correct
                )
            )

            if selected:

                selected_letter = (
                    str(selected).strip()[0].upper()
                )

                if selected_letter == correct:

                    st.success(
                        f"**Câu {i + 1}:** ✅ Chính xác"
                    )

                else:

                    st.error(
                        f"**Câu {i + 1}:** ❌ Sai\n\n"
                        f"Đáp án đúng: **{correct_text}**"
                    )

            else:

                st.warning(
                    f"**Câu {i + 1}:** ⚪ Chưa trả lời\n\n"
                    f"Đáp án đúng: **{correct_text}**"
                )
