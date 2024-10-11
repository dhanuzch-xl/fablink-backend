from OCC.Core.gp import gp_Trsf, gp_Ax1, gp_Dir
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.gp import gp_Pnt,gp_Pnt2d
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace
import math
from OCC.Core.BRepTools import breptools

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

from OCC.Core.GProp import GProp_GProps
from OCC.Core.BRepGProp import brepgprop_SurfaceProperties
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Trsf, gp_Dir, gp_Ax1, gp_Quaternion
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
import math
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire




def unwrap_cylindrical_face(node):
    """
    Unwrap a cylindrical face into a flat face, calculate the transformation (translation + rotation) 
    between the centroid of the cylindrical face and the unwrapped planar face, and apply that transformation.
    
    Args:
        node (FaceNode): The node containing the cylindrical face to unwrap.
    
    Returns:
        None: The function modifies the node's face directly.
    """
    # Step 1: Identify the surface type
    surface_adaptor = BRepAdaptor_Surface(node.face)
    surface_type = surface_adaptor.GetType()

    if surface_type == GeomAbs_Cylinder:
        print('Unwrapping cylindrical surface...')
        # Step 2: Extract cylindrical parameters (radius, height, etc.)
        cylinder = surface_adaptor.Cylinder()
        radius = cylinder.Radius()
        
        # Step 3: Get the centroid of the cylindrical face
        cylinder_location = cylinder.Position().Location()  # Centroid of the cylindrical face

        # Step 4: Get the parametric bounds of the cylindrical face
        u_min, u_max, v_min, v_max = breptools.UVBounds(node.face)

        # Step 5: Calculate unwrapped length (circumference = 2 * pi * radius)
        # Step 5: Calculate the unwrapped length based on the angular span of the cylindrical face
        angular_span = u_max - u_min  # Angular extent in radians

        # The unwrapped length for the cylindrical face
        length = angular_span * radius  # Arc length for the unwrapped face
        # Step 6: Create the 4 edges (rectangular shape in 3D space)
        p1 = gp_Pnt(0, 0, v_min)  # Bottom-left in global space
        p2 = gp_Pnt(length, 0, v_min)  # Bottom-right in global space
        p3 = gp_Pnt(length, 0, v_max)  # Top-right in global space
        p4 = gp_Pnt(0, 0, v_max)  # Top-left in global space

        # Create edges from these points
        edge1 = BRepBuilderAPI_MakeEdge(p1, p2).Edge()
        edge2 = BRepBuilderAPI_MakeEdge(p2, p3).Edge()
        edge3 = BRepBuilderAPI_MakeEdge(p3, p4).Edge()
        edge4 = BRepBuilderAPI_MakeEdge(p4, p1).Edge()

        # Step 7: Create the wire (closed loop of edges) for the planar face
        wire = BRepBuilderAPI_MakeWire(edge1, edge2, edge3, edge4).Wire()

        # Step 8: Create the planar face from the wire
        planar_face = BRepBuilderAPI_MakeFace(wire).Face()

        # Step 9: Calculate the centroid of the newly unwrapped planar face
        props = GProp_GProps()
        brepgprop_SurfaceProperties(planar_face, props)
        planar_centroid = props.CentreOfMass()

        # Step 10: Calculate the normal vectors of the cylindrical and planar faces
        cylinder_axis = cylinder.Axis().Direction()  # Normal vector of the cylindrical face
        planar_normal = gp_Dir(0, 0, 1)  # Assuming planar face is aligned along Z-axis initially

        # Step 11: Calculate the rotation needed to align the planar face's normal with the cylindrical face's axis
        # Calculate the rotation axis and angle
        rotation_axis = planar_normal.Crossed(cylinder_axis)  # Rotation axis (cross product of normals)
        rotation_angle = planar_normal.AngleWithRef(cylinder_axis, rotation_axis)  # Rotation angle
        
        # Step 12: Construct the rotation transformation
        rotation_trsf = gp_Trsf()
        rotation_trsf.SetRotation(gp_Ax1(planar_centroid, rotation_axis), rotation_angle)  # Rotate around planar centroid
        
        # Apply the rotation to the unwrapped planar face
        rotated_planar_face = BRepBuilderAPI_Transform(planar_face, rotation_trsf, True).Shape()

        # Step 13: Construct the translation transformation
        translation_vec = gp_Vec(planar_centroid, cylinder_location)  # Translate from planar face's centroid to cylinder's centroid
        translation_trsf = gp_Trsf()
        translation_trsf.SetTranslation(translation_vec)

        # Apply the translation to the rotated planar face
        transformed_planar_face = BRepBuilderAPI_Transform(rotated_planar_face, translation_trsf, True).Shape()

        # Step 14: Replace the cylindrical face with the fully transformed planar face
        node.face = transformed_planar_face
        node.surface_type = "Planar"  # Mark the node as planar

    # Recursively apply the same operation to all child nodes
    for child in node.children:
        unwrap_cylindrical_face(child)
