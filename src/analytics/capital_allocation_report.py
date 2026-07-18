import sqlite3
import pandas as pd
import os

DB = "nifty100.db"

OUTPUT = "output"

os.makedirs(OUTPUT, exist_ok=True)

conn = sqlite3.connect(DB)

cashflow = pd.read_excel(
    "output/cashflow_intelligence.xlsx"
)

companies = pd.read_sql(
    "SELECT id, company_name FROM companies",
    conn
)

conn.close()

print("Cashflow records:", len(cashflow))
# =====================================================
# PATTERN CHANGES
# =====================================================

changes = []

for _, row in cashflow.iterrows():

    changes.append({

        "company_id": row["company_id"],

        "company_name": row.get(
            "company_name",
            row["company_id"]
        ),

        "previous_pattern": "Previous Year",

        "current_pattern": row[
            "capital_allocation_label"
        ],

        "change_detected": "No Historical Comparison"

    })

changes_df = pd.DataFrame(changes)

changes_df.to_csv(

    "output/pattern_changes.csv",

    index=False

)

print("Pattern Changes Saved")
# =====================================================
# DISTRIBUTION SUMMARY
# =====================================================

distribution = (

    cashflow.groupby(
        "capital_allocation_label"
    )

    .size()

    .reset_index(name="company_count")

)

distribution = distribution.sort_values(

    "company_count",

    ascending=False

)

# Save Summary

distribution.to_excel(

    "output/capital_allocation_distribution.xlsx",

    index=False

)

print("=" * 60)
print("Capital Allocation Report Completed")
print("=" * 60)
print("Companies Processed :", len(cashflow))
print("Patterns Found      :", distribution.shape[0])
print("Distribution File   : output/capital_allocation_distribution.xlsx")
print("Pattern Changes     : output/pattern_changes.csv")
print("=" * 60)

print("\nDistribution Summary\n")

print(distribution)