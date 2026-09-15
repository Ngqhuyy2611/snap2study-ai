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
#
# Mục tiêu:
# - Giữ giao diện sáng
# - Không để dark mode làm mất chữ
# - Làm các container có border rõ hơn
# - Không dùng CSS toàn cục kiểu "* { color: ... }"
#   để tránh phá Flashcard / Quiz
#

st.markdown(
    """
<style>

/* =====================================================
   BASE
   ===================================================== */

.stApp {
    background: #F6F8FC !important;
    color: #101828 !important;
}

.block-container {
    max-width: 1150px !important;
    padding-top: 2rem !important;
    padding-bottom: 4rem !important;
}


/* =====================================================
   MAIN TEXT
   ===================================================== */

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


/* =====================================================
   SIDEBAR HISTORY BUTTON
   ===================================================== */

[data-testid="stSidebar"] .stButton > button {
    background: #FFFFFF !important;
    color: #344054 !important;

    border: 1px solid #E4E7EC !important;
    border-radius: 12px !important;

    min-height: 42px !important;

    text-align: left !important;

    box-shadow:
        0 2px 6px rgba(16, 24, 40, 0.04) !important;

    transition: all 0.18s ease !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: #F7F6FF !important;
    color: #5146D8 !important;

    border-color: #B8B3FF !important;

    transform: translateY(-1px);
}


/* =====================================================
   NORMAL BUTTON
   ===================================================== */

.stButton > button {
    border-radius: 12px !important;

    min-height: 45px !important;

    font-weight: 700 !important;

    background: #FFFFFF !important;
    color: #344054 !important;

    border: 1px solid #D0D5DD !important;

    box-shadow:
        0 1px 2px rgba(16, 24, 40, 0.05) !important;

    transition:
        all 0.18s ease !important;
}

.stButton > button:hover {
    background: #F8F7FF !important;

    color: #5146D8 !important;

    border-color: #8B82FF !important;

    box-shadow:
        0 5px 14px rgba(99, 91, 255, 0.12) !important;

    transform: translateY(-1px);
}


/* =====================================================
   PRIMARY BUTTON
   ===================================================== */

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

    border: none !important;

    box-shadow:
        0 9px 24px rgba(99, 91, 255, 0.32) !important;

    transform: translateY(-1px);
}


/* =====================================================
   FILE UPLOADER
   ===================================================== */

[data-testid="stFileUploader"] {
    color: #344054 !important;
}

[data-testid="stFileUploaderDropzone"] {
    background: #FFFFFF !important;

    border: 2px dashed #B8B3FF !important;

    border-radius: 18px !important;

    box-shadow:
        0 4px 14px rgba(16, 24, 40, 0.05) !important;

    transition: all 0.18s ease !important;
}

[data-testid="stFileUploaderDropzone"]:hover {
    background: #F9F8FF !important;

    border-color: #635BFF !important;

    box-shadow:
        0 7px 18px rgba(99, 91, 255, 0.10) !important;
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
   RADIO
   ===================================================== */

[data-testid="stRadio"] label {
    color: #344054 !important;
}

[data-testid="stRadio"] p {
    color: #344054 !important;
}


/* =====================================================
   CHECKBOX
   ===================================================== */

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

    box-shadow:
        0 3px 10px rgba(16, 24, 40, 0.04) !important;
}

[data-testid="stExpander"] p {
    color: #344054 !important;
}


/* =====================================================
   ALERT
   ===================================================== */

[data-testid="stAlert"] {
    border-radius: 14px !important;
}


/* =====================================================
   STREAMLIT CONTAINER BORDER
   ===================================================== */

[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: #DDE1E8 !important;

    border-radius: 18px !important;

    background: #FFFFFF !important;

    box-shadow:
        0 4px 12px rgba(16, 24, 40, 0.04) !important;
}


/* =====================================================
   DIVIDER
   ===================================================== */

hr {
    border-color: #E4E7EC !important;
}


/* =====================================================
   PROGRESS BAR
   ===================================================== */

[data-testid="stProgressBar"] {
    background: #E4E7EC !important;
}


/* =====================================================
   IMAGE
   ===================================================== */

[data-testid="stImage"] img {
    border-radius: 18px !important;

    border: 1px solid #E4E7EC !important;

    box-shadow:
        0 6px 18px rgba(16, 24, 40, 0.07) !important;
}


/* =====================================================
   TABLE / DATAFRAME
   ===================================================== */

[data-testid="stDataFrame"] {
    border-radius: 14px !important;

    overflow: hidden !important;
}


/* =====================================================
   SMOOTH
   ===================================================== */

html {
    scroll-behavior: smooth;
}


/* =====================================================
   IMPORTANT
   =====================================================

   KHÔNG dùng:
       * { color: ... }

   vì Flashcard và Quiz có CSS riêng.
   Nếu ép màu toàn bộ phần tử, giao diện card
   sẽ bị phá hoặc chữ bị chìm.
   ===================================================== */

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

                # Reset main Flashcard
                st.session_state.main_flashcard_index = 0
                st.session_state.main_flashcard_flipped = False

                # Reset review Flashcard
                st.session_state.review_flashcard_index = 0
                st.session_state.review_flashcard_flipped = False
                st.session_state.review_cards = []

                # Reset Quiz
                st.session_state.quiz_submitted = False
                st.session_state.quiz_score = 0
                st.session_state.quiz_total = 0
                st.session_state.quiz_percentage = 0
                st.session_state.quiz_answers = []

                st.rerun()

            st.caption(timestamp)


# =========================================================
# HEADER
# =========================================================

# =========================
# HOMEPAGE HERO
# =========================

st.markdown(
    """
    <style>
    /* ===== HERO ===== */

    .snap-hero {
        position: relative;
        overflow: hidden;
        margin: 10px 0 35px 0;
        padding: 55px 35px 50px 35px;
        border-radius: 28px;
        text-align: center;
        background:
            radial-gradient(
                circle at 20% 20%,
                rgba(255,255,255,0.22),
                transparent 32%
            ),
            radial-gradient(
                circle at 80% 80%,
                rgba(167,139,250,0.30),
                transparent 35%
            ),
            linear-gradient(
                135deg,
                #5B4BDB 0%,
                #6D5CE7 45%,
                #7C5CFC 100%
            );
        box-shadow:
            0 18px 45px rgba(91, 75, 219, 0.22),
            inset 0 1px 0 rgba(255,255,255,0.25);
    }

    .snap-hero::before {
        content: "";
        position: absolute;
        width: 260px;
        height: 260px;
        border-radius: 50%;
        background: rgba(255,255,255,0.08);
        top: -120px;
        left: -80px;
    }

    .snap-hero::after {
        content: "";
        position: absolute;
        width: 220px;
        height: 220px;
        border-radius: 50%;
        background: rgba(255,255,255,0.07);
        bottom: -120px;
        right: -70px;
    }

    .snap-hero-content {
        position: relative;
        z-index: 2;
    }

    .snap-logo {
        font-size: 52px;
        font-weight: 800;
        letter-spacing: -1.5px;
        color: white;
        margin-bottom: 8px;
    }

    .snap-logo-ai {
        opacity: 0.9;
        font-weight: 500;
    }

    .snap-tagline {
        color: rgba(255,255,255,0.96);
        font-size: 24px;
        font-weight: 700;
        margin: 8px 0 15px 0;
    }

    .snap-description {
        max-width: 700px;
        margin: 0 auto;
        color: rgba(255,255,255,0.84);
        font-size: 16px;
        line-height: 1.7;
    }

    /* ===== FEATURE CARDS ===== */

    .feature-card {
        height: 100%;
        padding: 25px 22px;
        border-radius: 20px;
        background: white;
        border: 1px solid #E6E8F0;
        box-shadow:
            0 8px 25px rgba(16,24,40,0.06);
        text-align: center;
        transition: all 0.2s ease;
    }

    .feature-icon {
        width: 52px;
        height: 52px;
        margin: 0 auto 14px auto;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #F0EDFF;
        font-size: 26px;
    }

    .feature-title {
        color: #101828;
        font-size: 17px;
        font-weight: 750;
        margin-bottom: 7px;
    }

    .feature-text {
        color: #667085;
        font-size: 14px;
        line-height: 1.55;
    }

    /* ===== START SECTION ===== */

    .start-title {
        text-align: center;
        color: #101828;
        font-size: 25px;
        font-weight: 750;
        margin-top: 42px;
        margin-bottom: 5px;
    }

    .start-subtitle {
        text-align: center;
        color: #667085;
        font-size: 14px;
        margin-bottom: 18px;
    }

    @media (max-width: 700px) {
        .snap-hero {
            padding: 40px 22px;
            border-radius: 22px;
        }

        .snap-logo {
            font-size: 39px;
        }

        .snap-tagline {
            font-size: 20px;
        }

        .snap-description {
            font-size: 14px;
        }
    }
    </style>

    <div class="snap-hero">
        <div class="snap-hero-content">

            <div class="snap-logo">
                📚 Snap2Study
                <span class="snap-logo-ai">AI</span>
            </div>

            <div class="snap-tagline">
                Học thông minh hơn từ chính tài liệu của bạn
            </div>

            <div class="snap-description">
                Biến ảnh bài học thành
                <b>Tóm tắt + Flashcard + Quiz</b>
                bằng OCR và Gemini AI.
                <br>
                Học nhanh hơn. Ôn tập hiệu quả hơn.
            </div>

        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================
# FEATURES
# =========================

st.markdown(
    """
    <div style="
        text-align:center;
        margin-bottom:20px;
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
        <div class="feature-card">
            <div class="feature-icon">📷</div>

            <div class="feature-title">
                Nhận diện tài liệu
            </div>

            <div class="feature-text">
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
        <div class="feature-card">
            <div class="feature-icon">🃏</div>

            <div class="feature-title">
                Flashcard thông minh
            </div>

            <div class="feature-text">
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
        <div class="feature-card">
            <div class="feature-icon">❓</div>

            <div class="feature-title">
                Quiz kiểm tra
            </div>

            <div class="feature-text">
                Kiểm tra mức độ hiểu bài
                và tìm ra những phần cần ôn lại.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================
# START STUDY
# =========================

st.markdown(
    """
    <div class="start-title">
        🚀 Bắt đầu học
    </div>

    <div class="start-subtitle">
        Tải lên ảnh tài liệu của bạn để Snap2Study bắt đầu xử lý.
    </div>
    """,
    unsafe_allow_html=True
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


    # =====================================================
    # CREATE STUDY SET
    # =====================================================

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

            # =============================================
            # OCR PREVIEW
            # =============================================

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


                    # =====================================
                    # SAVE STUDY DATA
                    # =====================================

                    st.session_state.study_data = (
                        study_data
                    )


                    # =====================================
                    # RESET MAIN FLASHCARD
                    # =====================================

                    st.session_state.main_flashcard_index = 0
                    st.session_state.main_flashcard_flipped = False


                    # =====================================
                    # RESET REVIEW
                    # =====================================

                    st.session_state.review_cards = []

                    st.session_state.review_flashcard_index = 0
                    st.session_state.review_flashcard_flipped = False


                    # =====================================
                    # RESET QUIZ
                    # =====================================

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
