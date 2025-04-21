from flask import Flask, request, jsonify
from datetime import datetime
from collections import deque
from flask_cors import CORS  # Import CORS

app = Flask(_name_)
CORS(app)  # Enable CORS for all routes
app.config['JSON_SORT_KEYS'] = False

# Initialize configuration with default values
def get_default_config():
    return {
        1: {"name": "Tomato", "min_threshold": 30, "max_threshold": 60, "automatic_mode": True, "manual_duration": 0, "relay_status": "OFF"},
        2: {"name": "Lettuce", "min_threshold": 40, "max_threshold": 70, "automatic_mode": True, "manual_duration": 0, "relay_status": "OFF"},
        3: {"name": "Pepper", "min_threshold": 35, "max_threshold": 65, "automatic_mode": True, "manual_duration": 0, "relay_status": "OFF"},
        4: {"name": "Strawberry", "min_threshold": 25, "max_threshold": 55, "automatic_mode": True, "manual_duration": 0, "relay_status": "OFF"}
    }

# Configuration storage
crop_config = get_default_config()

# Data storage (last 10 readings)
sensor_data = deque(maxlen=10)

def update_config_from_sensor_data(sensor_data):
    """Update the configuration based on the latest sensor data"""
    if not sensor_data:
        return
    
    latest_data = sensor_data[-1]['data']
    
    for i in range(1, 5):
        sensor_key = f"sensor{i}"
        if sensor_key in latest_data:
            sensor = latest_data[sensor_key]
            
            # Update crop name if different (case-insensitive)
            if 'crop_name' in sensor and sensor['crop_name'].lower() != crop_config[i]['name'].lower():
                crop_config[i]['name'] = sensor['crop_name']
            
            # Update thresholds if they exist in sensor data
            if 'min_threshold' in sensor:
                crop_config[i]['min_threshold'] = sensor['min_threshold']
            if 'max_threshold' in sensor:
                crop_config[i]['max_threshold'] = sensor['max_threshold']
            
            # Update relay status if it exists in sensor data
            if 'relay_status' in sensor:
                crop_config[i]['relay_status'] = sensor['relay_status']
            
            # Update mode if it exists in sensor data
            if 'mode' in sensor:
                crop_config[i]['automatic_mode'] = (sensor['mode'].upper() == "AUTO")

@app.route('/update_crop', methods=['POST'])
def update_crop():
    data = request.json
    if not data or "crop_number" not in data:
        return jsonify({"status": "error", "message": "Missing crop_number"}), 400

    crop_num = data["crop_number"]
    if crop_num not in crop_config:
        return jsonify({"status": "error", "message": "Invalid crop number"}), 400

    # Update only provided fields
    for field in data:
        if field in crop_config[crop_num] and field != "crop_number":
            crop_config[crop_num][field] = data[field]

    return jsonify({
        "status": "success",
        "message": f"Crop {crop_num} updated",
        "config": crop_config[crop_num]
    })

@app.route('/reset_all', methods=['POST'])
def reset_all():
    global crop_config
    crop_config = get_default_config()
    return jsonify({"status": "success", "message": "All crops reset to defaults"})

@app.route('/get_config', methods=['GET'])
def get_config():
    crop_num = request.args.get('crop', type=int)
    if crop_num and crop_num in crop_config:
        return jsonify(crop_config[crop_num])
    return jsonify({k: v for k, v in crop_config.items()})

@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "No data received"}), 400

    timestamp = datetime.now().isoformat()
    
    # Store the data with current configuration
    entry = {
        "timestamp": timestamp,
        "data": data,
        "config": {k: v for k, v in crop_config.items()}
    }
    sensor_data.append(entry)
    
    # Update configuration based on sensor data
    update_config_from_sensor_data(sensor_data)
    
    return jsonify({"status": "success", "message": "Data stored"})

@app.route('/get_data', methods=['GET'])
def get_data():
    if not sensor_data:
        return jsonify({"status": "error", "message": "No data available"}), 404
    
    # Ensure the latest data reflects current configuration
    latest_data = sensor_data[-1].copy()
    latest_data['config'] = {k: v for k, v in crop_config.items()}
    return jsonify(latest_data)

@app.route('/set_manual', methods=['POST'])
def set_manual():
    data = request.json
    if not data or "crop_number" not in data or "duration" not in data:
        return jsonify({"status": "error", "message": "Missing parameters"}), 400

    crop_num = data["crop_number"]
    if crop_num not in crop_config:
        return jsonify({"status": "error", "message": "Invalid crop number"}), 400

    crop_config[crop_num]["automatic_mode"] = False
    crop_config[crop_num]["manual_duration"] = data["duration"] * 60 * 1000  # Convert minutes to milliseconds
    crop_config[crop_num]["relay_status"] = "ON"  # Relay is turned ON in manual mode

    return jsonify({
        "status": "success",
        "message": f"Crop {crop_num} set to manual for {data['duration']} minutes",
        "config": crop_config[crop_num]
    })

if _name_ == '_main_':
    app.run(host='0.0.0.0',port=10004, debug=True)
