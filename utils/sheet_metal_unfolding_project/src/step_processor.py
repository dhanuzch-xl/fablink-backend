import os
import argparse
from OCC.Extend.DataExchange import read_step_file
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_FACE
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.BRepExtrema import BRepExtrema_DistShapeShape
from OCC.Core.GProp import GProp_GProps
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_EDGE, TopAbs_WIRE
from OCC.Core.BRepAdaptor import BRepAdaptor_Curve
from OCC.Core.GeomAbs import GeomAbs_Line
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.BRepGProp import brepgprop
from OCC.Display.SimpleGui import init_display
# from OCC.Core.Quantity import Quantity_NOC_RED
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.AIS import AIS_Shape
# from OCC.Core.Aspect import Aspect_TOM_NONE
from OCC.Core.GeomAbs import GeomAbs_Cylinder, GeomAbs_Plane
from math import isclose
import ezdxf
from OCC.Core.BRepBndLib import brepbndlib
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
import math
from math import degrees
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Ax1, gp_Ax2, gp_Ax3, gp_Trsf, gp_Dir
from OCC.Core.TopoDS import topods
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform



class FaceNode:
    """
    Class to represent a face node in the parent-child hierarchy.
    Each node represents a processed face with a list of its connected (child) faces.
    """
    def __init__(self, face):
        self.face = face
        self.children = []
        self.edges = []  # Edges connected to the face
        self.vertices = []  # Vertices connected to the face
        self.surface_type = None  # Planar, Cylindrical
        self.processed = False  # Whether this face has been processed
        self.parent = None  # Parent node
        self.bend_angle = None  # Angle between this face and its parent (if applicable)
        self.axis = None  # Axis of the bend
        self.bend_center = None  # Center of the bend
        self.inner_radius = None  # Inner radius of the bend
        self.tangent_vectors = []  # Tangent vectors at the bend
        self.vertexDict = {}  # Dictionary to track vertex positions before and after bending
        self.bend_dir = None # Bending direction up or down

    def add_child(self, child_face):
        """Add a child to this face node."""
        child_node = FaceNode(child_face)
        self.children.append(child_node)
        return child_node



