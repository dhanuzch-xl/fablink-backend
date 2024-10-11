# src/bend_analysis.py
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface, BRepAdaptor_Curve

from OCC.Core.gp import gp_Vec
from OCC.Core.TopAbs import TopAbs_VERTEX
from OCC.Core.TopAbs import TopAbs_EDGE
from OCC.Core.gp import gp_Trsf, gp_Pnt
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopoDS import topods
import warnings
from OCC.Core.GeomAbs import GeomAbs_Cylinder, GeomAbs_Plane
from OCC.Core.GeomAPI import GeomAPI_ProjectPointOnCurve
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.GProp import GProp_GProps
from OCC.Core.BRepTools import breptools
from OCC.Core.BRep import BRep_Tool




def add_child(node, child_node, bend_angle=None, bend_type=None):
    """
    Adds a child node and stores the bend angle and type.
    """
    node.children.append(child_node)
    child_node.parent = node  # Set the parent of the child node
    child_node.bend_angle = bend_angle  # Set the bend angle for the child node
    child_node.bend_type = bend_type  # Set the bend type (optional)

def analyze_edges_and_vertices(node):
    """
    Analyzes the edges and vertices of the face and stores them in the node.
    """
    # Analyze edges
    exp_edge = TopExp_Explorer(node.face, TopAbs_EDGE)
    while exp_edge.More():
        edge = topods.Edge(exp_edge.Current())
        node.edges.append(edge)
        exp_edge.Next()

    # Analyze vertices
    exp_vertex = TopExp_Explorer(node.face, TopAbs_VERTEX)
    while exp_vertex.More():
        vertex = topods.Vertex(exp_vertex.Current())
        node.vertices.append(vertex)
        exp_vertex.Next()

def analyze_surface_type(node):
    """
    Determines whether the face is planar or cylindrical.
    """
    surf = BRepAdaptor_Surface(node.face)
    surf_type = surf.GetType()

    if surf_type == 0:  # Flat face (plane)
        node.surface_type = "Flat"
    elif surf_type == 1:  # Cylindrical face (typically a bend)
        node.surface_type = "Cylindrical"
    else:
        node.surface_type = "Unknown"

def track_vertices(node, transformation=None):
    """
    Function to track the vertices of the bend node's face.
    Vertices are stored in the vertexDict before and after bending.
    
    Args:
        transformation (gp_Trsf): The transformation (unfolding) to be applied to vertices.
    """
    for vertex in node.vertices:
        original_position = BRep_Tool.Pnt(vertex)  # Original position using BRep_Tool_Pnt
        
        # Apply transformation (e.g., unfolding) if provided
        if transformation:
            unfolded_position = gp_Pnt(original_position.X(), original_position.Y(), original_position.Z())
            unfolded_position.Transform(transformation)  # Apply the transformation
        else:
            unfolded_position = original_position  # No transformation applied yet

        # Store the original and unfolded positions in vertexDict
        node.vertexDict[vertex] = (original_position, unfolded_position)
    

def calculate_tangent_vectors(node):
    """
    Calculate tangent vectors for smooth unfolding at the bend.
    Tangent vectors are based on the cross-product of radial vectors.
    """
    tangent_vectors = []
    # Assuming we have two vertices connected by an edge, calculate tangents
    if len(node.edges) > 0 and len(node.vertices) >= 2:
        for edge in node.edges:
            # Calculate tangent using vertices connected by the edge
            vertex1 = node.vertices[0]
            vertex2 = node.vertices[1]
            tangent = gp_Vec(BRep_Tool.Pnt(vertex1), BRep_Tool.Pnt(vertex2)).Normalized()
            tangent_vectors.append(tangent)

    node.tangent_vectors = tangent_vectors


def calculate_bend_direction(node):
    """
    Determines the bend direction ('up' or 'down') based on the position of the bend's center and edges.
    """
    # Ensure that the face has the necessary attributes
    if node.surface_type == "Cylindrical" and node.bend_center:
        edge_positions = []

        # Calculate the center of mass (or centroid) for each edge
        for edge in node.edges:
            props = GProp_GProps()
            brepgprop.LinearProperties(edge, props)  # Get the properties of the edge
            center_of_mass = props.CentreOfMass()  # Get the center of mass (centroid)
            edge_positions.append(center_of_mass)
            
        # Compute the average position of all edges
        average_position = sum([pos.Z() for pos in edge_positions]) / len(edge_positions)

        # Compare the average position with the bend center's position to determine the bend direction
        if average_position > node.bend_center.Z():
            node.bend_dir = "down"
        else:
            node.bend_dir = "up"

def calculate_bend_center(node):
    """
    Calculate the bend center for a cylindrical face.
    Args:
        bend_face (TopoDS_Face): The face that represents the bend.

    Returns:
        gp_Pnt: The calculated bend center point.
    """
    # Create an adaptor for the surface of the face
    surface_adaptor = BRepAdaptor_Surface(node.face)
    
    # Check if the surface is cylindrical
    if surface_adaptor.GetType() == GeomAbs_Cylinder:
        # Extract the cylinder from the surface
        cylinder = surface_adaptor.Cylinder()
        # Get the center of the cylinder
        node.bend_center = cylinder.Location()
        
    else:
        raise ValueError("The provided face is not cylindrical, cannot calculate bend center.")

