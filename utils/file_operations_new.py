import os
import uuid
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCC.Core.gp import gp_Vec, gp_Dir
from werkzeug.utils import secure_filename
from OCC.Extend.DataExchange import read_step_file_with_names_colors, write_stl_file, write_step_file, read_step_file
from utils.hole_operations import recognize_hole_faces, recognize_holes_new
from utils.find_edges import get_edges, edge_to_dict
from utils.sheet_metal_unfolding_project.src.main import build_and_process_tree, unfold_tree
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

def save_tree_to_stl(root_node, output_dir,unfold):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Helper function to save each face node as an STL file
    def save_node_stl(node, output_dir,unfold):
        # Create a unique filename based on node's face_id
        unique_filename = str(uuid.uuid4())
        stl_filename = f"{unique_filename}_{node.face_id}.stl"
        stl_path = os.path.join(output_dir, stl_filename)
        thickness = 2.0  # Adjust thickness as needed
        if node.face is not None:
            # we dont save cylindrical faces if we flatten the shape
            if not unfold:
                # Extrude the face to create a solid
                extrusion_vector = gp_Vec(0,0,1) * thickness
                prism_maker = BRepPrimAPI_MakePrism(node.face, extrusion_vector)
                solid = prism_maker.Shape()

                # Convert the solid geometry to STL format and save it
                write_stl_file(solid, stl_path)
                # Update node.face to be the STL file path
                node.stlpath = stl_filename
                # Recognize holes and store hole data
                node.hole_data = recognize_holes_new(solid)

            if unfold:
                if node.surface_type =='Flat':
                    # Extrude the face to create a solid
                    extrusion_vector = gp_Vec(0,0,1) * thickness
                    prism_maker = BRepPrimAPI_MakePrism(node.face, extrusion_vector)
                    solid = prism_maker.Shape()

                    # Convert the solid geometry to STL format and save it
                    write_stl_file(solid, stl_path)
                    # Update node.face to be the STL file path
                    node.unfold_stlpath = stl_filename
                    # Recognize holes and store hole data
                    node.unfold_hole_data = recognize_holes_new(solid)
        else:
            print(f"Node {node.face_id} does not have a valid face geometry to save.")

        # Recursively save the child nodes if any
        for child in node.children:
            save_node_stl(child, output_dir,unfold)

    # Start the recursive saving from the root node
    save_node_stl(root_node, output_dir,unfold)



def process_step_file(file_path, output_dir):
    try:
        # Extract edge data
        # edges = [edge_to_dict(edge) for edge in get_edges(shape)]

        # Build and process the tree
        root_node = build_and_process_tree(file_path, cad_view=False, thickness=2.0, min_area=300.0)
        # Save the tree to STL files and update nodes
        save_tree_to_stl(root_node, output_dir,unfold=False)

        unfold_tree(root_node)
        save_tree_to_stl(root_node, output_dir,unfold=True)

        return {
            # 'stl_filename': stl_filename,
            # 'edges': edges,
            'root_node': root_node
        }
    except Exception as e:
        return {'error': str(e)}
