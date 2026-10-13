import pytest
from core.scoring import score_assortment_candidates, recommend_assortment, explain_assortment_plan
P=[{"product_id":"a","name":"A","category":"X","units_sold":100,"gross_margin_pct":20,"inventory_units":10},{"product_id":"b","name":"B","category":"Y","units_sold":200,"gross_margin_pct":40,"inventory_units":20},{"product_id":"c","name":"C","category":"X","units_sold":150,"gross_margin_pct":30,"inventory_units":15}]
def test_scores_sorted():
 r=score_assortment_candidates(P); assert r[0]["product_id"]=="b" and r[0]["score"]>r[-1]["score"]
def test_missing_fields_disclosed():
 r=score_assortment_candidates([{"product_id":"a"}])[0]; assert len(r["missing_fields"])==3 and r["score"]==50
def test_limit_respected(): assert recommend_assortment(P,2)["selected_count"]==2
def test_category_minimums_met():
 r=recommend_assortment(P,2,{"X":2}); assert sum(x["category"]=="X" for x in r["assortment"])==2 and not r["unmet_category_minimums"]
def test_unmet_minimum_reported(): assert recommend_assortment(P,1,{"X":2})["unmet_category_minimums"]=={"X":2}
def test_duplicate_ids_rejected():
 with pytest.raises(ValueError): score_assortment_candidates([P[0],P[0]])
def test_invalid_margin_rejected():
 with pytest.raises(ValueError): score_assortment_candidates([dict(P[0],gross_margin_pct=101)])
def test_explanation_calls_for_review(): assert "Human merchandising review" in explain_assortment_plan(recommend_assortment(P,2))
