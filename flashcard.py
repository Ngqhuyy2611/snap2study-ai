import streamlit as st


def display_flashcards(
    flashcards,
    title="🃏 Flashcard"
):
    """
    Hiển thị Flashcard dạng card nổi.
    Tự động tách state giữa Flashcard chính và Flashcard ôn lại.
    """

    if not flashcards:
        st.warning("Chưa có Flashcard.")
        return

    # =========================================================
    # STATE PREFIX
    # =========================================================

    # Nếu là phần "Ôn lại", dùng state riêng
    if "ôn lại" in title.lower() or "review" in title.lower():
        state_prefix = "review"
    else:
        state_prefix = "main"

    index_key = f"{state_prefix}_flashcard_index"
    flipped_key = f"{state_prefix}_flashcard_flipped"

    if index_key not in st.session_state:
        st.session_state[index_key] = 0

    if flipped_key not in st.session_state:
        st.session_state[flipped_key] = False

    total = len(flashcards)

    # Bảo vệ index
    if st.session_state[index_key] >= total:
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

    # =========================================================
    # CSS
    # =========================================================

    st.markdown(
        """
<style>

/* =========================================================
   FLASHCARD SECTION
   ========================================================= */

.snap-flashcard-title {
    text-align: center;
    margin-top: 28px;
    margin-bottom: 4px;
    color: #101828;
    font-size: 29px;
    font-weight: 800;
    letter-spacing: -0.5px;
}

.snap-flashcard-subtitle {
    text-align: center;
    color: #667085;
    font-size: 14px;
    margin-bottom: 20px;
}


/* =========================================================
   FLOATING CARD
   ========================================================= */

.snap-card {
    width: 100%;
    min-height: 335px;
    box-sizing: border-box;

    border-radius: 28px;

    padding: 42px 45px;

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;

    text-align: center;

    position: relative;

    margin: 22px 0 24px 0;

    box-shadow:
        0 20px 45px rgba(67, 56, 202, 0.16),
        0 6px 18px rgba(16, 24, 40, 0.08);
}


/* =========================================================
   QUESTION CARD
   ========================================================= */

.snap-card-question {
    background:
        radial-gradient(
            circle at top right,
            rgba(129, 140, 248, 0.28),
            transparent 35%
        ),
        linear-gradient(
            135deg,
            #f8f7ff 0%,
            #eef3ff 100%
        );

    border: 1px solid #d9d6ff;
}


/* =========================================================
   ANSWER CARD
   ========================================================= */

.snap-card-answer {
    background:
        radial-gradient(
            circle at top right,
            rgba(52, 211, 153, 0.22),
            transparent 35%
        ),
        linear-gradient(
            135deg,
            #effcf6 0%,
            #eef8ff 100%
        );

    border: 1px solid #bcebd3;

    box-shadow:
        0 20px 45px rgba(16, 185, 129, 0.13),
        0 6px 18px rgba(16, 24, 40, 0.07);
}


/* =========================================================
   CARD NUMBER
   ========================================================= */

.snap-card-number {
    color: #667085;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1.5px;

    margin-bottom: 17px;

    text-transform: uppercase;
}


/* =========================================================
   BADGES
   ========================================================= */

.snap-card-badge {
    display: inline-block;

    padding: 8px 17px;

    border-radius: 999px;

    font-size: 12px;
    font-weight: 800;

    letter-spacing: 0.8px;

    margin-bottom: 22px;
}

.snap-question-badge {
    color: #5146d8;
    background: #e9e7ff;

    box-shadow:
        0 4px 12px rgba(99, 91, 255, 0.10);
}

.snap-answer-badge {
    color: #087443;
    background: #dff8e9;

    box-shadow:
        0 4px 12px rgba(16, 185, 129, 0.10);
}


/* =========================================================
   QUESTION TEXT
   ========================================================= */

.snap-question-text {
    max-width: 820px;

    color: #101828;

    font-size: 25px;
    line-height: 1.55;

    font-weight: 750;

    margin: 0 auto;
}


/* =========================================================
   ANSWER TEXT
   ========================================================= */

.snap-answer-text {
    max-width: 820px;

    color: #101828;

    font-size: 21px;
    line-height: 1.65;

    font-weight: 600;

    margin: 0 auto;
}


/* =========================================================
   HINT
   ========================================================= */

.snap-card-hint {
    color: #667085;

    font-size: 13px;

    margin-top: 26px;
}


/* =========================================================
   DIFFICULTY
   ========================================================= */

.snap-difficulty {
    display: inline-block;

    margin-top: 23px;

    padding: 7px 14px;

    border-radius: 999px;

    background: rgba(255,255,255,0.72);

    border: 1px solid #d0d5dd;

    color: #475467;

    font-size: 12px;

    font-weight: 700;
}


/* =========================================================
   MEMORY AREA
   ========================================================= */

.snap-memory-title {
    text-align: center;

    color: #344054;

    font-size: 15px;

    font-weight: 750;

    margin: 20px 0 12px 0;
}


/* =========================================================
   BUTTONS
   ========================================================= */

.snap-flashcard-wrap .stButton > button {
    border-radius: 13px;
    min-height: 46px;
    font-weight: 750;
}


/* =========================================================
   MOBILE
   ========================================================= */

@media (max-width: 768px) {

    .snap-card {
        min-height: 300px;
        padding: 32px 22px;
        border-radius: 23px;
    }

    .snap-question-text {
        font-size: 21px;
    }

    .snap-answer-text {
        font-size: 18px;
    }

    .snap-flashcard-title {
        font-size: 25px;
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
        f'<div class="snap-flashcard-title">{title}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="snap-flashcard-subtitle">'
        'Lật thẻ để kiểm tra khả năng ghi nhớ'
        '</div>',
        unsafe_allow_html=True
    )

    # =========================================================
    # PROGRESS
    # =========================================================

    st.progress(
        (index + 1) / total,
        text=f"📚 Thẻ {index + 1} / {total}"
    )

    # =========================================================
    # QUESTION SIDE
    # =========================================================

    if not flipped:

        card_html = (
            '<div class="snap-card snap-card-question">'
            f'<div class="snap-card-number">'
            f'FLASHCARD {index + 1:02d}'
            '</div>'
            '<div class="snap-card-badge snap-question-badge">'
            '❓ CÂU HỎI'
            '</div>'
            f'<div class="snap-question-text">'
            f'{question}'
            '</div>'
            '<div class="snap-card-hint">'
            '💡 Hãy thử tự trả lời trước khi lật thẻ'
            '</div>'
            '</div>'
        )

        st.markdown(
            card_html,
            unsafe_allow_html=True
        )

        if st.button(
            "🔄  Lật thẻ",
            use_container_width=True,
            type="primary",
            key=f"{state_prefix}_flip_{index}"
        ):
            st.session_state[flipped_key] = True
            st.rerun()

    # =========================================================
    # ANSWER SIDE
    # =========================================================

    else:

        card_html = (
            '<div class="snap-card snap-card-answer">'
            f'<div class="snap-card-number">'
            f'FLASHCARD {index + 1:02d}'
            '</div>'
            '<div class="snap-card-badge snap-answer-badge">'
            '✅ ĐÁP ÁN'
            '</div>'
            f'<div class="snap-answer-text">'
            f'{answer}'
            '</div>'
        )

        if difficulty:
            card_html += (
                f'<div class="snap-difficulty">'
                f'📊 Độ khó: {difficulty}'
                f'</div>'
            )

        card_html += '</div>'

        st.markdown(
            card_html,
            unsafe_allow_html=True
        )

        # =====================================================
        # MEMORY
        # =====================================================

        st.markdown(
            '<div class="snap-memory-title">'
            '🧠 Bạn nhớ thẻ này đến mức nào?'
            '</div>',
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button(
                "😕 Chưa nhớ",
                use_container_width=True,
                key=f"{state_prefix}_not_{index}"
            ):
                st.session_state[flipped_key] = False
                st.toast("💡 Hãy ôn lại thẻ này!")
                st.rerun()

        with col2:
            if st.button(
                "🤔 Hơi nhớ",
                use_container_width=True,
                key=f"{state_prefix}_half_{index}"
            ):
                st.session_state[flipped_key] = False
                st.toast("📖 Ôn thêm một lần nữa nhé!")
                st.rerun()

        with col3:
            if st.button(
                "😊 Đã nhớ",
                use_container_width=True,
                key=f"{state_prefix}_remembered_{index}"
            ):
                st.session_state[flipped_key] = False
                st.toast("🎉 Tuyệt vời!")
                st.rerun()

    # =========================================================
    # NAVIGATION
    # =========================================================

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "←  Thẻ trước",
            use_container_width=True,
            disabled=(index == 0),
            key=f"{state_prefix}_previous_{index}"
        ):
            st.session_state[index_key] -= 1
            st.session_state[flipped_key] = False
            st.rerun()

    with col2:

        if st.button(
            "Thẻ tiếp  →",
            use_container_width=True,
            disabled=(index == total - 1),
            key=f"{state_prefix}_next_{index}"
        ):
            st.session_state[index_key] += 1
            st.session_state[flipped_key] = False
            st.rerun()
