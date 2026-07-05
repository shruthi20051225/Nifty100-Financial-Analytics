"""
Sprint 2 - Day 11
Cash Flow KPI Engine
"""

from typing import Optional


# ==========================================================
# FREE CASH FLOW
# ==========================================================

def free_cash_flow(
    operating_activity: float,
    investing_activity: float
) -> float:
    """
    FCF = CFO + CFI
    (Investing Activity is usually negative)
    """
    return operating_activity + investing_activity


# ==========================================================
# CFO QUALITY SCORE
# ==========================================================

def cfo_quality_score(
    average_cfo: float,
    average_pat: float
):
    """
    CFO / PAT
    """

    if average_pat == 0:
        return None

    score = average_cfo / average_pat

    if score > 1:
        return "High Quality"

    if score >= 0.5:
        return "Moderate"

    return "Accrual Risk"


# ==========================================================
# CAPEX INTENSITY
# ==========================================================

def capex_intensity(
    investing_activity: float,
    sales: float
):
    """
    abs(CFI) / Sales
    """

    if sales == 0:
        return None

    value = abs(investing_activity) / sales * 100

    if value < 3:
        label = "Asset Light"

    elif value <= 8:
        label = "Moderate"

    else:
        label = "Capital Intensive"

    return round(value,2), label


# ==========================================================
# FCF CONVERSION
# ==========================================================

def fcf_conversion(
    free_cash_flow_value: float,
    operating_profit: float
):

    if operating_profit == 0:
        return None

    return round(
        free_cash_flow_value /
        operating_profit * 100,
        2
    )


# ==========================================================
# CAPITAL ALLOCATION
# ==========================================================

def capital_allocation_pattern(
    cfo: float,
    cfi: float,
    cff: float
):
    """
    8-pattern classifier
    """

    signs = (
        "+" if cfo >= 0 else "-",
        "+" if cfi >= 0 else "-",
        "+" if cff >= 0 else "-"
    )

    patterns = {

        ("+","-","-"):
            "Reinvestor",

        ("+","+","-"):
            "Liquidating Assets",

        ("-","+","+"):
            "Distress Signal",

        ("-","-","+"):
            "Growth Funded by Debt",

        ("+","+","+"):
            "Cash Accumulator",

        ("-","-","-"):
            "Pre-Revenue",

        ("+","-","+"):
            "Mixed"
    }

    return patterns.get(
        signs,
        "Unknown"
    )