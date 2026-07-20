
import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

df = pd.read_sql(
    "SELECT DISTINCT peer_group FROM peer_percentiles ORDER BY peer_group",
    conn,
)

print(df)

conn.close()