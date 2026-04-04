import random

def predict_premium_ai(location, risk_score, policy):
    """
    Simulated Machine Learning Model for predicting Weekly Premiums.
    Analyzes historical risk factors such as geographical location and past weather/water-logging trends.
    """
    base = 50
    # Simulated Historical Weather / Flood Risk Database
    history_risk = {
        "high": {"water_logging_freq": 0.8, "base_surcharge": 20},
        "medium": {"water_logging_freq": 0.4, "base_surcharge": 10},
        "low": {"water_logging_freq": 0.05, "base_surcharge": -2} # AI identifies safe zone, subtracts ₹2
    }
    
    zone_data = history_risk.get(location, history_risk["medium"])
    base += zone_data["base_surcharge"]
    
    # Policy multiplier
    if policy == "standard":
        base += 20
    elif policy == "pro":
        base += 50
    
    # ML model adjustment based on a combination of active risk score and statistical probability
    ml_adjustment = int((risk_score * 5) + (zone_data["water_logging_freq"] * 10))
    
    final_premium = base + ml_adjustment
    return max(0, final_premium)
