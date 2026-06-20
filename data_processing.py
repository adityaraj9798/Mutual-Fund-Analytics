import pandas as pd
import numpy as np
import os
import glob
import sqlite3
from sqlalchemy import create_engine

# Setup directories and DB connection (Fixed paths)
os.makedirs('processed', exist_ok=True)
engine = create_engine('sqlite:///bluestock_mf.db')

def clean_nav_history(file_path):
    print("Cleaning nav_history...")
    df = pd.read_csv(file_path)
    
    df['date'] = pd.to_datetime(df['date'], dayfirst=True, format='mixed', errors='coerce')
    df = df.dropna(subset=['date', 'nav'])
    df = df.drop_duplicates(subset=['amfi_code', 'date'])
    df = df[df['nav'] > 0]
    df = df.sort_values(['amfi_code', 'date'])
    
    df = df.set_index('date').groupby('amfi_code')[['nav']].apply(
        lambda x: x.resample('D').ffill()
    ).drop(columns='amfi_code', errors='ignore').reset_index()
    
    # CRITICAL: Rename 'nav' to 'nav_value' to perfectly match the database schema
    df.rename(columns={'nav': 'nav_value'}, inplace=True)
    
    df.to_csv('processed/cleaned_nav_history.csv', index=False)
    df.to_sql('fact_nav', con=engine, if_exists='append', index=False)
    print(f"✅ nav_history cleaned and loaded. Rows: {len(df)}")

def clean_transactions(file_path):
    print("Cleaning investor_transactions...")
    df = pd.read_csv(file_path)
    
    df['transaction_type'] = df['transaction_type'].str.title().str.strip()
    valid_types = ['Sip', 'Lumpsum', 'Redemption']
    df = df[df['transaction_type'].isin(valid_types)]
    
    df = df[df['amount'] > 0]
    df['date'] = pd.to_datetime(df['date'], dayfirst=True, format='mixed', errors='coerce')
    
    if 'kyc_status' in df.columns:
        df['kyc_status'] = df['kyc_status'].str.upper()
        df = df[df['kyc_status'].isin(['VERIFIED', 'PENDING', 'REJECTED'])]
    
    df.to_csv('processed/cleaned_investor_transactions.csv', index=False)
    df.to_sql('fact_transactions', con=engine, if_exists='append', index=False)
    print(f"✅ transactions cleaned and loaded. Rows: {len(df)}")

def clean_performance(file_path):
    print("Cleaning scheme_performance...")
    df = pd.read_csv(file_path)
    
    return_cols = ['return_1y', 'return_3y', 'return_5y']
    for col in return_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    df['anomaly_flag'] = np.where((df['return_1y'] > 150) | (df['return_1y'] < -90), 1, 0)
    df = df[(df['expense_ratio'] >= 0.1) & (df['expense_ratio'] <= 2.5)]
    
    df.to_csv('processed/cleaned_scheme_performance.csv', index=False)
    df.to_sql('fact_performance', con=engine, if_exists='append', index=False)
    print(f"✅ performance cleaned and loaded. Rows: {len(df)}")

def process_remaining_files():
    print("Processing remaining datasets...")
    raw_files = glob.glob('raw/*.csv')
    processed_targets = ['nav_history', 'investor_transactions', 'scheme_performance']
    
    for file in raw_files:
        filename = os.path.basename(file)
        if not any(target in filename for target in processed_targets):
            try:
                df = pd.read_csv(file)
                df.dropna(how='all', inplace=True)
                clean_name = f"cleaned_{filename}"
                df.to_csv(f'processed/{clean_name}', index=False)
                
                table_name = filename.replace('.csv', '')
                df.to_sql(table_name, con=engine, if_exists='replace', index=False)
                print(f"✅ {filename} processed and loaded.")
            except Exception as e:
                print(f"❌ Error processing {filename}: {e}")

if __name__ == "__main__":
    print("Initializing database schema...")
    conn = sqlite3.connect('bluestock_mf.db')
    with open('sql/schema.sql', 'r') as file:
        conn.executescript(file.read())
    conn.close()
            
    # Fixed paths to look directly in 'raw/'
    if os.path.exists('raw/nav_history.csv'): clean_nav_history('raw/nav_history.csv')
    if os.path.exists('raw/investor_transactions.csv'): clean_transactions('raw/investor_transactions.csv')
    if os.path.exists('raw/scheme_performance.csv'): clean_performance('raw/scheme_performance.csv')
    
    process_remaining_files()
    print("ETL Pipeline Complete!")