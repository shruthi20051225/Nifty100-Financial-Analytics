import sqlite3
import os
import pandas as pd


DB = "nifty100.db"


def test_financial_ratios_exists():

    conn = sqlite3.connect(DB)

    rows = conn.execute(
        "SELECT COUNT(*) FROM financial_ratios"
    ).fetchone()[0]

    conn.close()

    assert rows >= 1100


def test_peer_percentiles_exists():

    conn = sqlite3.connect(DB)

    rows = conn.execute(
        "SELECT COUNT(*) FROM peer_percentiles"
    ).fetchone()[0]

    conn.close()

    assert rows > 0


def test_screener_output_exists():

    assert os.path.exists(
        "output/screener_output.xlsx"
    )


def test_peer_report_exists():

    assert os.path.exists(
        "output/peer_comparison.xlsx"
    )


def test_radar_folder_exists():

    assert os.path.exists(
        "reports/radar_charts"
    )


def test_capital_allocation_exists():

    assert os.path.exists(
        "output/capital_allocation.csv"
    )


def test_ratio_edge_cases_exists():

    assert os.path.exists(
        "output/ratio_edge_cases.log"
    )


def test_quality_compounder():

    xls = pd.ExcelFile(
        "output/screener_output.xlsx"
    )

    df = pd.read_excel(
        xls,
        "Quality Compounder"
    )

    assert len(df) >= 5


def test_peer_sheets():

    xls = pd.ExcelFile(
        "output/peer_comparison.xlsx"
    )

    assert len(xls.sheet_names) >= 1


def test_database_exists():

    assert os.path.exists(DB)