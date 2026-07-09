import os

import pandas as pd

from src.screener.presets import PresetScreeners


os.makedirs("output", exist_ok=True)

preset = PresetScreeners()

screeners = {
    "Quality Compounder": preset.quality_compounder(),
    "Value Pick": preset.value_pick(),
    "Growth Accelerator": preset.growth_accelerator(),
    "Dividend Champion": preset.dividend_champion(),
    "Debt Free Bluechip": preset.debt_free_bluechip(),
    "Turnaround Watch": preset.turnaround_watch(),
}

with pd.ExcelWriter("output/screener_output.xlsx") as writer:

    for name, df in screeners.items():
        df.to_excel(
            writer,
            sheet_name=name[:31],
            index=False,
        )

print("screener_output.xlsx generated successfully.")