from flask import Flask, request, jsonify

app = Flask(__name__)

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

            # Store the latest received data
            latest_data = {
                "temperature": temperature,
                "humidity": humidity,
                "soil_moisture": soil_moisture
            }
            
            # Log sensor data
            print(f"Received Data - Temperature: {temperature}°C, Humidity: {humidity}%, Soil Moisture: {soil_moisture}%")

            return jsonify({"message": "Data received"}), 200
        return jsonify({"error": "Invalid data"}), 400

    elif request.method == 'GET':
        if latest_data:
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

    # GET returns the current thresholds
    return jsonify(thresholds), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
