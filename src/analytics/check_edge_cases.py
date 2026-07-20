import sqlite3
import pandas as pd

# ----------------------------
# Connect to database
# ----------------------------
conn = sqlite3.connect("nifty100.db")

# Companies
companies = pd.read_sql(
    """
SELECT
    id,
    company_name,
    roe_percentage,
    roce_percentage
FROM companies
""",
    conn,
)

# Financial ratios
ratios = pd.read_sql(
    """
SELECT
    company_id,
    year,
    return_on_equity_pct
FROM financial_ratios
""",
    conn,
)

conn.close()

# ----------------------------
# Remove TTM rows
# ----------------------------
ratios = ratios[ratios["year"] != "TTM"].copy()

# Convert dates safely
ratios["year"] = pd.to_datetime(ratios["year"], errors="coerce")

ratios = ratios.dropna(subset=["year"])

# ----------------------------
# Latest year only
# ----------------------------
latest = ratios.sort_values("year").groupby("company_id").tail(1)

# ----------------------------
# Merge
# ----------------------------
merged = companies.merge(latest, left_on="id", right_on="company_id", how="inner")

# ----------------------------
# Write log
# ----------------------------
count = 0

with open("output/ratio_edge_cases.log", "w", encoding="utf-8") as log:

    log.write("RATIO EDGE CASES\n")
    log.write("=" * 60 + "\n\n")

    for _, row in merged.iterrows():

        if pd.isna(row["roe_percentage"]):
            continue

        if pd.isna(row["return_on_equity_pct"]):
            continue

        diff = abs(row["roe_percentage"] - row["return_on_equity_pct"])

        if diff > 5:

            if diff > 20:
                category = "Data Source Issue"
            elif diff > 10:
                category = "Version Difference"
            else:
                category = "Formula Discrepancy"

            log.write(f"Company : {row['company_name']}\n")

            log.write(f"Company ID : {row['id']}\n")

            log.write(f"Latest Year : {row['year'].date()}\n")

            log.write(f"Source ROE : {row['roe_percentage']}\n")

            log.write(f"Calculated ROE : {row['return_on_equity_pct']}\n")

            log.write(f"Difference : {diff:.2f}%\n")

            log.write(f"Category : {category}\n")

            log.write("-" * 60 + "\n")

            count += 1

    if count == 0:
        log.write("No edge cases found.\n")

print("ratio_edge_cases.log generated.")
print("Edge cases:", count)
