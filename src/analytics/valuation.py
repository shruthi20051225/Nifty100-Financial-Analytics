import sqlite3
import pandas as pd
import os

DB = "nifty100.db"

conn = sqlite3.connect(DB)

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

companies = pd.read_sql(
    "SELECT * FROM companies",
    conn
)

market = pd.read_sql(
    "SELECT * FROM market_cap",
    conn
)

conn.close()

# ---------------- Latest Year ----------------

ratios = ratios[
    ratios["year"] == "2024-03-01 00:00:00"
]

market = market[
    market["year"] == 2024
]

# ---------------- Merge ----------------

df = ratios.merge(
    companies,
    left_on="company_id",
    right_on="id",
    how="left"
)

df = df.merge(
    market,
    on="company_id",
    how="left"
)

# ---------------- FCF Yield ----------------

df["FCF Yield (%)"] = (
    df["free_cash_flow_cr"] /
    df["market_cap_crore"]
) * 100

# ---------------- Valuation Flag ----------------

def valuation(pe):

    if pd.isna(pe):
        return "Unknown"

    if pe > 30:
        return "Caution"

    elif pe < 15:
        return "Discount"

    else:
        return "Fair"

df["Valuation Flag"] = df["pe_ratio"].apply(
    valuation
)

# ---------------- PE vs Median ----------------

median_pe = df["pe_ratio"].median()

df["PE vs Median (%)"] = (
    (df["pe_ratio"] - median_pe)
    / median_pe
) * 100

# ---------------- Output ----------------

summary = df[
    [
        "company_id",
        "company_name",
        "market_cap_crore",
        "enterprise_value_crore",
        "pe_ratio",
        "pb_ratio",
        "ev_ebitda",
        "dividend_yield_pct",
        "FCF Yield (%)",
        "PE vs Median (%)",
        "Valuation Flag"
    ]
]

os.makedirs(
    "output",
    exist_ok=True
)

summary.to_excel(
    "output/valuation_summary.xlsx",
    index=False
)

summary[
    summary["Valuation Flag"] != "Fair"
].to_csv(
    "output/valuation_flags.csv",
    index=False
)

print("valuation_summary.xlsx generated")
print("valuation_flags.csv generated")
print("Rows:", len(summary))