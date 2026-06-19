import sqlite3

conn = sqlite3.connect("nifty100.db")

tables = conn.execute("""
SELECT name
FROM sqlite_master
WHERE type='table'
""").fetchall()

for table in tables:
    name = table[0]

    count = conn.execute(
        f"SELECT COUNT(*) FROM {name}"
    ).fetchone()[0]

    print(name, count)

conn.close()
