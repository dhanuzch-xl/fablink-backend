import os
from OCC.Extend.DataExchange import write_stl_file, read_step_file_with_names_colors
from utils.find_edges import get_edges, edge_to_dict
from utils.hole_operations import recognize_hole_faces  # Adjusted import

def convert_step_file(file_path, output_dir):
    # Read STEP file with names and colors
    big_shp_dict = read_step_file_with_names_colors(file_path)

    if not big_shp_dict:
        raise ValueError("Failed to read STEP file")

    shape = list(big_shp_dict.keys())[0]

    # Create STL filename and path
    stl_filename = os.path.basename(file_path).rsplit('.', 1)[0] + '.stl'
    stl_path = os.path.join(output_dir, stl_filename)

    # Convert to STL and save
    write_stl_file(shape, stl_path)

    # Extract holes and edges
    holes = recognize_hole_faces(file_path)
    edges = [edge_to_dict(edge) for edge in get_edges(shape)]

    return stl_filename, holes, edges

def convert_step_to_stl(filename, model_dir, output_dir):
    step_path = os.path.join(model_dir, f"{filename}.step")
    stl_path = os.path.join(output_dir, f"{filename}.stl")

    if not os.path.exists(step_path):
        raise FileNotFoundError(f"STEP file {filename}.step not found")

    shape = read_step_file(step_path)
    write_stl_file(shape, stl_path)

    return stl_path
