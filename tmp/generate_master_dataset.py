import csv
from statistics import median
import os

# Updated correct paths and mappings
FILE1 = "health_fitness_dataset.csv"
FILE3 = "Personalized_Diet_Recommendations.csv"

def analyze_and_clean():
    print("--- 1. Analyzing health_fitness_dataset.csv (Corrected Mapping) ---")
    
    data = []
    with open(FILE1, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                # Map actual fields from the inspected headers
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

    print(f"Total valid individual rows parsed: {len(data)}")
    
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
    
    if not healthy_subset:
        print("[!] Loosening healthy criteria to BMI 18.5-27 and 6+ hours sleep.")
        healthy_subset = [
            r for r in data 
            if 18.5 <= r['bmi'] <= 27 
            and r['sleep_hours'] >= 6
        ]

    if healthy_subset:
        metrics = ['target_calories', 'hydration_liters', 'sleep_hours', 'bmi', 'daily_steps', 'stress_level']
        print("\n--- Optimal Health Baseline (Median Point) ---")
        for m in metrics:
            val = median([r[m] for r in healthy_subset])
            print(f"{m:20}: {val:.2f}")

    # --- 2. Incorporate Dietary Recommendation Averages (FILE3) ---
    print("\n--- 2. Analyzing Personalized_Diet_Recommendations.csv ---")
    diet_data = []
    with open(FILE3, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                diet_data.append({
                    'calories': int(row['Recommended_Meal_Plan_Calories']),
                    'protein': int(row['Recommended_Meal_Plan_Protein']),
                    'carbs': int(row['Recommended_Meal_Plan_Carbs']),
                    'fats': int(row['Recommended_Meal_Plan_Fats'])
                })
            except: continue
    
    if diet_data:
        print("\n--- Global Nutrient Baseline (Median Recommended Intake) ---")
        print(f"Calories : {median([d['calories'] for d in diet_data]):.1f}")
        print(f"Protein  : {median([d['protein'] for d in diet_data]):.1f}g")
        print(f"Carbs    : {median([d['carbs'] for d in diet_data]):.1f}g")
        print(f"Fats     : {median([d['fats'] for d in diet_data]):.1f}g")

    # --- 3. Create Master Dataset (Consistently Cleaned) ---
    master_csv_path = "master_health_data.csv"
    fieldnames = ['age', 'gender', 'height_cm', 'weight_kg', 'bmi', 'target_calories', 
                  'hydration_liters', 'sleep_hours', 'daily_steps', 'stress_level', 'activity_type']
    
    with open(master_csv_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(data)
        
    print(f"\n[✓] Master cleaned dataset saved to: {master_csv_path}")

if __name__ == "__main__":
    analyze_and_clean()
