import os
import shutil

import pytesseract

from PIL import (
    Image,
    ImageEnhance,
    ImageFilter,
    ImageOps
)


# =========================================================
# TESSERACT PATH
# =========================================================

WINDOWS_TESSERACT_PATH = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

if (
    os.name == "nt"
    and os.path.exists(WINDOWS_TESSERACT_PATH)
):

    pytesseract.pytesseract.tesseract_cmd = (
        WINDOWS_TESSERACT_PATH
    )

elif shutil.which("tesseract"):

    pytesseract.pytesseract.tesseract_cmd = (
        shutil.which("tesseract")
    )


# =========================================================
# IMAGE PREPROCESSING
# =========================================================

def preprocess_image(image):

    image = image.convert("L")

    enhancer = ImageEnhance.Contrast(image)

    image = enhancer.enhance(2.5)

    image = image.filter(
        ImageFilter.SHARPEN
    )

    image = ImageOps.autocontrast(
        image
    )

    return image


# =========================================================
# OCR
# =========================================================

def extract_text(image):

    if (
        isinstance(image, (str, bytes))
        or hasattr(image, "read")
    ):

        image = Image.open(image)

    image = preprocess_image(image)

    custom_config = (
        r"--oem 3 --psm 6"
    )

    text = pytesseract.image_to_string(
        image,
        lang="vie+eng",
        config=custom_config
    )

    return text.strip()
