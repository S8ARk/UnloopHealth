"""
================================================================================
 HEALTH & NUTRITION ML PIPELINE
 Inspired by:
   - CGMacros (PhysioNet) – continuous glucose + macronutrient data
   - Personalized Medical Diet Recommendations (Kaggle)
   - Food Nutrition Dataset (Kaggle)
   - Nutrition, Physical Activity & Obesity (Kaggle)
   - AI4FoodDB (PMC/NCBI) – wearable + lifestyle data
   - Health & Fitness Dataset (Kaggle)
================================================================================

Features
--------
  1. Synthetic data generation that mimics all 6 datasets
  2. Multi-class health risk classification (Random Forest + XGBoost)
  3. Dietary category classification (Balanced / Deficit / Surplus / Unhealthy)
  4. Obesity risk prediction (Logistic Regression + Gradient Boosting)
  5. Future health metric forecasting (next 30 days) via time-series regression
  6. Interactive CLI: enter your own vitals/diet data and get instant predictions
  7. Full evaluation report: accuracy, confusion matrix, feature importance

Usage
-----
  pip install numpy pandas scikit-learn xgboost matplotlib seaborn joblib
  python health_nutrition_ml_pipeline.py
"""

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")          # headless – saves plots to files
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import (
    accuracy_score, classification_report,
    confusion_matrix, mean_absolute_error, r2_score
)
from sklearn.pipeline import Pipeline
import joblib
import os

# ─── optional XGBoost ────────────────────────────────────────────────────────
try:
    from xgboost import XGBClassifier
    HAS_XGB = True
except ImportError:
    HAS_XGB = False
    print("[INFO] xgboost not found – using GradientBoostingClassifier instead.\n")

np.random.seed(42)

# ═══════════════════════════════════════════════════════════════════════════════
#  1. SYNTHETIC DATA GENERATION
# ═══════════════════════════════════════════════════════════════════════════════

