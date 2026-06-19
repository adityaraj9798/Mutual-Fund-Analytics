import pandas as pd
import os
import glob

def inspect_csv_files():
    print("\n--- Inspecting Raw Data Files ---")
    
    # Points to the raw data directory you set up
    raw_data_dir = 'data/raw/' 
    csv_files = glob.glob(os.path.join(raw_data_dir, '*.csv'))
    
    if not csv_files:
        print("No CSV files found. Please ensure the 10 CSVs are in 'data/raw/'.")
        return

    for file in csv_files:
        print(f"\n📁 Loading: {os.path.basename(file)}")
        try:
            df = pd.read_csv(file)
            print(f"Shape: {df.shape}")
            print(f"Data Types:\n{df.dtypes.to_string()}")
            print(f"Head:\n{df.head(2).to_string()}") 
            
            # Identify any immediate anomalies (missing values)
            missing_count = df.isnull().sum().sum()
            if missing_count > 0:
                print(f"⚠️ Anomaly Note: Found {missing_count} total missing values.")
            else:
                print("✅ No missing values detected.")
        except Exception as e:
            print(f"❌ Error loading {file}: {e}")

def validate_fund_master():
    print("\n--- Exploring Fund Master & Validating AMFI Codes ---")
    
    # Assuming these are the names of your provided CSVs
    fund_master_path = 'data/raw/fund_master.csv'
    nav_history_path = 'data/raw/nav_history.csv'
    
    if not os.path.exists(fund_master_path) or not os.path.exists(nav_history_path):
        print("⚠️ Waiting for 'fund_master.csv' and 'nav_history.csv' to run AMFI validation.")
        return

    master_df = pd.read_csv(fund_master_path)
    nav_df = pd.read_csv(nav_history_path)

    # 1. Explore fund master
    print("\nUnique Fund Houses:")
    print(master_df['fund_house'].unique() if 'fund_house' in master_df.columns else "Column 'fund_house' not found")
    
    print("\nCategories & Sub-categories:")
    if 'category' in master_df.columns and 'sub_category' in master_df.columns:
        print(master_df[['category', 'sub_category']].drop_duplicates().to_string(index=False))
    
    print("\nRisk Grades:")
    print(master_df['risk_grade'].unique() if 'risk_grade' in master_df.columns else "Column 'risk_grade' not found")

    # 2. Validate AMFI codes
    if 'scheme_code' in master_df.columns and 'scheme_code' in nav_df.columns:
        master_codes = set(master_df['scheme_code'].unique())
        nav_codes = set(nav_df['scheme_code'].unique())
        
        missing_in_nav = master_codes - nav_codes
        
        print("\n--- Data Quality Summary ---")
        if not missing_in_nav:
            print("✅ Perfect Match: Every AMFI code in fund_master exists in nav_history.")
        else:
            print(f"⚠️ Data Quality Issue: Found {len(missing_in_nav)} scheme codes in fund_master missing from nav_history.")
            print(f"Sample of missing codes: {list(missing_in_nav)[:5]}")
    else:
        print("⚠️ Cannot validate codes: 'scheme_code' column missing.")

if __name__ == "__main__":
    inspect_csv_files()
    validate_fund_master()