# Explainability

## Inputs
The agent reads product IDs, names, categories, units sold, gross margin percentage, and inventory units supplied by the operator. Missing numeric fields are disclosed and receive a midpoint normalized component.

## Decision
Numeric features are min-max normalized within the candidate batch. The score weights are sales 50%, gross margin 30%, and inventory 20%, scaled to 0–100. Products are selected by score while attempting requested category minimums. This is a relative heuristic, not a future-sales forecast.

## Limits
The agent does not model seasonality, price elasticity, lead times, shelf capacity, cannibalization, or regional preferences, and has no live retail integrations. Human review is required.

## Tool: score-assortment-candidates
### Inputs and Data Sources
A list of product records supplied by the operator.
### Decision and Reasoning
Validates records, normalizes supplied metrics within the batch, and applies documented weights.
### Outputs and Evidence
Returns scores, component scores, and missing fields.
### Limits and Constraints
Scores are relative to the supplied batch and are not forecasts.
### Failure Handling
Raises a clear ValueError for malformed records or invalid numeric values.
### Human Review
Verify the data and candidate-set representativeness.

## Tool: recommend-assortment
### Inputs and Data Sources
Product records, desired assortment size, and optional category minimums.
### Decision and Reasoning
Attempts category minimums, then fills remaining slots by descending score without duplicate products.
### Outputs and Evidence
Returns selected products and unmet category minimums.
### Limits and Constraints
Cannot satisfy infeasible constraints or account for unprovided business factors.
### Failure Handling
Rejects invalid sizes, minimums, and duplicate IDs.
### Human Review
Review the assortment before operational changes.

## Tool: explain-assortment-plan
### Inputs and Data Sources
A recommendation result from the local planner.
### Decision and Reasoning
Summarizes the selected products and constraints without adding facts.
### Outputs and Evidence
Returns a concise explanation.
### Limits and Constraints
Cannot explain facts absent from the result.
### Failure Handling
Raises a clear ValueError for malformed results.
### Human Review
Use the explanation to support, not replace, merchandising judgment.
