import os
import json

from dotenv import load_dotenv
from google import genai


# =========================================================
# SETUP
# =========================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "Không tìm thấy GEMINI_API_KEY"
    )

client = genai.Client(
    api_key=api_key
)


# =========================================================
# GENERATE STUDY MATERIAL
# =========================================================

def generate_study_material(
    text,
    number_of_cards=5
):

    prompt = f"""
Bạn là Snap2Study AI, một trợ lý học tập
dành cho học sinh THPT.

Hãy đọc tài liệu dưới đây và tạo một bộ ôn tập.

YÊU CẦU:

1. Xác định chủ đề chính.

2. Tạo một phần tóm tắt ngắn,
dễ hiểu và chỉ dựa trên tài liệu.

3. Tạo {number_of_cards} Flashcard.

Mỗi Flashcard gồm:

- question
- answer
- difficulty

4. Tạo 5 câu hỏi trắc nghiệm.

Mỗi câu hỏi gồm:

- question
- options: đúng 4 lựa chọn A, B, C, D
- answer: chỉ ghi chữ cái A, B, C hoặc D
- correct_answer: ghi đầy đủ nội dung đáp án đúng

5. Chỉ sử dụng kiến thức có trong tài liệu.

6. Không tự bịa thêm kiến thức.

7. Nếu tài liệu không đủ thông tin,
hãy tạo ít nội dung hơn thay vì bịa.

8. Nội dung phải phù hợp với học sinh THPT.

9. Câu hỏi nên kiểm tra kiến thức quan trọng
thay vì hỏi những chi tiết không cần thiết.

CHỈ TRẢ VỀ JSON.

Cấu trúc JSON bắt buộc:

{{
    "topic": "Tên chủ đề",

    "summary": "Tóm tắt bài học",

    "flashcards": [
        {{
            "question": "Câu hỏi",
            "answer": "Câu trả lời",
            "difficulty": "Dễ"
        }}
    ],

    "quiz": [
        {{
            "question": "Câu hỏi",
            "options": [
                "A. Đáp án A",
                "B. Đáp án B",
                "C. Đáp án C",
                "D. Đáp án D"
            ],
            "answer": "A",
            "correct_answer": "Nội dung đầy đủ của đáp án đúng"
        }}
    ]
}}

TÀI LIỆU:

{text}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    result = response.text.strip()


    # =====================================================
    # REMOVE MARKDOWN CODE BLOCK
    # =====================================================

    if result.startswith("```json"):
        result = result[7:]

    elif result.startswith("```"):
        result = result[3:]

    if result.endswith("```"):
        result = result[:-3]


    # =====================================================
    # PARSE JSON
    # =====================================================

    return json.loads(
        result.strip()
    )
