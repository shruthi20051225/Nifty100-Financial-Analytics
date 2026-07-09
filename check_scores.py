import pandas as pd

xls = pd.ExcelFile("output/screener_output.xlsx")

for sheet in xls.sheet_names:

    df = pd.read_excel(xls, sheet)

    if "composite_quality_score" in df.columns:

        print()

        print(sheet)

        print(
            df[
                [
                    "company_id",
                    "composite_quality_score"
                ]
            ].head()
        )