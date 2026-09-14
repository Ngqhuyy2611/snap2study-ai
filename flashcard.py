import streamlit as st


def display_flashcards(flashcards):

    if not flashcards:
        st.warning("Chưa có Flashcard.")
        return

    # Khởi tạo trạng thái
    if "flashcard_index" not in st.session_state:
        st.session_state.flashcard_index = 0

    if "flashcard_flipped" not in st.session_state:
        st.session_state.flashcard_flipped = False

    index = st.session_state.flashcard_index
    flipped = st.session_state.flashcard_flipped

    card = flashcards[index]

    # =========================
    # TIÊU ĐỀ
    # =========================

    st.subheader("🃏 Flashcard")

    st.progress(
        (index + 1) / len(flashcards),
        text=f"Thẻ {index + 1} / {len(flashcards)}"
    )

    st.write("")

    # =========================
    # MẶT TRƯỚC
    # =========================

    if not flipped:

        with st.container(border=True):

            st.markdown(
                "<div style='text-align:center;'>"
                "<p style='color:#667085;'>CÂU HỎI</p>"
                "</div>",
                unsafe_allow_html=True
            )

            st.markdown(
                f"## {card['question']}"
            )

            st.markdown(
                "<div style='text-align:center;'>"
                "<p style='color:#98A2B3;'>"
                "💡 Hãy thử trả lời trước khi lật thẻ"
                "</p>"
                "</div>",
                unsafe_allow_html=True
            )

        st.write("")

        if st.button(
            "↻  Lật thẻ",
            use_container_width=True
        ):
            st.session_state.flashcard_flipped = True
            st.rerun()

    # =========================
    # MẶT SAU
    # =========================

    else:

        with st.container(border=True):

            st.markdown(
                "<div style='text-align:center;'>"
                "<p style='color:#667085;'>ĐÁP ÁN</p>"
                "</div>",
                unsafe_allow_html=True
            )

            st.markdown(
                f"## {card['answer']}"
            )

        st.write("")

        # =========================
        # ĐÁNH GIÁ
        # =========================

        st.markdown("**Bạn nhớ thẻ này không?**")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("😕 Chưa nhớ", use_container_width=True):
                st.toast("💡 Hãy đánh dấu để ôn lại thẻ này!")

        with col2:
            if st.button("🤔 Hơi nhớ", use_container_width=True):
                st.toast("📖 Bạn có thể ôn lại thẻ này!")

        with col3:
            if st.button("😊 Đã nhớ", use_container_width=True):
                st.toast("🎉 Tuyệt vời!")

        st.write("")

        # =========================
        # ĐIỀU HƯỚNG
        # =========================

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
                disabled=(index == len(flashcards) - 1)
            ):
                st.session_state.flashcard_index += 1
                st.session_state.flashcard_flipped = False
                st.rerun()