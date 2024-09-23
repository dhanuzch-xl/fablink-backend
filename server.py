import os
import json
from flask import Flask, send_file, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename
from OCC.Extend.DataExchange import read_step_file_with_names_colors, write_stl_file, write_step_file
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCylinder
from OCC.Core.gp import gp_Pnt
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCC.Core.TopoDS import TopoDS_Face
from OCC.Core.GeomAbs import GeomAbs_Cylinder
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepBndLib import brepbndlib_Add
from OCC.Extend.TopologyUtils import TopologyExplorer
from flask_cors import CORS

app = Flask(__name__, static_folder='output', static_url_path='/output')
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins

# Path to the models and output directory
MODEL_DIR = os.path.join(os.getcwd(), 'models')
OUTPUT_DIR = os.path.join(os.getcwd(), 'output')
ALLOWED_EXTENSIONS = {'stl', 'step', 'stp'}

# Helper function to check file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to recognize face geometry and extract hole properties
def recognize_face(a_face):
    if not isinstance(a_face, TopoDS_Face):
        return None

    surf = BRepAdaptor_Surface(a_face, True)
    surf_type = surf.GetType()

    if surf_type == GeomAbs_Cylinder:
        gp_cyl = surf.Cylinder()
        location = gp_cyl.Location()
        axis = gp_cyl.Axis().Direction()
        diameter = gp_cyl.Radius() * 2

        return {
            "position": {"x": location.X(), "y": location.Y(), "z": location.Z()},
            "diameter": diameter,
            "axis": {"x": axis.X(), "y": axis.Y(), "z": axis.Z()}
        }
    return None

# Function to recognize and extract all hole faces in batch mode
def recognize_hole_faces(step_file):
    big_shp_dict = read_step_file_with_names_colors(step_file)
    shapes = big_shp_dict.keys()

    holes = []
    for shape in shapes:
        for face in TopologyExplorer(shape).faces():
            hole_data = recognize_face(face)
            if hole_data:
                holes.append(hole_data)
    return holes

# Route to upload a file (STEP or STL) and load both STL and holes data
from OCC.Extend.DataExchange import read_step_file_with_names_colors

@app.route('/api/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(MODEL_DIR, filename)
        file.save(file_path)

        # If it's a STEP file, convert it to STL and extract hole data
        if filename.endswith('.step') or filename.endswith('.stp'):
            # Read STEP file using a function that returns names, colors, and shapes
            big_shp_dict = read_step_file_with_names_colors(file_path)
            
            if not big_shp_dict:
                return jsonify({'error': 'Failed to read STEP file'}), 500

            # Extract the shape from the dictionary (keys in the dictionary are TopoDS_Shape objects)
            shape = list(big_shp_dict.keys())[0]  # Get the first shape (adjust if needed)

            stl_filename = filename.rsplit('.', 1)[0] + '.stl'
            stl_path = os.path.join(OUTPUT_DIR, stl_filename)

            # Convert STEP to STL and save
            write_stl_file(shape, stl_path)

            # Extract hole data (assuming recognize_hole_faces can handle this)
            holes = recognize_hole_faces(file_path)

            # Return both the STL URL and hole data
            return jsonify({'stlUrl': f'/output/{stl_filename}', 'holes': holes}), 200

        # If it's already an STL file, just return the STL URL (no hole data)
        elif filename.endswith('.stl'):
            return jsonify({'stlUrl': f'/output/{filename}', 'holes': []}), 200

    return jsonify({'error': 'File type not allowed'}), 400

# Route to convert STEP to STL
@app.route('/convert_step_to_stl/<filename>', methods=['GET'])
def convert_step_to_stl(filename):
    step_path = os.path.join(MODEL_DIR, f"{filename}.step")
    stl_path = os.path.join(OUTPUT_DIR, f"{filename}.stl")

    if not os.path.exists(step_path):
        return jsonify({"error": f"STEP file {filename}.step not found"}), 404

    if not os.path.exists(stl_path):
        shape = read_step_file(step_path)
        write_stl_file(shape, stl_path)  # Convert to STL and save

    return send_file(stl_path, as_attachment=False)  # Serve the STL file

# Route to change hole size
@app.route('/api/change_hole_size', methods=['POST'])
def change_hole_size():
    data = request.json
    new_size = data.get('newSize')

    if new_size is None:
        return jsonify({"error": "New hole size not provided"}), 400

    # Load the STEP file
    step_path = os.path.join(MODEL_DIR, 'WP-2.step')  # Example STEP file name
    if not os.path.exists(step_path):
        return jsonify({"error": "STEP file not found"}), 404

    shape = read_step_file(step_path)

    # Modify the hole size by applying a boolean cut with a new cylinder
    modified_shape = modify_hole_size(shape, new_size)

    # Save the modified STEP file
    modified_step_path = os.path.join(OUTPUT_DIR, 'WP-2_modified.step')
    write_step_file(modified_shape, modified_step_path)

    return jsonify({"message": "Hole size modified", "modified_file": f"/output/WP-2_modified.step"}), 200

def modify_hole_size(shape, new_size):
    # Assuming the holes are cylinders, create a new cylinder with the updated size
    new_hole_radius = new_size / 2.0
    new_hole = BRepPrimAPI_MakeCylinder(new_hole_radius, 10).Shape()  # Modify cylinder dimensions

    # Find the existing holes in the shape and replace them with the new size
    modified_shape = BRepAlgoAPI_Cut(shape, new_hole).Shape()

    return modified_shape

if __name__ == '__main__':
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    app.run(host="0.0.0.0", port=5000, debug=True)
