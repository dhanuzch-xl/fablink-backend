import os
import argparse
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.IFSelect import IFSelect_RetDone, IFSelect_ItemsByEntity
from OCC.Extend.TopologyUtils import TopologyExplorer
import numpy as np
#imports for cad viewer
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Dir
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Display.SimpleGui import init_display
from OCC.Core.AIS import AIS_Shape
from OCC.Core.BRep import BRep_Tool
from OCC.Core.AIS import AIS_Shape
from OCC.Core.TopoDS import TopoDS_Vertex

#custom libraries 
from face_operations import find_faces_with_thickness, get_face_normal
from step_processor import  process_faces_connected_to_base,display_hierarchy
import bend_analysis
from transform_node import align_box_root_to_z_axis #unwrap_cylindrical_face
from unfold_multi import traverse_and_unfold
debug_identified_faces = False



def parse_arguments():
    parser = argparse.ArgumentParser(description='Process a STEP file to find faces with specified thickness.')
    parser.add_argument('step_file', type=str, help='Path to the STEP file')
    parser.add_argument('-t', '--thickness', type=float, default=6, help='Thickness to find (default: 6)')
    return parser.parse_args()


def build_tree(shape,thickness,min_area):
    try:
        # Collect face data in the first pass, including their areas
        all_faces = TopologyExplorer(shape).faces()
        # Find the faces with the specified thickness
        pairs = find_faces_with_thickness(all_faces, thickness,min_area)
        if debug_identified_faces:
            first_elements = [x[0] for x in pairs]
            display, start_display, add_menu, add_function_to_menu = init_display()
            display_cad(display,faces=first_elements,shape=shape)
            start_display()

        #root_face_node,faces = process_parallel_faces_with_hierarchy(pairs)
        faces,root_node = process_faces_connected_to_base(pairs,thickness)
        # Display the hierarchy
        display_hierarchy(root_node)

        return faces, root_node
    except Exception as e:
        print(f"An error occurred during building tree: {str(e)}")
        return None, None

