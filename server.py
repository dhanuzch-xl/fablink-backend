import os
from flask import Flask, send_file, jsonify, request, send_from_directory
from werkzeug.utils import secure_filename
import uuid
from utils.file_operations import allowed_file, convert_step_to_stl, process_step_file, save_uploaded_file, read_step, write_step, write_step_to_stl
from utils.hole_operations import modify_hole_size

app = Flask(__name__, static_folder='static')

# Set secret key for session management
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_default_secret_key')

# Route to serve the index.html file
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

# Route to serve static files (CSS, JS)
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

# Path to the models and output directory
MODEL_DIR = os.path.join(os.getcwd(), 'models')
OUTPUT_DIR = os.path.join(os.getcwd(), 'output')
ALLOWED_EXTENSIONS = {'stl', 'step', 'stp'}

@app.route('/output/<path:filename>')
def serve_output_file(filename):
    return send_from_directory(OUTPUT_DIR, filename)

@app.route('/api/upload_file', methods=['POST'])
def upload_file():
    # Check if the request contains a file
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Check if the file type is allowed
    if file and allowed_file(file.filename):
        # Save the uploaded file using a utility function
        unique_filename, file_path = save_uploaded_file(file, OUTPUT_DIR)

        # If it's a STEP file, process it (convert to STL, extract hole and edge data)
        if unique_filename.endswith(('.step', '.stp')):
            result = process_step_file(file_path, unique_filename, OUTPUT_DIR)
            if result.get('error'):
                return jsonify({'error': result['error']}), 500

            # Return STL URL and extracted hole and edge data
            return jsonify({
                'stlUrl': f"/output/{result['stl_filename']}",
                'holes': result['holes'],
                'edges': result['edges'],
                'params':result['params']
            }), 200

        # If it's an STL file, return the URL without processing
        elif unique_filename.endswith('.stl'):
            return jsonify({'stlUrl': f"/output/{unique_filename}", 'holes': []}), 200

    return jsonify({'error': 'File type not allowed'}), 400

# Route to convert STEP to STL
@app.route('/convert_step_to_stl/<filename>', methods=['GET'])
def convert_to_stl(filename):
    try:
        stl_path = convert_step_to_stl(filename, MODEL_DIR, OUTPUT_DIR)
        return send_file(stl_path, as_attachment=False)
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 404

@app.route('/api/upload_stud', methods=['POST'])
def upload_and_place_stud():
    if 'file' not in request.files:
        app.logger.error("No stud file in request")
        return jsonify({'error': 'No stud file provided'}), 400

    stud_file = request.files['file']
    app.logger.info(f"Received file: {stud_file.filename}")

    if stud_file.filename == '':
        app.logger.error("No file selected")
        return jsonify({'error': 'No selected file'}), 400

    if stud_file and allowed_file(stud_file.filename):
        original_filename = secure_filename(stud_file.filename)
        unique_filename = str(uuid.uuid4()) + "_" + original_filename
        file_path = os.path.join(OUTPUT_DIR, unique_filename)
        stud_file.save(file_path)
        app.logger.info(f"File saved to: {file_path}")

        if unique_filename.lower().endswith(('.step', '.stp')):
            stud_shape = read_step(file_path)
            stud_stl_filename = unique_filename.rsplit('.', 1)[0] + '.stl'
            stud_stl_path = os.path.join(OUTPUT_DIR, stud_stl_filename)

            # Convert STEP to STL
            write_step_to_stl(stud_shape, stud_stl_path)
            app.logger.info(f"Converted to STL: {stud_stl_path}")

            return jsonify({'stlUrl': f'/output/{stud_stl_filename}'}), 200

    app.logger.error("File type not allowed")
    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/api/change_hole_size', methods=['POST'])
def change_hole_size():
    data = request.json
    new_size = data.get('newSize')
    hole_data = data.get('holeData')  # Ensure the hole's position and depth are passed
    step_file_name = data.get('stepFile')  # Ensure the file name is passed

    if new_size is None or hole_data is None or step_file_name is None:
        return jsonify({"error": "New hole size, hole data, or STEP file not provided"}), 400

    # Load the STEP file dynamically based on the provided file name
    step_path = os.path.join(MODEL_DIR, step_file_name)
    if not os.path.exists(step_path):
        return jsonify({"error": f"STEP file {step_file_name} not found"}), 404

    # Read the STEP file
    shape = read_step(step_path)

    # Modify the hole size by applying a boolean cut with a new cylinder
    modified_shape = modify_hole_size(shape, new_size, hole_data)

    # Save the modified STEP file with a new name
    modified_step_path = os.path.join(OUTPUT_DIR, f"{step_file_name.rsplit('.', 1)[0]}_modified.step")
    write_step(modified_shape, modified_step_path)

    # Convert the modified STEP file to an STL
    modified_stl_path = os.path.join(OUTPUT_DIR, f"{step_file_name.rsplit('.', 1)[0]}_modified.stl")
    write_step_to_stl(modified_shape, modified_stl_path)  # Convert to STL

    # Return both the modified STEP and STL file URLs
    return jsonify({
        "message": "Hole size modified",
        "modified_step_file": f"/output/{os.path.basename(modified_step_path)}",
        "modified_stl_file": f"/output/{os.path.basename(modified_stl_path)}"
    }), 200

if __name__ == '__main__':
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    app.run(host="0.0.0.0", port=5000, debug=True)