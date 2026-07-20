import os
import pandas as pd

from src.screener.presets import PresetScreeners
from src.screener.composite_score import compute_composite_score

# Create output folder if it doesn't exist
os.makedirs("output", exist_ok=True)

# Load all preset screeners
preset = PresetScreeners()

screeners = {
    "Quality Compounder": preset.quality_compounder(),
    "Value Pick": preset.value_pick(),
    "Growth Accelerator": preset.growth_accelerator(),
    "Dividend Champion": preset.dividend_champion(),
    "Debt Free Bluechip": preset.debt_free_bluechip(),
    "Turnaround Watch": preset.turnaround_watch(),
}

# Export to Excel
with pd.ExcelWriter("output/screener_output.xlsx", engine="openpyxl") as writer:

    for sheet_name, df in screeners.items():

        if len(df) == 0:
            df.to_excel(writer, sheet_name=sheet_name[:31], index=False)
            continue

        # Compute Composite Score
        df = compute_composite_score(df)

        # Sort highest score first
        df = df.sort_values(by="composite_quality_score", ascending=False)

        # Export
        df.to_excel(writer, sheet_name=sheet_name[:31], index=False)

print("=" * 50)
print("Sprint 3 Day 17 Completed")
print("Generated: output/screener_output.xlsx")
print("=" * 50)

# Show summary
for sheet_name, df in screeners.items():
    print(f"{sheet_name:<25} : {len(df)} companies")
