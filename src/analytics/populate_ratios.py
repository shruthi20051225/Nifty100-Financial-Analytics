import sqlite3
import pandas as pd

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    debt_to_equity,
    interest_coverage,
    asset_turnover,
)

from src.analytics.cashflow_kpis import (
    free_cash_flow,
)

DB = "nifty100.db"

conn = sqlite3.connect(DB)

pl = pd.read_sql("SELECT * FROM profitandloss", conn)
bs = pd.read_sql("SELECT * FROM balancesheet", conn)
cf = pd.read_sql("SELECT * FROM cashflow", conn)

df = (
    pl.merge(
        bs,
        on=["company_id", "year"],
        how="left"
    )
    .merge(
        cf,
        on=["company_id", "year"],
        how="left"
    )
)

rows = []

for _, r in df.iterrows():

    rows.append({

        "company_id":
            r["company_id"],

        "year":
            r["year"],

        "net_profit_margin_pct":
            net_profit_margin(
                r["net_profit"],
                r["sales"]
            ),

        "operating_profit_margin_pct":
            operating_profit_margin(
                r["operating_profit"],
                r["sales"]
            ),

        "return_on_equity_pct":
            return_on_equity(
                r["net_profit"],
                r["equity_capital"],
                r["reserves"]
            ),

        "debt_to_equity":
            debt_to_equity(
                r["borrowings"],
                r["equity_capital"],
                r["reserves"]
            ),

        "interest_coverage":
            interest_coverage(
                r["operating_profit"],
                r["other_income"],
                r["interest"]
            ),

        "asset_turnover":
            asset_turnover(
                r["sales"],
                r["total_assets"]
            ),

        "free_cash_flow_cr":
            free_cash_flow(
                r["operating_activity"],
                r["investing_activity"]
            ),

        "earnings_per_share":
            r["eps"],

        "dividend_payout_ratio_pct":
            r["dividend_payout"],

        "total_debt_cr":
            r["borrowings"],

        "cash_from_operations_cr":
            r["operating_activity"]

    })

ratio_df = pd.DataFrame(rows)

ratio_df.to_sql(
    "financial_ratios",
    conn,
    if_exists="replace",
    index=False
)

print("Rows inserted:", len(ratio_df))

conn.close()