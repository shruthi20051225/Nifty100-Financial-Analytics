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
---

# Sprint 5 – NLP Intelligence & Automated Reporting

## Objectives

* Build an NLP engine to extract financial insights.
* Generate automated Pros & Cons for every company.
* Develop Cash Flow Intelligence metrics.
* Generate professional company and sector PDF reports.
* Create a portfolio summary report.

## NLP Module

### Implemented

* Financial analysis parser
* Automated Pros & Cons generator
* Confidence score calculation
* Rule-based financial insights

### Outputs

* analysis_parsed.csv
* parse_failures.csv
* pros_cons_generated.csv

---

# Cash Flow Intelligence

Computed:

* CFO Quality Score
* CFO Quality Classification
* CapEx Intensity
* Free Cash Flow Conversion
* Distress Signal Detection
* Deleveraging Detection
* Capital Allocation Classification

Generated:

* cashflow_intelligence.xlsx
* distress_alerts.csv

---

# Automated Reports

Generated:

### Company Reports

* Two-page Company Tearsheets

### Sector Reports

* Sector-wise Financial Reports

### Portfolio Report

* Portfolio Summary PDF

---

# Outputs Generated

## Excel Reports

* cashflow_intelligence.xlsx

## CSV Reports

* analysis_parsed.csv
* parse_failures.csv
* pros_cons_generated.csv
* distress_alerts.csv

## PDF Reports

* Company Tearsheets
* Sector Reports
* Portfolio Summary

---

# Key Features Added

* NLP Financial Analysis
* Automated Pros & Cons
* Cash Flow Intelligence
* Capital Allocation Analytics
* Company PDF Tearsheets
* Sector Reports
* Portfolio Summary Report

# Sprint 6 – Clustering, REST API, Testing & Final Project Validation

## Objectives

Sprint 6 focused on completing the analytics platform by implementing machine learning-based company clustering, developing REST APIs using FastAPI, performing automated testing with Pytest, optimizing database performance, and preparing the project for final deployment and documentation.

---

## Machine Learning & Analytics

### KMeans Company Clustering

Implemented KMeans clustering to classify Nifty 100 companies into financial archetypes using key financial metrics.

### Features Used

- Return on Equity (ROE)
- Debt to Equity Ratio
- Operating Profit Margin
- Asset Turnover
- Free Cash Flow

### Outputs Generated

- `cluster_labels.csv`
- `cluster_profile.csv`
- `portfolio_stats.csv`
- `outlier_report.csv`
- `elbow_plot.png`
- `correlation_heatmap.png`

---

## REST API Development (FastAPI)

Developed a REST API layer for accessing financial data through standardized endpoints.

### API Modules

- Health API
- Companies API
- Financial Ratios API
- Profit & Loss API
- Balance Sheet API
- Cash Flow API
- Screener API
- Sector API
- Peer Comparison API
- Market Capitalization API
- Documents API
- Portfolio Statistics API

### Features

- OpenAPI (Swagger) Documentation
- JSON Responses
- SQLite Integration
- Request Logging
- CORS Middleware

---

## Automated Testing

Implemented automated testing using Pytest.

### Test Modules

- ETL Tests
- Financial KPI Tests
- Data Quality Tests
- Health API Tests
- Companies API Tests
- Screener API Tests
- Sector API Tests
- Peer API Tests

### Outputs

- `pytest_report.html`

---

## Performance Optimization

Optimized SQLite database performance by creating indexes on frequently queried columns.

### Database Optimization

Indexes created for:

- Financial Ratios
- Profit & Loss
- Balance Sheet
- Cash Flow
- Market Capitalization
- Sectors
- Peer Groups

### Performance Testing

- Concurrent API Load Testing
- Dashboard Integration Testing
- Streamlit + FastAPI Compatibility Testing
- Performance Notes Documentation

Outputs:

- `perf_notes.md`
- `performance_summary.txt`

---

## Documentation

Prepared project documentation including:

- Analyst Guide (PDF)
- Updated README
- OpenAPI Specification
- Acceptance Checklist

---

## Deliverables

### Reports

- cluster_labels.csv
- cluster_profile.csv
- portfolio_stats.csv
- outlier_report.csv
- elbow_plot.png
- correlation_heatmap.png

### APIs

- FastAPI Server
- OpenAPI Documentation
- REST Endpoints

### Testing

- Pytest Test Suite
- HTML Test Report

### Documentation

- Analyst Guide
- Acceptance Checklist
- Performance Notes

---

## Sprint 6 Summary

Sprint 6 completed the Nifty100 Financial Analytics Platform by integrating machine learning, REST APIs, automated testing, performance optimization, and comprehensive documentation. The platform now supports financial analysis, company screening, peer benchmarking, clustering, valuation analytics, and interactive dashboard visualization through both a web interface and REST API.

# Author

**Shruthi Meena R**

Nifty100 Financial Analytics Platform

End-to-End Financial Analytics & Dashboard Project

