import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

DB = Path("out") / "kpi.db"

st.title("KPI Dashboard (Demo)")

if not DB.exists():
    st.warning("Run `python etl/clean_and_load.py` first.")
    st.stop()

with sqlite3.connect(DB) as conn:
    df = pd.read_sql_query("SELECT * FROM orders", conn)

st.metric("Rows", len(df))
st.metric("Total revenue", f"${df['revenue'].sum():,.2f}")

st.subheader("Revenue by Region")
by_region = (
    df.groupby("region", as_index=False)["revenue"]
    .sum()
    .sort_values("revenue", ascending=False)
)
st.bar_chart(by_region, x="region", y="revenue")

st.subheader("Data Preview")
st.dataframe(df)

