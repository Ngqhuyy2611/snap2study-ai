from ai import generate_study_material

print("Bắt đầu gọi Gemini...")

text = """
Công thức động năng: Wđ = (1/2)mv²
Công thức thế năng trọng trường: Wt = mgh
Định luật bảo toàn cơ năng: Wđ + Wt = không đổi
"""

try:
    print("Đang gửi yêu cầu...")
    study_material = generate_study_material(text)
    print("===== FLASHCARD =====")
    print(study_material["flashcards"])
except Exception as e:
    print("Lỗi xảy ra:")
    print(e)