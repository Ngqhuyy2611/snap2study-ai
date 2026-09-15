import streamlit as st


def display_flashcards(
    flashcards,
    title="🃏 Flashcard"
):

    if not flashcards:
        st.warning("Chưa có Flashcard.")
        return

    # =====================================================
    # SESSION STATE
    # =====================================================

    if "flashcard_index" not in st.session_state:
        st.session_state.flashcard_index = 0

    if "flashcard_flipped" not in st.session_state:
        st.session_state.flashcard_flipped = False

    # Kiểm tra index
    if st.session_state.flashcard_index >= len(flashcards):

        st.session_state.flashcard_index = 0
        st.session_state.flashcard_flipped = False

    index = st.session_state.flashcard_index

    flipped = st.session_state.flashcard_flipped

    card = flashcards[index]

    question = str(
        card.get(
            "question",
            "Không có câu hỏi."
        )
    )

    answer = str(
        card.get(
            "answer",
            "Không có đáp án."
        )
    )

    difficulty = str(
        card.get(
            "difficulty",
            ""
        )
    )

    total = len(flashcards)

    # =====================================================
    # CSS
    # =====================================================

    st.markdown(
        """
        <style>

        /* ==============================
           FLASHCARD
        ============================== */

        .flashcard-box {
            border-radius: 24px;
            padding: 35px 30px;
            margin: 20px 0;

            min-height: 280px;

            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;

            text-align: center;

            box-shadow:
                0 10px 30px rgba(0, 0, 0, 0.08);
        }


        .flashcard-question-box {

            background:
                linear-gradient(
                    135deg,
                    #f5f3ff,
                    #eef4ff
                );

            border: 2px solid #ddd9ff;
        }


        .flashcard-answer-box {

            background:
                linear-gradient(
                    135deg,
                    #ecfdf3,
                    #eff8ff
                );

            border: 2px solid #c9f0dc;
        }


        .flashcard-label {

            font-size: 13px;

            font-weight: 800;

            letter-spacing: 1px;

            margin-bottom: 20px;

            padding: 7px 15px;

            border-radius: 999px;

            display: inline-block;
        }


        .question-label {

            color: #5146d8;

            background: #e9e7ff;
        }


        .answer-label {

            color: #087443;

            background: #dff7e9;
        }


        .flashcard-number {

            color: #667085;

            font-size: 13px;

            font-weight: 700;

            margin-bottom: 12px;
        }


        .flashcard-question-text {

            color: #101828;

            font-size: 25px;

            font-weight: 750;

            line-height: 1.5;

            margin: 10px 0;
        }


        .flashcard-answer-text {

            color: #101828;

            font-size: 21px;

            font-weight: 600;

            line-height: 1.6;

            margin: 10px 0;
        }


        .flashcard-hint {

            color: #667085;

            font-size: 14px;

            margin-top: 25px;
        }


        .difficulty {

            margin-top: 20px;

            padding: 7px 15px;

            border-radius: 999px;

            background: rgba(255,255,255,0.8);

            border: 1px solid #d0d5dd;

            color: #475467;

            font-size: 13px;

            font-weight: 700;
        }


        .flashcard-title {

            text-align: center;

            font-size: 28px;

            font-weight: 800;

            color: #101828;

            margin-top: 20px;

            margin-bottom: 5px;
        }


        .flashcard-subtitle {

            text-align: center;

            color: #667085;

            font-size: 14px;

            margin-bottom: 20px;
        }


        .memory-question {

            text-align: center;

            color: #344054;

            font-weight: 700;

            margin: 15px 0;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # TITLE
    # =====================================================

    st.markdown(
        f"""
        <div class="flashcard-title">
            {title}
        </div>

        <div class="flashcard-subtitle">
            Lật thẻ để kiểm tra khả năng ghi nhớ
        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # PROGRESS
    # =====================================================

    st.progress(
        (index + 1) / total,
        text=f"📚 Thẻ {index + 1} / {total}"
    )

    st.write("")

    # =====================================================
    # QUESTION
    # =====================================================

    if not flipped:

        st.markdown(
            f"""
            <div class="flashcard-box flashcard-question-box">

                <div class="flashcard-number">
                    FLASHCARD {index + 1:02d}
                </div>

                <div class="flashcard-label question-label">
                    ❓ CÂU HỎI
                </div>

                <div class="flashcard-question-text">
                    {question}
                </div>

                <div class="flashcard-hint">
                    💡 Hãy thử trả lời trước khi lật thẻ
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        if st.button(
            "🔄 Lật thẻ",
            use_container_width=True,
            type="primary"
        ):

            st.session_state.flashcard_flipped = True

            st.rerun()

    # =====================================================
    # ANSWER
    # =====================================================

    else:

        st.markdown(
            f"""
            <div class="flashcard-box flashcard-answer-box">

                <div class="flashcard-number">
                    FLASHCARD {index + 1:02d}
                </div>

                <div class="flashcard-label answer-label">
                    ✅ ĐÁP ÁN
                </div>

                <div class="flashcard-answer-text">
                    {answer}
                </div>

                <div class="difficulty">
                    📊 Độ khó: {difficulty}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        # =================================================
        # MEMORY
        # =================================================

        st.markdown(
            """
            <div class="memory-question">
                🧠 Bạn nhớ thẻ này đến mức nào?
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            if st.button(
                "😕 Chưa nhớ",
                use_container_width=True
            ):

                st.session_state.flashcard_flipped = False

                st.toast(
                    "💡 Hãy ôn lại thẻ này!"
                )

                st.rerun()

        with col2:

            if st.button(
                "🤔 Hơi nhớ",
                use_container_width=True
            ):

                st.session_state.flashcard_flipped = False

                st.toast(
                    "📖 Có thể ôn lại lần nữa!"
                )

                st.rerun()

        with col3:

            if st.button(
                "😊 Đã nhớ",
                use_container_width=True
            ):

                st.session_state.flashcard_flipped = False

                st.toast(
                    "🎉 Tuyệt vời!"
                )

                st.rerun()

        st.write("")

        # =================================================
        # NAVIGATION
        # =================================================

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "← Thẻ trước",
                use_container_width=True,
                disabled=(index == 0)
            ):

                st.session_state.flashcard_index -= 1

                st.session_state.flashcard_flipped = False

                st.rerun()

        with col2:

            if st.button(
                "Thẻ tiếp →",
                use_container_width=True,
                disabled=(index == total - 1)
            ):

                st.session_state.flashcard_index += 1

                st.session_state.flashcard_flipped = False

                st.rerun()
