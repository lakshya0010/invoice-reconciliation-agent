from typing import TypedDict, List, Optional

class ReconciliationState(TypedDict):
    invoice_id : str
    raw_document : bytes

    extracted_invoice : dict
    extracted_confidence : float

    matched_po : Optional[dict]
    po_match_confidence : float
    po_match_reasoning : str

    discrepancies : List[dict]
    discrepancy_confidence : float

    final_decision : str
    decision_reasoning : str