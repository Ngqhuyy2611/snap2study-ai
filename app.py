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

    # Main Flashcard
    "main_flashcard_index": 0,
    "main_flashcard_flipped": False,

    # Review Flashcard
    "review_flashcard_index": 0,
    "review_flashcard_flipped": False,

    # Quiz
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
    background: #F6F8FC !important;
    color: #101828 !important;
}

.block-container {
    max-width: 1150px !important;
    padding-top: 2rem !important;
    padding-bottom: 4rem !important;
}

h1,
h2,
h3,
h4,
h5,
h6 {
    color: #101828 !important;
}

p,
li {
    color: #344054;
}

[data-testid="stCaptionContainer"] {
    color: #667085 !important;
}


/* =====================================================
   SIDEBAR
   ===================================================== */

[data-testid="stSidebar"] {
    background: #FFFFFF !important;
    border-right: 1px solid #E4E7EC !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4 {
    color: #101828 !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    color: #344054 !important;
}

[data-testid="stSidebar"] .stButton > button {
    background: #FFFFFF !important;
    color: #344054 !important;
    border: 1px solid #E4E7EC !important;
    border-radius: 12px !important;
    min-height: 42px !important;
    text-align: left !important;
    box-shadow: 0 2px 6px rgba(16, 24, 40, 0.04) !important;
    transition: all 0.18s ease !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: #F7F6FF !important;
    color: #5146D8 !important;
    border-color: #B8B3FF !important;
}


/* =====================================================
   BUTTON
   ===================================================== */

.stButton > button {
    border-radius: 12px !important;
    min-height: 45px !important;
    font-weight: 700 !important;
    background: #FFFFFF !important;
    color: #344054 !important;
    border: 1px solid #D0D5DD !important;
    box-shadow: 0 1px 2px rgba(16, 24, 40, 0.05) !important;
}

.stButton > button:hover {
    background: #F8F7FF !important;
    color: #5146D8 !important;
    border-color: #8B82FF !important;
    box-shadow: 0 5px 14px rgba(99, 91, 255, 0.12) !important;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(
        135deg,
        #635BFF 0%,
        #7C6FFF 100%
    ) !important;

    color: #FFFFFF !important;
    border: none !important;

    box-shadow:
        0 7px 18px rgba(99, 91, 255, 0.25) !important;
}

.stButton > button[kind="primary"]:hover {
    background: linear-gradient(
        135deg,
        #574FE8 0%,
        #7062F5 100%
    ) !important;

    color: #FFFFFF !important;
}


/* =====================================================
   FILE UPLOADER
   ===================================================== */

[data-testid="stFileUploaderDropzone"] {
    background: #FFFFFF !important;
    border: 2px dashed #B8B3FF !important;
    border-radius: 18px !important;
    box-shadow: 0 4px 14px rgba(16, 24, 40, 0.05) !important;
}

[data-testid="stFileUploaderDropzone"]:hover {
    background: #F9F8FF !important;
    border-color: #635BFF !important;
}

[data-testid="stFileUploaderDropzone"] p,
[data-testid="stFileUploaderDropzone"] span {
    color: #344054 !important;
}


/* =====================================================
   INPUT
   ===================================================== */

[data-baseweb="input"] {
    background: #FFFFFF !important;
    border-radius: 12px !important;
}

[data-baseweb="input"] input {
    background: #FFFFFF !important;
    color: #101828 !important;
}

textarea {
    background: #FFFFFF !important;
    color: #101828 !important;
}


/* =====================================================
   RADIO / CHECKBOX
   ===================================================== */

[data-testid="stRadio"] label,
[data-testid="stRadio"] p,
[data-testid="stCheckbox"] label {
    color: #344054 !important;
}


/* =====================================================
   EXPANDER
   ===================================================== */

