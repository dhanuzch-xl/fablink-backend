# src/bend_analysis.py
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface, BRepAdaptor_Curve
from OCC.Core.gp import gp_Vec
from OCC.Core.TopAbs import TopAbs_VERTEX
from OCC.Core.TopAbs import TopAbs_EDGE
from OCC.Core.gp import gp_Trsf, gp_Pnt,gp_Quaternion
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopoDS import topods
import warnings
from OCC.Core.GeomAbs import GeomAbs_Cylinder, GeomAbs_Plane
from OCC.Core.GeomAPI import GeomAPI_ProjectPointOnCurve
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.GProp import GProp_GProps
from OCC.Core.BRepTools import breptools
from OCC.Core.BRep import BRep_Tool
import math
from OCC.Extend.TopologyUtils import TopologyExplorer

def analyze_edges_and_vertices(node):
    """
    Analyzes the edges and vertices of the face and stores them in the node using TopologyExplorer.
    """
    # Create a TopologyExplorer instance for the face
    topology = TopologyExplorer(node.face)

    # Analyze edges from the face
    edges = topology.edges_from_face(node.face)  # Pass the face explicitly
    node.edges = list(edges)  # Store edges directly in the node

    # Analyze vertices from each edge
    for edge in node.edges:
        vertices = topology.vertices_from_edge(edge)  # Get vertices for each edge
        node.vertices.extend(vertices)  # Add vertices to the node's vertex list

    # find face_centre
    

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
        node.inner_radius = cylinder.Radius()
        
    else:
        raise ValueError("The provided face is not cylindrical, cannot calculate bend center.")


import math

def calculate_bend_angle(node):
    if node.surface_type == "Cylindrical":
        u_min, u_max, v_min, v_max = breptools.UVBounds(node.face)
        
        # Handle wrapping by checking if u_max < u_min
        if u_max < u_min:
            # Adjust angular span by unwrapping across 0 degrees
            node.bend_angle = (u_max + 360) - u_min
        else:
            node.bend_angle = u_max - u_min


def calculate_centre_of_mass(node):

    # Create a GProp_GProps object to store the properties of the face
    props = GProp_GProps()

    # Compute surface properties (like the centroid)
    brepgprop.SurfaceProperties(node.face, props)

    # Return the centroid of the face
    com = props.CentreOfMass()
    node.COM = [com.X(),com.Y(),com.Z()]



# def radial_vector(point, center, axis):
#     """
#     Calculate the radial vector between a point and the bend center.
#     """
#     vec = gp_Vec(point.XYZ()) - gp_Vec(center.XYZ())  # Convert points to vectors
#     vec.Normalize()
#     return vec

# def calculate_k_factor(inner_radius, thickness):
#     """
#     Calculate the k-factor based on the inner radius and thickness.
#     This is a placeholder for any k-factor calculation logic you have.
#     """
#     # Placeholder logic for k-factor; adjust this as necessary.
#     return 0.5  # Example value

# def get_edge_vertices(edge):
#     """
#     Retrieve the vertices of a given edge.
    
#     Args:
#         edge (TopoDS_Edge): The edge to extract vertices from.
        
#     Returns:
#         list: A list of gp_Pnt objects representing the vertices.
#     """
#     vertices = []
#     explorer = TopExp_Explorer(edge, TopAbs_VERTEX)
#     while explorer.More():
#         vertex = BRep_Tool.Pnt(topods.Vertex(explorer.Current()))
#         vertices.append(vertex)
#         explorer.Next()
#     return vertices


# import math
# from OCC.Core.gp import gp_Pnt, gp_Vec

# def parametric_cylinder_point(u, v, cylinder):
#     """
#     Computes the 3D coordinates of a point on a cylinder given its UV parameters,
#     taking into account the direction of the axis and any potential quadrant-related issues.
    
