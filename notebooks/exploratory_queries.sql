#Query 1 — Total Companies
SELECT COUNT(*) AS total_companies
FROM companies;

#Query 2 — Companies per Sector
SELECT broad_sector,
       COUNT(*) AS company_count
FROM sectors
GROUP BY broad_sector
ORDER BY company_count DESC;

#Query 3 — Top 10 Companies by ROE
SELECT company_name,
       roe_percentage
FROM companies
ORDER BY roe_percentage DESC
LIMIT 10;

#Query 4 — Highest Market Cap
SELECT company_id,
       MAX(market_cap_crore) AS market_cap
FROM market_cap
GROUP BY company_id
ORDER BY market_cap DESC
LIMIT 10;

#Query 5 — Average P/E Ratio
SELECT AVG(pe_ratio) AS avg_pe_ratio
FROM market_cap;

#Query 6 — Companies with Highest Sales
SELECT company_id,
       MAX(sales) AS max_sales
FROM profitandloss
GROUP BY company_id
ORDER BY max_sales DESC
LIMIT 10;

#Query 7 — Average ROE by Sector
SELECT s.broad_sector,
       AVG(c.roe_percentage) AS avg_roe
FROM companies c
JOIN sectors s
ON c.id = s.company_id
GROUP BY s.broad_sector
ORDER BY avg_roe DESC;

#Query 8 — Highest Stock Price
SELECT company_id,
       MAX(close_price) AS highest_price
FROM stock_prices
GROUP BY company_id
ORDER BY highest_price DESC
LIMIT 10;

#Query 9 — Companies with Most Years of Data
SELECT company_id,
       COUNT(DISTINCT year) AS years_available
FROM profitandloss
GROUP BY company_id
ORDER BY years_available DESC;

#Query 10 — Total Records per Table
SELECT 'companies' AS table_name,
       COUNT(*) AS row_count
FROM companies

UNION ALL

SELECT 'profitandloss',
       COUNT(*)
FROM profitandloss

UNION ALL

SELECT 'balancesheet',
       COUNT(*)
FROM balancesheet

UNION ALL

SELECT 'cashflow',
       COUNT(*)
FROM cashflow

UNION ALL

SELECT 'stock_prices',
       COUNT(*)
FROM stock_prices;

