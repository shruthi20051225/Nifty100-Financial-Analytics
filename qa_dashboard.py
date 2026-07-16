import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

companies = pd.read_sql("SELECT * FROM companies", conn)
ratios = pd.read_sql("SELECT * FROM financial_ratios", conn)
peer = pd.read_sql("SELECT * FROM peer_percentiles", conn)
valuation = pd.read_excel("output/valuation_summary.xlsx")

conn.close()

print("=" * 50)
print("DASHBOARD QA")
print("=" * 50)

print("Companies:", len(companies))
print("Financial Ratios:", len(ratios))
print("Peer Percentiles:", len(peer))
print("Valuation Rows:", len(valuation))

print("\nDashboard Tables Loaded Successfully")

print("\nSample Companies:")
print(companies["company_name"].head())

print("\nLatest Financial Ratio Sample:")
print(
    ratios[
        ratios["year"] == "2024-03-01 00:00:00"
    ][["company_id", "return_on_equity_pct"]].head()
)

print("\nQA Completed Successfully")