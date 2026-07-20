"""
CAGR Engine
Sprint 2 - Day 10

Computes CAGR for Revenue, PAT and EPS
along with all required edge-case flags.
"""

from typing import Optional, Tuple

# ==========================================================
# Edge Case Flags
# ==========================================================

POSITIVE = "POSITIVE"
DECLINE_TO_LOSS = "DECLINE_TO_LOSS"
TURNAROUND = "TURNAROUND"
BOTH_NEGATIVE = "BOTH_NEGATIVE"
ZERO_BASE = "ZERO_BASE"
INSUFFICIENT = "INSUFFICIENT"


# ==========================================================
# Generic CAGR Calculator
# ==========================================================


def calculate_cagr(
    start_value: float, end_value: float, years: int
) -> Tuple[Optional[float], str]:
    """
    CAGR Formula

    ((End / Start) ** (1 / Years) - 1) * 100

    Returns:
        (value, flag)
    """

    if years <= 0:
        return None, INSUFFICIENT

    if start_value == 0:
        return None, ZERO_BASE

    if start_value > 0 and end_value > 0:
        cagr = ((end_value / start_value) ** (1 / years) - 1) * 100
        return round(cagr, 2), POSITIVE

    if start_value > 0 and end_value < 0:
        return None, DECLINE_TO_LOSS

    if start_value < 0 and end_value > 0:
        return None, TURNAROUND

    if start_value < 0 and end_value < 0:
        return None, BOTH_NEGATIVE

    return None, INSUFFICIENT


# ==========================================================
# Revenue CAGR
# ==========================================================


def revenue_cagr(start_sales: float, end_sales: float, years: int):
    return calculate_cagr(start_sales, end_sales, years)


# ==========================================================
# PAT CAGR
# ==========================================================


def pat_cagr(start_profit: float, end_profit: float, years: int):
    return calculate_cagr(start_profit, end_profit, years)


# ==========================================================
# EPS CAGR
# ==========================================================


def eps_cagr(start_eps: float, end_eps: float, years: int):
    return calculate_cagr(start_eps, end_eps, years)
