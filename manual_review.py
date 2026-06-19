import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

query = """
SELECT company_id,
       COUNT(*) as records
FROM profitandloss
GROUP BY company_id
ORDER BY RANDOM()
LIMIT 5
"""

df = pd.read_sql(query, conn)

print(df)

conn.close()