import requests
import pandas as pd
import os

# Ensure the target directory exists
os.makedirs('data/raw', exist_ok=True)

# Dictionary of requested schemes
SCHEMES = {
    "HDFC_Top_100_Direct": 125497,
    "SBI_Bluechip": 119551,
    "ICICI_Bluechip": 120503,
    "Nippon_Large_Cap": 118632,
    "Axis_Bluechip": 119092,
    "Kotak_Bluechip": 120841
}

def fetch_and_save_nav(scheme_name, scheme_code):
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    
    try:
        response = requests.get(url)
        response.raise_for_status() 
        
        data = response.json()
        
        # Check if 'data' key exists (holds the NAV history)
        if "data" in data and len(data["data"]) > 0:
            df = pd.DataFrame(data["data"])
            
            # Save to raw CSV
            file_path = f"data/raw/{scheme_name}_{scheme_code}_live.csv"
            df.to_csv(file_path, index=False)
            print(f"✅ Success: Saved {scheme_name} to {file_path}")
        else:
            print(f"⚠️ Warning: No NAV data found for {scheme_name} ({scheme_code})")
            
    except Exception as e:
        print(f"❌ Error fetching {scheme_name} ({scheme_code}): {e}")

if __name__ == "__main__":
    print("Starting Live NAV Fetch...")
    for name, code in SCHEMES.items():
        fetch_and_save_nav(name, code)
    print("NAV Fetching Complete.")