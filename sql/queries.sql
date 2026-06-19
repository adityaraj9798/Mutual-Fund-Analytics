-- 1. Top 5 funds by AUM
SELECT f.fund_name, a.aum_value
FROM fact_aum a
JOIN dim_fund f ON a.amfi_code = f.amfi_code
ORDER BY a.aum_value DESC
LIMIT 5;

-- 2. Average NAV per month (Using SQLite string functions for dates)
SELECT strftime('%Y-%m', date) AS month, amfi_code, AVG(nav) as avg_nav
FROM fact_nav
GROUP BY strftime('%Y-%m', date), amfi_code
ORDER BY month DESC;

-- 3. SIP YoY Growth (Total SIP Amount by Year)
SELECT strftime('%Y', date) AS transaction_year, SUM(amount) AS total_sip_volume
FROM fact_transactions
WHERE transaction_type = 'Sip'
GROUP BY strftime('%Y', date)
ORDER BY transaction_year ASC;

-- 4. Transactions by state
SELECT i.state, COUNT(t.txn_id) AS total_transactions, SUM(t.amount) as total_volume
FROM fact_transactions t
JOIN dim_investor i ON t.investor_id = i.investor_id
GROUP BY i.state
ORDER BY total_volume DESC;

-- 5. Funds with expense_ratio < 1%
SELECT f.fund_name, p.expense_ratio, p.return_1y
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
WHERE p.expense_ratio < 1.0
ORDER BY p.expense_ratio ASC;

-- 6. Top 5 highest performing funds over 3 Years
SELECT f.fund_name, p.return_3y
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
ORDER BY p.return_3y DESC
LIMIT 5;

-- 7. Count of distinct investors by fund category
SELECT f.category, COUNT(DISTINCT t.investor_id) as unique_investors
FROM fact_transactions t
JOIN dim_fund f ON t.amfi_code = f.amfi_code
GROUP BY f.category;

-- 8. Identify massive Lumpsum transactions (Outlier detection)
SELECT t.txn_id, f.fund_name, t.amount, t.date
FROM fact_transactions t
JOIN dim_fund f ON t.amfi_code = f.amfi_code
WHERE t.transaction_type = 'Lumpsum' AND t.amount > 1000000
ORDER BY t.amount DESC;

-- 9. Fund Houses with the most schemes
SELECT fund_house, COUNT(amfi_code) AS total_schemes
FROM dim_fund
GROUP BY fund_house
ORDER BY total_schemes DESC;

-- 10. Daily Average Volatility (Max NAV - Min NAV spread per fund per month)
SELECT strftime('%Y-%m', date) as month, amfi_code, (MAX(nav) - MIN(nav)) as monthly_spread
FROM fact_nav
GROUP BY strftime('%Y-%m', date), amfi_code
ORDER BY monthly_spread DESC;