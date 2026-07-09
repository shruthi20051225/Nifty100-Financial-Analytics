import pandas as pd

xls = pd.ExcelFile(
    "output/screener_output.xlsx"
)

df = pd.read_excel(
    xls,
    "Quality Compounder"
)

print(df.head())
print()

print("Companies:", len(df))