from utils.json_util import extract_json
import json
from dotenv import load_dotenv
from schemas.state import ReconciliationState
from utils.confidence import compute_extraction_confidence
from tools.pdf_tools import extract_text_from_pdf
from tools.ocr_tools import extract_text_with_ocr
from langchain_groq import ChatGroq

load_dotenv()
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)


EXTRACTION_PROMPT = """
You are a Document Intelligence Agent.

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

def document_agent(state : ReconciliationState)->ReconciliationState:
    raw_doc = state["raw_document"]

    #Progressive Extraction
    text = extract_text_from_pdf(raw_doc)
    extraction_method = "pdf_text"

    if text is None or len(text.strip())==0:
        text = extract_text_with_ocr(raw_doc)
        extraction_method = "ocr"

    
    response = llm.invoke(
        EXTRACTION_PROMPT + "\n\nInvoice Text:\n" + text
        )
    

    #parsing
    try:
        content = response.content

        parsed = extract_json(content)

        if not isinstance(parsed, dict):
            raise ValueError("Parsed JSON is not a dict")
    except Exception:
        parsed = {
            "invoice_data": "",
            "llm_confidence": 0.3
        }
    
    extracted_invoice = parsed.get("invoice_data", {})
    llm_confidence = parsed.get("llm_confidence", 0.7)
    if not isinstance(extracted_invoice, dict):
        extracted_invoice = {}

    final_confidence, confidence_breakdown = compute_extraction_confidence(
        extracted=extracted_invoice,
        extraction_method=extraction_method,
        llm_confidence=llm_confidence
    )

    state["extracted_confidence"] = final_confidence
    state["extracted_invoice"] = extracted_invoice
    state["extracted_confidence_breakdown"] = confidence_breakdown
    state["extraction_method"] = extraction_method

    return state

