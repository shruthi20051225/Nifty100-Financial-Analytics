from fastapi import APIRouter, HTTPException
import sqlite3

router = APIRouter()

DB = "nifty100.db"


@router.get("/market-cap/{ticker}")
def market_cap_history(ticker: str):

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    rows = conn.execute(
        """
        SELECT *
        FROM market_cap
        WHERE company_id = ?
        ORDER BY year DESC
        """,
        (ticker.upper(),),
    ).fetchall()

    conn.close()

    if not rows:
        raise HTTPException(status_code=404, detail="Market cap data not found.")

    return [dict(r) for r in rows]
