import pandas as pd
import sqlite3
from pathlib import Path

DB_FILE = "nifty100.db"

HEADER_MAP = {
    "analysis": 1,
    "balancesheet": 1,
    "cashflow": 1,
    "companies": 1,
    "documents": 1,
    "profitandloss": 1,
    "financial_ratios": 0,
    "market_cap": 0,
    "peer_groups": 0,
    "sectors": 0,
    "stock_prices": 0,
}

conn = sqlite3.connect(DB_FILE)

audit = []

for file in Path("data/raw").glob("*.xlsx"):

    table_name = file.stem.lower()

    try:
        header_row = HEADER_MAP.get(table_name, 0)

        df = pd.read_excel(
            file,
            header=header_row
        )

        print(f"\nLoading {table_name}")
        print(f"Rows: {len(df)}")

        df.columns = [
            str(col).strip().lower().replace(" ", "_")
            for col in df.columns
        ]

        df.to_sql(
            table_name,
            conn,
            if_exists="replace",
            index=False
        )

        audit.append({
            "table": table_name,
            "rows_loaded": len(df),
            "status": "SUCCESS"
        })

    except Exception as e:

        print(f"ERROR: {table_name}")
        print(e)

        audit.append({
            "table": table_name,
            "rows_loaded": 0,
            "status": str(e)
        })

pd.DataFrame(audit).to_csv(
    "output/load_audit.csv",
    index=False
)

conn.close()

print("\nAll files loaded successfully!")