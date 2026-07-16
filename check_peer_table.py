import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

peer = pd.read_sql("SELECT * FROM peer_percentiles", conn)

print("Rows:", len(peer))

if len(peer) > 0:
    print(peer.head())
    print(peer.columns.tolist())

conn.close()