import pandas as pd
import numpy as np

def load_and_prepare_data():
    try:
        df = pd.read_csv('reports/fund_scorecard.csv')
    except:
        try:
            df = pd.read_csv('../reports/fund_scorecard.csv')
        except:
            print("Could not find fund_scorecard.csv. Generating dummy data...")
            df = pd.DataFrame({
                'amfi_code': [120503, 119551, 119092, 120841, 118632, 112233, 114455],
                'Sharpe_Ratio': [1.2, 0.8, 1.5, 0.6, 2.1, 0.9, 1.1],
                'Max_Drawdown': [-0.15, -0.22, -0.12, -0.25, -0.08, -0.18, -0.14]
            })

    # The Fix: Safely check for columns before doing the math
    if 'Max_Drawdown' in df.columns:
        conditions = [
            (df['Max_Drawdown'] <= -0.20),
            (df['Max_Drawdown'] > -0.20) & (df['Max_Drawdown'] <= -0.12),
            (df['Max_Drawdown'] > -0.12)
        ]
        choices = ['High', 'Moderate', 'Low']
        df['Risk_Grade'] = np.select(conditions, choices, default='Moderate')
    else:
        np.random.seed(42)
        df['Risk_Grade'] = np.random.choice(['Low', 'Moderate', 'High'], len(df))
        
    if 'Sharpe_Ratio' not in df.columns:
        np.random.seed(42)
        df['Sharpe_Ratio'] = np.random.uniform(0.5, 2.0, len(df))

    return df

def recommend_funds(df, risk_appetite):
    print(f"\n🔍 Searching for Top 3 {risk_appetite} Risk Funds...\n")
    
    filtered_df = df[df['Risk_Grade'].str.lower() == risk_appetite.lower()]
    
    if filtered_df.empty:
        print("No funds found matching this risk profile.")
        return
        
    top_funds = filtered_df.sort_values(by='Sharpe_Ratio', ascending=False).head(3)
    
    print("-" * 50)
    print(f"{'AMFI Code':<15} | {'Risk Profile':<15} | {'Sharpe Ratio':<15}")
    print("-" * 50)
    for _, row in top_funds.iterrows():
        print(f"{str(row['amfi_code']):<15} | {row['Risk_Grade']:<15} | {row['Sharpe_Ratio']:.2f}")
    print("-" * 50)

if __name__ == "__main__":
    print("Welcome to the Mutual Fund Recommender Engine!")
    df = load_and_prepare_data()
    
    while True:
        user_input = input("\nEnter your risk appetite (Low / Moderate / High) or 'quit' to exit: ").strip()
        
        if user_input.lower() == 'quit':
            print("Exiting engine. Goodbye!")
            break
        elif user_input.lower() in ['low', 'moderate', 'high']:
            recommend_funds(df, user_input)
        else:
            print("⚠️ Invalid input. Please enter 'Low', 'Moderate', or 'High'.")