from OCC.Core.gp import gp_Trsf, gp_Ax1, gp_Dir
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.gp import gp_Pnt
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface

def apply_rotation_to_node_and_children(node, transformation):
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
        apply_rotation_to_node_and_children(child, transformation)

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
    apply_rotation_to_node_and_children(root_node, rotation_transformation)

from OCC.Core.gp import gp_Vec, gp_Trsf, gp_Ax1, gp_Dir, gp_Pnt
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from math import acos
from OCC.Core.GeomAbs import GeomAbs_Cylinder, GeomAbs_Plane



from OCC.Core.gp import gp_Vec, gp_Dir
from math import acos

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
    return axis.Direction()  # Returns gp_Dir

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

    return angle, rotation_axis


def apply_rotation_to_node_and_children(node, transformation):
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
        apply_rotation_to_node_and_children(child, transformation)


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
    apply_rotation_to_node_and_children(root_node, transformation)
