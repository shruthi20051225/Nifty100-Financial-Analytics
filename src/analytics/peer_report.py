import os
import sqlite3
import pandas as pd

DB = "nifty100.db"

os.makedirs("output", exist_ok=True)

conn = sqlite3.connect(DB)

# Load peer percentiles
peer = pd.read_sql(
    """
    SELECT *
    FROM peer_percentiles
    """,
    conn,
)

conn.close()

# Pivot metrics into columns
report = peer.pivot_table(
    index=["company_id", "peer_group", "year"],
    columns="metric",
    values="percentile_rank"
).reset_index()

writer = pd.ExcelWriter(
    "output/peer_comparison.xlsx",
    engine="openpyxl"
)

groups = sorted(report["peer_group"].dropna().unique())

for group in groups:

    df = report[
        report["peer_group"] == group
    ].copy()

    # Median row
    median = df.select_dtypes(include="number").median()

    median_row = {}

    for col in df.columns:

        if col in median.index:
            median_row[col] = round(median[col], 2)
        else:
            median_row[col] = ""

    median_row["company_id"] = "PEER MEDIAN"

    df = pd.concat(
        [
            df,
            pd.DataFrame([median_row])
        ],
        ignore_index=True
    )

    sheet = str(group)[:31]

    df.to_excel(
        writer,
        sheet_name=sheet,
        index=False
    )

writer.close()

print("peer_comparison.xlsx generated.")