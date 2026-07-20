import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw")

files = RAW_PATH.glob("*.xlsx")

for file in files:
    try:
        df = pd.read_excel(file)

        print("\n" + "=" * 50)
        print(file.name)
        print("=" * 50)

        print("Rows:", len(df))
        print("Columns:", len(df.columns))

        print(df.head())

    except Exception as e:
        print(f"Error reading {file.name}: {e}")
