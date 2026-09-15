import streamlit as st


def display_flashcards(
    flashcards,
    title="🃏 Flashcard"
):

    if not flashcards:

        st.warning(
            "Chưa có Flashcard."
        )

        return


    # =====================================================
    # SESSION STATE
    # =====================================================

    if "flashcard_index" not in st.session_state:

        st.session_state.flashcard_index = 0


    if "flashcard_flipped" not in st.session_state:

        st.session_state.flashcard_flipped = False


    # Kiểm tra index

    if (
        st.session_state.flashcard_index
        >= len(flashcards)
    ):

        st.session_state.flashcard_index = 0

        st.session_state.flashcard_flipped = False


    index = st.session_state.flashcard_index

    flipped = st.session_state.flashcard_flipped

    card = flashcards[index]


    # =====================================================
    # TITLE
    # =====================================================

    st.markdown(
        f"""
<div style="
    text-align:center;
    margin-top:25px;
    margin-bottom:15px;
">
<h2>{title}</h2>
</div>
""",
        unsafe_allow_html=True
    )


    # =====================================================
    # PROGRESS
    # =====================================================

    st.progress(
        (index + 1) / len(flashcards),
        text=f"Thẻ {index + 1} / {len(flashcards)}"
    )


    st.write("")


    # =====================================================
    # QUESTION
    # =====================================================

    if not flipped:

        with st.container(border=True):

            st.markdown(
                """
<div style="
    text-align:center;
    color:#635BFF;
    font-weight:700;
    font-size:14px;
    margin-bottom:15px;
">
CÂU HỎI
</div>
""",
                unsafe_allow_html=True
            )


            st.markdown(
                f"""
<div style="
    text-align:center;
    font-size:25px;
    font-weight:700;
    color:#101828;
    padding:25px 10px;
">
{card.get("question", "")}
</div>
""",
                unsafe_allow_html=True
            )


            st.markdown(
                """
<div style="
    text-align:center;
    color:#98A2B3;
    margin-top:15px;
">
💡 Hãy thử trả lời trước khi lật thẻ
</div>
""",
                unsafe_allow_html=True
            )


        st.write("")


        if st.button(
            "🔄 Lật thẻ",
            use_container_width=True
        ):

            st.session_state.flashcard_flipped = True

            st.rerun()


    # =====================================================
    # ANSWER
    # =====================================================

    else:

        with st.container(border=True):

            st.markdown(
                """
<div style="
    text-align:center;
    color:#12B76A;
    font-weight:700;
    font-size:14px;
    margin-bottom:15px;
">
ĐÁP ÁN
</div>
""",
                unsafe_allow_html=True
            )


            st.markdown(
                f"""
<div style="
    text-align:center;
    font-size:22px;
    font-weight:600;
    color:#101828;
    padding:25px 10px;
">
{card.get("answer", "")}
</div>
""",
                unsafe_allow_html=True
            )


            if card.get("difficulty"):

                st.markdown(
                    f"""
<div style="
    text-align:center;
    color:#667085;
    margin-top:10px;
">
Độ khó:
<b>{card.get("difficulty")}</b>
</div>
""",
                    unsafe_allow_html=True
                )


        st.write("")


        st.markdown(
            """
<div style="
    text-align:center;
    font-weight:600;
">
Bạn nhớ thẻ này không?
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
                disabled=(
                    index == len(flashcards) - 1
                )
            ):

                st.session_state.flashcard_index += 1

                st.session_state.flashcard_flipped = False

                st.rerun()
