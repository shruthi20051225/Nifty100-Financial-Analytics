import sqlite3

conn = sqlite3.connect("nifty100.db")

count = conn.execute(
    """
    SELECT COUNT(*)
    FROM peer_percentiles
    """
).fetchone()

print(count)

conn.close()