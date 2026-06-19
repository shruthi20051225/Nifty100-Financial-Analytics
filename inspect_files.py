# inspect_files.py

import pandas as pd
from pathlib import Path

for file in Path("data/raw").glob("*.xlsx"):

    print("\n" + "="*50)
    print(file.name)

    df = pd.read_excel(
        file,
        header=None
    )

    print(df.head(3).to_string())