import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

query = """
SELECT
    company_id,
    COUNT(DISTINCT year) AS year_count
FROM profitandloss
GROUP BY company_id
ORDER BY year_count
"""

df = pd.read_sql(query, conn)

print("All Companies:")
print(df)

# Companies with less than 5 years of data
few_years = df[df["year_count"] < 5]

print("\nCompanies with less than 5 years of data:")
print(few_years)

# Export CSV
few_years.to_csv(
    "output/companies_less_than_5_years.csv",
    index=False
)

print("\nCSV file created successfully!")

conn.close()