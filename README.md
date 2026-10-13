# Retail Assortment Planning Agent

An offline, explainable starter agent that ranks candidate retail products using supplied sales, gross margin, and inventory data, then recommends a requested assortment size.

## Quick start
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m pytest -q
python3 -m core.cli examples/products.json --limit 4
```

## Input fields
Each product may contain `product_id`, `name`, `category`, `units_sold`, `gross_margin_pct`, and `inventory_units`. Numeric values must be non-negative; margin must be 0–100.

## Scoring
Within the supplied batch, each numeric metric is min-max normalized. The score weights are sales 50%, gross margin 30%, and inventory 20%, scaled to 0–100. Equal-valued columns use 0.5. Missing metrics also use a 0.5 component and are disclosed. Scores are relative heuristics, not forecasts.

## Limits
This prototype does not model seasonality, price elasticity, supplier lead times, shelf capacity, cannibalization, or regional preferences. It does not connect to POS/ERP systems or update inventory. Human merchandisers should review the recommendations before acting.
