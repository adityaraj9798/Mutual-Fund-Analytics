# Bluestock Mutual Fund Analytics Capstone 

## Project Overview
This project is an end-to-end data engineering and analytics solution for Mutual Fund performance and investor behavior. It features an automated ETL pipeline, quantitative financial risk modeling (Sharpe, VaR, Max Drawdown), and an interactive Power BI dashboard for business intelligence.

## Tech Stack
* **Language:** Python 3.x
* **Libraries:** Pandas, NumPy, Matplotlib
* **Database:** SQLite
* **Visualization:** Power BI
* **Version Control:** Git & GitHub

## Dataset Descriptions
* `fact_nav.csv`: Daily historical Net Asset Values and benchmark comparisons.
* `fact_transactions.csv`: Granular investor transaction logs (SIP, Lumpsum).
* `fact_aum.csv`: Monthly Assets Under Management tracking.
* `dim_fund.csv`: Fund metadata, categories, and AMFI codes.
* `fund_scorecard.csv`: Computed financial metrics (Alpha, Beta, CAGR, Sharpe).

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone [YOUR_GITHUB_REPO_LINK_HERE]
   cd "Mutual Fund Analytics"