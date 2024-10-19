import os
import uuid
from werkzeug.utils import secure_filename
from OCC.Extend.DataExchange import read_step_file_with_names_colors, write_stl_file, write_step_file, read_step_file
from utils.hole_operations import recognize_hole_faces
from utils.find_edges import get_edges, edge_to_dict
from OCC.Core.GProp import GProp_GProps
from OCC.Core.BRepGProp import brepgprop_SurfaceProperties, brepgprop_VolumeProperties
from OCC.Core.BRepBndLib import brepbndlib_Add
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.GeomAbs import GeomAbs_Plane
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_FACE


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

def process_step_file(file_path, unique_filename, output_dir):
    try:
        # Read the STEP file to get shape and colors
        big_shp_dict = read_step_file_with_names_colors(file_path)
        if not big_shp_dict:
            return {'error': 'Failed to read STEP file'}

        # Extract the shape from the dictionary (keys are TopoDS_Shape objects)
        shape = list(big_shp_dict.keys())[0]

        # Generate STL filename and path
        stl_filename = unique_filename.rsplit('.', 1)[0] + '.stl'
        stl_path = os.path.join(output_dir, stl_filename)

        # Convert STEP to STL and save
        write_stl_file(shape, stl_path)

        # Extract hole data
        holes = recognize_hole_faces(file_path)

        # Extract edge data
        edges = [edge_to_dict(edge) for edge in get_edges(shape)]

        # Dummy part properties
        part_properties = {
            "flat_area": 1000.0,
            "flat_perimeter": 200.0,
            "flat_bounding_box": "100.00 x 50.00 x 2.00",
            "folded_bounding_box": "80.00 x 40.00 x 30.00",
            "is_part_sheet_metal": True,
            "material_thickness": 2.0,
            "num_bends": 3,
            "num_holes": 5
        }

        # Return data in the required format
        return {
            'id': unique_filename,
            'stl_filename': stl_filename,
            'holes': holes,
            'edges': edges,
            'part_properties': part_properties
        }

    except Exception as e:
        return {'error': str(e)}
