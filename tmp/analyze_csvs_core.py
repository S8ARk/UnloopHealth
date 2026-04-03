import csv
from statistics import median
import os

# Paths to the CSV files
FILE1 = "health_fitness_dataset.csv"
FILE2 = "Nutrition__Physical_Activity__and_Obesity.csv"
FILE3 = "Personalized_Diet_Recommendations.csv"

def analyze_and_clean():
    print("--- 1. Analyzing health_fitness_dataset.csv (Standard Library) ---")
    
    data = []
    with open(FILE1, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert numeric fields
            try:
                row['age'] = int(row['age'])
                row['bmi'] = float(row['bmi'])
                row['daily_calories'] = int(row['daily_calories'])
                row['protein_g'] = float(row['protein_g'])
                row['carbs_g'] = float(row['carbs_g'])
                row['fat_g'] = float(row['fat_g'])
                row['water_liters'] = float(row['water_liters'])
                row['sleep_hours'] = float(row['sleep_hours'])
                row['activity_days_week'] = int(row['activity_days_week'])
                data.append(row)
            except (ValueError, TypeError):
                continue

    print(f"Total valid rows parsed: {len(data)}")
    
    # --- Finding the 'Optimal Health' Median Point ---
    # Define "Healthy" as BMI 18.5-25, 7-9h sleep, 3+ activity days, 2L+ water
    healthy_subset = [
        r for r in data 
        if 18.5 <= r['bmi'] <= 25 
        and 7 <= r['sleep_hours'] <= 9
        and r['activity_days_week'] >= 3
        and r['water_liters'] >= 2
    ]
    
    print(f"Healthy individuals found: {len(healthy_subset)}")
    
    if healthy_subset:
        metrics = ['daily_calories', 'protein_g', 'carbs_g', 'fat_g', 'water_liters', 'sleep_hours', 'bmi']
        print("\n--- Optimal Health Baseline (Median of Healthy Individuals) ---")
        for m in metrics:
            val = median([r[m] for r in healthy_subset])
            print(f"{m:20}: {val:.2f}")
    else:
        print("\n[!] No individuals met the strict 'Healthy' criteria in this sample.")

    # --- Create Master Dataset (Cleaned) ---
    master_csv_path = "master_health_data.csv"
    fieldnames = ['age', 'gender', 'height_cm', 'weight_kg', 'bmi', 'daily_calories', 
                  'protein_g', 'carbs_g', 'fat_g', 'water_liters', 'sleep_hours', 'activity_days_week']
    
    with open(master_csv_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(data)
        
    print(f"\n[✓] Master cleaned dataset saved to: {master_csv_path}")

if __name__ == "__main__":
    analyze_and_clean()
