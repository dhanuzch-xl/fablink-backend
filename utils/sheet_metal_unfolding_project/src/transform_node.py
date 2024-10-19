from OCC.Core.gp import gp_Trsf, gp_Ax1, gp_Dir
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.gp import gp_Pnt,gp_Pnt2d
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace
import math
from OCC.Core.BRepTools import breptools
from OCC.Core.BRep import BRep_Tool
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Ax1, gp_Ax2, gp_Ax3, gp_Trsf, gp_Dir

from OCC.Core.GeomAbs import GeomAbs_BSplineSurface

def apply_transformation_to_node_and_children(node, transformation):
    """
    Recursively apply the given transformation to the current node's face
    and propagate it to all child nodes.

    Args:
        node (FaceNode): The current face node to transform.
        transformation (gp_Trsf): The transformation to apply (rotation).
    """
    # Apply transformation to the current face
    transformed_face = BRepBuilderAPI_Transform(node.face, transformation, True).Shape()
    node.face = transformed_face  # Update the node's face to the transformed face

    # Recursively apply transformation to all child nodes
    for child in node.children:
        apply_transformation_to_node_and_children(child, transformation)

def rotate_box(root_node, angle_in_radians, axis='Z'):
    """
    Rotate the entire box (represented by the root node) by applying
    a rotation transformation around the specified axis.

    Args:
        root_node (FaceNode): The root node of the face hierarchy.
        angle_in_radians (float): The rotation angle in radians.
        axis (str): The axis to rotate around ('X', 'Y', or 'Z').
    """
    # Define the axis of rotation
    if axis == 'X':
        rotation_axis = gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(1, 0, 0))
    elif axis == 'Y':
        rotation_axis = gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 1, 0))
    else:  # Default to Z-axis rotation
        rotation_axis = gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1))

    # Create the transformation (rotation)
    rotation_transformation = gp_Trsf()
    rotation_transformation.SetRotation(rotation_axis, angle_in_radians)

    # Apply the transformation to the root node and all its children
    apply_transformation_to_node_and_children(root_node, rotation_transformation)

from OCC.Core.gp import gp_Vec, gp_Trsf, gp_Ax1, gp_Dir, gp_Pnt
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from math import acos
from OCC.Core.GeomAbs import GeomAbs_Cylinder, GeomAbs_Plane
from OCC.Core.gp import gp_Vec, gp_Dir
from math import acos
from face_operations import get_face_normal
from OCC.Core.GProp import GProp_GProps
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Trsf, gp_Dir, gp_Ax1, gp_Quaternion
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
import math
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
import bend_analysis

def update_face_params(node):
    bend_analysis.analyze_surface_type(node)  # Update surface type (e.g., planar, cylindrical)
    bend_analysis.analyze_edges_and_vertices(node)  # Analyze both edges and vertices
    node.axis = get_face_normal(node.face)
    bend_analysis.calculate_centre_of_mass(node)
    # If the node represents a cylindrical surface, calculate the bend center
    if node.surface_type == "Cylindrical":
        bend_analysis.calculate_bend_center(node)  # Call to calculate the bend center for now inner radius is also added in it
        bend_analysis.calculate_bend_direction(node)
        bend_analysis.calculate_tangent_vectors(node)  # Calculate tangent vectors for unfolding    
        bend_analysis.calculate_bend_angle(node)
    

def calculate_rotation_to_align_with_z(normal_vector):
    """
    Calculate the rotation axis and angle needed to align the given normal vector to the positive Z-axis.
    """
    z_axis = gp_Vec(0, 0, 1)  # Positive Z-axis

    # Convert normal_vector (gp_Dir) to gp_Vec
    normal_vec = gp_Vec(normal_vector.X(), normal_vector.Y(), normal_vector.Z())

    # Calculate the angle between the normal vector and Z-axis
    angle = acos(normal_vec.Normalized().Dot(z_axis))

    # Calculate the axis of rotation (cross product of normal and Z-axis)
    rotation_axis = normal_vec.Crossed(z_axis)
    print('Angle is {} and rotation axis is X: {}, Y: {}, Z: {}'.format(angle, rotation_axis.X(), rotation_axis.Y(), rotation_axis.Z()))
    return angle, rotation_axis


