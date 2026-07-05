import pytest

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
    debt_to_equity,
    interest_coverage,
    asset_turnover,
    net_debt,
)

# =====================================================
# DAY 8 – PROFITABILITY RATIOS
# =====================================================

def test_net_profit_margin_normal():
    assert net_profit_margin(100, 1000) == 10.0


def test_net_profit_margin_zero_sales():
    assert net_profit_margin(100, 0) is None


def test_operating_profit_margin_normal():
    assert operating_profit_margin(200, 1000) == 20.0


def test_operating_profit_margin_zero_sales():
    assert operating_profit_margin(200, 0) is None


def test_return_on_equity_normal():
    assert return_on_equity(150, 100, 400) == 30.0


def test_return_on_equity_negative_equity():
    assert return_on_equity(100, -50, -100) is None


def test_return_on_capital_employed_normal():
    assert return_on_capital_employed(
        ebit=250,
        equity_capital=100,
        reserves=400,
        borrowings=500,
    ) == 25.0


def test_return_on_assets_normal():
    assert return_on_assets(100, 500) == 20.0


def test_return_on_assets_zero_assets():
    assert return_on_assets(100, 0) is None


# =====================================================
# DAY 9 – LEVERAGE & EFFICIENCY
# =====================================================

def test_debt_to_equity_normal():
    assert debt_to_equity(500, 100, 400) == 1.0


def test_debt_to_equity_debt_free():
    assert debt_to_equity(0, 100, 400) == 0


def test_debt_to_equity_zero_equity():
    assert debt_to_equity(100, 0, 0) is None


def test_interest_coverage_normal():
    assert interest_coverage(
        operating_profit=300,
        other_income=100,
        interest=100,
    ) == 4.0


def test_interest_coverage_zero_interest():
    assert interest_coverage(
        operating_profit=300,
        other_income=50,
        interest=0,
    ) is None


def test_asset_turnover_normal():
    assert asset_turnover(1000, 500) == 2.0


def test_asset_turnover_zero_assets():
    assert asset_turnover(1000, 0) is None


def test_net_debt_positive():
    assert net_debt(500, 200) == 300


def test_net_debt_negative():
    assert net_debt(100, 250) == -150