import streamlit as st
import html


def display_quiz(quiz):

    if not quiz:

        st.warning(
            "Chưa có câu hỏi Quiz."
        )

        return

    # =====================================================
    # CUSTOM STYLE
    # =====================================================

    st.markdown(
        """
        <style>

        /* =====================================
           QUIZ HEADER
        ====================================== */

        .quiz-title {
            text-align: center;

            font-size: 28px;
            font-weight: 800;

            color: #101828;

            margin-top: 25px;
            margin-bottom: 5px;
        }

        .quiz-subtitle {
            text-align: center;

            color: #667085;

            font-size: 14px;

            margin-bottom: 25px;
        }

        /* =====================================
           QUESTION CARD
        ====================================== */

        .quiz-card {
            background:
                linear-gradient(
                    135deg,
                    #F8F7FF 0%,
                    #F2F6FF 100%
                );

            border: 1px solid rgba(99, 91, 255, 0.15);

            border-radius: 20px;

            padding: 24px 25px;

            margin-top: 18px;
            margin-bottom: 12px;

            box-shadow:
                0 8px 25px rgba(31, 41, 55, 0.07);
        }

        .quiz-number {
            display: inline-block;

            background: #E9E7FF;

            color: #5146D8;

            padding: 6px 13px;

            border-radius: 999px;

            font-size: 12px;

            font-weight: 800;

            margin-bottom: 13px;
        }

        .quiz-question {
            color: #101828;

            font-size: 18px;

            line-height: 1.55;

            font-weight: 700;
        }

        /* =====================================
           RESULT CARD
        ====================================== */

        .quiz-result {

            border-radius: 24px;

            padding: 32px;

            text-align: center;

            margin-top: 25px;
            margin-bottom: 25px;

            background:
                linear-gradient(
                    135deg,
                    #F5F3FF 0%,
                    #EEF4FF 100%
                );

            border: 1px solid rgba(99, 91, 255, 0.15);

            box-shadow:
                0 12px 35px rgba(31, 41, 55, 0.08);
        }

        .quiz-result-label {
            color: #667085;

            font-size: 14px;

            font-weight: 700;

            margin-bottom: 5px;
        }

        .quiz-score {
            color: #5146D8;

            font-size: 52px;

            font-weight: 900;

            line-height: 1.1;

            margin: 5px 0;
        }

        .quiz-percentage {
            color: #344054;

            font-size: 17px;

            font-weight: 700;
        }

        /* =====================================
           RESULT MESSAGE
        ====================================== */

        .quiz-message {

            text-align: center;

            font-size: 16px;

            font-weight: 700;

            margin: 10px 0 20px 0;

            color: #344054;
        }

        /* =====================================
           DETAIL
        ====================================== */

        .detail-title {

            font-size: 20px;

            font-weight: 800;

            color: #101828;

            margin-top: 25px;
            margin-bottom: 15px;
        }

        .result-item {

            border-radius: 14px;

            padding: 13px 16px;

            margin: 8px 0;

            font-size: 14px;

            font-weight: 600;
        }

        .result-correct {

            background: #ECFDF3;

            border: 1px solid #ABEFC6;

            color: #067647;
        }

        .result-wrong {

            background: #FEF3F2;

            border: 1px solid #FECDCA;

            color: #B42318;
        }

        .result-empty {

            background: #FFFAEB;

            border: 1px solid #FEDF89;

            color: #B54708;
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

    # =====================================================
    # QUIZ FORM
    # =====================================================

    with st.form("quiz_form"):

        answers = []

        for i, question in enumerate(quiz):

            question_text = html.escape(
                str(
                    question.get(
                        "question",
                        "Không có câu hỏi."
                    )
                )
            )

            # ---------------------------------------------
            # QUESTION CARD
            # ---------------------------------------------

            st.markdown(
                f"""
                <div class="quiz-card">

                    <div class="quiz-number">
                        ❓ CÂU {i + 1}
                    </div>

                    <div class="quiz-question">
                        {question_text}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            # ---------------------------------------------
            # OPTIONS
            # ---------------------------------------------

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
        # CALCULATE SCORE
        # =================================================

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

        st.session_state.review_cards = wrong_questions

        # =================================================
        # RESULT CARD
        # =================================================

        st.markdown(
            f"""
            <div class="quiz-result">

                <div class="quiz-result-label">
                    🎯 KẾT QUẢ CỦA BẠN
                </div>

                <div class="quiz-score">
                    {score} / {len(quiz)}
                </div>

                <div class="quiz-percentage">
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

            message = "🎉 Xuất sắc! Bạn đã nắm khá tốt kiến thức."

        elif percentage >= 50:

            message = "👍 Khá tốt! Hãy ôn thêm những phần còn chưa chắc."

        else:

            message = "📖 Đừng lo! Hãy xem lại bài và thử lại nhé."

        st.markdown(
            f"""
            <div class="quiz-message">
                {message}
            </div>
            """,
            unsafe_allow_html=True
        )

        # =================================================
        # PROGRESS
        # =================================================

        st.progress(
            percentage / 100,
            text=f"📊 Mức độ chính xác: {percentage}%"
        )

        # =================================================
        # REVIEW MESSAGE
        # =================================================

        if wrong_questions:

            st.markdown(
                """
                <div class="detail-title">
                    💡 Gợi ý ôn lại
                </div>
                """,
                unsafe_allow_html=True
            )

            st.info(
                f"Bạn có **{len(wrong_questions)} câu cần ôn lại**."
            )

            st.success(
                "🃏 Snap2Study đã chuyển những câu "
                "bạn làm chưa đúng thành Flashcard "
                "để bạn ôn lại."
            )

        else:

            st.success(
                "🏆 Tuyệt vời! Bạn không có câu sai."
            )

        # =================================================
        # DETAILED RESULT
        # =================================================

        st.markdown(
            """
            <div class="detail-title">
                📋 Kết quả chi tiết
            </div>
            """,
            unsafe_allow_html=True
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

                    st.markdown(
                        f"""
                        <div class="result-item result-correct">
                            Câu {i + 1} &nbsp;·&nbsp;
                            ✅ Chính xác
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                else:

                    correct_text = html.escape(
                        str(
                            question.get(
                                "correct_answer",
                                correct
                            )
                        )
                    )

                    st.markdown(
                        f"""
                        <div class="result-item result-wrong">
                            Câu {i + 1} &nbsp;·&nbsp;
                            ❌ Sai<br>
                            <small>
                                Đáp án đúng: {correct_text}
                            </small>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            else:

                correct_text = html.escape(
                    str(
                        question.get(
                            "correct_answer",
                            correct
                        )
                    )
                )

                st.markdown(
                    f"""
                    <div class="result-item result-empty">
                        Câu {i + 1} &nbsp;·&nbsp;
                        ⚪ Chưa trả lời<br>
                        <small>
                            Đáp án đúng: {correct_text}
                        </small>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
