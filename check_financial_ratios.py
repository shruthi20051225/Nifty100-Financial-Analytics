import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

# Total rows
count = pd.read_sql(
    "SELECT COUNT(*) AS total_rows FROM financial_ratios",
    conn
)

print("\nTotal Rows:")
print(count)

# Null count for every KPI column
query = """
SELECT
SUM(net_profit_margin_pct IS NULL) AS net_profit_margin_null,
SUM(operating_profit_margin_pct IS NULL) AS operating_profit_margin_null,
SUM(return_on_equity_pct IS NULL) AS roe_null,
SUM(debt_to_equity IS NULL) AS debt_to_equity_null,
SUM(interest_coverage IS NULL) AS interest_coverage_null,
SUM(asset_turnover IS NULL) AS asset_turnover_null,
SUM(free_cash_flow_cr IS NULL) AS free_cash_flow_null,
SUM(earnings_per_share IS NULL) AS eps_null,
SUM(dividend_payout_ratio_pct IS NULL) AS dividend_null,
SUM(total_debt_cr IS NULL) AS debt_null,
SUM(cash_from_operations_cr IS NULL) AS cfo_null
FROM financial_ratios;
"""

nulls = pd.read_sql(query, conn)

print("\nNull Counts:")
print(nulls.T)

conn.close()