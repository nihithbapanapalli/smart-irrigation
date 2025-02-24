import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

# Step 1: Load the dataset
data = pd.read_csv("Crop_recommendation.csv")

# Step 2: Preprocess the data
# Features (input variables) and target (output variable)
X = data[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
y = data['label']  # This is the target variable (the crop)

# Step 3: Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Step 4: Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Step 5: Initialize and train the Random Forest Classifier
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Step 6: Evaluate the model (optional, can be helpful to check accuracy)
accuracy = rf_model.score(X_test, y_test)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Step 7: Save the trained model and scaler using joblib
joblib.dump(rf_model, 'random_forest_model.pkl')
joblib.dump(scaler, 'scaler.pkl')
print("Model and Scaler have been saved!")  

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the trained model and scaler for Flask API (reuse saved files)
rf_model = joblib.load('random_forest_model.pkl')
scaler = joblib.load('scaler.pkl')

# Define the prediction route (POST method)
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Extract features from the request
        features = [
            data['N'],
            data['P'],
            data['K'],
            data['temperature'],
            data['humidity'],
            data['ph'],
            data['rainfall']
        ]
        
        # Standardize the input features using the saved scaler
        scaled_features = scaler.transform([features])

        # Make a prediction using the trained Random Forest model
        prediction = rf_model.predict(scaled_features)
        
        # Return the prediction as a JSON response
        return jsonify({'predicted_crop': prediction[0]})

    except Exception as e:
        return jsonify({'error': str(e)})

# Run the Flask server
if __name__ == '__main__':
    # Start the server only if running as a standalone script (not importing this file elsewhere)
    app.run(host='0.0.0.0', port=10000, debug=True)