def display_cad(display,faces=None, shape=None, root_node=None):
    """
    Display the CAD shape and node properties (tangent vectors, bend centers, etc.) 
    recursively in the viewer by traversing the node hierarchy.

    Args:
    - shape: The original CAD shape.
    - root_node: The root FaceNode object, which has children to traverse.
    - display: The OCC viewer display object.
    """

    # Define colors for different attributes
    c_vertex_color = Quantity_Color(0.0, 1.0, 0.0, Quantity_TOC_RGB)  # Blue for vertices
    vertex_color = Quantity_Color(0.0, 0.0, 1.0, Quantity_TOC_RGB)  # Blue for vertices
    tangent_vector_color = Quantity_Color(0.0, 1.0, 0.0, Quantity_TOC_RGB)  # Green for tangent vectors
    bend_center_color = Quantity_Color(1.0, 0.0, 0.0, Quantity_TOC_RGB)  # Red for bend center
    text_color = (0, 0, 0)  # Red color for the text message (in RGB format)

    # Scaling factor for tangent vectors
    tangent_vector_scale = 50.0  # Adjust this scale factor for better visibility

    # Offset distance to ensure tangent vectors are above the surface
    offset_distance = 0.0  # Adjust this to lift vectors away from the surface slightly

    # Recursive function to traverse nodes and display properties
    def traverse_and_display(node):
        # Highlight the current face in red (optional)
        ais_face = AIS_Shape(node.face)
        display.Context.Display(ais_face, False)
        display.Context.SetColor(ais_face, Quantity_Color(0.5, 0.5, 0.5, Quantity_TOC_RGB), False)
        display.Context.SetTransparency(ais_face, 0.0, False)

        # # Display vertices as small spheres with blue color
        # for vertex in node.vertices:
        #     point = BRep_Tool.Pnt(vertex)  # Get gp_Pnt from TopoDS_Vertex
        #     sphere = BRepPrimAPI_MakeSphere(point, 0.5).Shape()  # 0.5 is the radius of the sphere
        #     ais_sphere = AIS_Shape(sphere)  # Create an AIS_Shape to handle the shape
        #     display.Context.Display(ais_sphere, False)
        #     display.Context.SetColor(ais_sphere, vertex_color, False)  # Set color to blue
        
        # Display common as small spheres with green color
        common_vertex_pairs = node.vertexDict.get('before_unfld', [])
        if common_vertex_pairs:
            for vertex in common_vertex_pairs:
                # Check if the vertex is a TopoDS_Vertex
                if isinstance(vertex, TopoDS_Vertex):
                    point = BRep_Tool.Pnt(vertex)  # Get gp_Pnt from TopoDS_Vertex
                else:
                    # Assume it's a tuple of coordinates (x, y, z)
                    point = gp_Pnt(vertex[0], vertex[1], vertex[2])  # Create gp_Pnt from coordinates

                # Create a sphere at this point
                sphere = BRepPrimAPI_MakeSphere(point, 0.5).Shape()  # 0.5 is the radius of the sphere
                ais_sphere = AIS_Shape(sphere)  # Create an AIS_Shape to handle the shape
                
                # Display the sphere on the viewer
                display.Context.Display(ais_sphere, False)
                display.Context.SetColor(ais_sphere, c_vertex_color, False)  # Set color
            #diplay centre of common edge
            centroid = node.vertexDict.get('centroid_before_transform', [])

            # Assume the centroid is a tuple of coordinates (x, y, z)
            centroid_point = gp_Pnt(centroid[0], centroid[1], centroid[2])  # Create gp_Pnt from centroid coordinates

            # Create a sphere at the centroid point
            sphere = BRepPrimAPI_MakeSphere(centroid_point, 0.5).Shape()  # 0.5 is the radius of the sphere
            ais_sphere = AIS_Shape(sphere)  # Create an AIS_Shape to handle the shape

            # Display the sphere for the centroid on the viewer
            display.Context.Display(ais_sphere, False)
            display.Context.SetColor(ais_sphere, c_vertex_color, False)  # Set the color to green for centroids

        #Display tangent vectors as arrows with green color
        for tangent_vector in node.tangent_vectors:
            if node.bend_center:
                start_point = gp_Pnt(node.bend_center.X(), node.bend_center.Y(), node.bend_center.Z())  # Assuming node.bend_center is a gp_Pnt

                # Scale the tangent vector for better visibility
                scaled_vector = gp_Vec(tangent_vector.X(), tangent_vector.Y(), tangent_vector.Z()).Scaled(tangent_vector_scale)

                # Offset the start point to lift the vector above the surface
                normal_dir = gp_Dir(scaled_vector)  # Use the direction of the tangent vector
                offset_vec = gp_Vec(normal_dir).Multiplied(offset_distance)
                start_point = start_point.Translated(offset_vec)

                # Calculate the end point by adding the scaled vector
                end_point = start_point.Translated(scaled_vector)

                # Create and display the edge representing the tangent vector
                edge = BRepBuilderAPI_MakeEdge(start_point, end_point).Edge()
                ais_edge = AIS_Shape(edge)  # Create an AIS_Shape for the edge
                display.Context.Display(ais_edge, False)
                display.Context.SetColor(ais_edge, tangent_vector_color, False)  # Set color to green

        # Display bend center as a small sphere with red color
        if node.bend_center:
            bend_center_sphere = BRepPrimAPI_MakeSphere(node.bend_center, 1.0).Shape()  # Bend center as a sphere
            ais_bend_center = AIS_Shape(bend_center_sphere)  # Create an AIS_Shape
            display.Context.Display(ais_bend_center, False)
            display.Context.SetColor(ais_bend_center, bend_center_color, False)  # Set color to red

            # Display bend direction as a text message ('up' or 'down')
            if node.bend_dir:
                center_pt = gp_Pnt(node.bend_center.X(), node.bend_center.Y(), node.bend_center.Z() + 5)  # Offset the text position for visibility
                display.DisplayMessage(center_pt, node.bend_dir, message_color=text_color)  # Display the bend direction text

            if node.bend_angle:
                center_pt = gp_Pnt(node.bend_center.X()+10, node.bend_center.Y()+10, node.bend_center.Z())  # Offset the text position for visibility
                display.DisplayMessage(center_pt, str(node.bend_angle), message_color=text_color)  # Display the bend direction text
        # Traverse all child nodes recursively
        for child in node.children:
            traverse_and_display(child)
    
    # Recursive function to traverse nodes and display properties
    def display_faces(faces):
        # Highlight the current face in red (optional)
        for face in faces:
            ais_face = AIS_Shape(face)
            display.Context.Display(ais_face, False)
            display.Context.SetColor(ais_face, Quantity_Color(1.0, 0.0, 0.0, Quantity_TOC_RGB), False)
            display.Context.SetTransparency(ais_face, 0.0, False) 
    
    # Display the shape
    if shape:
        ais_shape = display.DisplayShape(shape, update=False)
    
    # Start the recursive traversal from the root node
    if root_node:
        traverse_and_display(root_node)
    
    # display faces
    if faces:
        display_faces(faces)

    # Set the view and display the updated scene
    display.View_Iso()
    display.FitAll()
    display.View.Update()
    display.View.Dump('highlighted_surfaces.png')



