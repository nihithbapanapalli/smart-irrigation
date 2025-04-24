from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
CORS(app)

# MongoDB configuration
MONGODB_URI = 'mongodb+srv://Sudharshan:1234567890@cluster0.dnfz0ji.mongodb.net/plant_monitoring?retryWrites=true&w=majority'
DB_NAME = 'plant_monitoring'

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]
collection = db.sensor_data  # Create/use 'sensor_data' collection

# Default thresholds in percentage
thresholds = {"min": 40, "max": 70}

# Variable to store the latest received sensor data
latest_data = None  
@app.route('/data', methods=['POST', 'GET'])
def data():
    global latest_data
    
    if request.method == 'POST':
        data = request.get_json()
        if data:
            temperature = data.get('temperature')
            humidity = data.get('humidity')
            soil_moisture = data.get('soil_moisture')

            latest_data = {
                "temperature": temperature,
                "humidity": humidity,
                "soil_moisture": soil_moisture,
                "timestamp": datetime.utcnow()
            }

            # Save to MongoDB
            collection.insert_one(latest_data)

            print(f"Received Data - Temperature: {temperature}°C, Humidity: {humidity}%, Soil Moisture: {soil_moisture}%")
            return jsonify({"message": "Data received and stored"}), 200
        
        return jsonify({"error": "Invalid data"}), 400

    elif request.method == 'GET':
        if latest_data:
            # Convert ObjectId to string to make it JSON serializable
            latest_data['_id'] = str(latest_data['_id']) if '_id' in latest_data else None
            print(f"Latest Data Retrieved: {latest_data}")
            return jsonify(latest_data), 200
        else:
            return jsonify({"error": "No data available"}), 404

@app.route('/threshold', methods=['GET', 'POST'])
def threshold():
    if request.method == 'POST':
        data = request.get_json()
        if data and 'min' in data and 'max' in data:
            thresholds['min'] = data['min']
            thresholds['max'] = data['max']
            return jsonify({"message": "Thresholds updated"}), 200
        return jsonify({"error": "Invalid data"}), 400

    return jsonify(thresholds), 200
@app.route('/history', methods=['GET'])
def history():
    try:
        # Get all documents from MongoDB, sorted by timestamp (newest first)
        records = list(collection.find().sort("timestamp", -1))
        
        # Convert ObjectId and datetime to string for JSON serialization
        for record in records:
            record['_id'] = str(record['_id'])
            record['timestamp'] = record['timestamp'].strftime('%Y-%m-%d %H:%M:%S')

        return jsonify(records), 200
    except Exception as e:
        print(f"Error retrieving history: {e}")
        return jsonify({"error": "Failed to fetch history"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10003, debug=True)
