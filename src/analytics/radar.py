import os
import sqlite3

import pandas as pd
import plotly.graph_objects as go

DB = "nifty100.db"

os.makedirs("reports/radar_charts", exist_ok=True)

conn = sqlite3.connect(DB)

ratios = pd.read_sql(
    """
    SELECT *
    FROM financial_ratios
    """,
    conn,
)

peer = pd.read_excel("data/raw/peer_groups.xlsx")

conn.close()

peer.columns = [c.lower() for c in peer.columns]

peer_col = None

for c in peer.columns:
    if "peer" in c:
        peer_col = c

if peer_col is None:
    raise Exception("Peer group column not found.")

peer = peer.rename(columns={peer_col: "peer_group"})

df = ratios.merge(
    peer,
    on="company_id",
    how="left"
)

metrics = [
    "return_on_equity_pct",
    "net_profit_margin_pct",
    "debt_to_equity",
    "asset_turnover",
    "interest_coverage",
]

for company in df["company_id"].unique():

    company_df = df[df.company_id == company]

    if company_df.empty:
        continue

    latest = company_df.iloc[-1]

    if pd.isna(latest["peer_group"]):
        continue

    peer_df = df[df.peer_group == latest["peer_group"]]

    company_values = []
    peer_values = []

    for metric in metrics:

        company_values.append(latest.get(metric, 0))
        peer_values.append(peer_df[metric].mean())

    categories = metrics + [metrics[0]]

    company_values.append(company_values[0])
    peer_values.append(peer_values[0])

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=company_values,
            theta=categories,
            fill="toself",
            name=company,
        )
    )

    fig.add_trace(
        go.Scatterpolar(
            r=peer_values,
            theta=categories,
            name="Peer Average",
        )
    )

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=True,
        title=f"{company} Radar Chart",
    )

    fig.write_image(
        f"reports/radar_charts/{company}_radar.png"
    )

print("Radar charts generated.")