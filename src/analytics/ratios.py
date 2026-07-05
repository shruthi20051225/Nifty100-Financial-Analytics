from typing import Optional


def net_profit_margin(net_profit: float, sales: float) -> Optional[float]:
    """Net Profit Margin (%)"""
    if sales == 0:
        return None
    return round((net_profit / sales) * 100, 2)


def operating_profit_margin(operating_profit: float, sales: float) -> Optional[float]:
    """Operating Profit Margin (%)"""
    if sales == 0:
        return None
    return round((operating_profit / sales) * 100, 2)


def roe(net_profit: float, equity: float, reserves: float) -> Optional[float]:
    """Return on Equity (%)"""
    capital = equity + reserves

    if capital <= 0:
        return None

    return round((net_profit / capital) * 100, 2)


def roce(
    ebit: float,
    equity: float,
    reserves: float,
    borrowings: float,
) -> Optional[float]:
    """Return on Capital Employed (%)"""

    capital = equity + reserves + borrowings

    if capital <= 0:
        return None

    return round((ebit / capital) * 100, 2)


def roa(net_profit: float, total_assets: float) -> Optional[float]:
    """Return on Assets (%)"""

    if total_assets == 0:
        return None

    return round((net_profit / total_assets) * 100, 2)

def debt_to_equity(borrowings: float, equity: float, reserves: float):
    """
    Debt to Equity Ratio
    """

    if borrowings == 0:
        return 0

    capital = equity + reserves

    if capital <= 0:
        return None

    return round(borrowings / capital, 2)


def high_leverage_flag(de_ratio, sector):
    """
    High leverage warning.
    Financial companies are exempt.
    """

    if sector == "Financials":
        return False

    if de_ratio is None:
        return False

    return de_ratio > 5


def interest_coverage(
    operating_profit,
    other_income,
    interest
):
    """
    Interest Coverage Ratio
    """

    if interest == 0:
        return None

    return round(
        (operating_profit + other_income) / interest,
        2
    )


def icr_label(interest):
    """
    Debt-free companies
    """

    if interest == 0:
        return "Debt Free"

    return ""


def icr_warning(icr):
    """
    Company unable to comfortably cover interest.
    """

    if icr is None:
        return False

    return icr < 1.5


def net_debt(
    borrowings,
    investments
):
    """
    Net Debt
    """

    return borrowings - investments


def asset_turnover(
    sales,
    total_assets
):
    """
    Asset Turnover Ratio
    """

    if total_assets == 0:
        return None

    return round(
        sales / total_assets,
        2
    )

