class PudamiAI:
    def __init__(self):
        # Optimal parameters for crop health
        self.targets = {"moisture": [35, 65], "ph": [6.2, 7.2], "n": [30, 60]}

    def analyze_field(self, data, terrain_risk=True):
        insights = []
        risk_level = "Low"
        
        # Cross-Logic: Moisture + Topography
        if float(data['vol']) > 60 and terrain_risk:
            insights.append("HIGH RISK: Possible waterlogging detected in field depressions.")
            risk_level = "High"

        # Nutrient & pH Logic
        if float(data['ph']) < self.targets['ph'][0]:
            insights.append("ADVICE: Soil is too acidic. Nutrient uptake may be limited.")
            risk_level = "Medium" if risk_level != "High" else "High"

        if float(data['n']) < self.targets['n'][0]:
            insights.append(f"ADVICE: Nitrogen is low ({data['n']}). Apply organic fertilizer.")

        return {
            "insights": insights,
            "risk": risk_level,
            "recommendation": "Rotate to Legumes" if float(data['n']) < 30 else "Continue Wheat"
        }