def parse_arguments():
    """
    Parses command line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description='Process a STEP file to find faces with specified thickness.')
    parser.add_argument('step_file', type=str, help='Path to the STEP file')
    parser.add_argument('-t', '--thickness', type=float, default=6, help='Thickness to find (default: 6)')
    return parser.parse_args()


def find_faces_with_thickness(shape, thickness, min_area=300, tolerance=1e-6):
    """
    Finds faces in a STEP file with a specified thickness.

    Args:
        step_filename (str): Path to the STEP file.
        thickness (float): Thickness to search for.
        min_area (float): Minimum area of faces to consider.
        tolerance (float): Tolerance for comparing thicknesses.

    Returns:
        list: List of faces with specified thickness.
    """

    # Collect face data in the first pass, including their areas
    faces = []
    exp = TopExp_Explorer(shape, TopAbs_FACE)
    while exp.More():
        face = topods.Face(exp.Current())
        surf = BRepAdaptor_Surface(face)
        normal = get_face_normal(face)
            # Calculate the face area
        props = GProp_GProps()
        brepgprop.SurfaceProperties(face, props)
        area = props.Mass()
        if area >= min_area:
            faces.append({
                "face": face,
                "normal": normal,
                "area": area,
                "processed": False
            })
        exp.Next()

    # Find plates with the specified thickness
    plates = []
    for i, data in enumerate(faces):
        if data["processed"]:
            continue
        for j, other_data in enumerate(faces):
            if i == j or other_data["processed"]:
                continue
            if data["normal"].IsParallel(other_data["normal"], tolerance):
                dist_shape_shape = BRepExtrema_DistShapeShape(data["face"], other_data["face"])
                face_thickness = dist_shape_shape.Value()
                if isclose(face_thickness, thickness, rel_tol=tolerance):
                    #ToDo:find_top_face
                    #bottom_face = find_bottom_plate_transformed(data["face"],other_data["face"])
                    plates.append((data["face"],other_data["face"]))
                    data["processed"] = other_data["processed"] = True
                    print(f"Found face pair with thickness {thickness}: Faces {i+1} and {j+1}, Area: {data['area']}")
                    break

    if not plates:
        print("No plates found with the specified thickness.")
    return plates


def get_face_centroid(face):
    """
    Calculates the centroid of a given face.

    Args:
        face (topods.Face): The face whose centroid is to be calculated.

    Returns:
        gp_Pnt: The centroid of the face.
    """
    props = GProp_GProps()
    brepgprop.SurfaceProperties(face, props)
    return props.CentreOfMass()

def faces_are_equal(face1, face2, thickness, tolerance=1e-6):
    """
    Determines if two faces are equal based on their centroids and a specified thickness.

    Args:
        face1 (topods.Face): The first face to compare.
        face2 (topods.Face): The second face to compare.
        thickness (float): Expected thickness between faces.
        tolerance (float): Tolerance for comparison.

    Returns:
        bool: True if faces are considered equal, False otherwise.
    """
    centroid1 = get_face_centroid(face1)
    centroid2 = get_face_centroid(face2)
    
    distance = centroid1.Distance(centroid2)
    max_distance = 1.01 * thickness # within 1% of thickness
    
    return isclose(distance, thickness, rel_tol=tolerance) and distance <= max_distance

def angle_between_vectors(vec1, vec2):
    """
    Calculates the angle between two vectors.

    Args:
        vec1 (gp_Vec): The first vector.
        vec2 (gp_Vec): The second vector.

    Returns:
        float: Angle in radians between the two vectors.
    """
    dot_product = vec1.Dot(vec2)
    magnitude = vec1.Magnitude() * vec2.Magnitude()
    angle = math.acos(dot_product / magnitude)
    return angle

def export_face_to_dxf(face, output_filename):
    """
    Exports a face to a DXF file.

    Args:
        face (topods.Face): The face to be exported.
        output_filename (str): Path for the output DXF file.
    """
    surf = BRepAdaptor_Surface(face)
    plane = surf.Plane()
    normal = gp_Vec(plane.Axis().Direction())

    z_axis = gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1))
    z_axis_vec = gp_Vec(z_axis.Direction())
    rotation_angle = angle_between_vectors(normal, z_axis_vec)

    if not normal.IsParallel(z_axis_vec, 1e-6):
        rotation_axis = normal.Crossed(z_axis_vec).Normalized()
        rotation_axis_dir = gp_Dir(rotation_axis)

        trsf = gp_Trsf()
        trsf.SetRotation(gp_Ax1(gp_Pnt(0, 0, 0), rotation_axis_dir), rotation_angle)
        face_transform = BRepBuilderAPI_Transform(face, trsf)
        face_transform.Build()
        face_transformed = face_transform.Shape()
    else:
        face_transformed = face

    doc = ezdxf.new()
    msp = doc.modelspace()

    wire_exp = TopExp_Explorer(face_transformed, TopAbs_WIRE)
    while wire_exp.More():
        wire = wire_exp.Current()
        edge_exp = TopExp_Explorer(wire, TopAbs_EDGE)
        while edge_exp.More():
            edge = edge_exp.Current()
            curve = BRepAdaptor_Curve(edge)

            if curve.GetType() == GeomAbs_Line:
                p1 = curve.Value(curve.FirstParameter())
                p2 = curve.Value(curve.LastParameter())
                msp.add_line((p1.X(), p1.Y()), (p2.X(), p2.Y()))
            else:
                prev_point = None
                for i in range(100):
                    u = curve.FirstParameter() + i / 99 * (curve.LastParameter() - curve.FirstParameter())
                    pnt = curve.Value(u)
                    if prev_point is not None:
                        msp.add_line((prev_point.X(), prev_point.Y()), (pnt.X(), pnt.Y()))
                    prev_point = pnt

            edge_exp.Next()
        wire_exp.Next()

    doc.saveas(output_filename)


def export_faces_to_dxf(faces, output_folder, thickness, min_area):
    """
    Exports a list of faces to DXF files.

    Args:
        faces (list of topods.Face): Faces to be exported.
        output_folder (str): Directory to store the DXF files.
        thickness (float): Thickness used to filter faces.
        min_area (float): Minimum area used to filter faces.
    """
    unique_faces = []
    
    for face in faces:
        is_duplicate = False
        for unique_face in unique_faces:
            if faces_are_equal(face, unique_face, thickness):
                is_duplicate = True
                break

        if not is_duplicate:
            unique_faces.append(face)

    for i, face in enumerate(unique_faces):
        props = GProp_GProps()
        brepgprop.SurfaceProperties(face, props)
        area = props.Mass()

        output_filename = os.path.join(output_folder, f"face_{i}.dxf")
        #print(f"Exporting face {i + 1} to DXF file: {output_filename}")
        export_face_to_dxf(face, output_filename)
        # else:
        #     continue
            #print(f"Skipping face {i + 1} due to area below the minimum threshold or because it's a rectangle")
   
def export_image_with_highlighted_faces(shape, faces_to_highlight, output_filename, display, fit_all=True):
    """
    Exports an image with certain faces highlighted.

    Args:
        shape (TopoDS_Shape): The overall shape to display.
        faces_to_highlight (list of topods.Face): Faces to be highlighted.
        output_filename (str): Path for the output image file.
        display (OCC.Display.SimpleGui.Display3d): Display object for rendering.
        fit_all (bool): Whether to fit the view to all objects.
    """
    # Clear the previous display context
    #display.Context.RemoveAll(False)

    # Display the shape
    ais_shape = display.DisplayShape(shape, update=False)

    # Highlight faces if needed
    if faces_to_highlight:
        red_color = Quantity_Color(1.0, 0.0, 0.0, Quantity_TOC_RGB)  # RGB red
        for face in faces_to_highlight:
            ais_face = AIS_Shape(face)
            display.Context.Display(ais_face, False)
            display.Context.SetColor(ais_face, red_color, False)
            display.Context.SetTransparency(ais_face, 0.0, False)

    display.View_Iso()
    if fit_all:
        display.FitAll()
    # Update the view and save the rendering to a file
    display.View.Update()
    display.View.Dump(output_filename)



def get_face_normal(face):
    """Get the normal vector of the surface at a given point."""
    surf = BRepAdaptor_Surface(face)
    if surf.GetType() == GeomAbs_Plane:
        gp_pln = surf.Plane()
        axis =  gp_pln.Axis()
    elif surf.GetType() == GeomAbs_Cylinder:
        gp_cyl = surf.Cylinder()
        axis =  gp_cyl.Axis()
    else:
        axis = None
    return axis.Direction()


def get_face_area(face):
    """
    Calculate the area of a face.

    Args:
        face (topods.Face): The face to calculate the area for.

    Returns:
        float: The area of the face.
    """
    props = GProp_GProps()
    brepgprop.SurfaceProperties(face, props)
    area = props.Mass()
    return area

def find_largest_face(pairs):
    """
    Find the face with the largest area from the pairs of faces.

    Args:
        pairs (list): List of face pairs [(face1, face2), (face3, face4), ...]

    Returns:
        topods.Face: The face with the largest area.
    """
    largest_face = None
    max_area = 0

    for pair in pairs:
        face1, face2 = pair

        # Get the area for both faces
        area1 = get_face_area(face1)
        area2 = get_face_area(face2)

        # Check if face1 is the largest face
        if area1 > max_area:
            largest_face = face1
            max_area = area1

        # Check if face2 is the largest face
        if area2 > max_area:
            largest_face = face2
            max_area = area2

    return largest_face





def process_faces_connected_to_base(pairs):
    """
    Process pairs of parallel faces, highlight only the faces connected directly or indirectly to the base face,
    and build a parent-child hierarchy of the connected faces.

    Args:
        pairs (list): List of face pairs [(face1, face2), (face3, face4), ...]

    Returns:
        tuple: A tuple containing:
            - highlighted_faces (list): List of faces connected to the base face.
            - root_node (FaceNode): The root of the parent-child hierarchy of faces.
    """
    highlighted_faces = []  # List of faces to highlight

    # Select the first face from the first pair as the base face
    base_face = find_largest_face(pairs)
    highlighted_faces.append(base_face)

    # Initialize queues
    queue1 = pairs[:]
    parent_queue = [base_face]

    # Initialize the parent-child tree with the base face
    root_node = FaceNode(base_face)
    face_to_node_map = {base_face: root_node}

    def check_connection(face1, face2):
        """Check if two faces are connected by proximity or shared edge."""
        return check_connection_optimized(face1, face2)

    # Process faces level by level, starting with the base face
    while parent_queue:
        parent_face = parent_queue.pop(0)  # Get the next parent face to process
        parent_node = face_to_node_map[parent_face]  # Get the parent node from the tree
        queue2 = []  # Secondary queue for unprocessed pairs

        while queue1:
            pair = queue1.pop(0)  # Get the next pair to process
            face1, face2 = pair

            if check_connection(parent_face, face1):
                # face1 is connected to parent_face
                highlighted_faces.append(face1)
                parent_queue.append(face1)
                
                # Add face1 as a child of parent_face in the hierarchy
                child_node = parent_node.add_child(face1)
                face_to_node_map[face1] = child_node
            elif check_connection(parent_face, face2):
                # face2 is connected to parent_face
                highlighted_faces.append(face2)
                parent_queue.append(face2)
            
                # Add face2 as a child of parent_face in the hierarchy
                child_node = parent_node.add_child(face2)
                face_to_node_map[face2] = child_node
            else:
                # Neither face is connected to parent_face, move the pair to queue2 for future processing
                queue2.append(pair)

        # Replace queue1 with queue2 for the next iteration
        queue1 = queue2

    return highlighted_faces, root_node


def get_bounding_box(face):
    """
    Get the bounding box of a face.

    Args:
        face (topods.Face): The face to get the bounding box for.

    Returns:
        Bnd_Box: The bounding box of the face.
    """
    bbox = Bnd_Box()
    brepbndlib.Add(face, bbox)
    return bbox

def bounding_boxes_intersect(bbox1, bbox2, tolerance=1e-6):
    """
    Check if two bounding boxes intersect within a given tolerance.

    Args:
        bbox1 (Bnd_Box): First bounding box.
        bbox2 (Bnd_Box): Second bounding box.
        tolerance (float): Tolerance for intersection.

    Returns:
        bool: True if the bounding boxes intersect, False otherwise.
    """
    expanded_bbox1 = Bnd_Box()
    expanded_bbox1.SetGap(tolerance)
    expanded_bbox1.Add(bbox1)

    expanded_bbox2 = Bnd_Box()
    expanded_bbox2.SetGap(tolerance)
    expanded_bbox2.Add(bbox2)

    return expanded_bbox1.IsOut(bbox2) == False

def check_connection_optimized(face1, face2, tolerance=1e-6):
    """
    Optimized check if two faces are connected using bounding box intersection and optional detailed checks.

    Args:
        face1 (topods.Face): The first face.
        face2 (topods.Face): The second face.
        tolerance (float): Tolerance for bounding box and edge comparison.

    Returns:
        bool: True if the faces are connected, False otherwise.
    """
    # Get the bounding boxes of both faces
    bbox1 = get_bounding_box(face1)
    bbox2 = get_bounding_box(face2)

    # Check if the bounding boxes intersect
    if bounding_boxes_intersect(bbox1, bbox2, tolerance):
        # If the bounding boxes intersect, check shared edges or proximity
        return True#check_for_shared_edge(face1, face2) or check_proximity(face1, face2)

    return False

def display_hierarchy(node, level=0):
    """
    Recursively display the hierarchy of faces (parents and children) in the console.

    Args:
        node (FaceNode): The current node to display.
        level (int): The current level of the hierarchy (used for indentation).
    """
    indent = "  " * level
    print(f"{indent}Face: {node.face}")

    # Recursively display children
    for child in node.children:
        display_hierarchy(child, level + 1)

def collect_connected_faces(faces, tolerance=1e-6):
    """
    Collects all faces connected to the first face in the list.

    Args:
        faces (list): List of topods.Face objects.
        tolerance (float): Tolerance for checking connection.

    Returns:
        list: List of connected faces.
    """
    connected_faces = []
    processed_faces = set()  # To track processed faces

    def dfs_collect(face, face_list):
        """
        Depth-first search to collect connected faces.
        """
        if face in processed_faces:
            return
        processed_faces.add(face)
        connected_faces.append(face)
        
        # Check all other faces for connection
        for other_face in face_list:
            if other_face not in processed_faces:
                if check_connection_optimized(face, other_face, tolerance):
                    dfs_collect(other_face, face_list)

    # Start DFS from the first face
    if faces:
        dfs_collect(faces[0], faces)

    return connected_faces

# if __name__ == "__main__":
#     args = parse_arguments()

#     step_filename = args.step_file
#     thickness_to_find = args.thickness
#     # step_filename = "sample1.step"  # Replace with the path to your STEP file
#     # thickness_to_find = 6  # Replace with the thickness you want to find
#     min_area = 300.0
#     output_folder = "output_dxf"

#     # Read the STEP file
#     print(f"Reading STEP file: {step_filename}")
#     shape = read_step_file(step_filename)

#     # Initialize the 3D display
#     display, start_display, add_menu, add_function_to_menu = init_display()

#     # Find the faces with the specified thickness
#     pairs = find_faces_with_thickness(shape, thickness_to_find)

#     #root_face_node,faces = process_parallel_faces_with_hierarchy(pairs)
#     faces,root_node = process_faces_connected_to_base(pairs)

#     # Display the hierarchy
#     display_hierarchy(root_node)
#     # Export image with highlighted faces
#     export_image_with_highlighted_faces(shape, faces, "output_with_highlight.png", display)

#     # Export image without highlighted faces
#     #export_image_with_highlighted_faces(shape, [], "output_without_highlight.png", display)

#     start_display()
#     # Export the faces to DXF files
#     #os.makedirs(output_folder, exist_ok=True)
#     #export_faces_to_dxf(faces, output_folder, thickness_to_find, min_area)
