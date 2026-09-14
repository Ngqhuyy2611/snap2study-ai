from PIL import Image
from ocr import extract_text
from ai import generate_study_material


def main():
    # Thay tên ảnh của bạn vào đây
    image_path = "test.jpg"          # hoặc "page-2.png"...

    print("1. Đang OCR ảnh...")
    image = Image.open(image_path)
    text = extract_text(image)
    print("===== VĂN BẢN OCR =====")
    print(text)
    print("\n" + "="*50 + "\n")

    print("2. Đang tạo Flashcard bằng Gemini...")
    study_material = generate_study_material(text)
    print("===== FLASHCARD =====")
    print(study_material["flashcards"])

if __name__ == "__main__":
    main()