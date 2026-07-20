import sqlite3
import pandas as pd
import os

DB_PATH = "nifty100.db"

os.makedirs("output", exist_ok=True)

conn = sqlite3.connect(DB_PATH)

# Load ratios
ratios = pd.read_sql(
    """
    SELECT *
    FROM financial_ratios
    """,
    conn,
)

# Load peer groups
peer = pd.read_excel("data/raw/peer_groups.xlsx")

# Merge
df = ratios.merge(peer, on="company_id", how="left")

# Rename peer group column if required
if "peer_group" not in df.columns:
    for col in df.columns:
        if "peer" in col.lower():
            df.rename(columns={col: "peer_group"}, inplace=True)
            break

metrics = [
    "return_on_equity_pct",
    "net_profit_margin_pct",
    "debt_to_equity",
    "interest_coverage",
    "asset_turnover",
]

records = []

for group in df["peer_group"].dropna().unique():

    group_df = df[df["peer_group"] == group].copy()

    for metric in metrics:

        if metric not in group_df.columns:
            continue

        ascending = metric == "debt_to_equity"

        group_df["percentile"] = (
            group_df[metric].rank(pct=True, ascending=ascending) * 100
        )

        for _, row in group_df.iterrows():

            records.append(
                {
                    "company_id": row["company_id"],
                    "peer_group": group,
                    "metric": metric,
                    "value": row[metric],
                    "percentile_rank": round(row["percentile"], 2),
                    "year": row["year"],
                }
            )

peer_percentiles = pd.DataFrame(records)

peer_percentiles.to_sql(
    "peer_percentiles",
    conn,
    if_exists="replace",
    index=False,
)

peer_percentiles.to_excel(
    "output/peer_percentiles.xlsx",
    index=False,
)

conn.close()

print("Peer percentile table created.")
print("Rows:", len(peer_percentiles))
