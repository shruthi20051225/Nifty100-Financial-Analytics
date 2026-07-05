from src.analytics.cashflow_kpis import *


def test_fcf():

    assert free_cash_flow(
        500,
        -120
    ) == 380


def test_quality_high():

    assert cfo_quality_score(
        200,
        100
    ) == "High Quality"


def test_quality_moderate():

    assert cfo_quality_score(
        70,
        100
    ) == "Moderate"


def test_quality_risk():

    assert cfo_quality_score(
        20,
        100
    ) == "Accrual Risk"


def test_capex():

    value,label = capex_intensity(
        -60,
        1000
    )

    assert label=="Moderate"


def test_fcf_conversion():

    assert fcf_conversion(
        400,
        500
    )==80


def test_pattern():

    assert capital_allocation_pattern(
        100,
        -50,
        -30
    )=="Reinvestor"


def test_pattern2():

    assert capital_allocation_pattern(
        -20,
        -50,
        -10
    )=="Pre-Revenue"