"""Explainable retail assortment scoring."""
FIELDS = ("units_sold", "gross_margin_pct", "inventory_units")
WEIGHTS = {"units_sold": .5, "gross_margin_pct": .3, "inventory_units": .2}

def score_assortment_candidates(products):
    if not isinstance(products, list) or not products:
        raise ValueError("products must be a non-empty list")
    seen=set(); clean=[]
    for p in products:
        if not isinstance(p, dict) or str(p.get("product_id", "")).strip() == "":
            raise ValueError("Each product needs a product_id")
        p=dict(p); pid=str(p["product_id"])
        if pid in seen: raise ValueError(f"Duplicate product_id: {pid}")
        seen.add(pid); p["product_id"]=pid
        p.setdefault("name", pid); p.setdefault("category", "Uncategorized")
        if not isinstance(p["name"], str) or not isinstance(p["category"], str): raise ValueError("name and category must be strings")
        for f in FIELDS:
            v=p.get(f)
            if v is not None and (isinstance(v, bool) or not isinstance(v,(int,float)) or v<0): raise ValueError(f"{f} must be a non-negative number")
            if f=="gross_margin_pct" and v is not None and v>100: raise ValueError("gross_margin_pct must be between 0 and 100")
        clean.append(p)
    ranges={}
    for f in FIELDS:
        vals=[p[f] for p in clean if p.get(f) is not None]
        ranges[f]=(min(vals),max(vals)) if vals else (None,None)
    result=[]
    for p in clean:
        comps={}; missing=[]; total=0
        for f in FIELDS:
            v=p.get(f); lo,hi=ranges[f]
            if v is None: missing.append(f); norm=.5
            elif lo is None or lo==hi: norm=.5
            else: norm=(v-lo)/(hi-lo)
            comps[f]=round(norm*100,2); total+=norm*WEIGHTS[f]
        result.append({"product_id":p["product_id"],"name":p["name"],"category":p["category"],"score":round(total*100,2),"component_scores":comps,"missing_fields":missing,"reason":"Relative weighted score: sales 50%, margin 30%, inventory 20%."})
    return sorted(result,key=lambda x:-x["score"])

def recommend_assortment(products, limit, category_minimums=None):
    if isinstance(limit,bool) or not isinstance(limit,int) or limit<1: raise ValueError("limit must be a positive integer")
    scored=score_assortment_candidates(products); mins=category_minimums or {}
    if not isinstance(mins,dict): raise ValueError("category_minimums must be an object")
    for cat,n in mins.items():
        if not isinstance(cat,str) or isinstance(n,bool) or not isinstance(n,int) or n<0: raise ValueError("category minimums must map strings to non-negative integers")
    selected=[]; ids=set(); unmet={}
    for cat,n in mins.items():
        available=[x for x in scored if x["category"]==cat]
        for item in available[:n]:
            if item["product_id"] not in ids and len(selected)<limit: selected.append(item); ids.add(item["product_id"])
        if len([x for x in selected if x["category"]==cat])<n: unmet[cat]=n
    for item in scored:
        if len(selected)>=limit: break
        if item["product_id"] not in ids: selected.append(item); ids.add(item["product_id"])
    selected.sort(key=lambda x:-x["score"])
    return {"assortment":selected,"requested_limit":limit,"selected_count":len(selected),"unmet_category_minimums":unmet,"scoring_weights":WEIGHTS,"human_review_required":True,"note":"Scores are relative heuristics, not sales forecasts. Human review is required."}

def explain_assortment_plan(result):
    if not isinstance(result,dict) or not isinstance(result.get("assortment"),list): raise ValueError("result must contain an assortment list")
    picks="; ".join(f'{x.get("name",x["product_id"])} ({x.get("score")}/100)' for x in result["assortment"]) or "No products selected"
    msg=f"Selected {result.get('selected_count',len(result['assortment']))} products: {picks}."
    if result.get("unmet_category_minimums"): msg+=f" Unmet category minimums: {result['unmet_category_minimums']}."
    return msg+" Human merchandising review is required."
