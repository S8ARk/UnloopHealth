import math

class RiskEngine:
    def __init__(self, weights=None):
        # Default weights derived from clinical focus in SDLC.md
        self.weights = weights or {
            "diabetes": {"sugar": 0.4, "gi_load": 0.3, "bmi": 0.3},
            "hypertension": {"sodium": 0.4, "sat_fat": 0.2, "bmi": 0.3, "stress": 0.1},
            "heart_disease": {"sat_fat": 0.4, "fiber": -0.3, "cholesterol": 0.3},
            "obesity": {"caloric_surplus": 0.7, "activity": -0.3}
        }
        
        # Clinical thresholds (e.g., sugar > 50g/d is high risk)
        self.thresholds = {
            "sugar": 50,      # grams/day
            "sodium": 2300,   # mg/day
            "sat_fat": 20,    # grams/day
            "fiber": 25,      # grams/day (lower is risky)
            "bmi": 27,        # overweight threshold
            "gi_load": 120    # daily load
        }

    def calculate_normalized_factor(self, value, threshold, inverse=False):
        """Scale factor from 0 to 100 based on threshold."""
        if threshold == 0: return 0
        
        if inverse:
            # For things like fiber where more is better
            score = max(0, min(100, (1 - (value / threshold)) * 100))
        else:
            score = max(0, min(100, (value / threshold) * 100))
        return score

    def calculate_diabetes_risk(self, averages, profile):
        """
        Input: 30-day averages {sugar, gi_load}, user profile {bmi}
        Output: score 0-100
        """
        f_sugar = self.calculate_normalized_factor(averages.get('sugar', 0), self.thresholds['sugar'])
        f_gi = self.calculate_normalized_factor(averages.get('gi_load', 0), self.thresholds['gi_load'])
        f_bmi = self.calculate_normalized_factor(profile.get('bmi', 22), self.thresholds['bmi'])

        w = self.weights['diabetes']
        score = (f_sugar * w['sugar']) + (f_gi * w['gi_load']) + (f_bmi * w['bmi'])
        return round(score, 1)

    def calculate_months_to_critical(self, current_score, previous_score, days_elapsed=30):
        """
        Estimate time until risk hits 'Critical' (85/100)
        """
        if days_elapsed <= 0: return None
        
        velocity = (current_score - previous_score) / days_elapsed  # Risk points per day
        
        if velocity <= 0:
            return float('inf')  # Improving or stable
            
        points_to_critical = 85 - current_score
        if points_to_critical <= 0:
            return 0  # Already critical
            
        days_to_critical = points_to_critical / velocity
        months = days_to_critical / 30
        return round(months, 1)

# Singleton instance
risk_engine = RiskEngine()
