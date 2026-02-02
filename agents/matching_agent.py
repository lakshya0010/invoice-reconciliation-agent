import json
from schemas.state import ReconciliationState
from tools.matching_tools import supplier_similarity, item_similarity


def matching_agent(state: ReconciliationState) -> ReconciliationState:
    invoice = state["extracted_invoice"]

    with open("data/purchase_orders.json", "r") as f:
        po_db = json.load(f)

    po_list = po_db.get("purchase_orders", [])

    best_score = -1.0
    best_po = None
    explanation = ""

    for po in po_list:
        supplier_score = supplier_similarity(
            invoice.get("supplier_name", ""),
            po.get("supplier", "")
        )

        item_score = item_similarity(
            invoice.get("line_items", []),
            po.get("line_items", [])
        )

        final_score = round(
            0.6 * supplier_score + 0.4 * item_score,
            2
        )


        if final_score >= best_score:
            best_score = final_score
            best_po = po
            explanation = (
                f"Supplier similarity={supplier_score:.2f}, "
                f"Item similarity={item_score:.2f}"
            )

    state["matched_po"] = best_po
    state["po_match_confidence"] = max(best_score, 0.0)
    state["po_match_reasoning"] = explanation

    return state


