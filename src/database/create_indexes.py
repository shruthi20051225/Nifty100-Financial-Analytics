import sqlite3

DB = "nifty100.db"

conn = sqlite3.connect(DB)
cur = conn.cursor()

indexes = [
    "CREATE INDEX IF NOT EXISTS idx_ratios_company ON financial_ratios(company_id);",
    "CREATE INDEX IF NOT EXISTS idx_ratios_year ON financial_ratios(year);",
    "CREATE INDEX IF NOT EXISTS idx_sector_company ON sectors(company_id);",
    "CREATE INDEX IF NOT EXISTS idx_sector_name ON sectors(broad_sector);",
    "CREATE INDEX IF NOT EXISTS idx_peer_company ON peer_percentiles(company_id);",
    "CREATE INDEX IF NOT EXISTS idx_peer_group ON peer_percentiles(peer_group);",
    "CREATE INDEX IF NOT EXISTS idx_market_company ON market_cap(company_id);",
    "CREATE INDEX IF NOT EXISTS idx_pl_company ON profitandloss(company_id);",
    "CREATE INDEX IF NOT EXISTS idx_bs_company ON balancesheet(company_id);",
    "CREATE INDEX IF NOT EXISTS idx_cf_company ON cashflow(company_id);",
]

for sql in indexes:
    cur.execute(sql)

conn.commit()
conn.close()

print("All indexes created successfully.")
