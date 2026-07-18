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

OUTPUT = "reports/portfolio"

os.makedirs(OUTPUT, exist_ok=True)

styles = getSampleStyleSheet()

conn = sqlite3.connect(DB)

companies = pd.read_sql("""

SELECT

c.id,
c.company_name,
c.roe_percentage,
c.roce_percentage,

s.broad_sector,
s.market_cap_category

FROM companies c

LEFT JOIN sectors s

ON c.id=s.company_id

""", conn)

ratios = pd.read_sql(

"SELECT * FROM financial_ratios",

conn

)

conn.close()
doc = SimpleDocTemplate(

os.path.join(

OUTPUT,

"portfolio_summary.pdf"

)

)

story = []

story.append(

Paragraph(

"<b><font size=22>Nifty100 Portfolio Summary</font></b>",

styles["Title"]

)

)

story.append(

Spacer(

1,

0.30*inch

)

)
# =====================================================
# ONE PAGE PER COMPANY
# =====================================================

for _, company in companies.sort_values("company_name").iterrows():

    story.append(
        Paragraph(
            f"<b><font size=18>{company['company_name']}</font></b>",
            styles["Heading1"]
        )
    )

    story.append(
        Paragraph(
            f"Sector : {company['broad_sector']}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"Market Cap : {company['market_cap_category']}",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 0.20 * inch))

    ratio = (
        ratios[
            ratios["company_id"] == company["id"]
        ]
        .sort_values("year")
    )

    if ratio.empty:

        story.append(
            Paragraph(
                "No financial ratio data available.",
                styles["BodyText"]
            )
        )

        story.append(
            Spacer(1, 0.50 * inch)
        )

        continue

    latest = ratio.iloc[-1]

    table_data = [

        ["Metric", "Value"],

        ["ROE %",
         latest.get("return_on_equity_pct", "")],

        ["Debt/Equity",
         latest.get("debt_to_equity", "")],

        ["Interest Coverage",
         latest.get("interest_coverage", "")],

        ["Net Profit Margin %",
         latest.get("net_profit_margin_pct", "")],

        ["Operating Margin %",
         latest.get("operating_profit_margin_pct", "")],

        ["EPS",
         latest.get("earnings_per_share", "")]
    ]

    table = Table(
        table_data,
        colWidths=[3.5 * inch, 2 * inch]
    )

    table.setStyle(TableStyle([

        ("GRID",(0,0),(-1,-1),0.5,colors.grey),

        ("BACKGROUND",(0,0),(-1,0),colors.darkblue),

        ("TEXTCOLOR",(0,0),(-1,0),colors.white),

        ("BACKGROUND",(0,1),(0,-1),colors.whitesmoke),

        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

        ("BOTTOMPADDING",(0,0),(-1,0),8)

    ]))

    story.append(table)

    story.append(Spacer(1, 0.30 * inch))
    from reportlab.platypus import PageBreak

    # ============================================
    # TREND ARROWS
    # ============================================

    if len(ratio) >= 2:

        previous = ratio.iloc[-2]

        def trend_arrow(current, previous):

            if pd.isna(current) or pd.isna(previous):
                return "-"

            diff = current - previous

            if abs(diff) <= abs(previous) * 0.02:
                return "→"

            elif diff > 0:
                return "↑"

            else:
                return "↓"

        trend_table = [

            ["Metric", "Trend"],

            ["ROE",
             trend_arrow(
                 latest["return_on_equity_pct"],
                 previous["return_on_equity_pct"]
             )],

            ["Net Profit Margin",
             trend_arrow(
                 latest["net_profit_margin_pct"],
                 previous["net_profit_margin_pct"]
             )],

            ["Operating Margin",
             trend_arrow(
                 latest["operating_profit_margin_pct"],
                 previous["operating_profit_margin_pct"]
             )],

            ["EPS",
             trend_arrow(
                 latest["earnings_per_share"],
                 previous["earnings_per_share"]
             )]

        ]

        tt = Table(
            trend_table,
            colWidths=[3.5 * inch, 1.5 * inch]
        )

        tt.setStyle(TableStyle([

            ("GRID",(0,0),(-1,-1),0.5,colors.grey),

            ("BACKGROUND",(0,0),(-1,0),colors.green),

            ("TEXTCOLOR",(0,0),(-1,0),colors.white),

            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold")

        ]))

        story.append(Spacer(1,0.20*inch))

        story.append(
            Paragraph(
                "<b>Trend Indicators</b>",
                styles["Heading2"]
            )
        )

        story.append(tt)

    # --------------------------------------------
    # PAGE BREAK
    # --------------------------------------------

    story.append(PageBreak())

# ==================================================
# SAVE PDF
# ==================================================

doc.build(story)

print("=" * 60)
print("Portfolio Summary Generated Successfully")
print("=" * 60)
print("Output : reports/portfolio/portfolio_summary.pdf")
print("=" * 60)