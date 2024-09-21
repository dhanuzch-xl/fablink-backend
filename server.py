from flask import Flask, send_file, jsonify
from flask_cors import CORS  # Import CORS
import os
from OCC.Extend.DataExchange import read_step_file, write_stl_file  # Import read/write functions from pythonocc

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Path to the models and output directory
MODEL_DIR = os.path.join(os.getcwd(), 'models')
OUTPUT_DIR = os.path.join(os.getcwd(), 'output')

# Route to convert STEP to STL
@app.route('/convert_step_to_stl/<filename>', methods=['GET'])
def convert_step_to_stl(filename):
    step_path = os.path.join(MODEL_DIR, f"{filename}.step")
    stl_path = os.path.join(OUTPUT_DIR, f"{filename}.stl")

    if not os.path.exists(step_path):
        return jsonify({"error": f"STEP file {filename}.step not found"}), 404

    if not os.path.exists(stl_path):
        shape = read_step_file(step_path)  # Read the STEP file
        write_stl_file(shape, stl_path)   # Convert to STL and save

    return send_file(stl_path, as_attachment=False)  # Serve the STL file

if __name__ == '__main__':
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    app.run(host="0.0.0.0", port=5000, debug=True)
