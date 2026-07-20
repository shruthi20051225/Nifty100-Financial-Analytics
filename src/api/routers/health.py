from fastapi import APIRouter
import sqlite3
import time

router = APIRouter()

DB = "nifty100.db"

START_TIME = time.time()


@router.get("/health")
def health():

    conn = sqlite3.connect(DB)

    cursor = conn.cursor()

    tables = [
        "companies",
        "profitandloss",
        "balancesheet",
        "cashflow",
        "market_cap",
        "documents",
        "sectors",
        "financial_ratios",
        "peer_percentiles",
        "analysis",
    ]

    counts = {}

    for table in tables:

        try:

            cursor.execute(f"SELECT COUNT(*) FROM {table}")

            counts[table] = cursor.fetchone()[0]

        except Exception:

            counts[table] = 0

    conn.close()

    return {
        "status": "ok",
        "version": "1.0.0",
        "uptime_seconds": round(time.time() - START_TIME, 2),
        "db_row_counts": counts,
    }
