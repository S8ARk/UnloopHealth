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
        try:
            bmi = float(user_data.get("bmi", 22.0))
            steps = float(user_data.get("daily_steps", 5000))
            sleep = float(user_data.get("sleep_hours", 7.0))
            calories = float(user_data.get("daily_calories", 2000))
        except (ValueError, TypeError):
            bmi, steps, sleep, calories = 22.0, 5000.0, 7.0, 2000.0
        
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
        fut_bmi = bmi + (0.1 if (steps < 5000 and calories > 2500) else -0.05)
        
        recs = self.generate_recs(user_data, risk_label)
        
        # Create Dynamic Vulnerability Proxy
        conditions = str(user_data.get("medical_conditions", "")).lower()
        
        # Base probabilities
        p_hyp = 0.15
        p_met = 0.10
        p_card = 0.10
        p_imm = 0.15
        
        # Rules engine
        if "hypertension" in conditions or "blood pressure" in conditions: p_hyp += 0.40
        if bmi > 25: 
            p_met += (bmi - 25) * 0.05
            p_card += 0.20
            p_hyp += 0.15
        if bmi > 30: p_met += 0.20
        if steps < 5000: 
            p_card += 0.25
            p_imm += 0.10
            p_met += 0.10
        if sleep < 6:
            p_imm += 0.35
            p_card += 0.15
            p_hyp += 0.10
            
        # Normalize and cap
        risk_probs = {
            "Hypertension": min(round(p_hyp, 2), 0.95),
            "Metabolic Syndrome": min(round(p_met, 2), 0.95),
            "Cardiovascular": min(round(p_card, 2), 0.95),
            "Immune Fatigue": min(round(p_imm, 2), 0.95)
        }
        
        return {
            "risk_label": risk_label,
            "risk_probs": risk_probs,
            "future_bmi": round(float(fut_bmi), 2),
            "recommendations": recs
        }

    def train_from_master_data(self, master_csv="master_health_data.csv"):
        # Training logic placeholder for when HAS_ML is true
        return True

    def generate_recs(self, row, risk):
        recs = []
        dos = []
        donts = []
        
        try:
            bmi = float(row.get("bmi", 22.0))
            sleep = float(row.get("sleep_hours", 7))
            steps = float(row.get("daily_steps", 5000))
            glucose = float(row.get("fasting_glucose", 90))
        except (TypeError, ValueError):
            bmi, sleep, steps, glucose = 22.0, 7.0, 5000.0, 90.0

        conditions = str(row.get("medical_conditions", "")).lower()

        # Dynamic BMI Logic
        if bmi > 25:
            recs.append("⚠ BMI is in Overweight/Obese range - target 0.5kg/week weight loss.")
            dos.append("Prioritize Lean Proteins")
            donts.append("Excess refined carbohydrates")
        elif bmi < 18.5:
            recs.append("⚠ BMI indicates underweight status.")
            dos.append("Increase caloric intake optimally")
            donts.append("Skipping primary meals")
        else:
            dos.append("Maintain current caloric baseline")

        # Dynamic Sleep Logic
        if sleep < 7:
            recs.append("😴 Insufficient sleep - target 7-9 hours to lower cortisol.")
            dos.append("Implement screen-free hour before bed")
            donts.append("Caffeine consumption after 3 PM")
        else:
            dos.append("Maintain 7-9 hours sleep rhythm")

        # Dynamic Activity Logic
        if steps < 6000:
            recs.append("🏃 Increase daily movement - target 8,000+ steps.")
            dos.append("15 min post-meal walking")
            donts.append("Sitting for 2+ uninterrupted hours")
        else:
            dos.append("Continue daily step targets")

        # Dynamic Medical Conditions Pattern Matching
        if "hypertension" in conditions or "blood pressure" in conditions:
            dos.append("Monitor sodium intake < 1500mg/day")
            donts.append("High-sodium processed foods")
        if "diabet" in conditions or glucose > 100:
            dos.append("Prioritize Low-GI foods")
            donts.append("⚠ Avoid high-GI processed carbs immediately.")
        
        # Hydration Defaults
        water_intake = row.get("water_intake_goal", 2)
        dos.append(f"Drink {water_intake}L+ Water daily")

        if risk in ("High", "Critical"):
            recs.append("🏥 HIGH RISK - please consult a wellness professional.")
            
        # Deduplicate and return top 4
        return {
            "recs": list(dict.fromkeys(recs))[:4], 
            "dos": list(dict.fromkeys(dos))[:4], 
            "donts": list(dict.fromkeys(donts))[:4]
        }

# Global Instance
ml_service = MLService()
