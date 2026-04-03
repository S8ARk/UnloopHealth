import pandas as pd
import numpy as np
import os

# Paths to the CSV files
FILE1 = "health_fitness_dataset.csv"
FILE2 = "Nutrition__Physical_Activity__and_Obesity.csv"
FILE3 = "Personalized_Diet_Recommendations.csv"

def analyze_and_clean():
    print("--- 1. Analyzing health_fitness_dataset.csv ---")
    df1 = pd.read_csv(FILE1)
    print(df1.info())
    print(df1.describe())
    
    print("\n--- 2. Analyzing Nutrition__Physical_Activity__and_Obesity.csv ---")
    df2 = pd.read_csv(FILE2)
    print(df2.info())
    
    print("\n--- 3. Analyzing Personalized_Diet_Recommendations.csv ---")
    df3 = pd.read_csv(FILE3)
    print(df3.info())
    print(df3.describe())

    # --- Data Cleaning & Merging Logic ---
    # We want to create a 'Master' dataset with common features:
    # Age, Gender, BMI, Nutrition (Calories, Protein, Carbs, Fat), Activity, and Health Category.

    # 1. Normalize df1
    # Assuming df1 has: Age, Gender, Weight, Height, BMI, etc.
    # Looking at the head from previous step: participant_id,date,age,gender,height_cm,weight_kg,bmi...
    df1_clean = df1[['age', 'gender', 'height_cm', 'weight_kg', 'bmi', 'daily_calories', 
                     'protein_g', 'carbs_g', 'fat_g', 'water_liters', 'sleep_hours', 'activity_days_week']]
    
    # 2. Find the "Max Satisfaction" (Optimal Health) point in df1
    # We can define "Healthy" as having Normal BMI (18.5-25), 7-9 hours sleep, 3+ activity days, and 2L+ water.
    healthy_mask = (
        (df1['bmi'] >= 18.5) & (df1['bmi'] <= 25) &
        (df1['sleep_hours'] >= 7) & (df1['sleep_hours'] <= 9) &
        (df1['activity_days_week'] >= 3) &
        (df1['water_liters'] >= 2)
    )
    healthy_subset = df1[healthy_mask]
    
    print("\n--- Optimal Health Baseline (Median of Healthy Individuals) ---")
    median_healthy = healthy_subset[['daily_calories', 'protein_g', 'carbs_g', 'fat_g', 'water_liters', 'sleep_hours', 'bmi']].median()
    print(median_healthy)

    # 3. Create Master Dataset
    # Since the datasets have different schemas, we will primarily use df1 as the base 
    # as it represents individual profiles, and augment it with patterns from others if possible.
    # For now, let's export the cleaned df1 as our 'Master' foundational dataset.
    
    master_csv_path = "master_health_data.csv"
    df1_clean.to_csv(master_csv_path, index=False)
    print(f"\n[✓] Master cleaned dataset saved to: {master_csv_path}")

if __name__ == "__main__":
    analyze_and_clean()
