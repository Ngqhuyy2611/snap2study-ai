import os
import json

from dotenv import load_dotenv
from google import genai


load_dotenv()

# 1) Ưu tiên đọc từ biến môi trường / file .env (chạy local)
api_key = os.getenv("GEMINI_API_KEY")

# 2) Nếu không có, thử đọc từ st.secrets (khi chạy trên Streamlit Cloud,
#    Secrets không phải lúc nào cũng tự inject vào os.environ)
if not api_key:
    try:
        import streamlit as st
        api_key = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        # Không chạy trong môi trường Streamlit (vd: test_ai.py, main.py chạy local)
        # hoặc chưa cấu hình secrets.toml -> bỏ qua, để rơi xuống lỗi bên dưới.
        pass

if not api_key:
    raise ValueError(
        "Không tìm thấy GEMINI_API_KEY. "
        "Chạy local: kiểm tra file .env có dòng GEMINI_API_KEY=... "
        "Chạy trên Streamlit Cloud: kiểm tra Manage app → Settings → Secrets."
    )

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_study_material(text, number_of_cards=5):

    prompt = f"""
Bạn là Snap2Study AI, một trợ lý học tập dành cho học sinh THPT.

Hãy đọc tài liệu dưới đây và tạo một bộ ôn tập.

YÊU CẦU:

1. Xác định chủ đề chính.
2. Tạo một phần tóm tắt ngắn, dễ hiểu.
3. Tạo {number_of_cards} flashcard.
4. Mỗi flashcard gồm:
   - question
   - answer
   - difficulty
5. Tạo 5 câu hỏi trắc nghiệm.
6. Mỗi câu có 4 lựa chọn A, B, C, D.
7. Chỉ sử dụng kiến thức có trong tài liệu.
8. Không tự bịa thêm kiến thức.
9. Nội dung phù hợp với học sinh THPT.

CHỈ TRẢ VỀ JSON.

Cấu trúc JSON:

{{
    "topic": "Tên chủ đề",

    "summary": "Tóm tắt ngắn gọn nội dung",

    "flashcards": [
        {{
            "question": "Câu hỏi",
            "answer": "Câu trả lời",
            "difficulty": "Dễ"
        }}
    ],

    "quiz": [
        {{
            "question": "Câu hỏi trắc nghiệm",
            "options": [
                "A. Đáp án A",
                "B. Đáp án B",
                "C. Đáp án C",
                "D. Đáp án D"
            ],
            "answer": "A"
        }}
    ]
}}

TÀI LIỆU:

{text}
"""

    # LƯU Ý: "gemini-3.6-flash" không phải tên model chuẩn của Gemini API.
    # Hãy chạy list_models.py để lấy danh sách model thật sự khả dụng
    # với API key của bạn (vd: "gemini-2.0-flash", "gemini-1.5-flash", ...)
    # rồi thay giá trị bên dưới cho đúng.
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    result = response.text.strip()

    # Loại bỏ markdown nếu Gemini trả về ```json
    if result.startswith("```json"):
        result = result[7:]

    if result.startswith("```"):
        result = result[3:]

    if result.endswith("```"):
        result = result[:-3]

    result = result.strip()

    try:
        return json.loads(result)

    except json.JSONDecodeError:
        raise ValueError(
            "Gemini không trả về JSON hợp lệ.\n\n"
            f"Kết quả Gemini trả về:\n{result}"
        )
