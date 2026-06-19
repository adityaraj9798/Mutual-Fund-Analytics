# Mutual Fund Analytics - Data Dictionary

## Dimension Tables

### `dim_fund`
| Column Name | Data Type | Business Definition | Source |
| :--- | :--- | :--- | :--- |
| `amfi_code` | INTEGER (PK) | Unique identifier for the mutual fund scheme assigned by AMFI. | `fund_master.csv` |
| `fund_name` | TEXT | The official marketing name of the mutual fund scheme. | `fund_master.csv` |
| `fund_house` | TEXT | The Asset Management Company (AMC) managing the fund. | `fund_master.csv` |
| `category` | TEXT | Broad classification (e.g., Equity, Debt, Hybrid). | `fund_master.csv` |
| `risk_grade` | TEXT | Risk assessment category (e.g., Low, Moderate, High). | `fund_master.csv` |

## Fact Tables

### `fact_nav`
| Column Name | Data Type | Business Definition | Source |
| :--- | :--- | :--- | :--- |
| `nav_id` | INTEGER (PK)| Auto-incrementing surrogate key. | Generated |
| `amfi_code` | INTEGER (FK)| Reference to the fund. | `nav_history.csv` |
| `date_id` | TEXT (FK) | Date of the NAV record (YYYY-MM-DD). | `nav_history.csv` |
| `nav_value` | REAL | Net Asset Value per unit at market close. | `nav_history.csv` |

### `fact_transactions`
| Column Name | Data Type | Business Definition | Source |
| :--- | :--- | :--- | :--- |
| `txn_id` | INTEGER (PK)| Unique identifier for the transaction. | `investor_transactions.csv`|
| `transaction_type`| TEXT | Method of investment: 'Sip', 'Lumpsum', or 'Redemption'.| `investor_transactions.csv`|
| `amount` | REAL | Total fiat value of the transaction in INR. | `investor_transactions.csv`|

### `fact_performance`
| Column Name | Data Type | Business Definition | Source |
| :--- | :--- | :--- | :--- |
| `return_1y` | REAL | 1-Year trailing return percentage. | `scheme_performance.csv`|
| `expense_ratio` | REAL | The annual maintenance charge levied by mutual funds (0.1% - 2.5%).| `scheme_performance.csv`|