import sqlite3

conn = sqlite3.connect("nifty100.db")

tables = [
    "companies",
    "sectors",
    "profitandloss",
    "balancesheet",
    "cashflow",
    "analysis",
    "documents",
    "prosandcons",
    "stock_prices",
    "financial_ratios",
    "peer_groups",
    "market_cap"
]

for table in tables:
    conn.execute(f"DELETE FROM {table}")

conn.commit()
conn.close()

print("Database cleared.")