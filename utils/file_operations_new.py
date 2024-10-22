import os
import uuid
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCC.Core.gp import gp_Vec, gp_Dir
from werkzeug.utils import secure_filename
from OCC.Extend.DataExchange import read_step_file_with_names_colors, write_stl_file, write_step_file, read_step_file
from utils.hole_operations import recognize_hole_faces, recognize_holes_new
from utils.find_edges import get_edges, edge_to_dict
from utils.sheet_metal_unfolding_project.src.main import build_and_process_tree, unfold_tree
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.GProp import GProp_GProps
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.IFSelect import IFSelect_RetDone, IFSelect_ItemsByEntity
#custom libraries 
from .get_specs import *

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
    num_holes = 0
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
# Function to compute the area of a face
def total_face_area(faces):
    """
    Compute and return the area of a given face.
    """
    props = GProp_GProps()
    total_area = 0.0
    for face in faces:
        brepgprop.SurfaceProperties(face, props)
        area = props.Mass()
        total_area += area
    print(f"Total surface area: {total_area} square units")
    return area

def read_my_step_file(filename):
    """read the STEP file and returns a compound"""
    step_reader = STEPControl_Reader()
    status = step_reader.ReadFile(filename)

    if status == IFSelect_RetDone:  # check status
        failsonly = False
        step_reader.PrintCheckLoad(failsonly, IFSelect_ItemsByEntity)
        step_reader.PrintCheckTransfer(failsonly, IFSelect_ItemsByEntity)
        step_reader.TransferRoot(1)
        a_shape = step_reader.Shape(1)
    else:
        print("Error: can't read file.")
        return
    return a_shape

def process_step_file(file_path, output_dir):
    params = list()
    params = {'flat_area':None,'perimeter':None,'num_holes':None,'box_dim':None,'is_sheet':None,'area':None, 'num_bends':None,'thickness':None}

    try:
        # Read the STEP file
        shape = read_my_step_file(file_path)
        # Extract edge data
        # edges = [edge_to_dict(edge) for edge in get_edges(shape)]
        # Build and process the tree
        is_sheet,thickness,faces,root_node = build_and_process_tree(file_path, cad_view=False, thickness=2.0, min_area=300.0)
        if is_sheet:
            # Save the tree to STL files and update nodes
            save_tree_to_stl(root_node, output_dir,unfold=False)

            unfold_tree(root_node)
            save_tree_to_stl(root_node, output_dir,unfold=True)
        params['is_sheet'] = is_sheet
        params['thickness']= round(thickness)
        params['area'] = total_face_area(faces)
        params['perimeter'] = total_laser_length(shape)
        num_bends,num_holes = num_bends_and_holes(root_node)
        params['num_holes'] = num_holes#get_specs.total_holes(root_node)
        params['num_bends'] = num_bends
        print(params)
        return {
            # 'stl_filename': stl_filename,
            # 'edges': edges,
            'root_node': root_node,
            'params':params
        }
    
    except Exception as e:
        return {'error': str(e)}
