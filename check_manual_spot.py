import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

query = """
SELECT
company_id,
year,
return_on_equity_pct,
net_profit_margin_pct,
debt_to_equity
FROM financial_ratios
ORDER BY company_id, year DESC
LIMIT 15;
"""

df = pd.read_sql(query, conn)

print(df)

conn.close()
