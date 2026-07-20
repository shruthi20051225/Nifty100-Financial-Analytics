from fastapi import APIRouter
import sqlite3
import pandas as pd

router = APIRouter()

DB = "nifty100.db"


@router.get("/portfolio/stats")
def portfolio_stats():

    conn = sqlite3.connect(DB)

    df = pd.read_sql("SELECT * FROM financial_ratios", conn)

    conn.close()

    numeric_cols = [
        "return_on_equity_pct",
        "operating_profit_margin_pct",
        "net_profit_margin_pct",
        "debt_to_equity",
        "interest_coverage",
        "asset_turnover",
        "free_cash_flow_cr",
        "earnings_per_share",
        "dividend_payout_ratio_pct",
    ]

    output = {}

    for col in numeric_cols:

        if col not in df.columns:

            continue

        output[col] = {
            "P10": round(df[col].quantile(0.10), 2),
            "P25": round(df[col].quantile(0.25), 2),
            "Median": round(df[col].median(), 2),
            "P75": round(df[col].quantile(0.75), 2),
            "P90": round(df[col].quantile(0.90), 2),
            "Mean": round(df[col].mean(), 2),
            "Std": round(df[col].std(), 2),
        }

    return output
