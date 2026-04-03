import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.ml_service import ml_service

def main():
    print("NutriCore ML Model Initialization...")
    
    # Check if master data exists
    master_csv = "master_health_data.csv"
    if not os.path.exists(master_csv):
        print(f"Error: {master_csv} missing. Run 'tmp/generate_master_dataset.py' first.")
        return
        
    success = ml_service.train_from_master_data(master_csv)
    
    if success:
        print("[✓] ML models successfully trained and saved.")
    else:
        print("[!] Initialization resulted in fallback (not enough data).")

if __name__ == "__main__":
    main()