def generate_dataset(n: int = 3000) -> pd.DataFrame:
    """
    Generates a realistic health + nutrition dataset synthesising the schema /
    feature space of all 6 referenced datasets.
    """
    # ── Demographics (AI4FoodDB + Health & Fitness) ──
    age           = np.random.randint(18, 75, n)
    gender        = np.random.choice(["Male", "Female"], n)
    height_cm     = np.where(gender == "Male",
                             np.random.normal(175, 8, n),
                             np.random.normal(163, 7, n))
    weight_kg     = np.random.normal(72, 18, n).clip(40, 160)
    bmi           = weight_kg / (height_cm / 100) ** 2

    # ── Activity (Nutrition, Physical Activity & Obesity dataset) ──
    activity_days_per_week = np.random.randint(0, 8, n)         # 0–7
    avg_steps_per_day      = (activity_days_per_week * 1800
                               + np.random.normal(0, 500, n)).clip(0, 25000)
    sedentary_hours        = np.random.uniform(4, 16, n)

    # ── Nutrition (Food Nutrition + Personalized Diet datasets) ──
    daily_calories  = np.random.normal(2200, 500, n).clip(800, 5000)
    protein_g       = np.random.normal(75, 25, n).clip(10, 250)
    carbs_g         = np.random.normal(280, 70, n).clip(50, 600)
    fat_g           = np.random.normal(85, 30, n).clip(10, 200)
    fiber_g         = np.random.normal(20, 8, n).clip(2, 60)
    sugar_g         = np.random.normal(60, 30, n).clip(0, 200)
    sodium_mg       = np.random.normal(2300, 800, n).clip(200, 6000)
    water_liters    = np.random.normal(2.0, 0.6, n).clip(0.5, 5.0)

    # ── CGM-like glucose features (CGMacros) ──
    fasting_glucose  = np.random.normal(95, 18, n).clip(60, 200)
    postmeal_glucose = fasting_glucose + np.random.normal(40, 20, n).clip(0, 120)
    glucose_variability = np.random.normal(15, 8, n).clip(2, 60)   # SD of CGM

    # ── Clinical / Wearable vitals (AI4FoodDB) ──
    systolic_bp      = np.random.normal(120, 18, n).clip(80, 200)
    diastolic_bp     = np.random.normal(78, 12, n).clip(50, 130)
    resting_hr       = np.random.normal(72, 12, n).clip(40, 120)
    sleep_hours      = np.random.normal(7.0, 1.2, n).clip(3, 12)
    stress_score     = np.random.randint(1, 11, n)                 # 1–10

    # ── Lab markers ──
    total_cholesterol = np.random.normal(195, 40, n).clip(100, 350)
    hdl               = np.random.normal(55, 15, n).clip(20, 110)
    ldl               = total_cholesterol - hdl - np.random.normal(30, 10, n)
    triglycerides     = np.random.normal(140, 60, n).clip(40, 500)
    hba1c             = (fasting_glucose / 28.7 + 2.15 +
                         np.random.normal(0, 0.3, n)).clip(4.0, 12.0)

    # ─── Derived targets ─────────────────────────────────────────────────────
    # 1) BMI category
    bmi_cat = pd.cut(bmi, bins=[0, 18.5, 25, 30, np.inf],
                     labels=["Underweight", "Normal", "Overweight", "Obese"])

    # 2) Diet Quality score → category
    diet_score = (
          (protein_g.clip(0, 100)   / 100) * 20
        + (fiber_g.clip(0, 40)      / 40)  * 20
        + (water_liters.clip(0, 3)  / 3)   * 15
        - (sugar_g.clip(0, 150)     / 150) * 15
        - (sodium_mg.clip(0, 5000)  / 5000) * 15
        + (activity_days_per_week   / 7)   * 15
    )
    diet_cat = pd.cut(diet_score,
                      bins=[-np.inf, 20, 35, 50, np.inf],
                      labels=["Unhealthy", "Poor", "Moderate", "Healthy"])

    # 3) Health Risk (multi-class) – rule-based composite
    risk_score = np.zeros(n)
    risk_score += (bmi > 30).astype(float) * 2
    risk_score += (bmi < 18.5).astype(float) * 1.5
    risk_score += (fasting_glucose > 126).astype(float) * 2
    risk_score += (systolic_bp > 140).astype(float) * 1.5
    risk_score += (total_cholesterol > 240).astype(float) * 1
    risk_score += (activity_days_per_week < 2).astype(float) * 1
    risk_score += (sleep_hours < 6).astype(float) * 1
    risk_score += (stress_score > 7).astype(float) * 0.5
    risk_score += (hba1c > 6.5).astype(float) * 2
    risk_score += np.random.normal(0, 0.5, n)

    health_risk = pd.cut(risk_score,
                         bins=[-np.inf, 1, 3, 5, np.inf],
                         labels=["Low", "Moderate", "High", "Critical"])

    # 4) Obesity risk (binary)
    obesity_risk = (bmi >= 30).astype(int)

    df = pd.DataFrame({
        "age": age,
        "gender": gender,
        "height_cm": height_cm.round(1),
        "weight_kg": weight_kg.round(1),
        "bmi": bmi.round(2),

        "activity_days_week": activity_days_per_week,
        "avg_steps_day": avg_steps_per_day.round(0).astype(int),
        "sedentary_hours": sedentary_hours.round(1),

        "daily_calories": daily_calories.round(0).astype(int),
        "protein_g": protein_g.round(1),
        "carbs_g": carbs_g.round(1),
        "fat_g": fat_g.round(1),
        "fiber_g": fiber_g.round(1),
        "sugar_g": sugar_g.round(1),
        "sodium_mg": sodium_mg.round(0).astype(int),
        "water_liters": water_liters.round(2),

        "fasting_glucose": fasting_glucose.round(1),
        "postmeal_glucose": postmeal_glucose.round(1),
        "glucose_variability": glucose_variability.round(2),

        "systolic_bp": systolic_bp.round(0).astype(int),
        "diastolic_bp": diastolic_bp.round(0).astype(int),
        "resting_hr": resting_hr.round(0).astype(int),
        "sleep_hours": sleep_hours.round(1),
        "stress_score": stress_score,

        "total_cholesterol": total_cholesterol.round(1),
        "hdl": hdl.round(1),
        "ldl": ldl.round(1),
        "triglycerides": triglycerides.round(1),
        "hba1c": hba1c.round(2),

        "bmi_category": bmi_cat.astype(str),
        "diet_quality": diet_cat.astype(str),
        "health_risk": health_risk.astype(str),
        "obesity_risk": obesity_risk,
    })
    return df


