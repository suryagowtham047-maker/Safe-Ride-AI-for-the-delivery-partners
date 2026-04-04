import random

def get_automated_disruptions(temp, weather):
    """
    Simulates 5 public/mock APIs to fetch real-time disruptions dynamically.
    """
    disruptions = []
    
    # 1. Extreme Weather (Real OR Simulated)
    if weather and "Rain" in weather:
        disruptions.append({"type": "Weather", "reason": "Heavy Rain & Waterlogging Risk", "severity": "medium"})
        
    # 2. Extreme Heat (Real OR Simulated)
    if temp and temp > 40:
        disruptions.append({"type": "Heatwave", "reason": f"Extreme Heatwave ({temp}°C)", "severity": "high"})
        
    # 3. Air Quality (Mock API) - Simulated AQI spike
    aqi = random.choice([50, 120, 180, 350])
    if aqi > 300:
        disruptions.append({"type": "AirQuality", "reason": f"Hazardous Smog (AQI {aqi})", "severity": "medium"})
        
    # 4. Traffic/Road Blockade (Mock Maps API)
    if random.random() < 0.25: # 25% chance of random roadblock simulation
        disruptions.append({"type": "Traffic", "reason": "Major Road Blockade API Trigger", "severity": "low"})
        
    # 5. Civic Disturbance/Curfew (Mock News API)
    if random.random() < 0.15: # 15% chance of civic issue
        disruptions.append({"type": "Civic", "reason": "Local Curfew Alert / Civil Unrest", "severity": "high"})
        
    return disruptions


def calculate_payouts(disruptions, policy='basic'):
    """
    Calculates zero-touch automated claim payouts based on parsed disruptions and user policy.
    """
    payouts = []
    policy = policy.lower()
    
    # Determine base payout magnitude per policy type
    base_magnitudes = {"basic": 50, "standard": 100, "pro": 250}
    multiplier = {"low": 1.0, "medium": 1.5, "high": 2.5}
    
    base_amount = base_magnitudes.get(policy, 50)
    
    for d in disruptions:
        amt = int(base_amount * multiplier.get(d["severity"], 1.0))
        payouts.append({
            "reason": d["reason"],
            "amount": amt
        })
        
    return payouts