[data-testid="stExpander"] {
    background: #FFFFFF !important;
    border: 1px solid #DDE1E8 !important;
    border-radius: 16px !important;
    box-shadow: 0 3px 10px rgba(16, 24, 40, 0.04) !important;
}

[data-testid="stExpander"] p {
    color: #344054 !important;
}


/* =====================================================
   CONTAINER
   ===================================================== */

[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: #DDE1E8 !important;
    border-radius: 18px !important;
    background: #FFFFFF !important;
    box-shadow: 0 4px 12px rgba(16, 24, 40, 0.04) !important;
}


/* =====================================================
   IMAGE
   ===================================================== */

[data-testid="stImage"] img {
    border-radius: 18px !important;
    border: 1px solid #E4E7EC !important;
    box-shadow: 0 6px 18px rgba(16, 24, 40, 0.07) !important;
}


/* =====================================================
   DIVIDER
   ===================================================== */

hr {
    border-color: #E4E7EC !important;
}


/* =====================================================
   HOMEPAGE HERO
   ===================================================== */

.snap-hero {
    width: 100%;
    box-sizing: border-box;
    padding: 58px 35px 52px 35px;
    margin: 5px 0 32px 0;

    border-radius: 28px;

    text-align: center;

    background:
        radial-gradient(
            circle at 15% 15%,
            rgba(255,255,255,0.20),
            transparent 30%
        ),
        radial-gradient(
            circle at 85% 85%,
            rgba(196,181,253,0.28),
            transparent 32%
        ),
        linear-gradient(
            135deg,
            #5748D8 0%,
            #6957E8 48%,
            #8065F5 100%
        );

    box-shadow:
        0 20px 45px rgba(91,75,219,0.20);

    color: white;
}

.snap-hero-title {
    font-size: 52px;
    line-height: 1.15;
    font-weight: 800;

    color: white !important;

    margin: 0;
    padding: 0;

    letter-spacing: -1.5px;
}

.snap-hero-ai {
    font-weight: 500;
    opacity: 0.90;
}

.snap-hero-subtitle {
    margin-top: 14px;

    font-size: 24px;
    line-height: 1.35;
    font-weight: 700;

    color: rgba(255,255,255,0.96) !important;
}

.snap-hero-description {
    max-width: 720px;

    margin: 16px auto 0 auto;

    font-size: 16px;
    line-height: 1.7;

    color: rgba(255,255,255,0.86) !important;
}

.snap-hero-description strong {
    color: #FFFFFF !important;
}


/* =====================================================
   HOMEPAGE FEATURE CARDS
   ===================================================== */

.home-feature {
    height: 100%;
    box-sizing: border-box;

    padding: 26px 22px;

    border-radius: 20px;

    background: #FFFFFF;

    border: 1px solid #E1E4EC;

    box-shadow:
        0 8px 25px rgba(16,24,40,0.06);

    text-align: center;
}

.home-feature-icon {
    width: 54px;
    height: 54px;

    margin: 0 auto 14px auto;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 16px;

    background: #F0EDFF;

    font-size: 27px;
}

.home-feature-title {
    font-size: 17px;
    font-weight: 750;

    color: #101828 !important;

    margin-bottom: 7px;
}

.home-feature-text {
    font-size: 14px;
    line-height: 1.55;

    color: #667085 !important;
}


/* =====================================================
   START SECTION
   ===================================================== */

.home-section-title {
    text-align: center;

    margin-top: 42px;
    margin-bottom: 6px;

    font-size: 25px;
    font-weight: 750;

    color: #101828 !important;
}

.home-section-subtitle {
    text-align: center;

    margin-bottom: 18px;

    font-size: 14px;

    color: #667085 !important;
}


/* =====================================================
   MOBILE
   ===================================================== */