def apply_transformation_to_node_and_children(node, transformation):
    # Apply transformation to the current face
    transformed_face = BRepBuilderAPI_Transform(node.face, transformation, True).Shape()
    node.face = transformed_face  # Update the node's face to the transformed face
    update_face_params(node)
    # Recursively apply transformation to all child nodes
    for child in node.children:
        apply_transformation_to_node_and_children(child, transformation)

def align_box_root_to_z_axis(root_node):
    """
    Align the normal vector of the face in the root node to the positive Z-axis.
    """
    # Step 1: Get the normal vector of the root node's face
    root_face_normal = get_face_normal(root_node.face)
    # Step 2: Calculate the rotation transformation to align the normal to Z-axis
    angle, rotation_axis = calculate_rotation_to_align_with_z(root_face_normal)

    # Step 3: Convert the rotation axis to a gp_Dir (direction)
    rotation_dir = gp_Dir(rotation_axis.X(), rotation_axis.Y(), rotation_axis.Z())

    # Step 4: Create the transformation
    transformation = gp_Trsf()
    transformation.SetRotation(gp_Ax1(gp_Pnt(0, 0, 0), rotation_dir), angle)

    # Step 5: Apply the transformation to the root node and all child nodes
    apply_transformation_to_node_and_children(root_node, transformation)

# def apply_flatten_transformation(parent_node,translation_vector,pivot_center):

#     # Step 1: Get the normal vector of the root node's face
#     root_face_normal = get_face_normal(parent_node.face)
#     # Step 2: Calculate the rotation transformation to align the normal to Z-axis
#     angle, rotation_axis = calculate_rotation_to_align_with_z(root_face_normal)

#     # Step 3: Convert the rotation axis to a gp_Dir (direction)
#     rotation_dir = gp_Dir(rotation_axis.X(), rotation_axis.Y(), rotation_axis.Z())

#     transformation = gp_Trsf()
#     #Step 6: Set the translation in the gp_Trsf object
#     transformation.SetTranslation(gp_Vec(translation_vector[0], translation_vector[1], translation_vector[2]))
#     # Step 5: Apply the transformation to the root node and all child nodes
#     apply_transformation_to_node_and_children(parent_node, transformation)
#     # Step 4: Create the transformation
#     transformation = gp_Trsf()
#     transformation.SetRotation(gp_Ax1(gp_Pnt(pivot_center[0],pivot_center[1],pivot_center[2]), rotation_dir), angle)
#     # Step 6: Set the translation in the gp_Trsf object
#     #transformation.SetTranslation(gp_Vec(translation_vector[0], translation_vector[1], translation_vector[2]))
#     # Step 5: Apply the transformation to the root node and all child nodes
#     apply_transformation_to_node_and_children(parent_node, transformation)
#     # Step 4: Create the transformation

# Function to compute the angle between two vectors
def angle_between_vectors(v1, v2):
    v1_u = v1 / np.linalg.norm(v1)
    v2_u = v2 / np.linalg.norm(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))



