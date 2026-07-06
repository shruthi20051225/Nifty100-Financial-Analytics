import sqlite3

conn = sqlite3.connect("nifty100.db")

cols = conn.execute(
    "PRAGMA table_info(financial_ratios)"
).fetchall()

for c in cols:
    print(c)

conn.close()