from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Crop data dictionary
crop_data = {
    "wheat": {
        "growth_days": 120,
        "water_required_per_acre_liters": 500000,
        "daily_water_consumption_liters": 4167,
        "soil_moisture_percent": 50
    },
    "rice": {
        "growth_days": 150,
        "water_required_per_acre_liters": 1000000,
        "daily_water_consumption_liters": 6667,
        "soil_moisture_percent": 70
    },
    "corn": {
        "growth_days": 110,
        "water_required_per_acre_liters": 600000,
        "daily_water_consumption_liters": 5455,
        "soil_moisture_percent": 60
    },
    "soybean": {
        "growth_days": 100,
        "water_required_per_acre_liters": 450000,
        "daily_water_consumption_liters": 4500,
        "soil_moisture_percent": 55
    },
    "barley": {
        "growth_days": 90,
        "water_required_per_acre_liters": 400000,
        "daily_water_consumption_liters": 4444,
        "soil_moisture_percent": 50
    },
    "oats": {
        "growth_days": 100,
        "water_required_per_acre_liters": 450000,
        "daily_water_consumption_liters": 4500,
        "soil_moisture_percent": 55
    },
    "sorghum": {
        "growth_days": 120,
        "water_required_per_acre_liters": 500000,
        "daily_water_consumption_liters": 4167,
        "soil_moisture_percent": 50
    },
    "millet": {
        "growth_days": 90,
        "water_required_per_acre_liters": 350000,
        "daily_water_consumption_liters": 3889,
        "soil_moisture_percent": 45
    },
    "potato": {
        "growth_days": 90,
        "water_required_per_acre_liters": 600000,
        "daily_water_consumption_liters": 6667,
        "soil_moisture_percent": 65
    },
    "sweet_potato": {
        "growth_days": 120,
        "water_required_per_acre_liters": 550000,
        "daily_water_consumption_liters": 4583,
        "soil_moisture_percent": 60
    },
    "cassava": {
        "growth_days": 300,
        "water_required_per_acre_liters": 800000,
        "daily_water_consumption_liters": 2667,
        "soil_moisture_percent": 55
    },
    "sugarcane": {
        "growth_days": 365,
        "water_required_per_acre_liters": 1500000,
        "daily_water_consumption_liters": 4109,
        "soil_moisture_percent": 70
    },
    "cotton": {
        "growth_days": 180,
        "water_required_per_acre_liters": 700000,
        "daily_water_consumption_liters": 3889,
        "soil_moisture_percent": 60
    },
    "sunflower": {
        "growth_days": 110,
        "water_required_per_acre_liters": 500000,
        "daily_water_consumption_liters": 4545,
        "soil_moisture_percent": 55
    },
    "canola": {
        "growth_days": 100,
        "water_required_per_acre_liters": 450000,
        "daily_water_consumption_liters": 4500,
        "soil_moisture_percent": 50
    },
    "peanut": {
        "growth_days": 120,
        "water_required_per_acre_liters": 500000,
        "daily_water_consumption_liters": 4167,
        "soil_moisture_percent": 55
    },
    "alfalfa": {
        "growth_days": 60,
        "water_required_per_acre_liters": 600000,
        "daily_water_consumption_liters": 10000,
        "soil_moisture_percent": 70
    },
    "clover": {
        "growth_days": 90,
        "water_required_per_acre_liters": 400000,
        "daily_water_consumption_liters": 4444,
        "soil_moisture_percent": 60
    },
    "tomato": {
        "growth_days": 90,
        "water_required_per_acre_liters": 600000,
        "daily_water_consumption_liters": 6667,
        "soil_moisture_percent": 65
    },
    "cucumber": {
        "growth_days": 60,
        "water_required_per_acre_liters": 500000,
        "daily_water_consumption_liters": 8333,
        "soil_moisture_percent": 70
    },
    "pepper": {
        "growth_days": 90,
        "water_required_per_acre_liters": 550000,
        "daily_water_consumption_liters": 6111,
        "soil_moisture_percent": 65
    },
    "onion": {
        "growth_days": 120,
        "water_required_per_acre_liters": 500000,
        "daily_water_consumption_liters": 4167,
        "soil_moisture_percent": 60
    },
    "garlic": {
        "growth_days": 150,
        "water_required_per_acre_liters": 450000,
        "daily_water_consumption_liters": 3000,
        "soil_moisture_percent": 55
    },
    "carrot": {
        "growth_days": 80,
        "water_required_per_acre_liters": 400000,
        "daily_water_consumption_liters": 5000,
        "soil_moisture_percent": 60
    },
    "lettuce": {
        "growth_days": 60,
        "water_required_per_acre_liters": 300000,
        "daily_water_consumption_liters": 5000,
        "soil_moisture_percent": 70
    },
    "cabbage": {
        "growth_days": 90,
        "water_required_per_acre_liters": 500000,
        "daily_water_consumption_liters": 5556,
        "soil_moisture_percent": 65
    },
    "broccoli": {
        "growth_days": 90,
        "water_required_per_acre_liters": 550000,
        "daily_water_consumption_liters": 6111,
        "soil_moisture_percent": 65
    },
    "cauliflower": {
        "growth_days": 90,
        "water_required_per_acre_liters": 550000,
        "daily_water_consumption_liters": 6111,
        "soil_moisture_percent": 65
    },
    "spinach": {
        "growth_days": 40,
        "water_required_per_acre_liters": 300000,
        "daily_water_consumption_liters": 7500,
        "soil_moisture_percent": 70
    },
    "pea": {
        "growth_days": 60,
        "water_required_per_acre_liters": 350000,
        "daily_water_consumption_liters": 5833,
        "soil_moisture_percent": 60
    },
    "bean": {
        "growth_days": 70,
        "water_required_per_acre_liters": 400000,
        "daily_water_consumption_liters": 5714,
        "soil_moisture_percent": 60
    },
    "lentil": {
        "growth_days": 100,
        "water_required_per_acre_liters": 350000,
        "daily_water_consumption_liters": 3500,
        "soil_moisture_percent": 55
    },
    "chickpea": {
        "growth_days": 120,
        "water_required_per_acre_liters": 400000,
        "daily_water_consumption_liters": 3333,
        "soil_moisture_percent": 50
    },
    "mustard": {
        "growth_days": 90,
        "water_required_per_acre_liters": 400000,
        "daily_water_consumption_liters": 4444,
        "soil_moisture_percent": 55
    },
    "sesame": {
        "growth_days": 100,
        "water_required_per_acre_liters": 350000,
        "daily_water_consumption_liters": 3500,
        "soil_moisture_percent": 50
    },
    "flax": {
        "growth_days": 90,
        "water_required_per_acre_liters": 400000,
        "daily_water_consumption_liters": 4444,
        "soil_moisture_percent": 55
    },
    "safflower": {
        "growth_days": 120,
        "water_required_per_acre_liters": 450000,
        "daily_water_consumption_liters": 3750,
        "soil_moisture_percent": 50
    },
    "grape": {
        "growth_days": 180,
        "water_required_per_acre_liters": 800000,
        "daily_water_consumption_liters": 4444,
        "soil_moisture_percent": 60
    },
    "apple": {
        "growth_days": 365,
        "water_required_per_acre_liters": 1000000,
        "daily_water_consumption_liters": 2739,
        "soil_moisture_percent": 65
    },
    "orange": {
        "growth_days": 365,
        "water_required_per_acre_liters": 1200000,
        "daily_water_consumption_liters": 3288,
        "soil_moisture_percent": 70
    },
    "banana": {
        "growth_days": 365,
        "water_required_per_acre_liters": 1500000,
        "daily_water_consumption_liters": 4109,
        "soil_moisture_percent": 75
    },
    "mango": {
        "growth_days": 365,
        "water_required_per_acre_liters": 1300000,
        "daily_water_consumption_liters": 3562,
        "soil_moisture_percent": 70
    },
    "papaya": {
        "growth_days": 365,
        "water_required_per_acre_liters": 1400000,
        "daily_water_consumption_liters": 3836,
        "soil_moisture_percent": 75
    },
    "pineapple": {
        "growth_days": 365,
        "water_required_per_acre_liters": 1000000,
        "daily_water_consumption_liters": 2739,
        "soil_moisture_percent": 60
    },
    "strawberry": {
        "growth_days": 90,
        "water_required_per_acre_liters": 500000,
        "daily_water_consumption_liters": 5556,
        "soil_moisture_percent": 70
    },
    "blueberry": {
        "growth_days": 120,
        "water_required_per_acre_liters": 600000,
        "daily_water_consumption_liters": 5000,
        "soil_moisture_percent": 65
    },
    "raspberry": {
        "growth_days": 120,
        "water_required_per_acre_liters": 550000,
        "daily_water_consumption_liters": 4583,
        "soil_moisture_percent": 65
    },
    "blackberry": {
        "growth_days": 120,
        "water_required_per_acre_liters": 550000,
        "daily_water_consumption_liters": 4583,
        "soil_moisture_percent": 65
    },
    "avocado": {
        "growth_days": 365,
        "water_required_per_acre_liters": 1200000,
        "daily_water_consumption_liters": 3288,
        "soil_moisture_percent": 70
    },
    "olive": {
        "growth_days": 365,
        "water_required_per_acre_liters": 800000,
        "daily_water_consumption_liters": 2192,
        "soil_moisture_percent": 60
    },
    "coconut": {
        "growth_days": 365,
        "water_required_per_acre_liters": 1500000,
        "daily_water_consumption_liters": 4109,
        "soil_moisture_percent": 75
    },
    "coffee": {
        "growth_days": 365,
        "water_required_per_acre_liters": 1000000,
        "daily_water_consumption_liters": 2739,
        "soil_moisture_percent": 70
    },
    "tea": {
        "growth_days": 365,
        "water_required_per_acre_liters": 900000,
        "daily_water_consumption_liters": 2466,
        "soil_moisture_percent": 65
    },
    "cocoa": {
        "growth_days": 365,
        "water_required_per_acre_liters": 1200000,
        "daily_water_consumption_liters": 3288,
        "soil_moisture_percent": 75
    }
}

