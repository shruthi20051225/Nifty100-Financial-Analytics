import sqlite3
import pandas as pd
import os

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

DB = "nifty100.db"

REPORT_DIR = "reports/tearsheets"

os.makedirs(REPORT_DIR, exist_ok=True)

styles = getSampleStyleSheet()

conn = sqlite3.connect(DB)

companies = pd.read_sql(
    "SELECT * FROM companies",
    conn
)

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

market = pd.read_sql(
    "SELECT * FROM market_cap",
    conn
)

cashflow = pd.read_sql(
    "SELECT * FROM cashflow",
    conn
)

conn.close()
# ======================================================
# CREATE TEARSHEET
# ======================================================

def create_tearsheet(company):

    company_id = company["id"]

    company_name = company["company_name"]

    pdf_file = os.path.join(

        REPORT_DIR,

        f"{company_id}_tearsheet.pdf"

    )

    doc = SimpleDocTemplate(

        pdf_file,

        pagesize=(8.27 * inch, 11.69 * inch)

    )

    story = []

    # ------------------------------------
    # TITLE
    # ------------------------------------

    title = Paragraph(

        f"<b><font size=18>{company_name}</font></b>",

        styles["Title"]

    )

    story.append(title)

    story.append(Spacer(1, 0.25 * inch))

    # ------------------------------------
    # COMPANY DETAILS
    # ------------------------------------

    info = [

        ["Company ID", company_id],

        ["ROE", company.get("roe_percentage", "")],

        ["ROCE", company.get("roce_percentage", "")],

        ["Face Value", company.get("face_value", "")],

        ["Book Value", company.get("book_value", "")],

        ["Website", company.get("website", "")]

    ]

    table = Table(

        info,

        colWidths=[2.2 * inch, 4.3 * inch]

    )

    table.setStyle(

        TableStyle([

            ("GRID", (0,0), (-1,-1), 0.5, colors.grey),

            ("BACKGROUND",(0,0),(0,-1),colors.lightgrey),

            ("FONTNAME",(0,0),(-1,-1),"Helvetica"),

            ("BOTTOMPADDING",(0,0),(-1,-1),8)

        ])

    )

    story.append(table)

    story.append(Spacer(1,0.30*inch))
        # =====================================================
    # FINANCIAL KPIs
    # =====================================================

    ratio = (
        ratios[
            ratios["company_id"] == company_id
        ]
        .sort_values("year")
    )

    market_data = (
        market[
            market["company_id"] == company_id
        ]
        .sort_values("year")
    )

    cash = (
        cashflow[
            cashflow["company_id"] == company_id
        ]
        .sort_values("year")
    )

    if not ratio.empty:

        latest_ratio = ratio.iloc[-1]

        ratio_table = [

            ["Metric", "Value"],

            ["ROE (%)",
             latest_ratio.get("return_on_equity_pct", "")],

            ["Debt / Equity",
             latest_ratio.get("debt_to_equity", "")],

            ["Interest Coverage",
             latest_ratio.get("interest_coverage", "")],

            ["Operating Margin (%)",
             latest_ratio.get("operating_profit_margin_pct", "")],

            ["Net Profit Margin (%)",
             latest_ratio.get("net_profit_margin_pct", "")],

            ["EPS",
             latest_ratio.get("earnings_per_share", "")],

            ["Free Cash Flow",
             latest_ratio.get("free_cash_flow_cr", "")]
        ]

        t = Table(
            ratio_table,
            colWidths=[3*inch,2*inch]
        )

        t.setStyle(TableStyle([

            ("GRID",(0,0),(-1,-1),0.5,colors.black),

            ("BACKGROUND",(0,0),(-1,0),colors.darkblue),

            ("TEXTCOLOR",(0,0),(-1,0),colors.white),

            ("BACKGROUND",(0,1),(0,-1),colors.beige),

            ("BOTTOMPADDING",(0,0),(-1,0),8)

        ]))

        story.append(
            Paragraph(
                "<b>Financial KPIs</b>",
                styles["Heading2"]
            )
        )

        story.append(t)

        story.append(
            Spacer(1,0.25*inch)
        )

    # =====================================================
    # MARKET VALUATION
    # =====================================================

    if not market_data.empty:

        latest_market = market_data.iloc[-1]

        valuation = [

            ["Metric","Value"],

            ["Market Cap",
             latest_market.get("market_cap_crore","")],

            ["Enterprise Value",
             latest_market.get("enterprise_value_crore","")],

            ["PE Ratio",
             latest_market.get("pe_ratio","")],

            ["PB Ratio",
             latest_market.get("pb_ratio","")],

            ["EV / EBITDA",
             latest_market.get("ev_ebitda","")],

            ["Dividend Yield %",
             latest_market.get("dividend_yield_pct","")]

        ]

        vt = Table(
            valuation,
            colWidths=[3*inch,2*inch]
        )

        vt.setStyle(TableStyle([

            ("GRID",(0,0),(-1,-1),0.5,colors.black),

            ("BACKGROUND",(0,0),(-1,0),colors.darkgreen),

            ("TEXTCOLOR",(0,0),(-1,0),colors.white),

            ("BACKGROUND",(0,1),(0,-1),colors.lightgreen)

        ]))

        story.append(

            Paragraph(
                "<b>Market Valuation</b>",
                styles["Heading2"]
            )

        )

        story.append(vt)

        story.append(
            Spacer(1,0.25*inch)
        )
            # =====================================================
    # CASH FLOW SUMMARY
    # =====================================================

    if not cash.empty:

        latest_cash = cash.iloc[-1]

        cash_table = [

            ["Metric", "Value"],

            ["Operating Activity",
             latest_cash.get("operating_activity", "")],

            ["Investing Activity",
             latest_cash.get("investing_activity", "")],

            ["Financing Activity",
             latest_cash.get("financing_activity", "")],

            ["Net Cash Flow",
             latest_cash.get("net_cash_flow", "")]
        ]

        ct = Table(
            cash_table,
            colWidths=[3 * inch, 2 * inch]
        )

        ct.setStyle(TableStyle([

            ("GRID",(0,0),(-1,-1),0.5,colors.black),

            ("BACKGROUND",(0,0),(-1,0),colors.darkred),

            ("TEXTCOLOR",(0,0),(-1,0),colors.white),

            ("BACKGROUND",(0,1),(0,-1),colors.whitesmoke)

        ]))

        story.append(
            Paragraph(
                "<b>Cash Flow Summary</b>",
                styles["Heading2"]
            )
        )

        story.append(ct)

        story.append(Spacer(1,0.25*inch))

    # =====================================================
    # PROS & CONS PLACEHOLDER
    # =====================================================

    story.append(
        Paragraph(
            "<b>Pros</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            "• Refer to generated Pros & Cons report for company-specific strengths.",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1,0.15*inch))

    story.append(
        Paragraph(
            "<b>Cons</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            "• Refer to generated Pros & Cons report for company-specific risks.",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1,0.30*inch))

    # =====================================================
    # FOOTER
    # =====================================================

    story.append(
        Paragraph(
            "<font size=8>Generated by Nifty100 Financial Analytics Dashboard</font>",
            styles["Normal"]
        )
    )

    # =====================================================
    # SAVE PDF
    # =====================================================

    doc.build(story)
    # =====================================================
# GENERATE ALL PDFS
# =====================================================

print("=" * 60)
print("Generating Company Tearsheets...")
print("=" * 60)

count = 0

for _, company in companies.iterrows():

    try:

        create_tearsheet(company)

        count += 1

        print(f"Generated : {company['company_name']}")

    except Exception as e:

        print(
            f"Skipped {company['company_name']} : {e}"
        )

print("=" * 60)
print("Completed")
print("PDFs Generated :", count)
print("Location : reports/tearsheets/")
print("=" * 60)