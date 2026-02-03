"""
Clean a messy CSV feed and load it into SQLite.

Thought process:
- Treat raw data like a real feed: assume it's imperfect.
- Make validation rules explicit and easy to change.
- Keep outputs reproducible so KPI numbers can be trusted.
"""

import sqlite3
from pathlib import Path

import pandas as pd

RAW = Path("data") / "raw_kpi_data.csv"
DB = Path("out") / "kpi.db"


def main() -> None:
    df = pd.read_csv(RAW)

    # 1) Remove duplicates (common in ingest pipelines).
    df = df.drop_duplicates()

    # 2) Coerce numeric fields; invalid parses become NaN.
    df["units"] = pd.to_numeric(df["units"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")

    # 3) Apply basic validation rules.
    # - Units must be positive and reasonable.
    # - Price must be positive.
    df = df[(df["units"] > 0) & (df["units"] < 1000)]
    df = df[df["unit_price"] > 0]

    # 4) Derived metrics used across reporting.
    df["revenue"] = df["units"] * df["unit_price"]

    DB.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB) as conn:
        df.to_sql("orders", conn, if_exists="replace", index=False)

    print(f"Loaded {len(df)} cleaned rows into {DB}")


if __name__ == "__main__":
    main()