# ═══════════════════════════════════════════════════════════════════════════════
#  2.  FEATURE COLUMNS
# ═══════════════════════════════════════════════════════════════════════════════

FEATURE_COLS = [
    "age", "bmi", "activity_days_week", "avg_steps_day", "sedentary_hours",
    "daily_calories", "protein_g", "carbs_g", "fat_g", "fiber_g",
    "sugar_g", "sodium_mg", "water_liters",
    "fasting_glucose", "postmeal_glucose", "glucose_variability",
    "systolic_bp", "diastolic_bp", "resting_hr",
    "sleep_hours", "stress_score",
    "total_cholesterol", "hdl", "ldl", "triglycerides", "hba1c",
]

# Gender → 0/1 added separately
ALL_FEATURES = FEATURE_COLS + ["gender_num"]


# ═══════════════════════════════════════════════════════════════════════════════
#  3.  MODEL TRAINING
# ═══════════════════════════════════════════════════════════════════════════════

def prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["gender_num"] = (df["gender"] == "Male").astype(int)
    return df[ALL_FEATURES]


def train_all_models(df: pd.DataFrame) -> dict:
    df = prepare_features(df.copy().assign(
        gender_num=(df["gender"] == "Male").astype(int)
    ))
    X = df[ALL_FEATURES].values
    results = {}

    # ── 3a. Health Risk Classifier ──────────────────────────────────────────
    print("▶  Training Health Risk Classifier …")
    le_risk = LabelEncoder()
    y_risk  = le_risk.fit_transform(df_raw["health_risk"])
    X_tr, X_te, y_tr, y_te = train_test_split(X, y_risk, test_size=0.2)

    clf_risk = RandomForestClassifier(n_estimators=200, max_depth=12, random_state=42)
    clf_risk.fit(X_tr, y_tr)
    preds = clf_risk.predict(X_te)
    acc   = accuracy_score(y_te, preds)
    print(f"   Health Risk  → Accuracy: {acc:.3f}")
    print(classification_report(y_te, preds, target_names=le_risk.classes_))
    results["health_risk"] = {"model": clf_risk, "encoder": le_risk, "accuracy": acc}

    # ── 3b. Diet Quality Classifier ─────────────────────────────────────────
    print("▶  Training Diet Quality Classifier …")
    le_diet = LabelEncoder()
    y_diet  = le_diet.fit_transform(df_raw["diet_quality"])
    X_tr, X_te, y_tr, y_te = train_test_split(X, y_diet, test_size=0.2)

    if HAS_XGB:
        clf_diet = XGBClassifier(n_estimators=200, max_depth=6,
                                 use_label_encoder=False,
                                 eval_metric="mlogloss", random_state=42)
    else:
        clf_diet = GradientBoostingClassifier(n_estimators=200, max_depth=5, random_state=42)

    clf_diet.fit(X_tr, y_tr)
    preds = clf_diet.predict(X_te)
    acc   = accuracy_score(y_te, preds)
    print(f"   Diet Quality → Accuracy: {acc:.3f}")
    print(classification_report(y_te, preds, target_names=le_diet.classes_))
    results["diet_quality"] = {"model": clf_diet, "encoder": le_diet, "accuracy": acc}

    # ── 3c. BMI Category Classifier ─────────────────────────────────────────
    print("▶  Training BMI Category Classifier …")
    le_bmi = LabelEncoder()
    y_bmi  = le_bmi.fit_transform(df_raw["bmi_category"])
    X_tr, X_te, y_tr, y_te = train_test_split(X, y_bmi, test_size=0.2)

    clf_bmi = RandomForestClassifier(n_estimators=150, random_state=42)
    clf_bmi.fit(X_tr, y_tr)
    preds = clf_bmi.predict(X_te)
    acc   = accuracy_score(y_te, preds)
    print(f"   BMI Category → Accuracy: {acc:.3f}\n")
    results["bmi_category"] = {"model": clf_bmi, "encoder": le_bmi, "accuracy": acc}

    # ── 3d. Obesity Risk (Binary) ────────────────────────────────────────────
    print("▶  Training Obesity Risk Classifier …")
    y_ob = df_raw["obesity_risk"].values
    X_tr, X_te, y_tr, y_te = train_test_split(X, y_ob, test_size=0.2)

    clf_ob = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(max_iter=500, random_state=42))
    ])
    clf_ob.fit(X_tr, y_tr)
    preds = clf_ob.predict(X_te)
    acc   = accuracy_score(y_te, preds)
    print(f"   Obesity Risk → Accuracy: {acc:.3f}\n")
    results["obesity_risk"] = {"model": clf_ob, "accuracy": acc}

    # ── 3e. Future BMI Regressor (30-day forecast) ──────────────────────────
    print("▶  Training Future BMI Forecaster (30-day) …")
    # Target: projected BMI after 30 days assuming current trajectory
    future_bmi = (df_raw["bmi"].values
                  - df_raw["activity_days_week"].values * 0.03
                  + (df_raw["daily_calories"].values - 2200) / 3500 * 0.2
                  + np.random.normal(0, 0.3, len(df_raw)))
    X_tr, X_te, y_tr, y_te = train_test_split(X, future_bmi, test_size=0.2)

    reg_bmi = Pipeline([
        ("scaler", StandardScaler()),
        ("reg", GradientBoostingRegressor(n_estimators=200, max_depth=5, random_state=42))
    ])
    reg_bmi.fit(X_tr, y_tr)
    preds_r = reg_bmi.predict(X_te)
    mae     = mean_absolute_error(y_te, preds_r)
    r2      = r2_score(y_te, preds_r)
    print(f"   Future BMI   → MAE: {mae:.3f}  R²: {r2:.3f}\n")
    results["future_bmi"] = {"model": reg_bmi, "mae": mae, "r2": r2}

    # ── 3f. Future Fasting Glucose Regressor ────────────────────────────────
    print("▶  Training Future Glucose Forecaster (30-day) …")
    future_glucose = (df_raw["fasting_glucose"].values
                      + (df_raw["carbs_g"].values - 280) * 0.05
                      - df_raw["activity_days_week"].values * 1.5
                      + df_raw["stress_score"].values * 0.8
                      + np.random.normal(0, 3, len(df_raw)))
    X_tr, X_te, y_tr, y_te = train_test_split(X, future_glucose, test_size=0.2)

    reg_gluc = Pipeline([
        ("scaler", StandardScaler()),
        ("reg", GradientBoostingRegressor(n_estimators=200, max_depth=5, random_state=42))
    ])
    reg_gluc.fit(X_tr, y_tr)
    preds_r = reg_gluc.predict(X_te)
    mae     = mean_absolute_error(y_te, preds_r)
    r2      = r2_score(y_te, preds_r)
    print(f"   Future Glucose → MAE: {mae:.3f}  R²: {r2:.3f}\n")
    results["future_glucose"] = {"model": reg_gluc, "mae": mae, "r2": r2}

    return results


