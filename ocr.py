import os
import shutil
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

# Đường dẫn Tesseract
# Trên Windows cần chỉ rõ đường dẫn cài đặt.
# Trên Linux/macOS (vd: Streamlit Cloud) thường tesseract đã có sẵn trong PATH,
# nên không cần set tesseract_cmd thủ công -> tự dò để tránh lỗi khi deploy.
_windows_tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

if os.name == "nt" and os.path.exists(_windows_tesseract_path):
    pytesseract.pytesseract.tesseract_cmd = _windows_tesseract_path
elif shutil.which("tesseract"):
    pytesseract.pytesseract.tesseract_cmd = shutil.which("tesseract")


def preprocess_image(image):
    # Chuyển sang đen trắng
    image = image.convert("L")
    
    # Tăng độ tương phản mạnh
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.5)
    
    # Làm nét
    image = image.filter(ImageFilter.SHARPEN)
    
    # Tự động điều chỉnh độ sáng
    image = ImageOps.autocontrast(image)
    
    return image

def extract_text(image):
    """
    Nhận vào một đối tượng PIL.Image (đã được mở sẵn ở nơi gọi hàm),
    KHÔNG phải đường dẫn file. Nếu lỡ truyền vào đường dẫn (str),
    hàm vẫn tự động mở giúp để tránh lỗi.
    """
    if isinstance(image, (str, bytes)) or hasattr(image, "read"):
        image = Image.open(image)

    image = preprocess_image(image)
    
    # Cấu hình tốt hơn cho công thức
    custom_config = r'--oem 3 --psm 6'
    
    text = pytesseract.image_to_string(
        image,
        lang="vie+eng",
        config=custom_config
    )
    return text.strip()