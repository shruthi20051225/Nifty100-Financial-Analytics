from fastapi import APIRouter, HTTPException
import sqlite3

router = APIRouter()

DB = "nifty100.db"


@router.get("/peers/{group_name}")
def peer_group(group_name: str):

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    rows = conn.execute(
        """
        SELECT
            company_id,
            peer_group,
            metric,
            value,
            percentile_rank,
            year
        FROM peer_percentiles
        WHERE LOWER(peer_group)=LOWER(?)
        ORDER BY company_id, year DESC
        """,
        (group_name,),
    ).fetchall()

    conn.close()

    if not rows:
        raise HTTPException(status_code=404, detail="Peer group not found.")

    return [dict(r) for r in rows]
