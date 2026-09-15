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
        "Không tìm thấy GEMINI_API_KEY. "
        "Hãy kiểm tra file .env hoặc Streamlit Secrets."
    )


client = genai.Client(
    api_key=api_key
)


# =========================================================
# GENERATE STUDY MATERIAL
# =========================================================

def generate_study_material(
    text,
    number_of_cards=5,
    number_of_quiz=5
):

    if not text or not text.strip():

        raise ValueError(
            "Nội dung tài liệu đang trống."
        )


    prompt = f"""
Bạn là Snap2Study AI,
một trợ lý học tập dành cho học sinh THPT.

NHIỆM VỤ:

Đọc tài liệu được cung cấp và tạo
một bộ ôn tập dựa CHỈ trên tài liệu đó.


YÊU CẦU:

1. Xác định chủ đề chính.

2. Tạo một phần tóm tắt ngắn,
rõ ràng và dễ hiểu.

3. Tạo tối đa {number_of_cards} Flashcard.

Mỗi Flashcard gồm:

- question
- answer
- difficulty

Difficulty chỉ được dùng:

"Dễ"
"Trung bình"
"Khó"


4. Tạo tối đa {number_of_quiz} câu hỏi trắc nghiệm.

Mỗi câu gồm:

- question
- options
- answer
- correct_answer


Options phải có đúng 4 lựa chọn:

A.
B.
C.
D.


answer phải CHỈ là một chữ:

A
B
C
hoặc D


correct_answer phải là nội dung đầy đủ
của đáp án đúng.


5. Chỉ sử dụng thông tin có trong tài liệu.

6. Không được tự bịa kiến thức.

7. Nếu tài liệu không đủ thông tin,
có thể tạo ít Flashcard hoặc Quiz hơn.

8. Ưu tiên kiến thức quan trọng.

9. Nội dung phù hợp học sinh THPT.

10. Không tạo câu hỏi có nhiều đáp án đúng.


CHỈ TRẢ VỀ JSON.

KHÔNG viết giải thích.

KHÔNG dùng Markdown.

CẤU TRÚC:

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

            "correct_answer": "Nội dung đầy đủ"
        }}
    ]
}}


TÀI LIỆU:

{text}
"""


    # =====================================================
    # CALL GEMINI
    # =====================================================

    response = client.models.generate_content(

        model="gemini-3.6-flash",

        contents=prompt
    )


    if not response.text:

        raise ValueError(
            "Gemini không trả về nội dung."
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


    result = result.strip()


    # =====================================================
    # PARSE JSON
    # =====================================================

    try:

        data = json.loads(result)

    except json.JSONDecodeError as e:

        raise ValueError(
            "AI trả về dữ liệu không đúng JSON. "
            f"Chi tiết: {e}"
        )


    # =====================================================
    # BASIC VALIDATION
    # =====================================================

    if not isinstance(data, dict):

        raise ValueError(
            "Dữ liệu AI trả về không hợp lệ."
        )


    if "flashcards" not in data:

        data["flashcards"] = []


    if "quiz" not in data:

        data["quiz"] = []


    if "summary" not in data:

        data["summary"] = (
            "Không có phần tóm tắt."
        )


    if "topic" not in data:

        data["topic"] = "Bài học mới"


    return data
