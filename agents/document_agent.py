import json
from schemas.state import ReconciliationState
from utils.confidence import compute_extraction_confidence
from tools.pdf_tools import extract_text_from_pdf
from tools.ocr_tools import extract_text_with_ocr


def document_agent(state : ReconciliationState):
    """
    Docstring for document_agent
    
    :param state: Description
    :type state: ReconciliationState

    1. Extracts text using PDF tools
    2. If low confidence use OCR
    3. Parse fields using LLM
    4. Return updated state
    """

"""You are a Document Intelligence Agent.

Extract structured invoice data from the provided text.
The text may be noisy, OCR-derived, incomplete, or poorly formatted.

Rules:
- Do NOT hallucinate missing values
- Use null if a field is absent
- Preserve original item descriptions
- Normalize all numbers

After extraction:
- Estimate your confidence (0.0–1.0) that the extracted data is accurate,
  based on clarity of text, completeness, and ambiguity.

Return ONLY valid JSON in this format:

{
  "invoice_data": {
    "invoice_number": string | null,
    "invoice_date": string | null,
    "supplier_name": string | null,
    "po_reference": string | null,
    "line_items": [
      {
        "description": string,
        "quantity": number | null,
        "unit_price": number | null,
        "line_total": number | null
      }
    ],
    "subtotal": number | null,
    "tax": number | null,
    "total": number | null
  },
  "llm_confidence": number
}
"""