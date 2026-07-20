from typing import Optional

# ==========================================================
# DAY 08 – PROFITABILITY RATIOS
# ==========================================================


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


def return_on_equity(
    net_profit: float, equity_capital: float, reserves: float
) -> Optional[float]:
    """Return on Equity (%)"""

    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return round((net_profit / equity) * 100, 2)


def return_on_capital_employed(
    ebit: float,
    equity_capital: float,
    reserves: float,
    borrowings: float,
) -> Optional[float]:
    """Return on Capital Employed (%)"""

    capital = equity_capital + reserves + borrowings

    if capital <= 0:
        return None

    return round((ebit / capital) * 100, 2)


def return_on_assets(net_profit: float, total_assets: float) -> Optional[float]:
    """Return on Assets (%)"""

    if total_assets == 0:
        return None

    return round((net_profit / total_assets) * 100, 2)


# ==========================================================
# DAY 09 – LEVERAGE & EFFICIENCY
# ==========================================================


def debt_to_equity(
    borrowings: float, equity_capital: float, reserves: float
) -> Optional[float]:
    """Debt to Equity Ratio"""

    equity = equity_capital + reserves

    if borrowings == 0:
        return 0

    if equity <= 0:
        return None

    return round(borrowings / equity, 2)


def high_leverage_flag(de_ratio: Optional[float], broad_sector: str) -> bool:
    """High leverage warning"""

    if de_ratio is None:
        return False

    if broad_sector.lower() == "financials":
        return False

    return de_ratio > 5


def interest_coverage(
    operating_profit: float, other_income: float, interest: float
) -> Optional[float]:
    """Interest Coverage Ratio"""

    if interest == 0:
        return None

    return round(
        (operating_profit + other_income) / interest,
        2,
    )


def icr_label(icr):
    """Debt Free label"""

    if icr is None:
        return "Debt Free"

    return ""


def interest_warning(icr):
    """Interest warning"""

    if icr is None:
        return False

    return icr < 1.5


def net_debt(borrowings: float, investments: float) -> float:
    """Net Debt"""

    return borrowings - investments


def asset_turnover(sales: float, total_assets: float) -> Optional[float]:
    """Asset Turnover"""

    if total_assets == 0:
        return None

    return round(sales / total_assets, 2)
