import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

ratios = pd.read_sql("SELECT * FROM financial_ratios", conn)

print("Rows:", len(ratios))
print("\nYears:")
print(ratios["year"].unique())

print("\nLatest year:")
print(ratios["year"].max())

conn.close()