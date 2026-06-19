# src/etl/normaliser.py

import re

def normalize_year(year):
    return int(str(year).strip())

def normalize_ticker(ticker):
    ticker = str(ticker).upper().strip()
    ticker = re.sub(r"[^A-Z0-9]", "", ticker)
    return ticker
