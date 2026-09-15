import os
import json
import time

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

client = genai.Client(api_key=api_key)


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
Bạn là Snap2Study AI, một trợ lý học tập dành cho học sinh THPT.

Hãy đọc tài liệu dưới đây và tạo một bộ ôn tập.

YÊU CẦU:

1. Xác định chủ đề chính.

2. Tạo một phần tóm tắt ngắn, rõ ràng, dễ hiểu.

3. Tạo tối đa {number_of_cards} Flashcard.

Mỗi Flashcard gồm:
- question
- answer
- difficulty

4. Tạo tối đa {number_of_quiz} câu hỏi trắc nghiệm.

Mỗi câu gồm:
- question
- options: đúng 4 lựa chọn
- answer: chỉ ghi A, B, C hoặc D
- correct_answer: ghi đầy đủ nội dung đáp án đúng

5. CHỈ sử dụng kiến thức xuất hiện trong tài liệu.

6. Không tự bịa thêm kiến thức.

7. Nếu tài liệu không đủ thông tin, hãy tạo ít câu hỏi hơn thay vì bịa.

8. Nội dung phù hợp với học sinh THPT.

9. Ưu tiên những kiến thức quan trọng.

10. Trả về JSON hợp lệ.

CẤU TRÚC JSON:

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

CHỈ TRẢ VỀ JSON.

TÀI LIỆU:
{text}
"""

    # =====================================================
    # RETRY KHI GEMINI QUÁ TẢI
    # =====================================================

    max_attempts = 3

    for attempt in range(max_attempts):

        try:

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            if not response.text:
                raise ValueError(
                    "Gemini không trả về nội dung."
                )

            result = response.text.strip()

            # Loại bỏ markdown code block nếu có
            if result.startswith("```json"):
                result = result[7:]

            elif result.startswith("```"):
                result = result[3:]

            if result.endswith("```"):
                result = result[:-3]

            result = result.strip()

            # Parse JSON
            data = json.loads(result)

            if not isinstance(data, dict):
                raise ValueError(
                    "Dữ liệu AI trả về không hợp lệ."
                )

            # Đảm bảo luôn có các key cần thiết
            data.setdefault(
                "topic",
                "Bài học mới"
            )

            data.setdefault(
                "summary",
                "Không có phần tóm tắt."
            )

            data.setdefault(
                "flashcards",
                []
            )

            data.setdefault(
                "quiz",
                []
            )

            return data

        except Exception as e:

            error_text = str(e)

            # Gemini 503 = server đang quá tải
            if (
                "503" in error_text
                or "UNAVAILABLE" in error_text
                or "high demand" in error_text.lower()
            ):

                if attempt < max_attempts - 1:

                    time.sleep(4)

                    continue

                raise RuntimeError(
                    "Gemini đang quá tải. "
                    "Bạn hãy thử tạo lại sau vài giây."
                )

            # Lỗi JSON
            if isinstance(e, json.JSONDecodeError):

                raise ValueError(
                    "AI trả về dữ liệu không đúng định dạng JSON."
                )

            raise
