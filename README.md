# KPI Dashboard + Data Quality Pipeline

A small analytics pipeline that cleans messy data, loads it into SQLite, and computes KPIs + anomaly checks.

## What it shows
- Data cleaning + validation (nulls, ranges, duplicates)
- Repeatable KPI queries
- Lightweight dashboard (Streamlit)

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