def calculate_normal(node):
    """Get the normal vector of the surface at a given point."""
    surf = BRepAdaptor_Surface(node.face)
    if surf.GetType() == GeomAbs_Plane:
        gp_pln = surf.Plane()
        node.axis =  gp_pln.Axis()
    elif surf.GetType() == GeomAbs_Cylinder:
        gp_cyl = surf.Cylinder()
        node.axis =  gp_cyl.Axis()
    else:
        node.axis = None
        
def calculate_bend_angle(node1, node2, thickness):

        # Ensure both bend center and axis are already populated
    if not node2.bend_center or not node2.axis:
        raise ValueError("Bend center or axis is missing")
    P_node = node1  # Assuming node1 is the flat node
    P_edge = P_node.edges[0]  # We need to get the edge from the flat node (assuming first edge for now)
    the_face = node2.face  # Assuming node2 is the cylindrical node

    s_Axis = node2.axis  # Axis of the cylindrical surface
    s_Center = node2.bend_center  # Center of the cylindrical surface

    # Investigate the parametric range of the cylindrical face
    face_adaptor = BRepAdaptor_Surface(the_face)
    if face_adaptor.GetType() == GeomAbs_Cylinder:
        cylinder = face_adaptor.Cylinder()
        radius = cylinder.Radius()

        # Get UV bounds of the face using BRepTools
        u_min, u_max, v_min, v_max = breptools.UVBounds(the_face)

        # Get vertices of the edge
        edge_vertices = get_edge_vertices(P_edge)
        edge_vec = gp_Vec(edge_vertices[0].X(), edge_vertices[0].Y(), edge_vertices[0].Z())  # Convert first vertex to gp_Vec
        # Use BRepAdaptor_Curve to create a curve from the edge and project the edge point onto the curve
        curve_adaptor = BRepAdaptor_Curve(P_edge)
        # edge_projector = GeomAPI_ProjectPointOnCurve(gp_Pnt(edge_vec), curve_adaptor.Curve().Curve())
        edge_projector = GeomAPI_ProjectPointOnCurve(edge_vertices[0], curve_adaptor.Curve().Curve())
        edge_param_u = edge_projector.LowerDistanceParameter()

        # Determine the start and end angles on the surface
        angle_start = u_min if abs(u_min - edge_param_u) < 1e-6 else u_max
        angle_end = u_max if angle_start == u_min else u_min

        # Calculate the bend angle
        bend_angle = abs(angle_end - angle_start)
        node2.bend_angle = bend_angle

        # Calculate tangent vectors for unfolding
        angle_tan = angle_start + bend_angle / 6.0

        # Calculate positions and radial vectors
        tan_pos = face_adaptor.Value(angle_tan, v_min)  # Correct method to retrieve the point
        first_vec = radial_vector(edge_vec, s_Center, s_Axis)
        sec_vec = radial_vector(tan_pos, s_Center, s_Axis)

        # Cross product to determine the direction
        cross_vec = first_vec.Crossed(sec_vec)
        triple_prod = cross_vec.Dot(gp_Vec(s_Axis.Direction()))  # Ensure Dot() is between two vectors
        if triple_prod < 0:
            node2.axis = s_Axis.Reversed()

        # Final tangent vector for transformation
        tan_vec = gp_Vec(s_Axis.Direction()).Crossed(first_vec)  # Ensure Cross() is between two vectors
        node2.tangent_vector = tan_vec

        # Adjust the tangent vector based on the parent face normal and edge
        if P_node.surface_type == "Flat":
            p_vec = gp_Vec(edge_vertices[1].X(), edge_vertices[1].Y(), edge_vertices[1].Z()) - gp_Vec(edge_vertices[0].X(), edge_vertices[0].Y(), edge_vertices[0].Z())
            p_vec.Normalize()
            p_tan_vec = gp_Vec(P_node.axis.Direction()).Crossed(p_vec)  # Ensure Cross() is between vectors
            if (tan_vec - p_tan_vec).Magnitude() > 1.0:
                node2.tangent_vector = p_tan_vec.Reversed()
            else:
                node2.tangent_vector = p_tan_vec

        # Calculate the inner radius based on the bend direction
        if node2.bend_dir == "up":
            inner_radius = radius
        else:
            inner_radius = radius - thickness

        node2.inner_radius = inner_radius

        # Calculate the k-factor and translation length
        k_factor = calculate_k_factor(inner_radius, thickness)
        node2.translation_length = (inner_radius + k_factor * thickness) * bend_angle
        return bend_angle, node2.bend_dir

    else:
        raise ValueError("The provided face is not cylindrical, cannot calculate bend angle.")


def radial_vector(point, center, axis):
    """
    Calculate the radial vector between a point and the bend center.
    """
    vec = gp_Vec(point.XYZ()) - gp_Vec(center.XYZ())  # Convert points to vectors
    vec.Normalize()
    return vec

def calculate_k_factor(inner_radius, thickness):
    """
    Calculate the k-factor based on the inner radius and thickness.
    This is a placeholder for any k-factor calculation logic you have.
    """
    # Placeholder logic for k-factor; adjust this as necessary.
    return 0.5  # Example value

def get_edge_vertices(edge):
    """
    Retrieve the vertices of a given edge.
    
    Args:
        edge (TopoDS_Edge): The edge to extract vertices from.
        
    Returns:
        list: A list of gp_Pnt objects representing the vertices.
    """
    vertices = []
    explorer = TopExp_Explorer(edge, TopAbs_VERTEX)
    while explorer.More():
        vertex = BRep_Tool.Pnt(topods.Vertex(explorer.Current()))
        vertices.append(vertex)
        explorer.Next()
    return vertices