# ═══════════════════════════════════════════════════════════════════════════════
#  4.  VISUALIZATION
# ═══════════════════════════════════════════════════════════════════════════════

def save_plots(df: pd.DataFrame, results: dict, out_dir: str = "."):
    os.makedirs(out_dir, exist_ok=True)
    sns.set_theme(style="whitegrid", palette="muted")

    # Feature importance – Health Risk
    fi = results["health_risk"]["model"].feature_importances_
    fi_df = pd.DataFrame({"feature": ALL_FEATURES, "importance": fi})
    fi_df = fi_df.sort_values("importance", ascending=False).head(15)

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle("Health & Nutrition ML Pipeline – Model Insights", fontsize=15, fontweight="bold")

    # Plot 1 – Feature Importance
    sns.barplot(data=fi_df, y="feature", x="importance", ax=axes[0, 0], palette="viridis")
    axes[0, 0].set_title("Top-15 Feature Importances (Health Risk RF)")

    # Plot 2 – BMI distribution by health risk
    order = ["Low", "Moderate", "High", "Critical"]
    order = [o for o in order if o in df["health_risk"].unique()]
    sns.boxplot(data=df, x="health_risk", y="bmi", order=order,
                ax=axes[0, 1], palette="RdYlGn_r")
    axes[0, 1].set_title("BMI Distribution by Health Risk Level")

    # Plot 3 – Glucose vs HbA1c
    sample = df.sample(500)
    axes[1, 0].scatter(sample["fasting_glucose"], sample["hba1c"],
                       c=sample["obesity_risk"], cmap="coolwarm", alpha=0.6, s=15)
    axes[1, 0].set_xlabel("Fasting Glucose (mg/dL)")
    axes[1, 0].set_ylabel("HbA1c (%)")
    axes[1, 0].set_title("Glucose vs HbA1c (red = obese)")

    # Plot 4 – Confusion matrix: health risk
    le_risk  = results["health_risk"]["encoder"]
    X_all    = prepare_features(df.assign(gender_num=(df["gender"] == "Male").astype(int)))[ALL_FEATURES].values
    y_all    = le_risk.transform(df["health_risk"])
    y_pred   = results["health_risk"]["model"].predict(X_all)
    cm       = confusion_matrix(y_all, y_pred)
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=le_risk.classes_,
                yticklabels=le_risk.classes_,
                ax=axes[1, 1])
    axes[1, 1].set_title("Confusion Matrix – Health Risk")

    plt.tight_layout()
    path = os.path.join(out_dir, "model_insights.png")
    plt.savefig(path, dpi=120)
    plt.close()
    print(f"[✓] Plot saved → {path}")


