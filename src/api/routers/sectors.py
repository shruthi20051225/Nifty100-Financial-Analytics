from fastapi import APIRouter, HTTPException
import sqlite3

router = APIRouter()

DB = "nifty100.db"


# =====================================================
# ALL SECTORS
# =====================================================


@router.get("/sectors")
def all_sectors():

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    rows = conn.execute("""
        SELECT
            broad_sector,
            COUNT(*) AS company_count,
            ROUND(AVG(c.roe_percentage),2) AS avg_roe,
            ROUND(AVG(c.roce_percentage),2) AS avg_roce
        FROM sectors s
        JOIN companies c
            ON s.company_id = c.id
        GROUP BY broad_sector
        ORDER BY broad_sector
    """).fetchall()

    conn.close()

    return [dict(r) for r in rows]


# =====================================================
# COMPANIES IN A SECTOR
# =====================================================


@router.get("/sectors/{sector}")
def sector_companies(sector: str):

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    rows = conn.execute(
        """
        SELECT
            c.id,
            c.company_name,
            s.sub_sector,
            c.roe_percentage,
            c.roce_percentage
        FROM companies c
        JOIN sectors s
            ON c.id=s.company_id
        WHERE s.broad_sector=?
        ORDER BY c.company_name
    """,
        (sector,),
    ).fetchall()

    conn.close()

    if len(rows) == 0:

        raise HTTPException(status_code=404, detail="Sector not found.")

    return [dict(r) for r in rows]


# =====================================================
# COMPANIES IN A SECTOR
# =====================================================


    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    rows = conn.execute(
        """
        SELECT
            c.id,
            c.company_name,
            s.broad_sector,
            s.sub_sector,
            c.roe_percentage,
            c.roce_percentage
        FROM companies c
        JOIN sectors s
            ON c.id = s.company_id
        WHERE LOWER(s.broad_sector) LIKE LOWER(?)
        ORDER BY c.company_name
        """,
        (f"%{sector}%",),
    ).fetchall()

    conn.close()

    if not rows:
        raise HTTPException(
            status_code=404, detail=f"No companies found for sector '{sector}'."
        )

    return [dict(r) for r in rows]
