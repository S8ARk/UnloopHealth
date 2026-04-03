import csv
from statistics import median
import os

# New correct paths to the CSV files
FILE1 = "health_fitness_dataset.csv"

def analyze_and_clean():
    print("--- Analyzing health_fitness_dataset.csv with Correct Headers ---")
    
    data = []
    with open(FILE1, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                # Map correct field names
                row['age'] = int(row['age'])
                row['bmi'] = float(row['bmi'])
                row['target_calories'] = int(row['target_calories'])
                row['sleep_hours'] = float(row['sleep_hours'])
                row['hydration_liters'] = float(row['hydration_liters'])
                row['daily_steps'] = int(row['daily_steps'])
                row['stress_level'] = int(row['stress_level'])
                data.append(row)
            except (ValueError, TypeError, KeyError):
                continue

    print(f"Total valid rows parsed: {len(data)}")
    
    # --- Finding the 'Optimal Health' Median Point ---
    # Define "Healthy" as BMI 18.5-25, 7-9h sleep, 8000+ steps, 2L+ water, Low Stress (<4)
    healthy_subset = [
        r for r in data 
        if 18.5 <= r['bmi'] <= 25 
        and 7 <= r['sleep_hours'] <= 9
        and r['daily_steps'] >= 8000
        and r['hydration_liters'] >= 2.0
        and r['stress_level'] <= 4
    ]
    
    print(f"Healthy individuals found: {len(healthy_subset)}")
    
    if healthy_subset:
        metrics = ['target_calories', 'hydration_liters', 'sleep_hours', 'bmi', 'daily_steps', 'stress_level']
        print("\n--- Optimal Health Baseline (Median of Healthy Individuals) ---")
        results = {}
        for m in metrics:
            val = median([r[m] for r in healthy_subset])
            results[m] = val
            print(f"{m:20}: {val:.2f}")
    else:
        print("\n[!] No individuals met the strict 'Healthy' criteria. Loosening criteria...")
        # Loosen criteria for a fallback
        healthy_subset = [r for r in data if 18.5 <= r['bmi'] <= 27]
        if healthy_subset:
            metrics = ['target_calories', 'hydration_liters', 'sleep_hours', 'bmi', 'daily_steps', 'stress_level']
            results = {}
            for m in metrics:
                val = median([r[m] for r in healthy_subset])
                results[m] = val
                print(f"{m:20}: {val:.2f} (Loosened Criteria)")

    # --- Create Master Dataset (Cleaned) ---
    master_csv_path = "master_health_data.csv"
    # Keep the most relevant features for our ML and UI
    fieldnames = ['age', 'gender', 'height_cm', 'weight_kg', 'bmi', 'target_calories', 
                  'hydration_liters', 'sleep_hours', 'daily_steps', 'stress_level', 'activity_type']
    
    with open(master_csv_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(data)
        
    print(f"\n[✓] Master cleaned dataset saved to: {master_csv_path}")

if __name__ == "__main__":
    analyze_and_clean()
