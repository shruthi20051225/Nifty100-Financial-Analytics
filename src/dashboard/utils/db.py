import sqlite3
import pandas as pd
import streamlit as st

DB = "nifty100.db"


@st.cache_data(ttl=600)
def get_companies():

    conn = sqlite3.connect(DB)

    df = pd.read_sql(
        "SELECT * FROM companies",
        conn
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_ratios():

    conn = sqlite3.connect(DB)

    df = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_profit_loss():

    conn = sqlite3.connect(DB)

    df = pd.read_sql(
        "SELECT * FROM profitandloss",
        conn
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_balance_sheet():

    conn = sqlite3.connect(DB)

    df = pd.read_sql(
        "SELECT * FROM balancesheet",
        conn
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_cashflow():

    conn = sqlite3.connect(DB)

    df = pd.read_sql(
        "SELECT * FROM cashflow",
        conn
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_peer_percentiles():

    conn = sqlite3.connect(DB)

    df = pd.read_sql(
        "SELECT * FROM peer_percentiles",
        conn
    )

    conn.close()

    return df

@st.cache_data(ttl=600)
def get_latest_ratios():

    conn = sqlite3.connect(DB)

    df = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn
    )

    conn.close()

    return df

@st.cache_data(ttl=600)
def get_pros_cons():

    conn = sqlite3.connect(DB)

    df = pd.read_sql(
        "SELECT * FROM prosandcons",
        conn
    )

    conn.close()

    return df
@st.cache_data(ttl=600)
def get_documents():

    conn = sqlite3.connect(DB)

    df = pd.read_sql(
        "SELECT * FROM documents",
        conn
    )

    conn.close()

    return df