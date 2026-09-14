import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

image = Image.open("test.jpg")

text = pytesseract.image_to_string(
    image,
    lang="vie+eng+ods"
)

print("===== KẾT QUẢ OCR =====")
print(text)