# Soil type adjustment factors
soil_adjustment_factors = {
    "sandy": 1.2,
    "loamy": 1.0,
    "clay": 0.8
}

# Function to fetch rainfall data from the API
def fetch_rainfall_data():
    api_url = "https://smart-irrigation-1.onrender.com/predict"
    try:
        response = requests.get(api_url)
        
        response.raise_for_status()
        data = response.json()
        return data.get("predicted_rainfall", 0.0)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching rainfall data: {e}")
        return 0.0

@app.route("/calculate", methods=["POST"])
def calculate_crop_details():
    data = request.json
    crop_name = data.get("crop_name", "").lower()
    land_area = data.get("land_area", 0)
    soil_type = data.get("soil_type", "").lower()
    
    if crop_name not in crop_data:
        return jsonify({"error": f"Crop '{crop_name}' not found in the database."}), 400
    
    crop = crop_data[crop_name]
    total_water_required = crop["water_required_per_acre_liters"] * land_area
    daily_water_consumption = crop["daily_water_consumption_liters"] * land_area
    soil_moisture = crop["soil_moisture_percent"]
    
    adjustment_factor = soil_adjustment_factors.get(soil_type, 1.0)
    total_water_required *= adjustment_factor
    daily_water_consumption *= adjustment_factor
    
    predicted_rainfall = fetch_rainfall_data()
    rainfall_liters_per_acre = predicted_rainfall * 4046.86
    
    water_with_rainfall = max(0, daily_water_consumption - rainfall_liters_per_acre)
    total_water_with_rainfall = max(0, total_water_required - (rainfall_liters_per_acre * crop["growth_days"]))
    
    response_data = {
        "crop": crop_name,
        "land_area": land_area,
        "growth_days": crop["growth_days"],
        "required_soil_moisture": soil_moisture,
        "soil_type": soil_type,
        "predicted_rainfall": predicted_rainfall,
        "daily_water_requirements": {
            "without_rainfall": daily_water_consumption,
            "with_rainfall": water_with_rainfall,
            "rainfall_contribution": rainfall_liters_per_acre
        },
        "total_water_requirements": {
            "without_rainfall": total_water_required,
            "with_rainfall": total_water_with_rainfall
        }
    }
    
    return jsonify(response_data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10002, debug=True)
