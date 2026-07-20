import numpy as np
import pandas as pd


def normalize(series):

    series = series.fillna(0)

    p10 = np.percentile(series, 10)
    p90 = np.percentile(series, 90)

    series = series.clip(p10, p90)

    if p90 == p10:
        return pd.Series([50] * len(series), index=series.index)

    return ((series - p10) / (p90 - p10)) * 100


def compute_composite_score(df):

    df = df.copy()

    # -------------------------
    # Profitability (35%)
    # -------------------------

    roe = normalize(df["return_on_equity_pct"])

    roce = normalize(df["return_on_equity_pct"])  # replace later with ROCE column

    npm = normalize(df["net_profit_margin_pct"])

    profitability = roe * 0.15 + roce * 0.10 + npm * 0.10

    # -------------------------
    # Cash Quality (30%)
    # -------------------------

    fcf = normalize(df["free_cash_flow_cr"])

    cfo = normalize(df["cash_from_operations_cr"])

    fcf_flag = (df["free_cash_flow_cr"] > 0).astype(int) * 100

    cash_quality = fcf * 0.15 + cfo * 0.10 + fcf_flag * 0.05

    # -------------------------
    # Growth (20%)
    # -------------------------

    if "revenue_cagr_5yr" in df.columns:
        revenue = normalize(df["revenue_cagr_5yr"])
    else:
        revenue = 0

    if "pat_cagr_5yr" in df.columns:
        pat = normalize(df["pat_cagr_5yr"])
    else:
        pat = 0

    growth = revenue * 0.10 + pat * 0.10

    # -------------------------
    # Leverage (15%)
    # -------------------------

    de = normalize(1 / (df["debt_to_equity"] + 1))

    icr = normalize(df["interest_coverage"].fillna(999))

    leverage = de * 0.10 + icr * 0.05

    df["composite_quality_score"] = (
        profitability + cash_quality + growth + leverage
    ).round(2)

    return df
