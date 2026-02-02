from schemas.state import ReconciliationState
from rapidfuzz import fuzz


def discrepency_agent(state: ReconciliationState) -> ReconciliationState:
    invoice = state.get("extracted_invoice")
    po = state.get("matched_po")

    discrepancies = []
    price_deltas = []

    # --- Safety ---
    if not invoice or not po:
        state["discrepancies"] = []
        state["discrepancy_confidence"] = 0.0
        return state

    invoice_items = invoice.get("line_items", [])
    po_items = po.get("line_items", [])

    # --- Compute price deltas ---
    for inv_item in invoice_items:
        inv_desc = inv_item.get("description", "")
        inv_price = inv_item.get("unit_price")

        for po_item in po_items:
            po_desc = po_item.get("description", "")
            po_price = po_item.get("unit_price")

            similarity = fuzz.partial_ratio(inv_desc.lower(), po_desc.lower())

            if similarity >= 80 and inv_price and po_price:
                delta = (inv_price - po_price) / po_price
                price_deltas.append(delta)

                # Individual price mismatch
                if delta >= 0.05:
                    discrepancies.append({
                        "type": "PRICE_MISMATCH",
                        "severity": "MEDIUM",
                        "confidence": round(min(delta * 1.5, 1.0), 2),
                        "explanation": (
                            f"Unit price for '{inv_desc}' is "
                            f"{delta*100:.1f}% higher than PO"
                        )
                    })

                break  # stop after best match


    # --- SYSTEMATIC PRICE INCREASE ---
    if len(price_deltas) >= 2:
        avg_delta = sum(price_deltas) / len(price_deltas)
        high_count = sum(1 for d in price_deltas if d >= 0.08)

        if high_count >= 2 and avg_delta >= 0.08:
            discrepancies.append({
                "type": "SYSTEMATIC_PRICE_INCREASE",
                "severity": "HIGH",
                "confidence": round(min(avg_delta * 1.5, 1.0), 2),
                "explanation": (
                    f"{high_count} line items show a consistent "
                    f"{avg_delta*100:.1f}% unit price increase "
                    f"compared to the purchase order"
                )
            })
    # --- TOTAL AMOUNT DISCREPANCY (Invoice 4 real pattern) ---
    inv_total = invoice.get("total")
    po_total = po.get("total")

    if inv_total and po_total:
        total_delta = (inv_total - po_total) / po_total

    if total_delta >= 0.08:
        discrepancies.append({
            "type": "TOTAL_PRICE_INCREASE",
            "severity": "HIGH",
            "confidence": round(min(total_delta * 1.2, 1.0), 2),
            "explanation": (
                f"Invoice total is {total_delta*100:.1f}% higher than "
                f"the purchase order total, indicating a hidden price increase"
            )
        })


    # --- Confidence ---
    discrepancy_confidence = (
        max(d["confidence"] for d in discrepancies)
        if discrepancies else 0.0
    )

    state["discrepancies"] = discrepancies
    state["discrepancy_confidence"] = discrepancy_confidence

    return state
