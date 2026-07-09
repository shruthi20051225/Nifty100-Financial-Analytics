import pandas as pd

xls = pd.ExcelFile(
    "output/peer_comparison.xlsx"
)

print("Sheets:")

for sheet in xls.sheet_names:
    print(sheet)

print()

print("Total:", len(xls.sheet_names))