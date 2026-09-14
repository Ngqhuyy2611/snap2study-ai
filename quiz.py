import streamlit as st


def display_quiz(quiz):

    if not quiz:
        st.warning("Chưa có câu hỏi Quiz.")
        return

    st.header("❓ Quiz")

    st.write(
        f"Kiểm tra kiến thức với {len(quiz)} câu hỏi."
    )

    st.write("")

    # =========================
    # FORM
    # =========================

    with st.form("quiz_form"):

        answers = []

        for i, question in enumerate(quiz):

            st.markdown(
                f"### Câu {i + 1}"
            )

            st.write(
                question["question"]
            )

            selected = st.radio(
                "Chọn đáp án:",
                question["options"],
                key=f"quiz_{i}",
                index=None
            )

            answers.append(selected)

            st.divider()

        submitted = st.form_submit_button(
            "📝 Nộp bài",
            use_container_width=True
        )

    # =========================
    # CHẤM ĐIỂM
    # =========================

    if submitted:

        score = 0

        for i, question in enumerate(quiz):

            selected = answers[i]

            correct = question["answer"]

            if selected:

                # Lấy chữ cái A/B/C/D
                selected_letter = selected[0]

                if selected_letter == correct:
                    score += 1

        st.divider()

        percentage = int(
            score / len(quiz) * 100
        )

        if percentage >= 80:

            st.success(
                f"🎉 Xuất sắc! Bạn đạt {score}/{len(quiz)} câu."
            )

        elif percentage >= 50:

            st.warning(
                f"👍 Khá tốt! Bạn đạt {score}/{len(quiz)} câu."
            )

        else:

            st.error(
                f"📖 Bạn đạt {score}/{len(quiz)} câu. "
                "Hãy ôn lại Flashcard nhé!"
            )

        st.progress(
            percentage / 100,
            text=f"Điểm số: {percentage}%"
        )

        # =========================
        # CHI TIẾT ĐÁP ÁN
        # =========================

        st.subheader("📋 Kết quả chi tiết")

        for i, question in enumerate(quiz):

            selected = answers[i]

            correct = question["answer"]

            if selected:

                selected_letter = selected[0]

                if selected_letter == correct:

                    st.success(
                        f"Câu {i + 1}: ✅ Chính xác"
                    )

                else:

                    st.error(
                        f"Câu {i + 1}: ❌ "
                        f"Đáp án đúng: {correct}"
                    )

            else:

                st.warning(
                    f"Câu {i + 1}: ⚪ Chưa trả lời "
                    f"— Đáp án đúng: {correct}"
                )