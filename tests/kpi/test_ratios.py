"""
Unit Tests for Financial Ratio Engine
Sprint 2 - Day 08 & Day 09
"""

import pytest

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    roe,
    roce,
    roa,
    debt_to_equity,
    high_leverage_flag,
    interest_coverage,
    icr_label,
    icr_warning,
    net_debt,
    asset_turnover,
)


# =====================================================
# DAY 08 TESTS
# =====================================================

def test_net_profit_margin():
    assert net_profit_margin(100, 500) == 20.00


def test_net_profit_margin_zero_sales():
    assert net_profit_margin(100, 0) is None


def test_operating_profit_margin():
    assert operating_profit_margin(120, 600) == 20.00


def test_operating_profit_margin_zero_sales():
    assert operating_profit_margin(120, 0) is None


def test_roe():
    assert roe(100, 200, 300) == 20.00


def test_negative_equity():
    assert roe(100, -500, 100) is None


def test_roce():
    assert roce(150, 300, 400, 300) == 15.00


def test_roa():
    assert roa(100, 500) == 20.00


# =====================================================
# DAY 09 TESTS
# =====================================================

def test_debt_to_equity():
    assert debt_to_equity(200, 100, 100) == 1.00


def test_debt_free():
    assert debt_to_equity(0, 100, 100) == 0


def test_interest_coverage():
    assert interest_coverage(100, 20, 20) == 6.00


def test_interest_zero():
    assert interest_coverage(100, 20, 0) is None


def test_icr_label():
    assert icr_label(0) == "Debt Free"


def test_icr_warning():
    assert icr_warning(1.2) is True


def test_high_leverage():
    assert high_leverage_flag(6, "Industrials") is True


def test_high_leverage_financial():
    assert high_leverage_flag(6, "Financials") is False


def test_net_debt():
    assert net_debt(500, 200) == 300


def test_asset_turnover():
    assert asset_turnover(1000, 500) == 2.00