#     Args:
#         u (float): The U parameter (angular component in radians).
#         v (float): The V parameter (height along the cylinder axis).
#         cylinder (gp_Cylinder): The cylindrical surface.
    
#     Returns:
#         gp_Pnt: The 3D point on the cylindrical surface.
#     """
#     # Get the axis and origin of the cylinder
#     axis = cylinder.Axis()
#     axis_origin = axis.Location()
#     axis_dir = gp_Vec(axis.Direction())

#     # Create a local (x, y) point on the cylindrical surface using cos(u) and sin(u)
#     x_local = math.cos(u) * cylinder.Radius()
#     y_local = math.sin(u) * cylinder.Radius()

#     # The z_offset is how much we translate along the axis (v parameter in the direction of the axis)
#     z_offset = axis_dir.Multiplied(v)

#     # Create the local point on the cylindrical surface
#     local_point = gp_Pnt(x_local, y_local, 0)

#     # Translate the local point along the axis direction
#     translated_point = local_point.Translated(z_offset)

#     # Finally, translate the point to the cylinder's origin
#     final_point = translated_point.Translated(gp_Vec(axis_origin.XYZ()))

#     return final_point


# def calculate_bend_center(node):
#     """
#     Computes the mid-surface point on a cylindrical or planar face.

#     - For cylindrical surfaces: the midpoint of the UV bounds is mapped to 3D space.
#     - For planar surfaces: the centroid (geometric center) of the face is returned.

#     Args:
#         the_face (TopoDS_Face): The face to compute the midpoint for.

#     Returns:
#         gp_Pnt: The midpoint on the surface in 3D space.
#     """
#     # Adapt the face to extract its surface type and geometry
#     the_face = node.face
#     face_adaptor = BRepAdaptor_Surface(the_face)

#     surface_type = face_adaptor.GetType()

#     if surface_type == GeomAbs_Cylinder:
#         # For cylindrical surfaces
#         node.bend_center =  compute_mid_surface_point_cylinder(the_face)
#     elif surface_type == GeomAbs_Plane:
#         # For planar surfaces, compute the centroid
#         node.bend_center =  compute_mid_surface_point_planar(the_face)
#     else:
#         raise ValueError("Unsupported surface type for this function.")


# def compute_mid_surface_point_cylinder(the_face):
#     """
#     Computes the mid-surface point on a cylindrical surface by taking the midpoint
#     of the UV bounds and mapping it to 3D space using the cylinder's parametric equation.

#     Args:
#         the_face (TopoDS_Face): The cylindrical face.

#     Returns:
#         gp_Pnt: The midpoint on the cylindrical surface in 3D space.
#     """
#     # Adapt the face to extract its surface type and geometry
#     face_adaptor = BRepAdaptor_Surface(the_face)

#     # Ensure the surface is cylindrical
#     if face_adaptor.GetType() != GeomAbs_Cylinder:
#         raise ValueError("The face is not a cylindrical surface.")

#     # Extract the cylinder properties
#     gp_cyl = face_adaptor.Cylinder()
#     cylinder_radius = gp_cyl.Radius()

#     # Get the UV bounds of the face
#     u_min, u_max, v_min, v_max = breptools.UVBounds(the_face)

#     # Compute the midpoint in UV space
#     u_mid = (u_min + u_max) / 2
#     v_mid = (v_min + v_max) / 2

#     # Convert the midpoint UV to a 3D point on the cylindrical surface
#     midpoint_3d = parametric_cylinder_point(u_mid, v_mid, gp_cyl)

#     return midpoint_3d




# def calculate_bend_angle(node1, node2):

#         # Ensure both bend center and axis are already populated
#     if not node2.bend_center or not node2.axis:
#         return
#     P_node = node1  # Assuming node1 is the flat node
#     P_edge = P_node.edges[0]  # We need to get the edge from the flat node (assuming first edge for now)
#     the_face = node2.face  # Assuming node2 is the cylindrical node

