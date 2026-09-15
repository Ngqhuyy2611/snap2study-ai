import streamlit as st


def display_quiz(quiz):

    if not quiz:

        st.warning(
            "Chưa có câu hỏi Quiz."
        )

        return


    st.header("❓ Quiz")

    st.write(
        f"Kiểm tra kiến thức với "
        f"{len(quiz)} câu hỏi."
    )

    st.write("")


    # =====================================================
    # QUIZ FORM
    # =====================================================

    with st.form("quiz_form"):

        answers = []


        for i, question in enumerate(quiz):

            st.markdown(
                f"### Câu {i + 1}"
            )

            st.write(
                question.get(
                    "question",
                    "Không có câu hỏi."
                )
            )


            selected = st.radio(
                "Chọn đáp án:",
                question.get(
                    "options",
                    []
                ),
                key=f"quiz_{i}",
                index=None
            )


            answers.append(selected)

            st.divider()


        submitted = st.form_submit_button(
            "📝 Nộp bài",
            use_container_width=True
        )


    # =====================================================
    # RESULT
    # =====================================================

    if submitted:

        score = 0

        wrong_questions = []


        for i, question in enumerate(quiz):

            selected = answers[i]

            correct = question.get(
                "answer",
                ""
            )


            if selected:

                selected_letter = selected[0]


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


        percentage = int(
            score / len(quiz) * 100
        )


        # =================================================
        # SAVE RESULT
        # =================================================

        st.session_state.quiz_score = score

        st.session_state.quiz_total = len(quiz)

        st.session_state.quiz_percentage = percentage

        st.session_state.review_cards = (
            wrong_questions
        )


        st.divider()


        # =================================================
        # SCORE MESSAGE
        # =================================================

        if percentage >= 80:

            st.success(
                f"🎉 Xuất sắc! Bạn đạt "
                f"{score}/{len(quiz)} câu."
            )


        elif percentage >= 50:

            st.warning(
                f"👍 Khá tốt! Bạn đạt "
                f"{score}/{len(quiz)} câu."
            )


        else:

            st.error(
                f"📖 Bạn đạt "
                f"{score}/{len(quiz)} câu. "
                f"Hãy ôn lại kiến thức nhé!"
            )


        st.progress(
            percentage / 100,
            text=f"Điểm số: {percentage}%"
        )


        # =================================================
        # REVIEW MESSAGE
        # =================================================

        if wrong_questions:

            st.divider()

            st.subheader(
                "💡 Gợi ý ôn lại"
            )

            st.write(
                f"Bạn có **{len(wrong_questions)} "
                f"câu cần ôn lại**."
            )

            st.info(
                "Snap2Study đã chuyển những câu "
                "bạn làm chưa đúng thành Flashcard "
                "để bạn ôn lại."
            )


        else:

            st.success(
                "🏆 Tuyệt vời! "
                "Bạn không có câu sai."
            )


        # =================================================
        # DETAILED RESULT
        # =================================================

        st.subheader(
            "📋 Kết quả chi tiết"
        )


        for i, question in enumerate(quiz):

            selected = answers[i]

            correct = question.get(
                "answer",
                ""
            )


            if selected:

                selected_letter = selected[0]


                if selected_letter == correct:

                    st.success(
                        f"Câu {i + 1}: "
                        f"✅ Chính xác"
                    )


                else:

                    correct_text = question.get(
                        "correct_answer",
                        correct
                    )

                    st.error(
                        f"Câu {i + 1}: ❌ "
                        f"Đáp án đúng: "
                        f"{correct_text}"
                    )


            else:

                correct_text = question.get(
                    "correct_answer",
                    correct
                )

                st.warning(
                    f"Câu {i + 1}: ⚪ Chưa trả lời "
                    f"— Đáp án đúng: "
                    f"{correct_text}"
                )
