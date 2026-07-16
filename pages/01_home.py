import streamlit as st
import plotly.express as px
from src.dashboard.utils.db import get_companies, get_ratios

st.set_page_config(layout="wide")

st.title("🏠 Nifty 100 Dashboard")

companies = get_companies()
ratios = get_ratios()

latest_year = ratios["year"].max()

latest = ratios[
    ratios["year"] == latest_year
].copy()

# ================= KPI Tiles =================

avg_roe = round(
    latest["return_on_equity_pct"].mean(),
    2
)

avg_de = round(
    latest["debt_to_equity"].mean(),
    2
)

avg_opm = round(
    latest["operating_profit_margin_pct"].mean(),
    2
)

total_companies = companies["id"].nunique()

positive_fcf = (
    latest["free_cash_flow_cr"] > 0
).sum()

avg_asset_turnover = round(
    latest["asset_turnover"].mean(),
    2
)

c1, c2, c3 = st.columns(3)

c1.metric(
    "Companies",
    total_companies
)

c2.metric(
    "Average ROE",
    f"{avg_roe}%"
)

c3.metric(
    "Average Debt/Equity",
    avg_de
)

c4, c5, c6 = st.columns(3)

c4.metric(
    "Average OPM",
    f"{avg_opm}%"
)

c5.metric(
    "Positive FCF",
    positive_fcf
)

c6.metric(
    "Asset Turnover",
    avg_asset_turnover
)

st.divider()

# ================= Sector Distribution =================

if "broad_sector" in companies.columns:

    sector = (
        companies.groupby("broad_sector")
        .size()
        .reset_index(name="Companies")
    )

    fig = px.pie(
        sector,
        names="broad_sector",
        values="Companies",
        title="Sector Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# ================= Top ROE =================

st.subheader("Top Companies by ROE")

top = latest.sort_values(
    "return_on_equity_pct",
    ascending=False
)

st.dataframe(
    top.head(10),
    use_container_width=True
)