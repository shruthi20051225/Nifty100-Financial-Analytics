from pathlib import Path

raw_path = Path("data/raw")

files = list(raw_path.glob("*.xlsx"))

print(f"Found {len(files)} Excel files\n")

for f in files:
    print(f.name)
    