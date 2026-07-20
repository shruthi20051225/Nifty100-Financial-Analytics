import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

print("Columns:")
df = pd.read_sql("SELECT * FROM peer_percentiles LIMIT 5", conn)

print(df.columns.tolist())

print("\nSample Data:")
print(df.head())

conn.close()