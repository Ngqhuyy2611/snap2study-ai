import streamlit as st

from PIL import Image
from datetime import datetime

from ocr import extract_text
from ai import generate_study_material
from flashcard import display_flashcards
from quiz import display_quiz


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Snap2Study AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "study_data": None,
    "history": [],
    "review_cards": [],
    "main_flashcard_index": 0,
    "main_flashcard_flipped": False,
    "review_flashcard_index": 0,
    "review_flashcard_flipped": False,
    "quiz_submitted": False,
    "quiz_score": 0,
    "quiz_total": 0,
    "quiz_percentage": 0,
    "quiz_answers": []
}

for key, value in defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value


# =========================================================
# GLOBAL STYLE
# =========================================================

st.markdown(
    """
<style>

.stApp {
    background: #F6F8FC;
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

.stButton > button {
    border-radius: 12px;
    min-height: 45px;
    font-weight: 700;
}

[data-testid="stFileUploaderDropzone"] {
    background: #FAFAFF;
    border: 1px dashed #B9B3FF;
    border-radius: 15px;
}

[data-testid="stFileUploaderDropzone"]:hover {
    border-color: #635BFF;
    background: #F7F6FF;
}

[data-testid="stAlert"] {
    border-radius: 14px;
}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        "## 📚 Lịch sử học tập"
    )

    st.caption(
        "Các bộ ôn tập được tạo trong phiên hiện tại."
    )

    if not st.session_state.history:

        st.info(
            "Chưa có bài học nào."
        )

    else:

        for i, item in enumerate(
            reversed(st.session_state.history)
        ):

            history_index = (
                len(st.session_state.history)
                - 1
                - i
            )

            topic = item.get(
                "topic",
                "Bài học không có tên"
            )

            timestamp = item.get(
                "time",
                ""
            )

            if st.button(
                f"📖 {topic}",
                key=f"history_{history_index}",
                use_container_width=True
            ):

                st.session_state.study_data = (
                    item["data"]
                )

                st.session_state.main_flashcard_index = 0
                st.session_state.main_flashcard_flipped = False

                st.session_state.review_flashcard_index = 0
                st.session_state.review_flashcard_flipped = False

                st.session_state.review_cards = []

                st.session_state.quiz_submitted = False
                st.session_state.quiz_answers = []

                st.rerun()

            st.caption(timestamp)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
# 📚 Snap2Study **AI**

### Học thông minh hơn từ chính tài liệu của bạn

Biến ảnh bài học thành **Tóm tắt + Flashcard + Quiz**
bằng OCR và Gemini AI.
"""
)


# =========================================================
# FEATURE CARDS
# =========================================================

col1, col2, col3 = st.columns(3)

with col1:

    with st.container(border=True):

        st.markdown("### 📷")

        st.markdown(
            "**Nhận diện tài liệu**"
        )

        st.caption(
            "OCR chuyển nội dung trong ảnh "
            "thành văn bản."
        )


with col2:

    with st.container(border=True):

        st.markdown("### 🃏")

        st.markdown(
            "**Flashcard thông minh**"
        )

        st.caption(
            "AI biến kiến thức thành "
            "câu hỏi và đáp án."
        )


with col3:

    with st.container(border=True):

        st.markdown("### ❓")

        st.markdown(
            "**Quiz kiểm tra**"
        )

        st.caption(
            "Kiểm tra mức độ hiểu bài "
            "sau khi học."
        )


# =========================================================
# UPLOAD
# =========================================================

st.divider()

st.markdown(
    "## 🚀 Bắt đầu học"
)

st.caption(
    "Tải lên một trang tài liệu để Snap2Study "
    "tạo bộ ôn tập cho bạn."
)

uploaded_file = st.file_uploader(
    "📷 Chọn ảnh bài học",
    type=[
        "jpg",
        "jpeg",
        "png"
    ]
)


# =========================================================
# PROCESS
# =========================================================

