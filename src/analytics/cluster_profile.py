import sqlite3
import os

import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt

from scipy.stats import zscore

DB = "nifty100.db"

OUTPUT = "output"
REPORTS = "reports"

os.makedirs(OUTPUT, exist_ok=True)
os.makedirs(REPORTS, exist_ok=True)

conn = sqlite3.connect(DB)

clusters = pd.read_csv("output/cluster_labels.csv")

ratios = pd.read_sql("SELECT * FROM financial_ratios", conn)

companies = pd.read_sql(
    """
    SELECT
        c.id,
        c.company_name,
        s.broad_sector
    FROM companies c
    LEFT JOIN sectors s
    ON c.id = s.company_id
    """,
    conn,
)

conn.close()
# ============================================================
# LATEST YEAR RATIOS
# ============================================================

latest = ratios.sort_values("year").groupby("company_id").tail(1)

df = latest.merge(clusters, on="company_id", how="left")

df = df.merge(companies, left_on="company_id", right_on="id", how="left")
# ============================================================
# FIX DUPLICATE COLUMN NAMES
# ============================================================

if "company_name_y" in df.columns:
    df["company_name"] = df["company_name_y"]
elif "company_name_x" in df.columns:
    df["company_name"] = df["company_name_x"]

if "broad_sector_y" in df.columns:
    df["broad_sector"] = df["broad_sector_y"]
elif "broad_sector_x" in df.columns:
    df["broad_sector"] = df["broad_sector_x"]

# ============================================================
# KPIs FOR ANALYSIS
# ============================================================

kpis = [
    "return_on_equity_pct",
    "debt_to_equity",
    "operating_profit_margin_pct",
    "free_cash_flow_cr",
    "interest_coverage",
    "asset_turnover",
    "earnings_per_share",
    "dividend_payout_ratio_pct",
    "cash_from_operations_cr",
    "net_profit_margin_pct",
]

# ============================================================
# CLUSTER PROFILE
# ============================================================

cluster_profile = df.groupby("cluster_name")[kpis].agg(["mean", "median"]).round(2)

cluster_profile.to_excel("output/cluster_profile.xlsx")

print("Cluster profile saved.")

# ============================================================
# PORTFOLIO STATISTICS
# ============================================================

rows = []

for col in kpis:

    s = df[col].dropna()

    rows.append(
        {
            "Metric": col,
            "P10": s.quantile(0.10),
            "P25": s.quantile(0.25),
            "P50": s.quantile(0.50),
            "P75": s.quantile(0.75),
            "P90": s.quantile(0.90),
            "Mean": s.mean(),
            "Std": s.std(),
        }
    )

portfolio = pd.DataFrame(rows)

portfolio = portfolio.round(2)

portfolio.to_csv("output/portfolio_stats.csv", index=False)

print("Portfolio statistics saved.")
# ============================================================
# CORRELATION HEATMAP
# ============================================================

corr = df[kpis].corr(method="pearson")

plt.figure(figsize=(10, 8))

sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)

plt.title("Correlation Heatmap of Financial KPIs")

plt.tight_layout()

plt.savefig("reports/correlation_heatmap.png", dpi=300)

plt.close()

print("Correlation heatmap saved.")

# ============================================================
# OUTLIER DETECTION (Z-SCORE BY SECTOR)
# ============================================================

outliers = []

sector_column = "broad_sector"

if "broad_sector_x" in df.columns:
    sector_column = "broad_sector_x"

elif "broad_sector_y" in df.columns:
    sector_column = "broad_sector_y"

for sector in df[sector_column].dropna().unique():

    sector_df = df[df[sector_column] == sector].copy()

    if len(sector_df) < 3:
        continue

    for metric in kpis:

        if metric not in sector_df.columns:
            continue

        values = sector_df[metric].fillna(sector_df[metric].median())

        if values.std() == 0:
            continue

        z = np.abs(zscore(values))

        sector_df["zscore"] = z

        flagged = sector_df[sector_df["zscore"] > 3]

        for _, row in flagged.iterrows():

            outliers.append(
                {
                    "company_id": row["company_id"],
                    "company_name": row["company_name"],
                    "sector": sector,
                    "metric": metric,
                    "value": row[metric],
                    "zscore": round(row["zscore"], 2),
                }
            )

# ============================================================
# SAVE OUTLIERS
# ============================================================

outlier_df = pd.DataFrame(outliers)

outlier_df.to_csv("output/outlier_report.csv", index=False)

print("Outlier report saved.")

# ============================================================
# SUMMARY
# ============================================================

print("=" * 60)
print("Cluster Profiling Completed")
print("=" * 60)
print("Cluster Profile      : output/cluster_profile.xlsx")
print("Portfolio Statistics : output/portfolio_stats.csv")
print("Outlier Report       : output/outlier_report.csv")
print("Correlation Heatmap  : reports/correlation_heatmap.png")
print("=" * 60)
