# 📈 Nifty100 Financial Analytics Platform

## Overview

The **Nifty100 Financial Analytics Platform** is an end-to-end financial data analytics project that analyzes the Nifty 100 companies using financial statements, key performance indicators (KPIs), screening tools, peer benchmarking, capital allocation analysis, valuation metrics, and an interactive Streamlit dashboard.

The project demonstrates a complete analytics pipeline consisting of data ingestion, database management, financial ratio computation, business analytics, peer comparison, valuation analysis, and dashboard visualization.

---

# Project Objectives

* Build a centralized SQLite database for Nifty 100 financial data.
* Compute profitability, leverage, liquidity, efficiency, growth, and cash flow KPIs.
* Develop a financial screener with customizable filters.
* Perform peer group benchmarking using percentile rankings.
* Analyze capital allocation patterns.
* Generate valuation metrics for investment analysis.
* Build an interactive Streamlit dashboard for financial exploration.

---

# Technology Stack

* Python
* Pandas
* NumPy
* SQLite
* Streamlit
* Plotly
* Matplotlib
* OpenPyXL
* Pytest

---

# Project Structure

```
Nifty100 Financial Analytics
│
├── config/
├── data/
├── db/
├── docs/
├── logs/
├── notebooks/
├── output/
├── pages/
├── reports/
├── src/
│   ├── analytics/
│   ├── dashboard/
│   ├── screener/
│   └── utils/
├── tests/
├── nifty100.db
├── app.py
├── requirements.txt
└── README.md
```

---

# Sprint 1 – Database & ETL Pipeline

## Objectives

* Import raw financial datasets
* Clean and validate data
* Build SQLite database
* Load structured financial tables

## Work Completed

* Imported company master dataset
* Imported Profit & Loss statements
* Imported Balance Sheet data
* Imported Cash Flow statements
* Imported Market Capitalization data
* Imported Annual Reports metadata
* Imported Sector classifications
* Created SQLite database
* Implemented ETL pipeline
* Added database validation scripts

## Database Tables

* companies
* profitandloss
* balancesheet
* cashflow
* market_cap
* documents
* sectors
* financial_ratios
* peer_percentiles

---

# Sprint 2 – Financial KPI Engine

## Objectives

* Calculate financial ratios
* Generate CAGR metrics
* Compute cash flow KPIs
* Perform capital allocation analysis

## Implemented KPIs

### Profitability

* Return on Equity (ROE)
* Return on Capital Employed (ROCE)
* Net Profit Margin
* Operating Profit Margin

### Leverage

* Debt to Equity Ratio
* Interest Coverage Ratio

### Efficiency

* Asset Turnover
* Working Capital Metrics

### Growth

* Revenue CAGR
* Profit CAGR
* EPS CAGR

### Cash Flow

* Free Cash Flow
* CFO Quality
* FCF Conversion
* CapEx Intensity

### Capital Allocation

* Classified companies into multiple capital allocation patterns.

---

# Sprint 3 – Financial Screener & Peer Analysis

## Objectives

* Build financial screening engine
* Generate preset screeners
* Compute peer percentile rankings
* Produce comparison reports

## Financial Screeners

Implemented six predefined screeners:

* Quality Compounder
* Value Pick
* Growth Accelerator
* Dividend Champion
* Debt-Free Blue Chip
* Turnaround Watch

## Peer Analysis

Computed percentile rankings for:

* ROE
* ROCE
* Net Profit Margin
* Revenue CAGR
* Profit CAGR
* EPS CAGR
* Debt to Equity
* Asset Turnover
* Interest Coverage
* Free Cash Flow

Generated:

* Screener Output
* Peer Comparison Report
* Radar Charts

---

# Sprint 4 – Streamlit Dashboard & Valuation Module

## Objectives

Develop an interactive financial analytics dashboard and valuation engine.

## Dashboard Screens

### Home

* Company summary
* KPI cards
* Industry overview

### Company Profile

* Company details
* Revenue trend
* Profit trend
* Financial KPIs
* Pros & Cons

### Financial Screener

* Interactive filters
* Preset screeners
* Live filtering
* CSV Export

### Peer Comparison

* Radar chart
* Peer percentile rankings
* Comparative metrics

### Trend Analysis

* Historical KPI trends
* Multi-metric comparison

### Sector Analysis

* Sector-wise analytics
* Bubble charts
* Median sector KPIs

### Capital Allocation

* Treemap visualization
* Capital allocation categories

### Annual Reports

* Annual report browser
* Download links

---

# Valuation Module

Computed:

* FCF Yield
* P/E Ratio
* P/B Ratio
* EV/EBITDA
* Dividend Yield
* Valuation Flags

Generated:

* valuation_summary.xlsx
* valuation_flags.csv

---

# Outputs Generated

## Excel Reports

* valuation_summary.xlsx
* screener_output.xlsx
* peer_comparison.xlsx
* capital_allocation.csv

## CSV Reports

* valuation_flags.csv

## Dashboard

Interactive Streamlit Dashboard

---

# Key Features

* Financial Ratio Engine
* CAGR Calculator
* Cash Flow Analytics
* Capital Allocation Classification
* Financial Screener
* Peer Benchmarking
* Radar Charts
* Valuation Analysis
* Interactive Dashboard
* Annual Report Viewer

---

# Installation

Clone the repository:

```bash
git clone <repository_url>
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the dashboard:

```bash
streamlit run app.py
```

---

# Future Enhancements

* Live NSE/BSE market data integration
* Portfolio optimization
* DCF valuation model
* AI-powered investment recommendations
* Financial statement forecasting
* Real-time alerts
* Portfolio tracking

---

# Author

**Shruthi Meena**

Nifty100 Financial Analytics Platform

End-to-End Financial Analytics & Dashboard Project