# ═══════════════════════════════════════════════════════════════════════════════
#  5.  DIETARY RECOMMENDATIONS ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

def generate_recommendations(row: dict, risk: str, diet: str) -> list:
    recs = []
    if row["bmi"] > 30:
        recs.append("⚠  BMI is in the Obese range – target 0.5–1 kg/week weight loss via caloric deficit.")
    if row["bmi"] < 18.5:
        recs.append("⚠  BMI is below healthy range – increase caloric intake with nutrient-dense foods.")
    if row["fasting_glucose"] > 100:
        recs.append("🩸 Elevated fasting glucose – reduce refined carbs, increase fiber & daily walking.")
    if row["hba1c"] > 5.7:
        recs.append("🩸 Pre-diabetic HbA1c – consult a physician; adopt a low-GI diet.")
    if row["systolic_bp"] > 130:
        recs.append("❤️  Elevated blood pressure – reduce sodium (<2000 mg/day), increase potassium-rich foods.")
    if row["activity_days_week"] < 3:
        recs.append("🏃 Low activity – aim for ≥150 min/week moderate-intensity aerobic exercise (WHO guideline).")
    if row["sleep_hours"] < 7:
        recs.append("😴 Insufficient sleep – target 7–9 hours; sleep deprivation raises cortisol & appetite.")
    if row["water_liters"] < 1.5:
        recs.append("💧 Low hydration – increase water intake to ≥2 L/day.")
    if row["fiber_g"] < 15:
        recs.append("🌾 Low dietary fiber – add vegetables, legumes, whole grains (target ≥25 g/day).")
    if row["stress_score"] >= 8:
        recs.append("🧘 High stress – consider mindfulness, yoga, or CBT to lower cortisol.")
    if risk in ("High", "Critical"):
        recs.append("🏥 HIGH RISK – please schedule a comprehensive metabolic panel with your physician.")
    if not recs:
        recs.append("✅ Current profile looks healthy – maintain your lifestyle and schedule annual check-ups.")
    return recs


