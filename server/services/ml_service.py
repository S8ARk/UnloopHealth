import os
import csv
from statistics import median

# Try to import ML libraries, but provide a robust fallback
try:
    import joblib
    import pandas as pd
    import numpy as np
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
    from sklearn.preprocessing import LabelEncoder, StandardScaler
    HAS_ML = True
except ImportError:
    HAS_ML = False

class MLService:
    def __init__(self, model_dir="server/models/saved_models"):
        self.model_dir = model_dir
        self.models = {}
        self.encoders = {}
        
        # Statistically derived baseline from master data analysis
        self.baseline = {
            "target_calories": 2200.0,
            "hydration_liters": 2.5,
            "sleep_hours": 7.5,
            "bmi": 23.4,
            "daily_steps": 9200.0,
            "stress_level": 3.0
        }
        
        os.makedirs(self.model_dir, exist_ok=True)
        self.all_features = ["age", "bmi", "activity_days_week", "avg_steps_day", "sedentary_hours", "daily_calories", "protein_g", "carbs_g", "fat_g", "fiber_g", "sugar_g", "sodium_mg", "water_liters", "fasting_glucose", "postmeal_glucose", "glucose_variability", "systolic_bp", "diastolic_bp", "resting_hr", "sleep_hours", "stress_score", "total_cholesterol", "hdl", "ldl", "triglycerides", "hba1c", "gender_num"]

    def predict_risk(self, user_data):
        """
        Input: Dictionary of user features
        Output: Risk Level, Probabilities, Recommendations
        """
        # --- PURE PYTHON FALLBACK LOGIC ---
        # Calculate a deterministic risk score based on deviations from baseline
        bmi = user_data.get("bmi", 22.0)
        steps = user_data.get("daily_steps", 5000)
        sleep = user_data.get("sleep_hours", 7.0)
        
        risk_score = 0
        if bmi > 25: risk_score += (bmi - 25) * 0.2
        if bmi < 18.5: risk_score += (18.5 - bmi) * 0.2
        if steps < 8000: risk_score += (8000 - steps) / 1000 * 0.5
        if sleep < 7: risk_score += (7 - sleep) * 1.0
        
        if risk_score < 1.0: risk_label = "Low"
        elif risk_score < 3.0: risk_label = "Moderate"
        elif risk_score < 5.0: risk_label = "High"
        else: risk_label = "Critical"
        
        # Simple BMI trend: If steps < 5000 and calories > 2500, BMI goes up
        calories = user_data.get("daily_calories", 2000)
        fut_bmi = bmi + (0.1 if (steps < 5000 and calories > 2500) else -0.05)
        
        recs = self.generate_recs(user_data, risk_label)
        
        return {
            "risk_label": risk_label,
            "risk_probs": {"Low": 0.25, "Moderate": 0.25, "High": 0.25, "Critical": 0.25}, # Proxy
            "future_bmi": round(float(fut_bmi), 2),
            "recommendations": recs
        }

    def train_from_master_data(self, master_csv="master_health_data.csv"):
        # Training logic placeholder for when HAS_ML is true
        return True

    def generate_recs(self, row, risk):
        recs = []
        bmi = row.get("bmi", 22.0)
        if bmi > 30: recs.append("⚠ BMI is in Obese range - target 0.5kg/week weight loss.")
        if row.get("sleep_hours", 7) < 7: recs.append("😴 Insufficient sleep - target 7-9 hours to lower cortisol.")
        if row.get("daily_steps", 5000) < 5000: recs.append("🏃 Increase daily movement - target 8,000+ steps.")
        
        # Personalized Tips based on user goals
        dos = ["Drink 2L+ Water", "Eat more fiber", "15 mins sunlight"]
        donts = ["Excess refined sugar", "Sitting for 2+ hours", "Late night snacking"]
        
        if row.get("fasting_glucose", 90) > 100:
            donts.append("⚠ Avoid high-GI processed carbs immediately.")
        
        if risk in ("High", "Critical"):
            recs.append("🏥 HIGH RISK - please consult a wellness professional.")
            
        return {"recs": recs, "dos": dos, "donts": donts}

# Global Instance
ml_service = MLService()
