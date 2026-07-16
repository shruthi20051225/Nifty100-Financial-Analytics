import streamlit as st
import plotly.express as px
import pandas as pd

from src.dashboard.utils.db import (
    get_companies,
    get_ratios
)

st.title("🏭 Sector Analysis")

companies = get_companies()
ratios = get_ratios()

# ---------------- Merge ----------------

df = ratios.merge(
    companies,
    left_on="company_id",
    right_on="id",
    how="left"
)

# ---------------- Latest FY ----------------

df = df[
    df["year"] == "2024-03-01 00:00:00"
].copy()

# ---------------- Clean company names ----------------

df["company_name"] = df["company_name"].fillna("Unknown")
df["company_name"] = df["company_name"].astype(str)

company_list = sorted(df["company_name"].unique())

selected_company = st.selectbox(
    "Select Company",
    company_list
)

company = df[
    df["company_name"] == selected_company
]

if company.empty:
    st.warning("No data available.")
    st.stop()

# ---------------- Company Details ----------------

st.subheader("Financial Metrics")

st.dataframe(
    company[
        [
            "company_name",
            "return_on_equity_pct",
            "operating_profit_margin_pct",
            "debt_to_equity",
            "asset_turnover",
            "free_cash_flow_cr"
        ]
    ],
    use_container_width=True
)

# ---------------- Scatter Plot ----------------

fig = px.scatter(
    company,
    x="asset_turnover",
    y="return_on_equity_pct",
    size="free_cash_flow_cr",
    hover_name="company_name",
    title="ROE vs Asset Turnover"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------- Bar Chart ----------------

fig2 = px.bar(
    company,
    x="company_name",
    y=[
        "return_on_equity_pct",
        "operating_profit_margin_pct"
    ],
    barmode="group",
    title="ROE vs Operating Margin"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ---------------- KPI Cards ----------------

latest = company.iloc[0]

c1, c2, c3 = st.columns(3)

c1.metric(
    "ROE",
    f"{latest['return_on_equity_pct']:.2f}%"
)

c2.metric(
    "Debt / Equity",
    f"{latest['debt_to_equity']:.2f}"
)

c3.metric(
    "Free Cash Flow",
    f"{latest['free_cash_flow_cr']:.2f}"
)

c4, c5 = st.columns(2)

c4.metric(
    "Operating Margin",
    f"{latest['operating_profit_margin_pct']:.2f}%"
)

c5.metric(
    "Asset Turnover",
    f"{latest['asset_turnover']:.2f}"
)