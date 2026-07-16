import streamlit as st
import plotly.express as px

from src.dashboard.utils.db import get_ratios

st.title("💰 Capital Allocation")

ratios = get_ratios()

ratios = ratios[
    ratios["year"] == "2024-03-01 00:00:00"
]

def classify(row):

    if row["free_cash_flow_cr"] > 0 and row["debt_to_equity"] < 1:
        return "High Quality"

    if row["free_cash_flow_cr"] > 0:
        return "Cash Generator"

    if row["debt_to_equity"] > 2:
        return "Highly Leveraged"

    return "Average"

ratios["Capital Pattern"] = ratios.apply(
    classify,
    axis=1
)

summary = (
    ratios
    .groupby("Capital Pattern")
    .size()
    .reset_index(name="Companies")
)

fig = px.treemap(
    summary,
    path=["Capital Pattern"],
    values="Companies",
    title="Capital Allocation Patterns"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.dataframe(
    ratios[
        [
            "company_id",
            "Capital Pattern",
            "free_cash_flow_cr",
            "debt_to_equity"
        ]
    ],
    use_container_width=True
)