from fastapi import APIRouter, Query, HTTPException
import sqlite3

router = APIRouter()

DB = "nifty100.db"


# =====================================================
# GET ALL COMPANIES
# =====================================================


@router.get("/companies")
def get_companies(
    sector: str | None = Query(default=None),
    market_cap_category: str | None = Query(default=None),
    search: str | None = Query(default=None),
):

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    query = """
    SELECT
        c.id,
        c.company_name,
        s.broad_sector,
        s.sub_sector,
        s.market_cap_category,
        c.roe_percentage,
        c.roce_percentage
    FROM companies c
    LEFT JOIN sectors s
        ON c.id = s.company_id
    WHERE 1=1
    """

    params = []

    if sector:
        query += " AND s.broad_sector=?"
        params.append(sector)

    if market_cap_category:
        query += " AND s.market_cap_category=?"
        params.append(market_cap_category)

    if search:
        query += """
        AND (
            c.company_name LIKE ?
            OR c.id LIKE ?
        )
        """
        params.append(f"%{search}%")
        params.append(f"%{search}%")

    query += " ORDER BY c.company_name"

    rows = conn.execute(query, params).fetchall()

    conn.close()

    return [dict(x) for x in rows]


# =====================================================
# GET SINGLE COMPANY
# =====================================================


@router.get("/companies/{ticker}")
def get_company(ticker: str):

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    company = conn.execute(
        """
        SELECT
            c.*,
            s.broad_sector,
            s.sub_sector,
            s.market_cap_category
        FROM companies c
        LEFT JOIN sectors s
            ON c.id=s.company_id
        WHERE c.id=?
        """,
        (ticker.upper(),),
    ).fetchone()

    if company is None:

        conn.close()

        raise HTTPException(status_code=404, detail="Company not found")

    ratios = conn.execute(
        """
        SELECT *
        FROM financial_ratios
        WHERE company_id=?
        ORDER BY year DESC
        LIMIT 1
        """,
        (ticker.upper(),),
    ).fetchone()

    conn.close()

    return {"company": dict(company), "latest_ratios": dict(ratios) if ratios else None}


# =====================================================
# COMPANY RATIOS
# =====================================================


@router.get("/companies/{ticker}/ratios")
def company_ratios(ticker: str):

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    rows = conn.execute(
        """
        SELECT *
        FROM financial_ratios
        WHERE company_id=?
        ORDER BY year DESC
        """,
        (ticker.upper(),),
    ).fetchall()

    conn.close()

    if len(rows) == 0:

        raise HTTPException(status_code=404, detail="No ratio data found.")

    return [dict(r) for r in rows]


# =====================================================
# COMPANY PROFIT & LOSS
# =====================================================


@router.get("/companies/{ticker}/pl")
def company_profit_loss(ticker: str):

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    rows = conn.execute(
        """
        SELECT *
        FROM profitandloss
        WHERE company_id=?
        ORDER BY year DESC
        """,
        (ticker.upper(),),
    ).fetchall()

    conn.close()

    if len(rows) == 0:
        raise HTTPException(status_code=404, detail="No Profit & Loss data found.")

    return [dict(r) for r in rows]


# =====================================================
# COMPANY BALANCE SHEET
# =====================================================


@router.get("/companies/{ticker}/bs")
def company_balance_sheet(ticker: str):

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    rows = conn.execute(
        """
        SELECT *
        FROM balancesheet
        WHERE company_id=?
        ORDER BY year DESC
        """,
        (ticker.upper(),),
    ).fetchall()

    conn.close()

    if len(rows) == 0:

        raise HTTPException(status_code=404, detail="No Balance Sheet data found.")

    return [dict(r) for r in rows]


# =====================================================
# COMPANY CASH FLOW
# =====================================================


@router.get("/companies/{ticker}/cashflow")
def company_cashflow(ticker: str):

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    rows = conn.execute(
        """
        SELECT *
        FROM cashflow
        WHERE company_id=?
        ORDER BY year DESC
        """,
        (ticker.upper(),),
    ).fetchall()

    conn.close()

    if len(rows) == 0:

        raise HTTPException(status_code=404, detail="No Cash Flow data found.")

    return [dict(r) for r in rows]
