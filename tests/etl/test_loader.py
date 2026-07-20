import sqlite3


DB = "nifty100.db"


def get_count(table):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(*) FROM {table}")
    value = cur.fetchone()[0]
    conn.close()
    return value


def test_companies_loaded():
    assert get_count("companies") >= 90


def test_profit_loss_loaded():
    assert get_count("profitandloss") > 0


def test_balance_sheet_loaded():
    assert get_count("balancesheet") > 0


def test_cashflow_loaded():
    assert get_count("cashflow") > 0


def test_market_cap_loaded():
    assert get_count("market_cap") > 0


def test_documents_loaded():
    assert get_count("documents") > 0


def test_sectors_loaded():
    assert get_count("sectors") > 0


def test_financial_ratios_loaded():
    assert get_count("financial_ratios") > 0


def test_peer_percentiles_loaded():
    assert get_count("peer_percentiles") > 0


def test_database_exists():
    conn = sqlite3.connect(DB)
    assert conn is not None
    conn.close()