# ═══════════════════════════════════════════════════════════════════════════════
#  6.  INTERACTIVE PREDICTION CLI
# ═══════════════════════════════════════════════════════════════════════════════

PROMPTS = [
    ("age",                "Age (years)",                              35),
    ("weight_kg",          "Weight (kg)",                             72),
    ("height_cm",          "Height (cm)",                            170),
    ("gender",             "Gender [Male/Female]",                 "Male"),
    ("activity_days_week", "Activity days/week (0–7)",                 3),
    ("avg_steps_day",      "Average steps/day",                    8000),
    ("sedentary_hours",    "Sedentary hours/day",                     8),
    ("daily_calories",     "Daily calories (kcal)",                2200),
    ("protein_g",          "Protein intake (g/day)",                  75),
    ("carbs_g",            "Carbohydrate intake (g/day)",            280),
    ("fat_g",              "Fat intake (g/day)",                      85),
    ("fiber_g",            "Fiber intake (g/day)",                    20),
    ("sugar_g",            "Sugar intake (g/day)",                    50),
    ("sodium_mg",          "Sodium intake (mg/day)",               2300),
    ("water_liters",       "Water intake (L/day)",                   2.0),
    ("fasting_glucose",    "Fasting blood glucose (mg/dL)",           90),
    ("postmeal_glucose",   "Post-meal glucose (mg/dL)",              130),
    ("glucose_variability","Glucose variability / SD (mg/dL)",        12),
    ("systolic_bp",        "Systolic blood pressure (mmHg)",         120),
    ("diastolic_bp",       "Diastolic blood pressure (mmHg)",         78),
    ("resting_hr",         "Resting heart rate (bpm)",                70),
    ("sleep_hours",        "Sleep hours/night",                       7.0),
    ("stress_score",       "Stress score (1–10)",                      4),
    ("total_cholesterol",  "Total cholesterol (mg/dL)",              190),
    ("hdl",                "HDL cholesterol (mg/dL)",                 55),
    ("ldl",                "LDL cholesterol (mg/dL)",                110),
    ("triglycerides",      "Triglycerides (mg/dL)",                  130),
    ("hba1c",              "HbA1c (%)",                              5.2),
]


def get_input(prompt: str, default):
    try:
        val = input(f"  {prompt} [{default}]: ").strip()
        if val == "":
            return default
        return type(default)(val)
    except (ValueError, EOFError):
        return default


