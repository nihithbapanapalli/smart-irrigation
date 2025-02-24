import pandas as pd
import numpy as np
import requests
import joblib
from sklearn.ensemble import RandomForestRegressor
from flask import Flask, request, jsonify
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Weather API function to get dynamic weather data
def get_weather_data():
    # Visual Crossing API URL (Replace with your actual API key)
    url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Tamil%20Nadu'
    api_key = 'ZPCQSYFN7F9UF2LAFNFY9WMQM'  # Replace with your actual API key
    params = {
        'unitGroup': 'us',
        'key': api_key,
        'contentType': 'json'
    }
    
    # Fetch data from Visual Crossing API
    response = requests.get(url, params=params)
    data = response.json()
    
    # Check if data is valid
    if "days" in data:
        return data["days"]
    else:
        return []

# Data preprocessing to convert raw weather data into usable DataFrame
def process_weather_data(weather_data):
    processed_data = []
    
    # Extract data for each day
    for day in weather_data:
        date = day.get('datetime')
        tempmax = day.get('tempmax')
        tempmin = day.get('tempmin')
        temp = day.get('temp')
        humidity = day.get('humidity')
        windspeed = day.get('windspeed')
        cloudcover = day.get('cloudcover')
        precip = day.get('precip')
        
        # Store the data in a list of dictionaries
        processed_data.append({
            'datetime': date,
            'tempmax': tempmax,
            'tempmin': tempmin,
            'temp': temp,
            'humidity': humidity,
            'windspeed': windspeed,
            'cloudcover': cloudcover,
            'precip': precip
        })
    
    # Convert the data to a DataFrame
    df = pd.DataFrame(processed_data)
    
    # Convert datetime column to datetime object
    df['datetime'] = pd.to_datetime(df['datetime'])
    
    # Handle missing values (if any) only for numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
    
    # Extract features (you can add more features depending on the dataset)
    df['day_of_year'] = df['datetime'].dt.dayofyear  # Day of year feature
    df['month'] = df['datetime'].dt.month  # Month feature
    
    # Drop 'datetime' as it's no longer needed for training
    df.drop('datetime', axis=1, inplace=True)
    
    return df

# Load the model (from file if it's already trained)
def load_model():
    try:
        model = joblib.load('rainfall_model.pkl')  # Load model from file
    except FileNotFoundError:
        model = None  # If model doesn't exist, return None
    return model

# Save the model to a file after training
def save_model(model):
    joblib.dump(model, 'rainfall_model.pkl')

# Train the model
def train_model(df):
    # Define features (X) and target (y)
    X = df.drop('precip', axis=1)  # Use all columns except 'precip' for features
    y = df['precip']  # Target variable (precipitation)
    
    # Create and train RandomForestRegressor model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # Save the trained model to a file
    save_model(model)
    
    return model

# Flask API Endpoint to make prediction based on dynamic weather data
@app.route('/predict', methods=['GET'])
def predict():
    # Fetch live weather data from Visual Crossing API
    weather_data = get_weather_data()
    
    if not weather_data:
        return jsonify({"error": "Failed to fetch weather data"}), 500
    
    # Process the weather data into a DataFrame
    df = process_weather_data(weather_data)
    
    # Load the model (use a pre-trained model if available)
    model = load_model()
    
    # If model is not trained yet, train it with the new weather data
    if model is None:
        model = train_model(df)  # Train the model with the weather data
    
    # We use the first row of the weather data (latest available data)
    latest_data = df.iloc[0]
    
    # Prepare the features for prediction (exclude target column 'precip')
    features = latest_data.drop('precip').values.reshape(1, -1)
    
    # Make a prediction
    prediction = model.predict(features)[0]
    
    return jsonify({
        "predicted_rainfall": prediction,
        "weather_data": latest_data.to_dict()
    })

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True) 
