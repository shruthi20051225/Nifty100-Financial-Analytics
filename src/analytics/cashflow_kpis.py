from typing import Optional


def free_cash_flow(
    operating_activity: float,
    investing_activity: float
) -> float:
    """
    Free Cash Flow
    FCF = CFO + Investing Activity
    """
    return operating_activity + investing_activity


def cfo_quality_score(
    cfo: float,
    pat: float
) -> Optional[str]:
    """
    CFO Quality
    """

    if pat == 0:
        return None

    ratio = cfo / pat

    if ratio > 1:
        return "High Quality"

    elif ratio >= 0.5:
        return "Moderate"

    else:
        return "Accrual Risk"


def capex_intensity(
    investing_activity: float,
    sales: float
):
    """
    CapEx Intensity (%)
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

    return round(value, 2), label


def fcf_conversion(
    free_cash_flow_value: float,
    operating_profit: float
):
    """
    FCF Conversion
    """

    if operating_profit == 0:
        return None

    return round(
        free_cash_flow_value /
        operating_profit * 100,
        2
    )


def capital_allocation_pattern(
    cfo,
    cfi,
    cff,
    cfo_pat_ratio=1
):
    """
    8-pattern capital allocation classifier
    """

    signs = (
        "+" if cfo >= 0 else "-",
        "+" if cfi >= 0 else "-",
        "+" if cff >= 0 else "-"
    )

    if signs == ("+", "-", "-"):
        if cfo_pat_ratio > 1:
            return "Shareholder Returns"
        return "Reinvestor"

    if signs == ("+", "+", "-"):
        return "Liquidating Assets"

    if signs == ("-", "+", "+"):
        return "Distress Signal"

    if signs == ("-", "-", "+"):
        return "Growth Funded by Debt"

    if signs == ("+", "+", "+"):
        return "Cash Accumulator"

    if signs == ("-", "-", "-"):
        return "Pre-Revenue"

    if signs == ("+", "-", "+"):
        return "Mixed"

    return "Unknown"