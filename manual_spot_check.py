import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

query = """
SELECT
company_id,
year,
return_on_equity_pct,
debt_to_equity
FROM financial_ratios
WHERE company_id IN ('ABB','TCS','INFY')
ORDER BY company_id, year DESC;
"""

df = pd.read_sql(query, conn)

print(df)

conn.close()
