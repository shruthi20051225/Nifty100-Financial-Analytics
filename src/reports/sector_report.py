import sqlite3
import pandas as pd
import os

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

DB = "nifty100.db"

OUTPUT = "reports/sector"

os.makedirs(OUTPUT, exist_ok=True)

styles = getSampleStyleSheet()

conn = sqlite3.connect(DB)

companies = pd.read_sql("""

SELECT

c.id,
c.company_name,
c.roce_percentage,
c.roe_percentage,

s.broad_sector,
s.sub_sector,
s.index_weight_pct,
s.market_cap_category

FROM companies c

LEFT JOIN sectors s

ON c.id = s.company_id

""", conn)

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

market = pd.read_sql(
    "SELECT * FROM market_cap",
    conn
)

conn.close()
# =====================================================
# CREATE SECTOR REPORT
# =====================================================

def create_sector_report(sector_name, sector_df):

    pdf_path = os.path.join(
        OUTPUT,
        f"{sector_name}_report.pdf"
    )

    doc = SimpleDocTemplate(pdf_path)

    story = []

    story.append(

        Paragraph(

            f"<b><font size=18>{sector_name} Sector Report</font></b>",

            styles["Title"]

        )

    )

    story.append(Spacer(1, 0.25 * inch))

    # ---------------------------------------
    # SUMMARY
    # ---------------------------------------

    story.append(

        Paragraph(
            "<b>Sector Summary</b>",
            styles["Heading2"]
        )

    )

    story.append(

        Paragraph(
            f"Total Companies : {len(sector_df)}",
            styles["BodyText"]
        )

    )

    story.append(Spacer(1, 0.20 * inch))

    # ---------------------------------------
    # COMPANY TABLE
    # ---------------------------------------

    table_data = [[

        "Company",

        "ROE",

        "ROCE",

        "PE",

        "PB"

    ]]

    for _, company in sector_df.iterrows():

        cid = company["id"]

        ratio = (

            ratios[
                ratios["company_id"] == cid
            ]

            .sort_values("year")

        )

        market_data = (

            market[
                market["company_id"] == cid
            ]

            .sort_values("year")

        )

        if ratio.empty:

            continue

        latest_ratio = ratio.iloc[-1]

        roe = latest_ratio.get(
            "return_on_equity_pct",
            ""
        )

        roce = company.get(
            "roce_percentage",
            ""
        )

        if market_data.empty:

            pe = ""

            pb = ""

        else:

            latest_market = market_data.iloc[-1]

            pe = latest_market.get(
                "pe_ratio",
                ""
            )

            pb = latest_market.get(
                "pb_ratio",
                ""
            )

        table_data.append([

            company["company_name"],

            roe,

            roce,

            pe,

            pb

        ])
            # ---------------------------------------
    # TABLE STYLE
    # ---------------------------------------

    table = Table(
        table_data,
        colWidths=[
            3.2 * inch,
            0.9 * inch,
            0.9 * inch,
            0.9 * inch,
            0.9 * inch
        ]
    )

    table.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,0),colors.darkblue),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),

        ("GRID",(0,0),(-1,-1),0.5,colors.grey),

        ("BACKGROUND",(0,1),(-1,-1),colors.beige),

        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

        ("FONTNAME",(0,1),(-1,-1),"Helvetica"),

        ("BOTTOMPADDING",(0,0),(-1,0),8),

        ("FONTSIZE",(0,0),(-1,-1),9),

        ("WORDWRAP",(0,0),(-1,-1),True),

        ("VALIGN",(0,0),(-1,-1),"TOP")

    ]))

    story.append(table)

    doc.build(story)
    # =====================================================
# GENERATE REPORTS FOR ALL SECTORS
# =====================================================

# If your companies table has a "sector" column use it.
# Otherwise change "sector" below to your actual column name
# (for example industry, sector_name, etc.)

sector_column = "broad_sector"

if sector_column not in companies.columns:

    print("=" * 60)
    print("Sector column not found.")
    print("Available columns are:")
    print(companies.columns.tolist())
    print("=" * 60)

else:

    total = 0

    for sector in sorted(companies[sector_column].dropna().unique()):

        sector_df = companies[
            companies[sector_column] == sector
        ]

        create_sector_report(
            sector,
            sector_df
        )

        total += 1

        print(f"Generated : {sector}")

    print("=" * 60)
    print("Sector Reports Generated :", total)
    print("Saved to : reports/sector/")
    print("=" * 60)