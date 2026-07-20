import sqlite3
import pandas as pd
import re
import os

DB = "nifty100.db"

OUTPUT_FOLDER = "output"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

conn = sqlite3.connect(DB)

analysis = pd.read_sql("SELECT * FROM analysis", conn)

try:
    ratios = pd.read_sql(
        "SELECT company_id, revenue_cagr_5yr, pat_cagr_5yr FROM financial_ratios", conn
    )
except Exception:
    ratios = pd.DataFrame()

conn.close()

pattern = re.compile(r"(\d+)\s*Years?:?\s*(-?[\d.]+)%")

parsed_rows = []
failed_rows = []

metric_columns = [
    "compounded_sales_growth",
    "compounded_profit_growth",
    "stock_price_cagr",
    "roe",
]

for _, row in analysis.iterrows():

    company = row["company_id"]

    for metric in metric_columns:

        value = str(row[metric])

        match = pattern.search(value)

        if match:

            years = int(match.group(1))
            pct = float(match.group(2))

            parsed_rows.append(
                {
                    "company_id": company,
                    "metric_type": metric,
                    "period_years": years,
                    "value_pct": pct,
                }
            )

        else:

            failed_rows.append(
                {"company_id": company, "metric_type": metric, "raw_text": value}
            )

parsed = pd.DataFrame(parsed_rows)
failures = pd.DataFrame(failed_rows)

parsed.to_csv("output/analysis_parsed.csv", index=False)

failures.to_csv("output/parse_failures.csv", index=False)

# ---------------------------
# Optional validation
# ---------------------------

if not ratios.empty:

    review = []

    for _, row in parsed.iterrows():

        cid = row["company_id"]

        metric = row["metric_type"]

        value = row["value_pct"]

        ratio_row = ratios[ratios["company_id"] == cid]

        if ratio_row.empty:
            continue

        if metric == "compounded_sales_growth":

            calc = ratio_row.iloc[0]["revenue_cagr_5yr"]

        elif metric == "compounded_profit_growth":

            calc = ratio_row.iloc[0]["pat_cagr_5yr"]

        else:
            continue

        if pd.notna(calc):

            diff = abs(value - calc)

            if diff > 5:

                review.append(
                    {
                        "company_id": cid,
                        "metric": metric,
                        "parsed_value": value,
                        "computed_value": calc,
                        "difference": round(diff, 2),
                    }
                )

    pd.DataFrame(review).to_csv("output/cagr_manual_review.csv", index=False)

print("=" * 50)
print("Analysis Parser Completed")
print("=" * 50)
print("Parsed Rows :", len(parsed))
print("Failed Rows :", len(failures))

review_df = pd.DataFrame(review)

review_df.to_csv("output/cagr_manual_review.csv", index=False)

print("Generated : output/cagr_manual_review.csv")

print("Generated : output/analysis_parsed.csv")
print("Generated : output/parse_failures.csv")
