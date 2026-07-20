import sqlite3
import pandas as pd

from src.analytics.cashflow_kpis import capital_allocation_pattern

conn = sqlite3.connect("nifty100.db")

query = """
SELECT
    company_id,
    year,
    operating_activity,
    investing_activity,
    financing_activity
FROM cashflow
"""

df = pd.read_sql(query, conn)

conn.close()

output = []

for _, row in df.iterrows():

    cfo = row["operating_activity"]
    cfi = row["investing_activity"]
    cff = row["financing_activity"]

    pattern = capital_allocation_pattern(cfo, cfi, cff)

    output.append(
        {
            "company_id": row["company_id"],
            "year": row["year"],
            "cfo_sign": "+" if cfo >= 0 else "-",
            "cfi_sign": "+" if cfi >= 0 else "-",
            "cff_sign": "+" if cff >= 0 else "-",
            "pattern_label": pattern,
        }
    )

capital = pd.DataFrame(output)

capital.to_csv("output/capital_allocation.csv", index=False)

print("capital_allocation.csv generated")
print("Rows:", len(capital))
