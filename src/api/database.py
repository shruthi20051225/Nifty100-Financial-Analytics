import sqlite3

DB = "nifty100.db"


def get_connection():
    """
    Returns SQLite connection.
    """
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn
