import pytesseract
from PIL import Image
from pdf2image import convert_from_bytes

POPPLER_PATH = r"C:\poppler\Library\bin"
def extract_text_with_ocr(file_bytes:bytes)->str|None:
    """Performs ocr on pdf or image, returns none if fails"""

    try:
        images = convert_from_bytes(file_bytes)
        text_chunks = []

        for img in images:
            text = pytesseract.image_to_string(img)
            if text:
                text_chunks.append(text)
        
        full_text = "\n".join(text_chunks)

        if len(full_text.strip())<20:
            return None
        return full_text
    except Exception as e:
        return None
    