import threading
import subprocess
from flask import Flask, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)



def run_script(script_name):
    """Function to run a script using subprocess"""
    subprocess.Popen(["python3", script_name])

# Start all modules as separate threads
scripts = ["Backend.py", "Rainfall.py", "soil.py", "main.py"]
for script in scripts:
    thread = threading.Thread(target=run_script, args=(script,))
    thread.start()

@app.route("/")
def home():
    return jsonify({"message": "All modules are running on Render"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
