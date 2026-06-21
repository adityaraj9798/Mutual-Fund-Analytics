"""
Bluestock Mutual Fund Analytics - Master Execution Pipeline
This script orchestrates the execution of all Python modules in the ETL 
and Analytics pipeline.
"""

import subprocess
import os

def run_module(script_name):
    """Executes a Python script and handles output/errors."""
    print(f"\n[{script_name}] Starting execution...")
    if not os.path.exists(script_name):
        print(f"⚠️ Warning: '{script_name}' not found. Skipping.")
        return

    try:
        # Run the script and capture the output
        result = subprocess.run(['python', script_name], check=True, text=True, capture_output=True)
        print(f"✅ [{script_name}] Completed Successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ [{script_name}] Failed with error:\n{e.stderr}")

if __name__ == "__main__":
    print("🚀 Initializing Bluestock MF Analytics Pipeline...")
    
    # List your main executable Python scripts here in order
    pipeline_scripts = [
        "recommender.py" 
        # Add any other .py scripts you created here
    ]
    
    for script in pipeline_scripts:
        run_module(script)
        
    print("\n🎉 All pipeline modules executed.")