import numpy as np
def apply_flatten_transformation(parent_node,b1,b2,bend_angle,bend_radius,bend_axis):

    # Calculate the arc length
    arc_length = bend_radius * bend_angle

    # Straightened b2' along the XY plane, using arc length
    direction_b1_b2 = np.array([b2[0] - b1[0], b2[1] - b1[1], 0])  # Flatten to XY plane
    direction_b1_b2_normalized = direction_b1_b2 / np.linalg.norm(direction_b1_b2)
    b2_prime = b1 + direction_b1_b2_normalized * arc_length

    # Compute the rotation angle between b1-b2 and b1-b2'
    #rotation_angle = angle_between_vectors(b2 - b1, b2_prime - b1)
    # Compute the rotation axis using the cross product of b1-b2 and b1-b2'
    #rotation_axis = np.cross(b2 - b1, b2_prime - b1)
    #rotation_axis = np.array(b1_b2_edge[1])-np.array(b1_b2_edge[0])
    # Step 3: Convert the rotation axis to a gp_Dir (direction)
    #rotation_dir = gp_Dir(rotation_axis[0],rotation_axis[1],rotation_axis[2])

    translation_vector = b2_prime-b2
    pivot_center = b2
    #rotate
    transformation = gp_Trsf()
    transformation.SetRotation(gp_Ax1(gp_Pnt(pivot_center[0],pivot_center[1],pivot_center[2]), bend_axis), -bend_angle)
    apply_transformation_to_node_and_children(parent_node, transformation)
    #translate
    transformation = gp_Trsf()
    transformation.SetTranslation(gp_Vec(translation_vector[0], translation_vector[1], translation_vector[2]))
    apply_transformation_to_node_and_children(parent_node, transformation)

def unwrap_cylindrical_face(node):
    if node.surface_type == 'Cylindrical':
        common_vertices = node.vertexDict['after_unfld']
        if len(common_vertices) == 2:
            # Use the two common vertices for reference (forming the shared edge)
            child_vertex1 = common_vertices[0]
            child_vertex2 = common_vertices[1]

            common_vertex1 = gp_Pnt(*child_vertex1)
            common_vertex2 = gp_Pnt(*child_vertex2)

            # Step 1: Calculate unwrapped length and height
            surface_adaptor = BRepAdaptor_Surface(node.face)
            cylinder = surface_adaptor.Cylinder()
            radius = cylinder.Radius()
            axis = cylinder.Axis()
            axis_dir = axis.Direction()

            # Step 3: Get the parametric bounds of the cylindrical face
            u_min, u_max, v_min, v_max = breptools.UVBounds(node.face)
            angular_span = u_max - u_min  # Angular extent in radians
            unwrapped_length = angular_span * radius  # Arc length for the unwrapped face

            # Calculate the height along the axis direction
            height = v_max - v_min  # Assuming v corresponds linearly to the height along the axis

            # Step 2: Define the local coordinate system
            origin = common_vertex1

            # The tangent direction at u_min
            tangent_angle = u_min
            # Compute the point on the cylinder at u_min and v_min
            p_on_cylinder = surface_adaptor.Value(u_min, v_min)
            # Compute the derivative (tangent vector) at that point
            du = 1e-6  # A small increment
            p_next = surface_adaptor.Value(u_min + du, v_min)
            tangent_vec = gp_Vec(p_on_cylinder, p_next).Normalized()
            x_dir = gp_Dir(tangent_vec)

            # Ensure x_dir is orthogonal to axis_dir
            x_dir = x_dir.Crossed(axis_dir).Crossed(axis_dir)
            x_dir = gp_Dir(x_dir.XYZ())  # Normalize

            # Compute Y-direction as cross product of Z and X
            y_dir = axis_dir.Crossed(x_dir)
            y_dir = gp_Dir(y_dir.XYZ())  # Normalize

            # Create the local coordinate system (gp_Ax3)
            local_ax3 = gp_Ax3(origin, axis_dir, x_dir)

            # Create the unwrapped face in local coordinates
            p1 = gp_Pnt(0, 0, 0)  # Origin
            p2 = gp_Pnt(unwrapped_length, 0, 0)  # Along X-axis
            p3 = gp_Pnt(unwrapped_length, height, 0)  # Along X and Y
            p4 = gp_Pnt(0, height, 0)  # Along Y-axis

            # Create edges and wire
            edge1 = BRepBuilderAPI_MakeEdge(p1, p2).Edge()
            edge2 = BRepBuilderAPI_MakeEdge(p2, p3).Edge()
            edge3 = BRepBuilderAPI_MakeEdge(p3, p4).Edge()
            edge4 = BRepBuilderAPI_MakeEdge(p4, p1).Edge()

            wire_maker = BRepBuilderAPI_MakeWire()
            wire_maker.Add(edge1)
            wire_maker.Add(edge2)
            wire_maker.Add(edge3)
            wire_maker.Add(edge4)
            wire = wire_maker.Wire()

            # Create the planar face from the wire
            planar_face = BRepBuilderAPI_MakeFace(wire).Face()

            # Create the transformation from local to global coordinate system
            trsf = gp_Trsf()
            trsf.SetTransformation(local_ax3, gp_Ax3())

            # Apply the transformation
            brep_trsf = BRepBuilderAPI_Transform(planar_face, trsf, True)
            transformed_face = brep_trsf.Shape()

            # Replace the cylindrical face with the unwrapped planar face
            node.face = transformed_face
            node.surface_type = "Flat"  # Mark the node as planar

    # Recursively apply the same operation to all child nodes
    for child in node.children:
        unwrap_cylindrical_face(child)


