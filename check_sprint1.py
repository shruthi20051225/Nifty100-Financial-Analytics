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
    "financial_ratios",
    "peer_groups",
    "stock_prices"
]

print("\nSPRINT 1 DATABASE CHECK\n")

for table in tables:
    count = conn.execute(
        f"SELECT COUNT(*) FROM {table}"
    ).fetchone()[0]

    print(f"{table:<20} {count}")

conn.close()
