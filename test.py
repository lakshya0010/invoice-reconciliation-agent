from tools.ocr_tools import extract_text_with_ocr

with open("data/Invoice_1_Baseline.pdf", "rb") as f:
    raw = f.read()

text = extract_text_with_ocr(raw)

print("OCR TEXT:")
print(text[:1000] if text else "NO OCR TEXT")
