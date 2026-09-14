import streamlit as st
from PIL import Image

from ocr import extract_text
from ai import generate_study_material
from flashcard import display_flashcards
from quiz import display_quiz


# =========================
# CẤU HÌNH
# =========================

st.set_page_config(
    page_title="Snap2Study AI",
    page_icon="📚",
    layout="wide"
)


# =========================
# CSS CƠ BẢN
# =========================

st.markdown("""
<style>

.main {
    background-color: #f7f9fc;
}

.logo {
    font-size: 32px;
    font-weight: 800;
}

.tagline {
    color: #667085;
}

.hero {
    padding: 40px 20px;
    text-align: center;
}

.hero h1 {
    font-size: 42px;
    font-weight: 800;
}

.hero p {
    font-size: 18px;
    color: #667085;
}

</style>
""", unsafe_allow_html=True)


# =========================
# HEADER
# =========================

st.markdown(
    '<div class="logo">📚 Snap2Study AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="tagline">AI-powered study assistant</div>',
    unsafe_allow_html=True
)

st.divider()


# =========================
# HERO
# =========================

st.markdown("""
<div class="hero">

<h1>Biến tài liệu thành<br>bộ ôn tập bằng AI</h1>

<p>
Tải lên tài liệu và để Snap2Study AI
<br>
tạo Flashcard và Quiz cho bạn.
</p>

</div>
""", unsafe_allow_html=True)


# =========================
# UPLOAD
# =========================

uploaded_file = st.file_uploader(
    "📷 Chọn ảnh bài học",
    type=["jpg", "jpeg", "png"]
)


if uploaded_file:

    image = Image.open(uploaded_file)

    st.subheader("📄 Tài liệu")

    st.image(
        image,
        width=650
    )

    st.write("")

    # =========================
    # BUTTON
    # =========================

    if st.button(
        "✨ Tạo bộ ôn tập",
        use_container_width=True
    ):

        with st.spinner("🔍 Đang đọc tài liệu..."):

            text = extract_text(image)

        if not text:

            st.error(
                "❌ Không nhận diện được nội dung trong ảnh."
            )

        else:

            with st.expander("🔎 Nội dung đã nhận diện"):

                st.write(text)

            with st.spinner(
                "🤖 AI đang tạo Flashcard và Quiz..."
            ):

                try:

                    study_data = generate_study_material(
                        text,
                        number_of_cards=5
                    )

                    st.session_state.study_data = study_data

                    # Reset trạng thái flashcard mỗi khi có bộ dữ liệu mới,
                    # tránh lỗi index vượt quá số thẻ (vd: bộ mới ít thẻ hơn bộ cũ)
                    st.session_state.flashcard_index = 0
                    st.session_state.flashcard_flipped = False

                    st.success(
                        "🎉 Đã tạo bộ ôn tập thành công!"
                    )

                except Exception as e:

                    st.error(
                        f"❌ Có lỗi khi gọi AI: {e}"
                    )


# =========================
# HIỂN THỊ KẾT QUẢ
# =========================

if "study_data" in st.session_state:

    data = st.session_state.study_data

    st.divider()

    # =========================
    # TÓM TẮT
    # =========================

    st.header("📖 Tóm tắt")

    st.info(
        data.get(
            "summary",
            "Không có phần tóm tắt."
        )
    )

    st.divider()

    # =========================
    # FLASHCARD
    # =========================

    display_flashcards(
        data.get("flashcards", [])
    )

    st.divider()

    # =========================
    # QUIZ
    # =========================

    display_quiz(
        data.get("quiz", [])
    )