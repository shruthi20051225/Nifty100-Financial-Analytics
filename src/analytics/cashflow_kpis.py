import sqlite3
import pandas as pd
import numpy as np
import os

DB = "nifty100.db"

OUTPUT = "output"

os.makedirs(OUTPUT, exist_ok=True)

conn = sqlite3.connect(DB)

cashflow = pd.read_sql(
    "SELECT * FROM cashflow",
    conn
)

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

companies = pd.read_sql(
    "SELECT id, company_name FROM companies",
    conn
)

conn.close()


def latest(df):

    return (
        df.sort_values("year")
        .groupby("company_id")
        .tail(1)
    )


latest_cf = latest(cashflow)

results = []

alerts = []
for _, row in latest_cf.iterrows():

    company_id = row["company_id"]

    company = companies[
        companies["id"] == company_id
    ]

    if company.empty:
        continue

    company_name = company.iloc[0]["company_name"]

    ratio_history = (
        ratios[
            ratios["company_id"] == company_id
        ]
        .sort_values("year")
    )

    if ratio_history.empty:
        continue

    latest_ratio = ratio_history.iloc[-1]

    operating = row["operating_activity"]
    investing = row["investing_activity"]
    financing = row["financing_activity"]
    net_cash = row["net_cash_flow"]

    sales = latest_ratio.get("sales", np.nan)

    free_cash = latest_ratio.get(
        "free_cash_flow_cr",
        np.nan
    )

    cash_from_operations = latest_ratio.get(
        "cash_from_operations_cr",
        np.nan
    )

    merged = pd.merge(
        cashflow[
            cashflow["company_id"] == company_id
        ],
        ratio_history,
        on=["company_id", "year"],
        how="inner"
    )
        # ------------------------------------
    # CFO QUALITY
    # ------------------------------------

    quality_scores = []

    for _, r in merged.iterrows():

        profit = r.get(
            "net_profit_margin_pct",
            np.nan
        )

        cfo = r["operating_activity"]

        if pd.notna(profit) and profit != 0:

            quality_scores.append(
                cfo / profit
            )

    if len(quality_scores):

        cfo_quality = np.mean(
            quality_scores
        )

    else:

        cfo_quality = np.nan

    if pd.isna(cfo_quality):

        cfo_label = "Unknown"

    elif cfo_quality > 1:

        cfo_label = "High Quality"

    elif cfo_quality >= 0.5:

        cfo_label = "Moderate"

    else:

        cfo_label = "Accrual Risk"

    # ------------------------------------
    # CAPEX INTENSITY
    # ------------------------------------

    if pd.notna(sales) and sales != 0:

        capex_intensity = (
            abs(investing) / sales
        ) * 100

    else:

        capex_intensity = np.nan

    if pd.isna(capex_intensity):

        capex_label = "Unknown"

    elif capex_intensity < 3:

        capex_label = "Asset Light"

    elif capex_intensity <= 8:

        capex_label = "Moderate"

    else:

        capex_label = "Capital Intensive"

    # ------------------------------------
    # FCF CONVERSION
    # ------------------------------------

    if (
        pd.notna(free_cash)
        and pd.notna(cash_from_operations)
        and cash_from_operations != 0
    ):

        fcf_conversion = (
            free_cash
            / cash_from_operations
        ) * 100

    else:

        fcf_conversion = np.nan

    # ------------------------------------
    # DISTRESS
    # ------------------------------------

    distress = (
        pd.notna(operating)
        and pd.notna(financing)
        and operating < 0
        and financing > 0
    )

    # ------------------------------------
    # DELEVERAGING
    # ------------------------------------

    deleveraging = (
        pd.notna(financing)
        and financing < 0
    )

    # ------------------------------------
    # CAPITAL ALLOCATION
    # ------------------------------------

    if distress:

        capital_label = "Distress Signal"

    elif deleveraging:

        capital_label = "Deleveraging"

    elif (
        operating > 0
        and investing < 0
        and financing < 0
    ):

        capital_label = "Shareholder Return"

    elif (
        operating > 0
        and investing < 0
    ):

        capital_label = "Growth Investment"

    elif operating > 0:

        capital_label = "Cash Generator"

    else:

        capital_label = "Balanced"
            # ------------------------------------
    # FCF CAGR (Simple Estimate)
    # ------------------------------------

    fcf_history = (
        ratio_history["free_cash_flow_cr"]
        .dropna()
        .tolist()
    )

    if len(fcf_history) >= 5:

        first = fcf_history[-5]
        last = fcf_history[-1]

        if first > 0 and last > 0:

            fcf_cagr = (
                ((last / first) ** (1 / 4)) - 1
            ) * 100

        else:

            fcf_cagr = np.nan

    else:

        fcf_cagr = np.nan

    # ------------------------------------
    # SAVE RESULT
    # ------------------------------------

    results.append({

        "company_id": company_id,

        "company_name": company_name,

        "latest_year": row["year"],

        "operating_activity": operating,

        "investing_activity": investing,

        "financing_activity": financing,

        "net_cash_flow": net_cash,

        "cfo_quality_score": round(cfo_quality, 2)
        if pd.notna(cfo_quality) else np.nan,

        "cfo_quality_label": cfo_label,

        "capex_intensity_pct": round(capex_intensity, 2)
        if pd.notna(capex_intensity) else np.nan,

        "capex_label": capex_label,

        "fcf_cagr_5yr": round(fcf_cagr, 2)
        if pd.notna(fcf_cagr) else np.nan,

        "fcf_conversion_pct": round(fcf_conversion, 2)
        if pd.notna(fcf_conversion) else np.nan,

        "distress_flag": distress,

        "deleveraging_flag": deleveraging,

        "capital_allocation_label": capital_label

    })

    if distress:

        alerts.append({

            "company_id": company_id,

            "company_name": company_name,

            "operating_activity": operating,

            "financing_activity": financing,

            "net_cash_flow": net_cash

        })
        cashflow_df = pd.DataFrame(results)

alerts_df = pd.DataFrame(alerts)

cashflow_df.to_excel(
    "output/cashflow_intelligence.xlsx",
    index=False
)

alerts_df.to_csv(
    "output/distress_alerts.csv",
    index=False
)

print("=" * 60)
print("Cash Flow Intelligence Completed")
print("=" * 60)
print("Companies Processed :", len(cashflow_df))
print("Distress Companies  :", len(alerts_df))
print("Excel Saved         : output/cashflow_intelligence.xlsx")
print("Alerts Saved        : output/distress_alerts.csv")
print("=" * 60)