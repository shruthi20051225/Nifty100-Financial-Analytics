import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

df = pd.read_sql("""
SELECT company_id,
       year,
       return_on_equity_pct
FROM financial_ratios
LIMIT 20
""", conn)

print(df)

conn.close()