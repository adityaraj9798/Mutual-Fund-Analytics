-- DDL for Mutual Fund Analytics Star Schema

-- DIMENSION TABLES
CREATE TABLE IF NOT EXISTS dim_fund (
    amfi_code INTEGER PRIMARY KEY,
    fund_name TEXT NOT NULL,
    fund_house TEXT,
    category TEXT,
    sub_category TEXT,
    risk_grade TEXT
);

CREATE TABLE IF NOT EXISTS dim_date (
    date_id TEXT PRIMARY KEY, -- Format: YYYY-MM-DD
    full_date DATE,
    year INTEGER,
    month INTEGER,
    quarter INTEGER,
    day_of_week TEXT
);

CREATE TABLE IF NOT EXISTS dim_investor (
    investor_id INTEGER PRIMARY KEY,
    state TEXT,
    kyc_status TEXT
);

-- FACT TABLES
CREATE TABLE IF NOT EXISTS fact_nav (
    nav_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code INTEGER,
    date_id TEXT,
    nav_value REAL,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);

CREATE TABLE IF NOT EXISTS fact_transactions (
    txn_id INTEGER PRIMARY KEY AUTOINCREMENT,
    investor_id INTEGER,
    amfi_code INTEGER,
    date_id TEXT,
    transaction_type TEXT,
    amount REAL,
    FOREIGN KEY (investor_id) REFERENCES dim_investor(investor_id),
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);

CREATE TABLE IF NOT EXISTS fact_performance (
    perf_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code INTEGER,
    return_1y REAL,
    return_3y REAL,
    return_5y REAL,
    expense_ratio REAL,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

CREATE TABLE IF NOT EXISTS fact_aum (
    aum_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code INTEGER,
    date_id TEXT,
    aum_value REAL,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);