def field_completeness_score(extracted: dict)->float:
    """Measures how many fields present."""
    expected_fields = [
        "invoice_number",
        "invoice_date",
        "supplier_name",
        "line_items",
        "total"
    ]
    present = 0
    for field in expected_fields:
        value = extracted.get(field)
        if value not in [None, "", []]:
            present+=1
    return present/len(expected_fields)



def numeric_consistency_score(extracted: dict)->float:
    """Check internal numeric consistency of invoice"""
    checks = 0
    passes = 0
    line_items = extracted.get("line_items", [])

    for item in line_items:
        qty = item.get("quantity")
        unit = item.get("unit_price")
        total = item.get("line_total")

        if qty is not None and unit is not None and total is not None:
            checks+=1
            expected = qty*unit

            if abs(expected-total) <= 0.02*max(total,1):
                passes+=1
    
    if checks == 0:
        return 0.5
    return passes/checks


Method_confidence = {
    "pdf_text":0.95,
    "ocr":0.75,
    "vision_llm":0.85
}
def method_reliability_score(method: str)->float:
    return Method_confidence.get(method, 0.6)



def compute_extraction_confidence(
        extracted: dict,
        extraction_method: str,
        llm_confidence: float | None = None
) -> tuple[float,dict]:
    "Returns final score"

    completeness = field_completeness_score(extracted)
    numeric = numeric_consistency_score(extracted)
    method = method_reliability_score(extraction_method)
    llm = llm_confidence if llm_confidence is not None else 0.7

    final = round(
        0.35*completeness+
        0.30*numeric+
        0.20*method+
        0.15*llm,
        2
    )

    explaination = {
        "field_completeness": round(completeness, 2),
        "numeric_consistency": round(numeric, 2),
        "method_reliability": round(method, 2),
        "llm_confidence": round(llm, 2)
    }
    
    return final,explaination