def interactive_predict(results: dict):
    print("\n" + "═" * 70)
    print("  🩺  HEALTH & NUTRITION PREDICTOR  –  Enter Your Details")
    print("       (Press ENTER to accept default value in brackets)")
    print("═" * 70 + "\n")

    row = {}
    for key, prompt, default in PROMPTS:
        row[key] = get_input(prompt, default)

    # Derived
    row["bmi"]        = row["weight_kg"] / (row["height_cm"] / 100) ** 2
    row["gender_num"] = 1 if str(row["gender"]).strip().lower() == "male" else 0

    vec = np.array([[row[f] for f in ALL_FEATURES]], dtype=float)

    # Predictions
    le_risk  = results["health_risk"]["encoder"]
    le_diet  = results["diet_quality"]["encoder"]
    le_bmi   = results["bmi_category"]["encoder"]

    risk_pred  = le_risk.inverse_transform(results["health_risk"]["model"].predict(vec))[0]
    risk_proba = results["health_risk"]["model"].predict_proba(vec)[0]
    diet_pred  = le_diet.inverse_transform(results["diet_quality"]["model"].predict(vec))[0]
    bmi_pred   = le_bmi.inverse_transform(results["bmi_category"]["model"].predict(vec))[0]
    obesity    = results["obesity_risk"]["model"].predict(vec)[0]
    fut_bmi    = results["future_bmi"]["model"].predict(vec)[0]
    fut_gluc   = results["future_glucose"]["model"].predict(vec)[0]

    bmi_change = fut_bmi - row["bmi"]
    gluc_change = fut_gluc - row["fasting_glucose"]

    print("\n" + "═" * 70)
    print("  📊  PREDICTION RESULTS")
    print("═" * 70)
    print(f"  Current BMI             : {row['bmi']:.2f}  →  {bmi_pred}")
    print(f"  Health Risk Level       : {risk_pred}")
    risk_pct = {cls: f"{p*100:.1f}%" for cls, p in zip(le_risk.classes_, risk_proba)}
    print(f"  Risk Probabilities      : {risk_pct}")
    print(f"  Diet Quality            : {diet_pred}")
    print(f"  Obesity Risk            : {'⚠  YES' if obesity else '✅ NO'}")
    print()
    print(f"  ── 30-Day Forecast ──────────────────────────────────────────")
    arrow = ("📈" if bmi_change > 0 else "📉") if abs(bmi_change) > 0.05 else "➡"
    print(f"  Projected BMI           : {fut_bmi:.2f}  ({arrow} {bmi_change:+.2f} kg/m²)")
    arrow_g = ("📈" if gluc_change > 2 else "📉") if abs(gluc_change) > 2 else "➡"
    print(f"  Projected Fasting Glucose: {fut_gluc:.1f} mg/dL  ({arrow_g} {gluc_change:+.1f})")
    print()
    print("  ── Personalised Recommendations ─────────────────────────────")
    recs = generate_recommendations(row, risk_pred, diet_pred)
    for r in recs:
        print(f"  {r}")
    print("═" * 70 + "\n")


# ═══════════════════════════════════════════════════════════════════════════════
#  7.  SAVE & RELOAD MODELS
# ═══════════════════════════════════════════════════════════════════════════════

def save_models(results: dict, out_dir: str = "saved_models"):
    os.makedirs(out_dir, exist_ok=True)
    for name, obj in results.items():
        path = os.path.join(out_dir, f"{name}.pkl")
        joblib.dump(obj, path)
    print(f"[✓] Models saved to ./{out_dir}/")


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 70)
    print("  HEALTH & NUTRITION ML PIPELINE")
    print("  Inspired by CGMacros, AI4FoodDB, Kaggle Nutrition Datasets")
    print("=" * 70 + "\n")

    # Step 1 – Generate data
    print("▶  Generating synthetic dataset (n=3000) …")
    df_raw = generate_dataset(3000)
    print(f"   Dataset shape: {df_raw.shape}")
    print(f"   Columns: {list(df_raw.columns)}\n")

    # Quick data preview
    print("   Sample rows:")
    print(df_raw[["age", "bmi", "health_risk", "diet_quality",
                  "fasting_glucose", "hba1c"]].head(5).to_string(index=False))
    print()

    # Step 2 – Train models
    results = train_all_models(df_raw)

    # Step 3 – Save plots
    save_plots(df_raw, results, out_dir=".")

    # Step 4 – Save models
    save_models(results, out_dir="saved_models")

    # Step 5 – Cross-validation summary
    print("\n▶  Cross-Validation (5-fold) – Health Risk Classifier …")
    X_cv = prepare_features(df_raw.assign(
        gender_num=(df_raw["gender"] == "Male").astype(int)
    ))[ALL_FEATURES].values
    y_cv = results["health_risk"]["encoder"].transform(df_raw["health_risk"])
    cv_scores = cross_val_score(results["health_risk"]["model"], X_cv, y_cv, cv=5)
    print(f"   CV Accuracy: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}\n")

    # Step 6 – Interactive prediction
    try:
        interactive_predict(results)
    except KeyboardInterrupt:
        print("\n[Skipped interactive prediction]\n")
