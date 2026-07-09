import pandas as pd

xls = pd.ExcelFile("output/screener_output.xlsx")

print("Sheets:")

for sheet in xls.sheet_names:
    df = pd.read_excel(xls, sheet_name=sheet)
    print(f"{sheet}: {len(df)} companies")