def unwrap_bspline_face(node):
    """
    Unwrap a BSpline face into a flat face, calculate the transformation (translation + rotation) 
    between the centroid of the BSpline face and the unwrapped planar face, and apply that transformation.
    
    Args:
        node (FaceNode): The node containing the BSpline face to unwrap.
    
    Returns:
        None: The function modifies the node's face directly.
    """
    # Step 1: Identify the surface type
    surface_adaptor = BRepAdaptor_Surface(node.face)
    surface_type = surface_adaptor.GetType()

    if surface_type == GeomAbs_BSplineSurface:
        print('Unwrapping BSpline surface...')
        
        # Step 2: Extract the BSpline surface and its properties
        bspline_surface = surface_adaptor.Surface().BSplineSurface()
        u_degree = bspline_surface.UDegree()
        v_degree = bspline_surface.VDegree()
        control_points = bspline_surface.Poles()
        u_knots = bspline_surface.UKnots()
        v_knots = bspline_surface.VKnots()

        # Step 3: Get the parametric bounds of the BSpline surface
        u_min, u_max, v_min, v_max = breptools.UVBounds(node.face)

        # Step 4: Generate unwrapped points in 2D (flatten in parametric space)
        points_2d = []
        for u in u_knots:
            for v in v_knots:
                pnt_3d = bspline_surface.Value(u, v)  # Get 3D point on surface
                points_2d.append(gp_Pnt2d(u, v))  # Flattened in U, V space

        # Step 5: Create edges for the unwrapped BSpline face (you might need to interpolate between points)
        edges = []
        for i in range(len(points_2d) - 1):
            p1 = gp_Pnt(points_2d[i].X(), points_2d[i].Y(), v_min)  # Bottom-left
            p2 = gp_Pnt(points_2d[i + 1].X(), points_2d[i + 1].Y(), v_min)  # Bottom-right
            edge = BRepBuilderAPI_MakeEdge(p1, p2).Edge()
            edges.append(edge)

        # Step 6: Create the wire (closed loop of edges) for the planar face
        wire = BRepBuilderAPI_MakeWire(*edges).Wire()

        # Step 7: Create the planar face from the wire
        planar_face = BRepBuilderAPI_MakeFace(wire).Face()

        # Step 8: Calculate centroid and normal of planar face (similarly to your cylindrical case)
        props = GProp_GProps()
        brepgprop.SurfaceProperties(planar_face, props)
        planar_centroid = props.CentreOfMass()

        # Step 9: Calculate the rotation and translation transformations (if needed)
        # For BSpline surfaces, rotation might not be as straightforward as cylindrical, so you can simplify
        # to a translation only if necessary or apply a more complex surface alignment technique.

        # Step 10: Replace the BSpline face with the transformed planar face
        node.face = planar_face
        node.surface_type = "Planar"  # Mark the node as planar

    # Recursively apply the same operation to all child nodes
    for child in node.children:
        unwrap_bspline_face(child)