#     s_Axis = node2.axis  # Axis of the cylindrical surface
#     s_Center = node2.bend_center  # Center of the cylindrical surface

#     # Investigate the parametric range of the cylindrical face
#     face_adaptor = BRepAdaptor_Surface(the_face)
#     if face_adaptor.GetType() == GeomAbs_Cylinder:
#         cylinder = face_adaptor.Cylinder()
#         radius = cylinder.Radius()

#         # Get UV bounds of the face using BRepTools
#         u_min, u_max, v_min, v_max = breptools.UVBounds(the_face)

#         # Get vertices of the edge
#         edge_vertices = get_edge_vertices(P_edge)
#         edge_vec = gp_Vec(edge_vertices[0].X(), edge_vertices[0].Y(), edge_vertices[0].Z())  # Convert first vertex to gp_Vec
#         # Use BRepAdaptor_Curve to create a curve from the edge and project the edge point onto the curve
#         curve_adaptor = BRepAdaptor_Curve(P_edge)
#         # edge_projector = GeomAPI_ProjectPointOnCurve(gp_Pnt(edge_vec), curve_adaptor.Curve().Curve())
#         edge_projector = GeomAPI_ProjectPointOnCurve(edge_vertices[0], curve_adaptor.Curve().Curve())
#         edge_param_u = edge_projector.LowerDistanceParameter()

#         # Determine the start and end angles on the surface
#         angle_start = u_min if abs(u_min - edge_param_u) < 1e-6 else u_max
#         angle_end = u_max if angle_start == u_min else u_min

#         # Calculate the bend angle
#         bend_angle = abs(angle_end - angle_start)
#         node2.bend_angle = bend_angle

#         # Calculate tangent vectors for unfolding
#         angle_tan = angle_start + bend_angle / 6.0

#         # Calculate positions and radial vectors
#         tan_pos = face_adaptor.Value(angle_tan, v_min)  # Correct method to retrieve the point
#         first_vec = radial_vector(edge_vec, s_Center, s_Axis)
#         sec_vec = radial_vector(tan_pos, s_Center, s_Axis)

#         # Cross product to determine the direction
#         cross_vec = first_vec.Crossed(sec_vec)
#         triple_prod = cross_vec.Dot(gp_Vec(s_Axis.Direction()))  # Ensure Dot() is between two vectors
#         if triple_prod < 0:
#             node2.axis = s_Axis.Reversed()

#         # Final tangent vector for transformation
#         tan_vec = gp_Vec(s_Axis.Direction()).Crossed(first_vec)  # Ensure Cross() is between two vectors
#         node2.tangent_vector = tan_vec

#         # Adjust the tangent vector based on the parent face normal and edge
#         if P_node.surface_type == "Flat":
#             p_vec = gp_Vec(edge_vertices[1].X(), edge_vertices[1].Y(), edge_vertices[1].Z()) - gp_Vec(edge_vertices[0].X(), edge_vertices[0].Y(), edge_vertices[0].Z())
#             p_vec.Normalize()
#             p_tan_vec = gp_Vec(P_node.axis.Direction()).Crossed(p_vec)  # Ensure Cross() is between vectors
#             if (tan_vec - p_tan_vec).Magnitude() > 1.0:
#                 node2.tangent_vector = p_tan_vec.Reversed()
#             else:
#                 node2.tangent_vector = p_tan_vec

#         # Calculate the inner radius based on the bend direction
#         if node2.bend_dir == "up":
#             inner_radius = radius
#         else:
#             inner_radius = radius - node2.thickness

#         node2.inner_radius = inner_radius

#         # Calculate the k-factor and translation length
#         k_factor = calculate_k_factor(inner_radius, node2.thickness)
#         node2.translation_length = (inner_radius + k_factor * node2.thickness) * bend_angle
#         return bend_angle, node2.bend_dir

#     else:
#         raise ValueError("The provided face is not cylindrical, cannot calculate bend angle.")

