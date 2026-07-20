from fastapi import APIRouter, HTTPException
import sqlite3

router = APIRouter()

DB = "nifty100.db"


@router.get("/companies/{ticker}/documents")
def company_documents(ticker: str):

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    rows = conn.execute(
        """
        SELECT *
        FROM documents
        WHERE company_id = ?
        ORDER BY year DESC
        """,
        (ticker.upper(),),
    ).fetchall()

    conn.close()

    if not rows:
        raise HTTPException(status_code=404, detail="Documents not found.")

    return [dict(r) for r in rows]
