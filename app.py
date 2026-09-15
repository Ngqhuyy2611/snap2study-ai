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

if "study_data" not in st.session_state:
    st.session_state.study_data = None

if "history" not in st.session_state:
    st.session_state.history = []

if "review_cards" not in st.session_state:
    st.session_state.review_cards = []


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

/* ========================================================
   GLOBAL
   ======================================================== */

.stApp {
    background: #F6F8FC;
    color: #1D2939;
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}


/* ========================================================
   HEADER
   ======================================================== */

.snap-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 0 20px 0;
}

.snap-logo {
    display: flex;
    align-items: center;
    gap: 10px;
}

.snap-logo-icon {
    width: 42px;
    height: 42px;
    border-radius: 13px;
    background: linear-gradient(135deg, #635BFF, #4F8CFF);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 23px;
    box-shadow: 0 6px 18px rgba(99, 91, 255, 0.20);
}

.snap-logo-text {
    font-size: 23px;
    font-weight: 800;
    color: #1D2939;
    letter-spacing: -0.5px;
}

.snap-logo-ai {
    color: #635BFF;
}


/* ========================================================
   HERO
   ======================================================== */

.hero-section {
    text-align: center;
    padding: 55px 20px 45px 20px;
}

.hero-badge {
    display: inline-block;
    padding: 8px 15px;
    border-radius: 30px;
    background: #EEECFF;
    color: #635BFF;
    font-size: 14px;
    font-weight: 700;
    margin-bottom: 18px;
}

.hero-title {
    font-size: 48px;
    line-height: 1.12;
    font-weight: 850;
    letter-spacing: -1.8px;
    margin: 0;
    color: #101828;
}

.hero-gradient {
    background: linear-gradient(
        90deg,
        #635BFF,
        #4F8CFF
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-description {
    max-width: 650px;
    margin: 20px auto 0 auto;
    font-size: 18px;
    line-height: 1.7;
    color: #667085;
}


/* ========================================================
   FEATURE CARDS
   ======================================================== */

.feature-card {
    background: #FFFFFF;
    border: 1px solid #EAECF0;
    border-radius: 18px;
    padding: 25px 22px;
    height: 100%;
    box-shadow: 0 5px 20px rgba(16, 24, 40, 0.04);
}

.feature-icon {
    width: 48px;
    height: 48px;
    border-radius: 14px;
    background: #F0EEFF;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    margin-bottom: 16px;
}

.feature-title {
    font-size: 18px;
    font-weight: 750;
    color: #1D2939;
    margin-bottom: 7px;
}

.feature-text {
    font-size: 14px;
    line-height: 1.6;
    color: #667085;
}


/* ========================================================
   SECTION TITLES
   ======================================================== */

.section-title {
    text-align: center;
    font-size: 27px;
    font-weight: 800;
    color: #101828;
    margin-top: 35px;
    margin-bottom: 8px;
}

.section-description {
    text-align: center;
    color: #667085;
    margin-bottom: 25px;
}


/* ========================================================
   UPLOAD CARD
   ======================================================== */

.upload-card {
    background: #FFFFFF;
    border: 2px dashed #C7C2FF;
    border-radius: 22px;
    padding: 30px;
    margin-top: 15px;
    margin-bottom: 10px;
    box-shadow: 0 8px 28px rgba(16, 24, 40, 0.05);
}

.upload-title {
    text-align: center;
    font-size: 21px;
    font-weight: 750;
    color: #1D2939;
}

.upload-description {
    text-align: center;
    color: #667085;
    font-size: 14px;
    margin-top: 6px;
}


/* ========================================================
   FILE UPLOADER
   ======================================================== */

[data-testid="stFileUploader"] {
    background: transparent;
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


/* ========================================================
   BUTTONS
   ======================================================== */

.stButton > button {
    border-radius: 12px;
    border: none;
    min-height: 46px;
    font-weight: 700;
    font-size: 15px;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 18px rgba(99, 91, 255, 0.18);
}


/* ========================================================
   IMAGE
   ======================================================== */

[data-testid="stImage"] {
    border-radius: 16px;
    overflow: hidden;
}


/* ========================================================
   ALERT BOXES
   ======================================================== */

[data-testid="stAlert"] {
    border-radius: 14px;
}


/* ========================================================
   EXPANDER
   ======================================================== */

[data-testid="stExpander"] {
    border-radius: 14px;
    border: 1px solid #EAECF0;
    background: #FFFFFF;
}


/* ========================================================
   DIVIDER
   ======================================================== */

hr {
    border-color: #EAECF0;
}


/* ========================================================
   FOOTER
   ======================================================== */

.snap-footer {
    text-align: center;
    margin-top: 60px;
    padding-top: 25px;
    border-top: 1px solid #EAECF0;
    color: #98A2B3;
    font-size: 13px;
}

.snap-footer strong {
    color: #635BFF;
}


/* ========================================================
   MOBILE
   ======================================================== */

@media (max-width: 768px) {

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .hero-section {
        padding-top: 35px;
    }

    .hero-title {
        font-size: 35px;
    }

    .hero-description {
        font-size: 16px;
    }

    .snap-logo-text {
        font-size: 20px;
    }

    .feature-card {
        margin-bottom: 15px;
    }
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR - HISTORY
# =========================================================

with st.sidebar:

    st.markdown("## 📚 Lịch sử học tập")

    st.caption(
        "Các bộ ôn tập bạn đã tạo trong phiên hiện tại."
    )

    if not st.session_state.history:

        st.info("Chưa có bài học nào.")

    else:

        for i, item in enumerate(
            reversed(st.session_state.history)
        ):

            history_index = (
                len(st.session_state.history) - 1 - i
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

                st.session_state.study_data = item["data"]

                st.session_state.flashcard_index = 0
                st.session_state.flashcard_flipped = False

                st.session_state.review_cards = []

                st.rerun()

            st.caption(timestamp)


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="snap-header">
<div class="snap-logo">
<div class="snap-logo-icon">📚</div>

<div class="snap-logo-text">
Snap2Study <span class="snap-logo-ai">AI</span>
</div>

</div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# HERO
# =========================================================

st.markdown("""
<div class="hero-section">

<div class="hero-badge">
✨ AI-powered study assistant
</div>

<h1 class="hero-title">
Học thông minh hơn<br>
cùng <span class="hero-gradient">Snap2Study AI</span>
</h1>

<p class="hero-description">
Biến tài liệu học tập thành Flashcard và Quiz
bằng AI, giúp bạn ôn tập nhanh hơn và hiệu quả hơn.
</p>

</div>
""", unsafe_allow_html=True)


# =========================================================
# FEATURES
# =========================================================

col1, col2, col3 = st.columns(3)


with col1:

    st.markdown("""
<div class="feature-card">

<div class="feature-icon">
📷
</div>

<div class="feature-title">
Nhận diện tài liệu
</div>

<div class="feature-text">
Tải ảnh bài học và để OCR
chuyển nội dung trong ảnh thành văn bản.
</div>

</div>
""", unsafe_allow_html=True)


with col2:

    st.markdown("""
<div class="feature-card">

<div class="feature-icon">
🃏
</div>

<div class="feature-title">
Flashcard thông minh
</div>

<div class="feature-text">
AI biến nội dung bài học thành
những câu hỏi và đáp án dễ ôn tập.
</div>

</div>
""", unsafe_allow_html=True)


with col3:

    st.markdown("""
<div class="feature-card">

<div class="feature-icon">
❓
</div>

<div class="feature-title">
Quiz kiểm tra
</div>

<div class="feature-text">
Kiểm tra mức độ hiểu bài
với các câu hỏi trắc nghiệm do AI tạo.
</div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# UPLOAD SECTION
# =========================================================

st.markdown("""
<div class="section-title">
🚀 Bắt đầu học
</div>

<div class="section-description">
Tải lên một trang tài liệu để Snap2Study AI tạo bộ ôn tập cho bạn.
</div>
""", unsafe_allow_html=True)


st.markdown("""
<div class="upload-card">

<div class="upload-title">
📷 Tải tài liệu học tập
</div>

<div class="upload-description">
Chọn ảnh rõ nét của trang sách hoặc tài liệu.
</div>

</div>
""", unsafe_allow_html=True)


uploaded_file = st.file_uploader(
    "Chọn ảnh bài học",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed"
)


# =========================================================
# PROCESS IMAGE
# =========================================================

if uploaded_file:

    image = Image.open(uploaded_file)

    st.write("")

    st.subheader("📄 Tài liệu của bạn")

    col1, col2 = st.columns([1.2, 0.8])


    with col1:

        st.image(
            image,
            use_container_width=True
        )


    with col2:

        st.markdown("""
<div class="feature-card">

<div class="feature-title">
✨ Sẵn sàng tạo bộ ôn tập
</div>

<div class="feature-text">
Snap2Study AI sẽ đọc nội dung,
phân tích bài học và tạo Flashcard
cùng Quiz cho bạn.
</div>

</div>
""", unsafe_allow_html=True)

        st.write("")

        create_button = st.button(
            "✨ Tạo bộ ôn tập",
            use_container_width=True
        )


        if create_button:

            with st.spinner(
                "🔍 Đang đọc tài liệu..."
            ):

                text = extract_text(image)


            if not text:

                st.error(
                    "❌ Không nhận diện được nội dung trong ảnh."
                )


            else:

                with st.expander(
                    "🔎 Nội dung đã nhận diện"
                ):

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

                        # Reset flashcard
                        st.session_state.flashcard_index = 0
                        st.session_state.flashcard_flipped = False

                        # Reset review
                        st.session_state.review_cards = []

                        # ==============================
                        # SAVE HISTORY
                        # ==============================

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

                        # Chỉ giữ 10 bài gần nhất
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

                        st.error(
                            f"❌ Có lỗi khi gọi AI: {e}"
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

    st.markdown("""
<div class="section-title">
📖 Tóm tắt bài học
</div>
""", unsafe_allow_html=True)

    st.info(
        data.get(
            "summary",
            "Không có phần tóm tắt."
        )
    )


    # =====================================================
    # FLASHCARD
    # =====================================================

    st.divider()

    display_flashcards(
        data.get("flashcards", [])
    )


    # =====================================================
    # QUIZ
    # =====================================================

    st.divider()

    display_quiz(
        data.get("quiz", [])
    )


    # =====================================================
    # REVIEW WRONG ANSWERS
    # =====================================================

    if st.session_state.review_cards:

        st.divider()

        st.markdown("""
<div class="section-title">
🔁 Ôn lại phần chưa chắc
</div>

<div class="section-description">
Những câu bạn làm chưa đúng được chuyển thành
Flashcard để ôn lại.
</div>
""", unsafe_allow_html=True)

        display_flashcards(
            st.session_state.review_cards,
            title="🔁 Flashcard ôn lại"
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="snap-footer">

Made with ✨ by <strong>Snap2Study AI</strong>

<br>

AI-powered learning assistant for students

</div>
""", unsafe_allow_html=True)
