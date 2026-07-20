

from src.analytics.cagr import (
    calculate_cagr,
    revenue_cagr,
    pat_cagr,
    eps_cagr,
    POSITIVE,
    DECLINE_TO_LOSS,
    TURNAROUND,
    BOTH_NEGATIVE,
    ZERO_BASE,
    INSUFFICIENT,
)

# =====================================================
# Generic CAGR
# =====================================================


def test_normal_cagr():

    value, flag = calculate_cagr(100, 200, 5)

    assert flag == POSITIVE
    assert value is not None


def test_decline_to_loss():

    value, flag = calculate_cagr(100, -20, 5)

    assert value is None
    assert flag == DECLINE_TO_LOSS


def test_turnaround():

    value, flag = calculate_cagr(-50, 100, 5)

    assert value is None
    assert flag == TURNAROUND


def test_both_negative():

    value, flag = calculate_cagr(-20, -50, 5)

    assert value is None
    assert flag == BOTH_NEGATIVE


def test_zero_base():

    value, flag = calculate_cagr(0, 200, 5)

    assert value is None
    assert flag == ZERO_BASE


def test_insufficient():

    value, flag = calculate_cagr(100, 200, 0)

    assert value is None
    assert flag == INSUFFICIENT


# =====================================================
# Revenue CAGR
# =====================================================


def test_revenue_cagr():

    value, flag = revenue_cagr(1000, 1800, 5)

    assert flag == POSITIVE
    assert value is not None


# =====================================================
# PAT CAGR
# =====================================================


def test_pat_cagr():

    value, flag = pat_cagr(200, 400, 5)

    assert flag == POSITIVE
    assert value is not None


# =====================================================
# EPS CAGR
# =====================================================


def test_eps_cagr():

    value, flag = eps_cagr(20, 40, 5)

    assert flag == POSITIVE
    assert value is not None


# =====================================================
# Extra Positive Test
# =====================================================


def test_positive_case():

    value, flag = calculate_cagr(50, 100, 3)

    assert flag == POSITIVE
