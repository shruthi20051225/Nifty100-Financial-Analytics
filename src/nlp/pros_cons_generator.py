import sqlite3
import pandas as pd
import os

DB = "nifty100.db"

OUTPUT = "output"

os.makedirs(OUTPUT, exist_ok=True)

conn = sqlite3.connect(DB)

companies = pd.read_sql(
    "SELECT id, company_name, roe_percentage, roce_percentage FROM companies",
    conn
)

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

conn.close()


def latest_ratio(company):

    df = ratios[ratios["company_id"] == company]

    if df.empty:
        return None

    df = df.sort_values("year")

    return df.iloc[-1]


rows = []


def add(company, typ, rule, text, confidence):

    rows.append({

        "company_id": company,

        "type": typ,

        "rule_id": rule,

        "text": text,

        "confidence_pct": confidence

    })


for _, company in companies.iterrows():

    cid = company["id"]

    ratio = latest_ratio(cid)

    if ratio is None:
        continue

    pro_count = 0
    con_count = 0

    roe = ratio["return_on_equity_pct"]
    de = ratio["debt_to_equity"]
    fcf = ratio["free_cash_flow_cr"]
    opm = ratio["operating_profit_margin_pct"]
    npm = ratio["net_profit_margin_pct"]
    icr = ratio["interest_coverage"]
    asset = ratio["asset_turnover"]
    eps = ratio["earnings_per_share"]
    payout = ratio["dividend_payout_ratio_pct"]
    cfo = ratio["cash_from_operations_cr"]

    # ----------------------------
    # PRO 01
    # ----------------------------

    if pd.notna(roe) and roe >= 20:

        add(
            cid,
            "pro",
            "PRO01",
            "Consistently high return on equity demonstrates exceptional capital efficiency.",
            95
        )

        pro_count += 1

    # ----------------------------

    if pd.notna(de) and de == 0:

        add(
            cid,
            "pro",
            "PRO02",
            "Debt-free balance sheet provides strong financial flexibility.",
            94
        )

        pro_count += 1

    # ----------------------------

    if pd.notna(fcf) and fcf > 0:

        add(
            cid,
            "pro",
            "PRO03",
            "Positive free cash flow indicates healthy business fundamentals.",
            90
        )

        pro_count += 1

    # ----------------------------

    if pd.notna(opm) and opm >= 25:

        add(
            cid,
            "pro",
            "PRO04",
            "Operating margin above 25% reflects pricing power and cost discipline.",
            88
        )

        pro_count += 1

    # ----------------------------

    if pd.notna(npm) and npm >= 15:

        add(
            cid,
            "pro",
            "PRO05",
            "Healthy net profit margin supports sustainable profitability.",
            86
        )

        pro_count += 1

    # ----------------------------

    if pd.notna(icr) and icr >= 10:

        add(
            cid,
            "pro",
            "PRO06",
            "High interest coverage indicates negligible debt servicing risk.",
            90
        )

        pro_count += 1

    # ----------------------------

    if pd.notna(asset) and asset >= 1:

        add(
            cid,
            "pro",
            "PRO07",
            "Efficient asset utilization supports business growth.",
            82
        )

        pro_count += 1

    # ----------------------------

    if pd.notna(eps) and eps > 20:

        add(
            cid,
            "pro",
            "PRO08",
            "Strong earnings per share reflects shareholder value creation.",
            80
        )

        pro_count += 1

    # ----------------------------

    if pd.notna(payout):

        if 20 <= payout <= 70:

            add(
                cid,
                "pro",
                "PRO09",
                "Balanced dividend payout policy supports long-term growth.",
                80
            )

            pro_count += 1

    # ----------------------------

    if pd.notna(cfo) and cfo > 0:

        add(
            cid,
            "pro",
            "PRO10",
            "Positive operating cash flow supports business sustainability.",
            84
        )

        pro_count += 1
            # ----------------------------
    # CON RULES
    # ----------------------------

    if pd.notna(de) and de > 2:

        add(
            cid,
            "con",
            "CON01",
            f"Debt-to-equity ratio of {de:.2f} is elevated and warrants monitoring.",
            95
        )

        con_count += 1

    if pd.notna(fcf) and fcf < 0:

        add(
            cid,
            "con",
            "CON02",
            "Negative free cash flow raises concern about cash generation quality.",
            92
        )

        con_count += 1

    if pd.notna(opm) and opm < 10:

        add(
            cid,
            "con",
            "CON03",
            "Operating margin is relatively low and may indicate pricing pressure.",
            90
        )

        con_count += 1

    if pd.notna(npm) and npm < 5:

        add(
            cid,
            "con",
            "CON04",
            "Low net profit margin indicates weak profitability.",
            88
        )

        con_count += 1

    if pd.notna(icr) and icr < 1.5:

        add(
            cid,
            "con",
            "CON05",
            "Interest coverage below 1.5x suggests financial stress.",
            95
        )

        con_count += 1

    if pd.notna(roe) and roe < 10:

        add(
            cid,
            "con",
            "CON06",
            "Low return on equity indicates inefficient capital utilization.",
            85
        )

        con_count += 1

    if pd.notna(asset) and asset < 0.50:

        add(
            cid,
            "con",
            "CON07",
            "Low asset turnover indicates inefficient utilization of assets.",
            80
        )

        con_count += 1

    if pd.notna(payout) and payout > 100:

        add(
            cid,
            "con",
            "CON08",
            "Dividend payout above 100% may not be sustainable.",
            90
        )

        con_count += 1

    if pd.notna(cfo) and cfo < 0:

        add(
            cid,
            "con",
            "CON09",
            "Negative operating cash flow weakens business quality.",
            90
        )

        con_count += 1

    if pd.notna(eps) and eps < 5:

        add(
            cid,
            "con",
            "CON10",
            "Low earnings per share limits shareholder value creation.",
            75
        )

        con_count += 1

    # ----------------------------
    # FALLBACK RULES
    # ----------------------------

    if pro_count == 0:

        add(
            cid,
            "pro",
            "PRO99",
            "Business demonstrates stable operating performance.",
            65
        )

    if con_count == 0:

        add(
            cid,
            "con",
            "CON99",
            "Future financial performance should continue to be monitored.",
            65
        )

# ==========================================
# CREATE OUTPUT
# ==========================================

output = pd.DataFrame(rows)

output = output[
    output["confidence_pct"] >= 60
]

output = output.sort_values(
    [
        "company_id",
        "type"
    ]
)

output.to_csv(
    "output/pros_cons_generated.csv",
    index=False
)

print("=" * 60)
print("Pros & Cons Generator Completed")
print("=" * 60)
print("Companies Covered :", output["company_id"].nunique())
print("Total Signals     :", len(output))
print("Output File       : output/pros_cons_generated.csv")
print("=" * 60)