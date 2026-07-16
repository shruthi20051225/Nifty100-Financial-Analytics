import streamlit as st
import pandas as pd

from src.dashboard.utils.db import (
    get_companies,
    get_ratios
)

st.title("🔍 Nifty 100 Screener")

companies = get_companies()
ratios = get_ratios()

# Keep only FY2024 records
ratios = ratios[
    ratios["year"] == "2024-03-01 00:00:00"
]

df = ratios.merge(
    companies,
    left_on="company_id",
    right_on="id",
    how="left"
)

# ---------------- Sidebar ----------------

st.sidebar.header("Filters")

roe = st.sidebar.slider(
    "Minimum ROE",
    0,
    50,
    15
)

de = st.sidebar.slider(
    "Maximum Debt / Equity",
    0.0,
    5.0,
    1.0
)

opm = st.sidebar.slider(
    "Minimum Operating Margin",
    0,
    60,
    10
)

fcf = st.sidebar.number_input(
    "Minimum Free Cash Flow",
    value=0.0
)

# ---------------- Apply Filters ----------------

filtered = df[
    (df["return_on_equity_pct"] >= roe)
]

filtered = filtered[
    filtered["debt_to_equity"] <= de
]

filtered = filtered[
    filtered["operating_profit_margin_pct"] >= opm
]

filtered = filtered[
    filtered["free_cash_flow_cr"] >= fcf
]

# ---------------- Composite Score ----------------

filtered = filtered.copy()

filtered["Composite Score"] = (

    filtered["return_on_equity_pct"]*0.35 +

    filtered["operating_profit_margin_pct"]*0.30 +

    filtered["asset_turnover"]*10*0.20 +

    (5-filtered["debt_to_equity"])*10*0.15

)

filtered = filtered.sort_values(
    "Composite Score",
    ascending=False
)

st.success(f"{len(filtered)} Companies Found")

st.dataframe(

    filtered[
        [
            "company_name",
            "return_on_equity_pct",
            "operating_profit_margin_pct",
            "debt_to_equity",
            "free_cash_flow_cr",
            "Composite Score"
        ]
    ],

    use_container_width=True

)

csv = filtered.to_csv(index=False)

st.download_button(

    "⬇ Download CSV",

    csv,

    file_name="screener_output.csv",

    mime="text/csv"

)