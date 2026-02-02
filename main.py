import os
from agents.document_agent import document_agent
from schemas.state import ReconciliationState
from graphs.reconsiliation_graph import app
import json

def load_invoice(path:str)->bytes:
    abs_path = os.path.abspath(path)
    with open(abs_path, "rb") as f:
        data = f.read()
        return data
    

    
if __name__ == "__main__":
    raw_invoice = load_invoice("data/Invoice_4_Price_Trap.pdf")

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

    state = app.invoke(state)

    print("\n=== FINAL DECISION ===")
    print(state["final_decision"])
    print(state["decision_reasoning"])

    print("\n=== DISCREPANCIES ===")
    for d in state["discrepancies"]:
        print(d)


    print("\n=== FINAL OUTPUT (JSON) ===")
    print(json.dumps(state, indent=2))