if uploaded_file:

    image = Image.open(
        uploaded_file
    )

    st.divider()

    st.markdown(
        "## 📄 Tài liệu của bạn"
    )

    col1, col2 = st.columns(
        [1.2, 0.8]
    )

    with col1:

        st.image(
            image,
            use_container_width=True
        )

    with col2:

        with st.container(border=True):

            st.markdown(
                "### ✨ Sẵn sàng!"
            )

            st.write(
                "Snap2Study AI sẽ đọc tài liệu, "
                "phân tích nội dung và tạo "
                "Flashcard cùng Quiz."
            )

            create_button = st.button(
                "✨ Tạo bộ ôn tập",
                use_container_width=True,
                type="primary"
            )

    if create_button:

        # =================================================
        # OCR
        # =================================================

        with st.spinner(
            "🔍 Đang đọc tài liệu..."
        ):

            try:

                text = extract_text(
                    image
                )

            except Exception as e:

                st.error(
                    "❌ Không thể đọc tài liệu."
                )

                st.exception(e)

                text = ""

        if not text:

            st.error(
                "❌ Không nhận diện được nội dung "
                "trong ảnh. Hãy thử ảnh rõ hơn."
            )

        else:

            with st.expander(
                "🔎 Xem nội dung OCR"
            ):

                st.write(text)

            # =============================================
            # GEMINI
            # =============================================

            with st.spinner(
                "🤖 Gemini đang tạo bộ ôn tập..."
            ):

                try:

                    study_data = (
                        generate_study_material(
                            text,
                            number_of_cards=5,
                            number_of_quiz=5
                        )
                    )

                    st.session_state.study_data = (
                        study_data
                    )

                    # Reset Flashcard
                    st.session_state.main_flashcard_index = 0
                    st.session_state.main_flashcard_flipped = False

                    # Reset review
                    st.session_state.review_cards = []
                    st.session_state.review_flashcard_index = 0
                    st.session_state.review_flashcard_flipped = False

                    # Reset Quiz
                    st.session_state.quiz_submitted = False
                    st.session_state.quiz_score = 0
                    st.session_state.quiz_total = 0
                    st.session_state.quiz_percentage = 0
                    st.session_state.quiz_answers = []

                    # =====================================
                    # HISTORY
                    # =====================================

                    history_item = {
                        "topic": study_data.get(
                            "topic",
                            "Bài học mới"
                        ),
                        "time": datetime.now().strftime(
                            "%d/%m/%Y %H:%M"
                        ),
                        "data": study_data
                    }

                    st.session_state.history.append(
                        history_item
                    )

                    # Chỉ giữ 10 bài
                    if len(
                        st.session_state.history
                    ) > 10:

                        st.session_state.history = (
                            st.session_state.history[-10:]
                        )

                    st.success(
                        "🎉 Đã tạo bộ ôn tập thành công!"
                    )

                except Exception as e:

                    error_text = str(e)

                    if (
                        "503" in error_text
                        or "UNAVAILABLE" in error_text
                    ):

                        st.warning(
                            "⚠️ Gemini đang quá tải tạm thời. "
                            "Hãy bấm **Tạo bộ ôn tập** lại "
                            "sau vài giây."
                        )

                    else:

                        st.error(
                            f"❌ Có lỗi khi gọi AI: {error_text}"
                        )


# =========================================================
# STUDY RESULTS
# =========================================================

if st.session_state.study_data:

    data = st.session_state.study_data

    st.divider()

    # =====================================================
    # SUMMARY
    # =====================================================

    st.markdown(
        "## 📖 Tóm tắt bài học"
    )

    with st.container(border=True):

        st.write(
            data.get(
                "summary",
                "Không có phần tóm tắt."
            )
        )

    # =====================================================
    # FLASHCARDS
    # =====================================================

    st.divider()

    display_flashcards(
        data.get(
            "flashcards",
            []
        ),
        title="🃏 Flashcard",
        state_prefix="main"
    )

    # =====================================================
    # QUIZ
    # =====================================================

    st.divider()

    display_quiz(
        data.get(
            "quiz",
            []
        )
    )

    # =====================================================
    # REVIEW
    # =====================================================

    if st.session_state.review_cards:

        st.divider()

        st.markdown(
            "## 🔁 Ôn lại phần chưa chắc"
        )

        st.caption(
            "Những câu bạn làm chưa đúng "
            "được chuyển thành Flashcard."
        )

        display_flashcards(
            st.session_state.review_cards,
            title="🔁 Flashcard ôn lại",
            state_prefix="review"
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "✨ Snap2Study AI — AI-powered learning assistant for students"
)
