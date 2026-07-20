from fastapi import APIRouter, Query
import sqlite3

router = APIRouter()

DB = "nifty100.db"


@router.get("/screener")
def screener(
    min_roe: float | None = Query(default=None),
    max_de: float | None = Query(default=None),
    sector: str | None = Query(default=None),
):

    conn = sqlite3.connect(DB)

    conn.row_factory = sqlite3.Row

    query = """
    SELECT
        r.company_id,
        c.company_name,
        s.broad_sector,
        r.return_on_equity_pct,
        r.debt_to_equity,
        r.operating_profit_margin_pct,
        r.net_profit_margin_pct,
        r.free_cash_flow_cr
    FROM financial_ratios r
    JOIN companies c
        ON r.company_id = c.id
    LEFT JOIN sectors s
        ON c.id = s.company_id
    WHERE 1=1
    """

    params = []

    # -----------------------------
    # Filters
    # -----------------------------

    if min_roe is not None:
        query += " AND r.return_on_equity_pct >= ?"
        params.append(min_roe)

    if max_de is not None:
        query += " AND r.debt_to_equity <= ?"
        params.append(max_de)

    if sector:
        query += " AND s.broad_sector = ?"
        params.append(sector)

    query += """
    ORDER BY
        r.return_on_equity_pct DESC
    """

    rows = conn.execute(query, params).fetchall()

    conn.close()

    return [dict(r) for r in rows]
