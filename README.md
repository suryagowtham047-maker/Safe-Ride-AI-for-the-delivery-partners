# SafeRide AI for Delivery Partners
AI-powered parametric insurance platform that protects delivery workers from income loss due to external disruptions like weather and pollution.
## Team & Responsibilities
- Gowtham – Backend & System Design
- Chandu – API Integration
- Manikanta – AI/Risk Model
- Vijay – Dashboard & Presentation
- Kaveri – Frontend Development

## Problem Statement
Delivery workers lose income due to external conditions like rain, heat, and pollution. There is no system to protect their earnings.

## Persona
Example: Ravi, a delivery worker, cannot work during heavy rain and loses income.

## Workflow
- User registers
- Weekly plan is created
- System monitors weather
- If disruption occurs → payout is triggered

## Weekly Premium
Premium depends on location risk and past data.

## Parametric Triggers
- Heavy rain
- Extreme temperature
- High pollution

## AI Usage
- Risk calculation
- Premium adjustment
- Fraud detection

## Fraud Detection
- Detect duplicate users
- Check location mismatch
- Monitor unusual activity

## Tech Stack
- Flask
- HTML, CSS, JavaScript
- SQLite

## Future Scope
- Mobile app
- Live APIs
- Advanced AI
## Adversarial Defense & Anti-Spoofing Strategy
To prevent fraud and misuse, the system includes basic protection mechanisms.
- Identity Verification  
  Each user is verified to avoid duplicate accounts.
- Location Validation  
  User location is checked to ensure they are working in the correct area and not using fake GPS.
- Behavior Monitoring  
  The system tracks unusual activity such as frequent claims or unrealistic working patterns.
- Duplicate Claim Prevention  
  Prevents users from claiming multiple times for the same event.
- Anomaly Detection  
  Suspicious patterns (like many claims from the same area) are flagged.
- Risk-Based Control  
  High-risk users may require additional verification before payout.
## Market Crash Handling
The system is designed to handle large-scale disruptions affecting many users:
- Predicts claim surge using AI
- Applies dynamic payout limits
- Prioritizes verified users
- Adjusts future premiums based on risk
This ensures financial stability while still supporting genuine users.