@media (max-width: 700px) {

    .snap-hero {
        padding: 42px 20px;
        border-radius: 22px;
    }

    .snap-hero-title {
        font-size: 38px;
    }

    .snap-hero-subtitle {
        font-size: 20px;
    }

    .snap-hero-description {
        font-size: 14px;
    }
}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 📚 Lịch sử học tập")

    st.caption(
        "Các bộ ôn tập được tạo trong phiên hiện tại."
    )

    if not st.session_state.history:

        st.info("Chưa có bài học nào.")

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
                st.session_state.quiz_score = 0
                st.session_state.quiz_total = 0
                st.session_state.quiz_percentage = 0
                st.session_state.quiz_answers = []

                st.rerun()

            st.caption(timestamp)


# =========================================================
# HOMEPAGE HERO
# =========================================================

st.markdown(
    """
<div class="snap-hero">

    <div class="snap-hero-title">
        📚 Snap2Study
        <span class="snap-hero-ai">AI</span>
    </div>

    <div class="snap-hero-subtitle">
        Học thông minh hơn từ chính tài liệu của bạn
    </div>

    <div class="snap-hero-description">
        Biến ảnh bài học thành
        <strong>Tóm tắt + Flashcard + Quiz</strong>
        bằng OCR và Gemini AI.
        <br>
        Học nhanh hơn. Ôn tập hiệu quả hơn.
    </div>

</div>
""",
    unsafe_allow_html=True
)


# =========================================================
# FEATURE CARDS
# =========================================================

st.markdown(
    """
<div style="
    text-align:center;
    margin: 0 0 20px 0;
">

    <div style="
        font-size:25px;
        font-weight:750;
        color:#101828;
    ">
        ✨ Một tài liệu — nhiều cách học
    </div>

    <div style="
        color:#667085;
        font-size:14px;
        margin-top:6px;
    ">
        Snap2Study giúp bạn biến tài liệu thành một bộ ôn tập hoàn chỉnh.
    </div>

</div>
""",
    unsafe_allow_html=True
)


col1, col2, col3 = st.columns(3, gap="medium")


with col1:

    st.markdown(
        """
<div class="home-feature">

    <div class="home-feature-icon">
        📷
    </div>

    <div class="home-feature-title">
        Nhận diện tài liệu
    </div>

    <div class="home-feature-text">
        OCR chuyển nội dung trong ảnh
        thành văn bản để AI có thể xử lý.
    </div>

</div>
""",
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        """
<div class="home-feature">

    <div class="home-feature-icon">
        🃏
    </div>

    <div class="home-feature-title">
        Flashcard thông minh
    </div>

    <div class="home-feature-text">
        AI biến kiến thức quan trọng
        thành câu hỏi và đáp án dễ ôn tập.
    </div>

</div>
""",
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        """
<div class="home-feature">

    <div class="home-feature-icon">
        ❓
    </div>

    <div class="home-feature-title">
        Quiz kiểm tra
    </div>

    <div class="home-feature-text">
        Kiểm tra mức độ hiểu bài
        và tìm ra những phần cần ôn lại.
    </div>

</div>
""",
        unsafe_allow_html=True
    )


# =========================================================
# START STUDY
# =========================================================

st.markdown(
    """
<div class="home-section-title">
    🚀 Bắt đầu học
</div>

<div class="home-section-subtitle">
    Tải lên một trang tài liệu để Snap2Study tạo bộ ôn tập cho bạn.
</div>
""",
    unsafe_allow_html=True
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

    image = Image.open(uploaded_file)

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


    # =====================================================
    # CREATE STUDY SET
    # =====================================================

    if create_button:

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


                    st.session_state.main_flashcard_index = 0
                    st.session_state.main_flashcard_flipped = False


                    st.session_state.review_cards = []

                    st.session_state.review_flashcard_index = 0
                    st.session_state.review_flashcard_flipped = False


                    st.session_state.quiz_submitted = False
                    st.session_state.quiz_score = 0
                    st.session_state.quiz_total = 0
                    st.session_state.quiz_percentage = 0
                    st.session_state.quiz_answers = []


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
                        or "high demand" in error_text.lower()
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