def process_face_node(node):
    """
    Process a single face node to update all relevant attributes.
    This function safely updates each attribute step by step.
    """
    bend_analysis.analyze_surface_type(node)  # Update surface type (e.g., planar, cylindrical)
    bend_analysis.analyze_edges_and_vertices(node)  # Analyze both edges and vertices
    node.axis = get_face_normal(node.face)
    # If the node represents a cylindrical surface, calculate the bend center
    if node.surface_type == "Cylindrical":
        bend_analysis.calculate_bend_center(node)  # Call to calculate the bend center
        bend_analysis.calculate_bend_direction(node)
        bend_analysis.calculate_tangent_vectors(node)  # Calculate tangent vectors for unfolding    
        bend_analysis.calculate_bend_angle(node)
    # Further updates for axis, bend center, inner radius, etc.
    node.processed = True      # Mark this node as processed


def traverse_and_process_tree(node):
    """
    Recursively traverse the FaceNode tree, processing each node and its children.
    """
    if node is None or node.processed:
        return
    
    # Process current node's attributes
    process_face_node(node)

    # Process all child nodes
    for child in node.children:
        traverse_and_process_tree(child)
        get_common_vertices(node,child)

def get_common_vertices(parent, child, tolerance=1e-6):
    if parent is None or not child.processed:
        return
    vertices1 = [BRep_Tool.Pnt(v) for v in parent.vertices]  # Ensure parent.vertices are valid TopoDS_Vertex
    vertices2 = [BRep_Tool.Pnt(v) for v in child.vertices]

    # Use a set to track unique common vertices
    common_vertices_set = set()

    # Compare vertices from both faces to find common points within tolerance
    for point1 in vertices1:
        for point2 in vertices2:
            if point1.Distance(point2) <= tolerance:
                # Store the coordinates as a tuple (X, Y, Z) in the set
                common_vertices_set.add((point2.X(), point2.Y(), point2.Z()))  # Child's vertex

    # Convert the set back to a list for further use
    common_vertices = list(common_vertices_set)

    # If there are common vertices, store them in the vertexDict
    if common_vertices:
        if 'before_unfld' not in child.vertexDict:
            child.vertexDict['before_unfld'] = []
        if len(common_vertices) == 2:  # Adjusted condition for centroid calculation
            if 'centroid_before_transform' not in child.vertexDict:
                centroid = calculate_midpoint(common_vertices[0], common_vertices[1])
                child.vertexDict["centroid_before_transform"] = centroid
        # Append the new common vertices to the existing ones
        child.vertexDict['before_unfld'].extend(common_vertices)


def calculate_midpoint(vertex1, vertex2):
    return (np.array(vertex1) + np.array(vertex2)) / 2
           
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
if __name__ == "__main__":
    args = parse_arguments()
    step_filename = args.step_file
    thickness = args.thickness
    min_area = 10.0
    cad_view=True
    # Read the STEP file
    print(f"Reading STEP file: {step_filename}")
    shape = read_my_step_file(step_filename)
    
    # build_tree out of shape
    faces, root_node = build_tree(shape,thickness,min_area)

    # transform face
    align_box_root_to_z_axis(root_node)

    #process each face in the tree
    traverse_and_process_tree(root_node)

    #uwrap
    # Example usage
    #traverse_and_unfold(root_node) #from unfold_multy.py
    #unfold_and_transform(root_node)  # from unwrap.py
    #unwrap_cylindrical_face(root_node)  # from transform_node.py

    if cad_view:
        # Initialize the 3D display
        display, start_display, add_menu, add_function_to_menu = init_display()
        display_cad(display,root_node=root_node)
        start_display()