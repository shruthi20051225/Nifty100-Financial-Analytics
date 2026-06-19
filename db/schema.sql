PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS companies (
    company_id INTEGER PRIMARY KEY,
    company_name TEXT,
    ticker TEXT UNIQUE,
    sector TEXT
);

CREATE TABLE IF NOT EXISTS sectors (
    sector_id INTEGER PRIMARY KEY,
    sector_name TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS profitandloss (
    company_id INTEGER,
    year INTEGER,
    sales REAL,
    net_profit REAL,
    eps REAL,
    PRIMARY KEY (company_id, year),
    FOREIGN KEY (company_id)
        REFERENCES companies(company_id)
);

CREATE TABLE IF NOT EXISTS balancesheet (
    company_id INTEGER,
    year INTEGER,
    total_assets REAL,
    total_liabilities REAL,
    PRIMARY KEY (company_id, year),
    FOREIGN KEY (company_id)
        REFERENCES companies(company_id)
);

CREATE TABLE IF NOT EXISTS cashflow (
    company_id INTEGER,
    year INTEGER,
    operating_cashflow REAL,
    investing_cashflow REAL,
    financing_cashflow REAL,
    PRIMARY KEY (company_id, year),
    FOREIGN KEY (company_id)
        REFERENCES companies(company_id)
);

CREATE TABLE IF NOT EXISTS analysis (
    company_id INTEGER,
    year INTEGER,
    remarks TEXT,
    PRIMARY KEY (company_id, year),
    FOREIGN KEY (company_id)
        REFERENCES companies(company_id)
);

CREATE TABLE IF NOT EXISTS documents (
    document_id INTEGER PRIMARY KEY,
    company_id INTEGER,
    document_name TEXT,
    url TEXT,
    FOREIGN KEY (company_id)
        REFERENCES companies(company_id)
);

CREATE TABLE IF NOT EXISTS prosandcons (
    id INTEGER PRIMARY KEY,
    company_id INTEGER,
    pros TEXT,
    cons TEXT,
    FOREIGN KEY (company_id)
        REFERENCES companies(company_id)
);

CREATE TABLE IF NOT EXISTS stock_prices (
    company_id INTEGER,
    price_date DATE,
    open_price REAL,
    high_price REAL,
    low_price REAL,
    close_price REAL,
    volume INTEGER,
    PRIMARY KEY (company_id, price_date),
    FOREIGN KEY (company_id)
        REFERENCES companies(company_id)
);

CREATE TABLE IF NOT EXISTS financial_ratios (
    company_id INTEGER,
    year INTEGER,
    roe REAL,
    roce REAL,
    debt_equity REAL,
    pe_ratio REAL,
    PRIMARY KEY (company_id, year),
    FOREIGN KEY (company_id)
        REFERENCES companies(company_id)
);

CREATE TABLE IF NOT EXISTS peer_groups (
    company_id INTEGER,
    peer_company TEXT,
    FOREIGN KEY (company_id)
        REFERENCES companies(company_id)
);