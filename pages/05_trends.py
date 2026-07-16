import streamlit as st
import plotly.express as px

from src.dashboard.utils.db import (
    get_profit_loss,
    get_ratios,
    get_companies
)

st.title("📈 Trend Analysis")

companies = get_companies()

company = st.selectbox(
    "Select Company",
    companies["company_name"]
)

selected = companies[
    companies["company_name"] == company
].iloc[0]

pl = get_profit_loss()
ratios = get_ratios()

pl = pl[
    pl["company_id"] == selected["id"]
].sort_values("year")

ratios = ratios[
    ratios["company_id"] == selected["id"]
].sort_values("year")

metric = st.multiselect(
    "Select Metrics",
    [
        "Sales",
        "Net Profit",
        "Operating Profit",
        "ROE"
    ],
    default=["Sales"]
)

if "Sales" in metric:

    fig = px.line(
        pl,
        x="year",
        y="sales",
        markers=True,
        title="Sales Trend"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

if "Net Profit" in metric:

    fig = px.line(
        pl,
        x="year",
        y="net_profit",
        markers=True,
        title="Net Profit Trend"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

if "Operating Profit" in metric:

    fig = px.line(
        pl,
        x="year",
        y="operating_profit",
        markers=True,
        title="Operating Profit Trend"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

if "ROE" in metric:

    fig = px.line(
        ratios,
        x="year",
        y="return_on_equity_pct",
        markers=True,
        title="ROE Trend"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )