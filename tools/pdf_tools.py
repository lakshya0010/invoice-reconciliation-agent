import pdfplumber
from io import BytesIO

def extract_text_from_pdf(pdf_bytes:bytes)->str|None:
    """Attempts pdf extraction, returns None if fails"""

    try:
        text_chunks = []

        with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_chunks.append(page_text)
        
        fulltext = "\n".join(text_chunks)

        if len(fulltext)<20:
            return None
        return fulltext
    except Exception as e:
        return None

