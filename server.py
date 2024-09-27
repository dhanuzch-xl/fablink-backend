import os
from flask import Flask, send_file, jsonify, request, send_from_directory
from werkzeug.utils import secure_filename
from OCC.Extend.DataExchange import read_step_file_with_names_colors, write_stl_file, write_step_file, read_step_file
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCylinder
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCC.Extend.TopologyUtils import TopologyExplorer
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.GeomAbs import GeomAbs_Cylinder
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepBndLib import brepbndlib
from OCC.Core.TopoDS import TopoDS_Face
from OCC.Core.gp import gp_Ax2, gp_Dir, gp_Pnt
import uuid
from find_edges import get_edges, edge_to_dict

app = Flask(__name__, static_folder='static')
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

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'step', 'stp', 'stl'}

@app.route('/api/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        # Secure and unique filename
        original_filename = secure_filename(file.filename)
        unique_filename = str(uuid.uuid4()) + "_" + original_filename
        file_path = os.path.join(OUTPUT_DIR, unique_filename)
        file.save(file_path)

        # If it's a STEP file, convert it to STL and extract hole data
        if unique_filename.endswith('.step') or unique_filename.endswith('.stp'):
            # Read STEP file using a function that returns names, colors, and shapes
            big_shp_dict = read_step_file_with_names_colors(file_path)
            
            if not big_shp_dict:
                return jsonify({'error': 'Failed to read STEP file'}), 500

            # Extract the shape from the dictionary (keys in the dictionary are TopoDS_Shape objects)
            shape = list(big_shp_dict.keys())[0]  # Get the first shape (adjust if needed)

            # Generate a unique STL filename
            stl_filename = unique_filename.rsplit('.', 1)[0] + '.stl'
            stl_path = os.path.join(OUTPUT_DIR, stl_filename)

            # Convert STEP to STL and save
            write_stl_file(shape, stl_path)

            # Extract hole data (assuming recognize_hole_faces can handle this)
            holes = recognize_hole_faces(file_path)
            
            # Extract edge data
            edges = [edge_to_dict(edge) for edge in get_edges(shape)]

            # Return both the STL URL and hole data
            return jsonify({'stlUrl': f'/output/{stl_filename}', 'holes': holes, 'edges': edges}), 200
            #return jsonify({'stlUrl': f'/output/{stl_filename}', 'holes': holes}), 200
            # Return both the STL URL, hole data, and edge data

        # If it's already an STL file, just return the STL URL (no hole data)
        elif unique_filename.endswith('.stl'):
            return jsonify({'stlUrl': f'/output/{unique_filename}', 'holes': []}), 200

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
            stud_shape = read_step_file(file_path)
            stud_stl_filename = unique_filename.rsplit('.', 1)[0] + '.stl'
            stud_stl_path = os.path.join(OUTPUT_DIR, stud_stl_filename)

            # Convert STEP to STL
            write_stl_file(stud_shape, stud_stl_path)
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
    shape = read_step_file(step_path)

    # Modify the hole size by applying a boolean cut with a new cylinder
    modified_shape = modify_hole_size(shape, new_size, hole_data)

    # Save the modified STEP file with a new name
    modified_step_path = os.path.join(OUTPUT_DIR, f"{step_file_name.rsplit('.', 1)[0]}_modified.step")
    write_step_file(modified_shape, modified_step_path)

    # Convert the modified STEP file to an STL
    modified_stl_path = os.path.join(OUTPUT_DIR, f"{step_file_name.rsplit('.', 1)[0]}_modified.stl")
    write_stl_file(modified_shape, modified_stl_path)  # Convert to STL

    # Return both the modified STEP and STL file URLs
    return jsonify({
        "message": "Hole size modified",
        "modified_step_file": f"/output/{os.path.basename(modified_step_path)}",
        "modified_stl_file": f"/output/{os.path.basename(modified_stl_path)}"
    }), 200


def modify_hole_size(shape, new_size, hole_data):
    # Use the locked/selected hole data directly from the request
    hole_position = hole_data['position']  # Extract position
    hole_axis = hole_data['axis']  # Extract axis
    hole_depth = hole_data['depth']  # Extract depth

    # Create a new cylinder with the updated size and correct axis
    new_hole_radius = new_size / 2.0
    hole_location = gp_Pnt(hole_position['x'], hole_position['y'], hole_position['z'])  # Use the hole's position
    hole_axis_direction = gp_Dir(hole_axis['x'], hole_axis['y'], hole_axis['z'])  # Use the hole's axis

    # Create a cylindrical axis (gp_Ax2) for the cutting cylinder
    cutting_axis = gp_Ax2(hole_location, hole_axis_direction)

    # Create the cylinder aligned with the hole's axis
    new_hole = BRepPrimAPI_MakeCylinder(cutting_axis, new_hole_radius, hole_depth).Shape()

    # No need for transformation if the cylinder is already aligned
    # Perform a boolean cut to replace the old hole with the new one
    modified_shape = BRepAlgoAPI_Cut(shape, new_hole).Shape()

    return modified_shape



# Function to recognize face geometry and extract hole properties

def recognize_face(a_face):
    if not isinstance(a_face, TopoDS_Face):
        return None

    # Check if the surface is cylindrical
    surf = BRepAdaptor_Surface(a_face, True)
    surf_type = surf.GetType()

    if surf_type != GeomAbs_Cylinder:
        return None

    # Extract cylinder information
    gp_cyl = surf.Cylinder()
    location = gp_cyl.Location()
    axis = gp_cyl.Axis().Direction()
    diameter = gp_cyl.Radius() * 2

    # Calculate the bounding box to get the cylinder's height
    bbox = Bnd_Box()
    brepbndlib.Add(a_face, bbox)
    xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
    height = zmax - zmin

    # Additional check: ensure the height is proportional to the diameter
    if abs(height - diameter) > 0.1 * diameter:  # Adjust tolerance as needed
        return None

    # Return the hole properties if the checks pass
    return {
        "position": {"x": location.X(), "y": location.Y(), "z": location.Z()},
        "diameter": diameter,
        "depth": height,  # Depth is now computed as height
        "axis": {"x": axis.X(), "y": axis.Y(), "z": axis.Z()}
    }

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

if __name__ == '__main__':
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    app.run(host="0.0.0.0", port=5000, debug=True)
