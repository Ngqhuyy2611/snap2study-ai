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
    # STATE RIÊNG CHO TỪNG BỘ FLASHCARD
    # =====================================================

    index_key = f"{state_prefix}_flashcard_index"
    flipped_key = f"{state_prefix}_flashcard_flipped"

    if index_key not in st.session_state:
        st.session_state[index_key] = 0

    if flipped_key not in st.session_state:
        st.session_state[flipped_key] = False

    total = len(flashcards)

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

    # =====================================================
    # TITLE
    # =====================================================

    st.markdown(
        f"## {title}"
    )

    st.caption(
        "Lật từng thẻ để tự kiểm tra khả năng ghi nhớ."
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
    # FLASHCARD
    # =====================================================

    with st.container(border=True):

        if not flipped:

            st.markdown(
                f"### 🟣 FLASHCARD {index + 1:02d}"
            )

            st.info(
                "❓ **CÂU HỎI**\n\n"
                + question
            )

            st.caption(
                "💡 Hãy thử tự trả lời trước khi lật thẻ."
            )

            st.write("")

            if st.button(
                "🔄 Lật thẻ",
                use_container_width=True,
                type="primary",
                key=f"{state_prefix}_flip_{index}"
            ):

                st.session_state[flipped_key] = True
                st.rerun()

        else:

            st.markdown(
                f"### 🟢 FLASHCARD {index + 1:02d}"
            )

            st.success(
                "✅ **ĐÁP ÁN**\n\n"
                + answer
            )

            if difficulty:
                st.caption(
                    f"📊 Độ khó: **{difficulty}**"
                )

    # =====================================================
    # MEMORY CHECK
    # =====================================================

    if flipped:

        st.write("")

        st.markdown(
            "#### 🧠 Bạn nhớ thẻ này đến mức nào?"
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

    # =====================================================
    # NAVIGATION
    # =====================================================

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "← Thẻ trước",
            use_container_width=True,
            disabled=(index == 0),
            key=f"{state_prefix}_previous_{index}"
        ):

            st.session_state[index_key] -= 1
            st.session_state[flipped_key] = False

            st.rerun()

    with col2:

        if st.button(
            "Thẻ tiếp →",
            use_container_width=True,
            disabled=(index == total - 1),
            key=f"{state_prefix}_next_{index}"
        ):

            st.session_state[index_key] += 1
            st.session_state[flipped_key] = False

            st.rerun()
