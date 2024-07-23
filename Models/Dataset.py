import pandas as pd
import numpy as np

# Define lists of cities, soil types, and crops
cities = ["Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad", "Solapur", "Kolhapur", "Amravati", "Thane", "Jalgaon"]
soil_types = ["Black Soil", "Red Soil", "Laterite Soil", "Alluvial Soil"]
crops = ["Sugarcane", "Cotton", "Soybean", "Wheat", "Rice", "Maize"]


# Define functions to generate specific ranges for the cultivation cost and outcome
def generate_specific_cultivating_cost():
    return np.random.randint(8000, 12000)


def generate_specific_outcome():
    return np.random.randint(20000, 35000)


# Function to generate income for best crop sometimes greater and sometimes smaller than the outcome
def generate_varied_best_crop_income(outcome):
    if np.random.rand() > 0.5:  # 50% chance
        return outcome + np.random.randint(-5000, 15000)  # Can be greater or smaller
    else:
        return outcome - np.random.randint(-5000, 15000)  # Can be greater or smaller


# Generate dataset
data = []
for _ in range(1000):
    city = np.random.choice(cities)
    soil_type = np.random.choice(soil_types)
    fertilizer_cost = np.random.randint(1000, 5000)
    total_cultivating_cost = generate_specific_cultivating_cost()
    outcome = generate_specific_outcome()
    best_crop = np.random.choice(crops)
    best_crop_income = generate_varied_best_crop_income(outcome)

    data.append([city, soil_type, fertilizer_cost, total_cultivating_cost, outcome, best_crop, best_crop_income])

# Create DataFrame
df = pd.DataFrame(data,
                  columns=["City", "Soil Type", "Fertilizer Cost", "Total Cultivating Cost", "Outcome", "Best Crop",
                           "Income per Acre"])

# Save to CSV
df.to_csv("final_updated_maharashtra_agriculture_data.csv", index=False)
