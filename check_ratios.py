import sqlite3

conn = sqlite3.connect("nifty100.db")

count = conn.execute(
    "SELECT COUNT(*) FROM financial_ratios"
).fetchone()[0]

print("Rows:", count)

conn.close()