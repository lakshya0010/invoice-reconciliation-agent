import os
from agents.document_agent import document_agent
from schemas.state import ReconciliationState

def load_invoice(path:str)->bytes:
    abs_path = os.path.abspath(path)
    print("Loading invoice from:", abs_path)
    with open(abs_path, "rb") as f:
        data = f.read()
        print("Loaded bytes:", len(data))
        return data
    

    
if __name__ == "__main__":
    raw_invoice = load_invoice("data/Invoice_1_Baseline.pdf")

    state: ReconciliationState = {
        "invoice_id" : "invoice_1",
        "raw_document" : raw_invoice,

        "extracted_invoice":{},
        "extracted_confidence":0.0,
        "extracted_confidence_breakdown":{},
        "extraction_method":"",

        "matched_po":None,
        "po_match_confidence":0.0,
        "po_match_reasoning":{},

        "discrepancies":[],
        "discrepancy_confidence":0.0,

        "decision_reasoning": "",
        "final_decision":""
    }

    state = document_agent(state)

    print("\n--- EXTRACTION RESULT ---")
    print(state["extracted_invoice"])

    print("\n--- CONFIDENCE ---")
    print(state["extracted_confidence"])
    print(state["extracted_confidence_breakdown"])
    print("Method:", state["extraction_method"])