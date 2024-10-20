import os
import uuid
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCC.Core.gp import gp_Vec, gp_Dir
from werkzeug.utils import secure_filename
from OCC.Extend.DataExchange import read_step_file_with_names_colors, write_stl_file, write_step_file, read_step_file
from utils.hole_operations import recognize_hole_faces, recognize_holes_new
from utils.find_edges import get_edges, edge_to_dict
from utils.sheet_metal_unfolding_project.src.main import build_and_process_tree
#custom libraries 

def read_step(file_path):
    return read_step_file(file_path)

def write_step(shape,output_file_path):
    try:
        # Use OCC to write the shape to an STL file
        write_step_file(shape, output_file_path)
    except Exception as e:
        raise ValueError(f"Failed to write STL file: {e}")

def write_step_to_stl(shape, stl_path):
    try:
        # Use OCC to write the shape to an STL file
        write_stl_file(shape, stl_path)
    except Exception as e:
        raise ValueError(f"Failed to write STL file: {e}")
def save_uploaded_file(file, output_dir):
    # Secure and unique filename
    original_filename = secure_filename(file.filename)
    unique_filename = str(uuid.uuid4()) + "_" + original_filename
    file_path = os.path.join(output_dir, unique_filename)
    file.save(file_path)
    return unique_filename, file_path

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'stl', 'step', 'stp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_step_to_stl(filename, MODEL_DIR, OUTPUT_DIR):
    step_path = os.path.join(MODEL_DIR, f"{filename}.step")
    stl_path = os.path.join(OUTPUT_DIR, f"{filename}.stl")
    
    if not os.path.exists(stl_path):
        shape = read_step_file(step_path)
        write_stl_file(shape, stl_path)  # Convert to STL and save

    return stl_path


def save_tree_to_stl(root_node, unique_filename, output_dir):
    stl_filenames = []
    holes_data = []

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Helper function to save each face node as an STL file
    def save_node_stl(node, unique_filename, output_dir):
        # Create a unique filename based on node's face_id
        stl_filename = f"{unique_filename.rsplit('.', 1)[0]}_{node.face_id}.stl"
        stl_path = os.path.join(output_dir, stl_filename)

        # Assuming `node.face` contains the geometry of the face to be saved
        if node.face is not None:
            if node.surface_type == 'Flat':
                # Extrude the face to create a solid
                thickness = 2.0  # Adjust thickness as needed
                extrusion_vector = gp_Vec(node.axis.XYZ())*thickness  
                prism_maker = BRepPrimAPI_MakePrism(node.face, extrusion_vector)
                solid = prism_maker.Shape()

                # Convert the face geometry to STL format and save it
                write_stl_file(solid, stl_path)
                stl_filenames.append(stl_filename)
                node.face = solid
                # Recognize holes and store hole data
                node.hole_data = recognize_holes_new(node.face)
                if node.hole_data:
                    print('{} holes identified in {}'.format(len(node.hole_data),node.face_id))

                holes_data.append({
                    'face_id': node.face_id,
                    'hole_data': node.hole_data
                })
        else:
            print(f"Node {node.face_id} does not have a valid face geometry to save.")

        # Recursively save the child nodes if any
        for child in node.children:
            save_node_stl(child, unique_filename, output_dir)

    # Start the recursive saving from the root node
    save_node_stl(root_node, unique_filename, output_dir)
    
    return stl_filenames, holes_data

    

def process_step_file(file_path, unique_filename, output_dir):
    try:
        # Build and process the tree
        root_node = build_and_process_tree(file_path, cad_view=False, thickness=2.0, min_area=300.0)

        # Save the tree to STL files and collect holes data
        stl_filenames, holes_data = save_tree_to_stl(root_node, unique_filename, output_dir)

        return {
            'stl_filenames': stl_filenames,  # List of STL filenames
            'holes_data': holes_data         # List of holes data for each face
        }
    except Exception as e:
        return {'error': str(e)}
