import streamlit as st
import plotly.express as px

from src.dashboard.utils.db import (
    get_companies,
    get_ratios,
    get_profit_loss
)

st.title("🏢 Company Profile")

companies = get_companies()

company = st.selectbox(
    "Select Company",
    companies["company_name"]
)

selected = companies[
    companies["company_name"] == company
].iloc[0]

st.subheader(selected["company_name"])

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"**Ticker:** {selected['id']}")
    st.markdown(f"**Face Value:** {selected['face_value']}")
    st.markdown(f"**Book Value:** {selected['book_value']}")

with col2:
    st.markdown(f"**ROCE:** {selected['roce_percentage']}%")
    st.markdown(f"**ROE:** {selected['roe_percentage']}%")
    st.markdown(f"**Website:** {selected['website']}")

st.divider()

st.subheader("About Company")

st.write(selected["about_company"])

ratios = get_ratios()

company_ratios = ratios[
    ratios["company_id"] == selected["id"]
].copy()

if company_ratios.empty:

    st.warning("Ticker not found — please try another.")

    st.stop()

company_ratios = company_ratios.sort_values("year")

latest = company_ratios.iloc[-1]

st.subheader("Financial KPIs")

c1, c2, c3 = st.columns(3)

c1.metric(
    "ROE",
    f"{latest['return_on_equity_pct']:.2f}%"
)

c2.metric(
    "Debt/Equity",
    f"{latest['debt_to_equity']:.2f}"
)

c3.metric(
    "Free Cash Flow",
    f"{latest['free_cash_flow_cr']:.2f}"
)

c4, c5, c6 = st.columns(3)

c4.metric(
    "Operating Margin",
    f"{latest['operating_profit_margin_pct']:.2f}%"
)

c5.metric(
    "Net Profit Margin",
    f"{latest['net_profit_margin_pct']:.2f}%"
)

c6.metric(
    "Interest Coverage",
    f"{latest['interest_coverage']:.2f}"
)

st.divider()

pl = get_profit_loss()

company_pl = pl[
    pl["company_id"] == selected["id"]
].copy()

if not company_pl.empty:

    company_pl = company_pl.sort_values("year")

    st.subheader("Revenue & Net Profit")

fig = px.bar(
    company_pl,
    x="year",
    y=["sales", "net_profit"],
    barmode="group",
    title="Revenue vs Net Profit"
)

fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Amount",
    legend_title="Metric"
)

st.plotly_chart(
    fig,
    use_container_width=True
)