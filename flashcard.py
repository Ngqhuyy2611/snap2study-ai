import streamlit as st


def display_flashcards(
    flashcards,
    title="🃏 Flashcard",
    state_prefix="main"
):

    if not flashcards:
        st.warning("Chưa có Flashcard.")
        return

    # =====================================================
    # UNIQUE SESSION STATE
    # =====================================================

    index_key = f"{state_prefix}_flashcard_index"
    flipped_key = f"{state_prefix}_flashcard_flipped"

    if index_key not in st.session_state:
        st.session_state[index_key] = 0

    if flipped_key not in st.session_state:
        st.session_state[flipped_key] = False

    # =====================================================
    # CHECK INDEX
    # =====================================================

    if st.session_state[index_key] >= len(flashcards):

        st.session_state[index_key] = 0
        st.session_state[flipped_key] = False

    index = st.session_state[index_key]
    flipped = st.session_state[flipped_key]

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

.flashcard-wrapper {
    margin-top: 20px;
    margin-bottom: 25px;
}

.flashcard-card {
    border-radius: 24px;
    padding: 42px 35px;
    min-height: 300px;

    text-align: center;

    box-shadow:
        0 12px 35px rgba(16, 24, 40, 0.10);
}

.flashcard-question {
    background:
        linear-gradient(
            135deg,
            #F5F3FF 0%,
            #EEF4FF 100%
        );

    border: 2px solid #DDD9FF;
}

.flashcard-answer {
    background:
        linear-gradient(
            135deg,
            #ECFDF3 0%,
            #EFF8FF 100%
        );

    border: 2px solid #C8EFD9;
}

.flashcard-number {
    color: #667085;
    font-size: 13px;
    font-weight: 800;

    letter-spacing: 0.7px;

    margin-bottom: 15px;
}

.flashcard-label {
    display: inline-block;

    padding: 7px 15px;

    border-radius: 999px;

    font-size: 12px;
    font-weight: 800;

    letter-spacing: 0.5px;

    margin-bottom: 25px;
}

.flashcard-question-label {
    color: #5146D8;
    background: #E9E7FF;
}

.flashcard-answer-label {
    color: #087443;
    background: #DDF8EA;
}

.flashcard-question-text {
    color: #101828;

    font-size: 25px;
    font-weight: 750;

    line-height: 1.55;

    margin: 10px auto;

    max-width: 800px;
}

.flashcard-answer-text {
    color: #101828;

    font-size: 21px;
    font-weight: 600;

    line-height: 1.65;

    margin: 10px auto;

    max-width: 800px;
}

.flashcard-hint {
    color: #667085;

    font-size: 14px;

    margin-top: 28px;
}

.flashcard-difficulty {
    display: inline-block;

    margin-top: 25px;

    padding: 8px 16px;

    border-radius: 999px;

    background: rgba(255,255,255,0.8);

    border: 1px solid #D0D5DD;

    color: #475467;

    font-size: 13px;
    font-weight: 700;
}

.flashcard-title {
    text-align: center;

    color: #101828;

    font-size: 28px;
    font-weight: 800;

    margin-top: 20px;
    margin-bottom: 5px;
}

.flashcard-subtitle {
    text-align: center;

    color: #667085;

    font-size: 14px;

    margin-bottom: 20px;
}

.flashcard-memory-title {
    text-align: center;

    color: #344054;

    font-size: 15px;
    font-weight: 700;

    margin: 18px 0 12px 0;
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

        # CSS chỉ tạo nền/khung.
        # Nội dung được render bằng Streamlit
        # để tránh lỗi HTML hiển thị thành text.

        st.markdown(
            '<div class="flashcard-wrapper">'
            '<div class="flashcard-card flashcard-question">',
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
**FLASHCARD {index + 1:02d}**
            """
        )

        st.markdown(
            '<span class="flashcard-label '
            'flashcard-question-label">'
            '❓ CÂU HỎI'
            '</span>',
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
<div class="flashcard-question-text">
{question}
</div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
<div class="flashcard-hint">
💡 Hãy thử tự trả lời trước khi lật thẻ
</div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            "</div></div>",
            unsafe_allow_html=True
        )

        st.write("")

        if st.button(
            "🔄  Lật thẻ",
            use_container_width=True,
            type="primary"
        ):

            st.session_state[flipped_key] = True

            st.rerun()

    # =====================================================
    # ANSWER
    # =====================================================

    else:

        st.markdown(
            '<div class="flashcard-wrapper">'
            '<div class="flashcard-card flashcard-answer">',
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
**FLASHCARD {index + 1:02d}**
            """
        )

        st.markdown(
            '<span class="flashcard-label '
            'flashcard-answer-label">'
            '✅ ĐÁP ÁN'
            '</span>',
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
<div class="flashcard-answer-text">
{answer}
</div>
            """,
            unsafe_allow_html=True
        )

        if difficulty:

            st.markdown(
                f"""
<div class="flashcard-difficulty">
📊 Độ khó: {difficulty}
</div>
                """,
                unsafe_allow_html=True
            )

        st.markdown(
            "</div></div>",
            unsafe_allow_html=True
        )

        # =================================================
        # MEMORY
        # =================================================

        st.markdown(
            """
<div class="flashcard-memory-title">
🧠 Bạn nhớ thẻ này đến mức nào?
</div>
            """,
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            if st.button(
                "😕 Chưa nhớ",
                use_container_width=True,
                key=f"{state_prefix}_not_remembered_{index}"
            ):

                st.session_state[flipped_key] = False

                st.toast(
                    "💡 Hãy ôn lại thẻ này!"
                )

                st.rerun()

        with col2:

            if st.button(
                "🤔 Hơi nhớ",
                use_container_width=True,
                key=f"{state_prefix}_half_remembered_{index}"
            ):

                st.session_state[flipped_key] = False

                st.toast(
                    "📖 Có thể ôn lại lần nữa!"
                )

                st.rerun()

        with col3:

            if st.button(
                "😊 Đã nhớ",
                use_container_width=True,
                key=f"{state_prefix}_remembered_{index}"
            ):

                st.session_state[flipped_key] = False

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
                disabled=(index == 0),
                key=f"{state_prefix}_previous"
            ):

                st.session_state[index_key] -= 1

                st.session_state[flipped_key] = False

                st.rerun()

        with col2:

            if st.button(
                "Thẻ tiếp  →",
                use_container_width=True,
                disabled=(index == total - 1),
                key=f"{state_prefix}_next"
            ):

                st.session_state[index_key] += 1

                st.session_state[flipped_key] = False

                st.rerun()
