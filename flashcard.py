import streamlit as st
import html


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

    question = html.escape(
        str(card.get("question", ""))
    )

    answer = html.escape(
        str(card.get("answer", ""))
    )

    difficulty = html.escape(
        str(card.get("difficulty", ""))
    )

    total = len(flashcards)

    # =====================================================
    # CUSTOM STYLE
    # =====================================================

    st.markdown(
        """
        <style>

        /* ================================
           FLASHCARD CONTAINER
        ================================= */

        .snap-flashcard {
            border-radius: 24px;
            padding: 36px 35px;
            margin: 15px 0 25px 0;
            min-height: 300px;

            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;

            text-align: center;

            border: 1px solid rgba(99, 91, 255, 0.18);

            box-shadow:
                0 12px 35px rgba(31, 41, 55, 0.10);

            transition: all 0.25s ease;
        }

        .snap-flashcard-question {
            background:
                linear-gradient(
                    135deg,
                    #F5F3FF 0%,
                    #EEF4FF 100%
                );
        }

        .snap-flashcard-answer {
            background:
                linear-gradient(
                    135deg,
                    #ECFDF3 0%,
                    #EFF8FF 100%
                );

            border-color: rgba(18, 183, 106, 0.20);
        }

        /* ================================
           BADGE
        ================================= */

        .flashcard-badge {
            display: inline-block;

            padding: 7px 15px;

            border-radius: 999px;

            font-size: 12px;
            font-weight: 800;

            letter-spacing: 0.6px;

            margin-bottom: 22px;
        }

        .question-badge {
            color: #5146D8;
            background: #E9E7FF;
        }

        .answer-badge {
            color: #087443;
            background: #DDF8EA;
        }

        /* ================================
           CARD TEXT
        ================================= */

        .flashcard-text {
            color: #101828;

            font-size: 25px;
            font-weight: 700;

            line-height: 1.55;

            max-width: 760px;

            margin: 0 auto;
        }

        .flashcard-answer-text {
            color: #101828;

            font-size: 22px;
            font-weight: 600;

            line-height: 1.6;

            max-width: 760px;

            margin: 0 auto;
        }

        /* ================================
           HINT
        ================================= */

        .flashcard-hint {
            margin-top: 28px;

            color: #667085;

            font-size: 14px;
        }

        /* ================================
           DIFFICULTY
        ================================= */

        .difficulty-badge {
            margin-top: 25px;

            padding: 8px 16px;

            border-radius: 999px;

            background: rgba(255,255,255,0.75);

            color: #475467;

            font-size: 13px;
            font-weight: 700;

            border: 1px solid rgba(16,24,40,0.08);
        }

        /* ================================
           SECTION TITLE
        ================================= */

        .flashcard-section-title {
            text-align: center;

            margin-top: 20px;
            margin-bottom: 5px;

            font-size: 28px;
            font-weight: 800;

            color: #101828;
        }

        .flashcard-section-subtitle {
            text-align: center;

            color: #667085;

            font-size: 14px;

            margin-bottom: 20px;
        }

        /* ================================
           MEMORY LABEL
        ================================= */

        .memory-title {
            text-align: center;

            font-size: 15px;

            font-weight: 700;

            color: #344054;

            margin: 12px 0;
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
        <div class="flashcard-section-title">
            {title}
        </div>

        <div class="flashcard-section-subtitle">
            Lật thẻ để kiểm tra khả năng ghi nhớ của bạn
        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # PROGRESS
    # =====================================================

    progress_value = (index + 1) / total

    st.progress(
        progress_value,
        text=f"📚 Thẻ {index + 1} / {total}"
    )

    st.write("")

    # =====================================================
    # QUESTION SIDE
    # =====================================================

    if not flipped:

        st.markdown(
            f"""
            <div class="snap-flashcard snap-flashcard-question">

                <div class="flashcard-badge question-badge">
                    🃏 FLASHCARD {index + 1:02d}
                </div>

                <div class="flashcard-badge question-badge">
                    ❓ CÂU HỎI
                </div>

                <div class="flashcard-text">
                    {question}
                </div>

                <div class="flashcard-hint">
                    💡 Hãy thử tự trả lời trước khi lật thẻ
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        if st.button(
            "🔄  Lật thẻ",
            use_container_width=True,
            type="primary"
        ):
            st.session_state.flashcard_flipped = True
            st.rerun()

    # =====================================================
    # ANSWER SIDE
    # =====================================================

    else:

        st.markdown(
            f"""
            <div class="snap-flashcard snap-flashcard-answer">

                <div class="flashcard-badge answer-badge">
                    🃏 FLASHCARD {index + 1:02d}
                </div>

                <div class="flashcard-badge answer-badge">
                    ✅ ĐÁP ÁN
                </div>

                <div class="flashcard-answer-text">
                    {answer}
                </div>

                {
                    f'<div class="difficulty-badge">📊 Độ khó: {difficulty}</div>'
                    if difficulty
                    else ""
                }

            </div>
            """,
            unsafe_allow_html=True
        )

        # =================================================
        # MEMORY RATING
        # =================================================

        st.markdown(
            """
            <div class="memory-title">
                🧠 Bạn nhớ thẻ này đến mức nào?
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

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
                "←  Thẻ trước",
                use_container_width=True,
                disabled=(index == 0)
            ):

                st.session_state.flashcard_index -= 1

                st.session_state.flashcard_flipped = False

                st.rerun()

        with col2:

            if st.button(
                "Thẻ tiếp  →",
                use_container_width=True,
                disabled=(index == total - 1)
            ):

                st.session_state.flashcard_index += 1

                st.session_state.flashcard_flipped = False

                st.rerun()
