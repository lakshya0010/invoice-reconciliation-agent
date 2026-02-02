from rapidfuzz import fuzz

def supplier_similarity(a:str, b:str)->float:
    return fuzz.token_sort_ratio(a,b)/100

def item_similarity(invoice_items, po_items)->float:
    if not invoice_items or not po_items:
        return 0.0
    
    matches = 0
    for inv in invoice_items or not po_items:
        for po in po_items:
            if fuzz.partial_ratio(inv["description"], po["description"])>80:
                matches+=1
                break

    return matches/max(len(invoice_items),1)