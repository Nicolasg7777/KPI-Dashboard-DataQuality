# KPI Dashboard + Data Quality Pipeline

A small analytics pipeline that cleans messy source data, loads it into SQLite, and computes KPIs + anomaly checks.

## What it demonstrates
- Requirements -> data model -> validation -> reporting (end-to-end)
- Data cleaning + quality checks (nulls, ranges, duplicates)
- Repeatable KPI queries (SQL)
- Lightweight self-serve dashboard (Streamlit)

## Example data + outputs (portfolio snapshot)
Example **raw** input shape (CSV-style):

`raw_orders.csv`

| order_id | order_date  | channel | customer_id | sku  | quantity | unit_price | discount | refund_amount | subscription_flag |
|---:|---|---|---|---|---:|---:|---:|---:|---|
| 100234 | 2025-11-03 | shopify | C01922 | KF-01 | 2 | 42.00 | 5.00 | 0.00 | Y |
| 100235 | 2025-11-03 | amazon  | *(missing)* | KF-02 | 1 | 38.00 | 0.00 | 0.00 | N |

Example **data-quality summary** (what gets flagged before KPIs are produced):

| dq_check | failed_rows | action |
|---|---:|---|
| missing_customer_id | 12 | route to exceptions + exclude from customer metrics |
| duplicate_order_id | 3 | dedupe (keep latest) |
| negative_net_revenue | 5 | investigate refund/discount logic |

Example **KPI output** table (what the dashboard/report consumes):

| date | orders | gross_revenue | refunds | net_revenue | refund_rate |
|---|---:|---:|---:|---:|---:|
| 2025-11-03 | 418 | 17,982.00 | 621.00 | 17,361.00 | 3.45% |
| 2025-11-04 | 402 | 17,210.00 | 488.00 | 16,722.00 | 2.84% |

## Run
```bash
python -m venv .venv
. .venv/Scripts/activate
pip install -r requirements.txt

python etl/clean_and_load.py
streamlit run dashboard/app.py
```

## Notes
This project uses a small sample dataset on purpose so the logic is easy to review.

