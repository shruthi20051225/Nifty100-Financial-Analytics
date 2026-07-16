import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from src.dashboard.utils.db import get_peer_percentiles

st.title("👥 Peer Comparison")

# ---------------- Load Data ----------------

peer = get_peer_percentiles()

if peer.empty:
    st.warning("No peer data available.")
    st.stop()

# ---------------- Clean Data ----------------

peer["company_id"] = peer["company_id"].astype(str)
peer["peer_group"] = peer["peer_group"].astype(str)
peer["metric"] = peer["metric"].astype(str)
peer["year"] = peer["year"].astype(str)

# Keep only FY2024 rows
peer = peer[
    peer["year"].str.contains("2024", na=False)
]

if peer.empty:
    st.warning("No 2024 peer data found.")
    st.stop()

# ---------------- Select Peer Group ----------------

groups = sorted(peer["peer_group"].dropna().unique())

group = st.selectbox(
    "Select Peer Group",
    groups
)

group_df = peer[
    peer["peer_group"] == group
]

# ---------------- Select Company ----------------

companies = sorted(group_df["company_id"].dropna().unique())

company = st.selectbox(
    "Select Company",
    companies
)

company_df = group_df[
    group_df["company_id"] == company
]

# ---------------- Create Radar Data ----------------

pivot = company_df.pivot_table(
    index="company_id",
    columns="metric",
    values="percentile_rank",
    aggfunc="mean"
)

pivot = pivot.fillna(0)

if pivot.empty:
    st.warning("No radar chart data available.")
    st.stop()

metrics = list(pivot.columns)

values = pivot.iloc[0].tolist()

# Close polygon

metrics += [metrics[0]]
values += [values[0]]

# ---------------- Radar Chart ----------------

fig = go.Figure()

fig.add_trace(

    go.Scatterpolar(

        r=values,

        theta=metrics,

        fill="toself",

        name=company

    )

)

fig.update_layout(

    title=f"{company} Peer Percentile Radar",

    polar=dict(

        radialaxis=dict(

            visible=True,

            range=[0,100]

        )

    ),

    showlegend=False

)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ---------------- Company Metrics ----------------

st.subheader("Company Percentiles")

company_table = company_df[
    [
        "metric",
        "value",
        "percentile_rank",
        "year"
    ]
].sort_values("metric")

st.dataframe(
    company_table,
    use_container_width=True
)

st.divider()

# ---------------- Peer Group Table ----------------

st.subheader("Peer Group Data")

peer_table = group_df.pivot_table(

    index="company_id",

    columns="metric",

    values="percentile_rank",

    aggfunc="mean"

)

peer_table = peer_table.reset_index()

st.dataframe(
    peer_table,
    use_container_width=True
)