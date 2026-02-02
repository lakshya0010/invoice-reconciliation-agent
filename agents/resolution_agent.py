from schemas.state import ReconciliationState

def resolution_agent(state:ReconciliationState)-> ReconciliationState:
    po_conf = state.get("po_match_confidence", 0.0)
    discrepancies = state.get("discrepancies",[])
    disc_conf = state.get("discrepancy_confidence",0.0)

    # If PO reference was missing but match was inferred
    if (
        state["extracted_invoice"].get("po_reference") in [None, "", "N/A"]
        and state.get("po_match_confidence", 0.0) >= 0.8
    ):
        state["final_decision"] = "REVIEW"
        state["decision_reasoning"] = (
            "Invoice matched a purchase order using fuzzy supplier and item similarity, "
            "but no explicit PO reference was found. Human review recommended."
        )
        return state


    if po_conf>=0.85 and not discrepancies:
        decision = "AUTO_APPROVE"
        reasoning = (
            "Invoice matched a purchase order with high confidence "
            "and no discrepancies were detected."
        )

    elif disc_conf >= 0.7:
        decision = "ESCALATE"
        reasoning = (
            "High-confidence discrepancies were detected that require "
            "manual review or supplier clarification."
        )

    else:
        decision = "REVIEW"
        reasoning = (
            "Invoice matched a purchase order, but minor discrepancies "
            "or moderate uncertainty require human review."
        )

    state["final_decision"] = decision
    state["decision_reasoning"] = reasoning

    return state
