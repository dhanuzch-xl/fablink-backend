import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.gp import gp_Trsf
from OCC.Core.GProp import GProp_GProps
from OCC.Core.BRepGProp import brepgprop_SurfaceProperties
from OCC.Core.gp import gp_Pnt, gp_Trsf, gp_Vec, gp_Pnt
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform

from OCC.Core.gp import gp_Pnt
from OCC.Core.BRepBuilderAPI import (
    BRepBuilderAPI_MakePolygon,
    BRepBuilderAPI_MakeFace,
    BRepBuilderAPI_MakeWire,
    BRepBuilderAPI_MakeEdge,
    
    
)


from . import bend_analysis
from .transform_node import apply_flatten_transformation

# Function to calculate the transformation matrix from old point P1, target point P2, and normal vector N1
def get_transformation_matrix(P1, P2, N1):
    # Normalize the normal vector N1
    N1 = N1 / np.linalg.norm(N1)
    z_axis = np.array([0, 0, 1])  # Z-axis vector

    # Rotation: Align N1 with the Z-axis using Rodrigues' rotation formula
    if np.allclose(N1, z_axis):
        rotation_matrix = np.eye(4)  # No rotation needed
    else:
        rotation_axis = np.cross(N1, z_axis)
        rotation_axis /= np.linalg.norm(rotation_axis)
        angle = np.arccos(np.dot(N1, z_axis))
        K = np.array([
            [0, -rotation_axis[2], rotation_axis[1]],
            [rotation_axis[2], 0, -rotation_axis[0]],
            [-rotation_axis[1], rotation_axis[0], 0]
        ])
        R = np.eye(3) + np.sin(angle) * K + (1 - np.cos(angle)) * (K @ K)
        rotation_matrix = np.eye(4)
        rotation_matrix[:3, :3] = R

    # Apply rotation to P1
    P1_rotated = apply_transformation(P1, rotation_matrix)[:3]

    # Translation: Move the rotated P1 to P2
    translation_vector = np.array(P2) - P1_rotated
    translation_matrix = np.eye(4)
    translation_matrix[:3, 3] = translation_vector

    # Combine translation and rotation
    combined_matrix = translation_matrix @ rotation_matrix

    return combined_matrix

# Function to apply the transformation matrix to a 3D point
def apply_transformation(point, transformation_matrix):
    point_homogeneous = np.append(point, 1)  # Convert to homogeneous coordinates (x, y, z, 1)
    transformed_point = transformation_matrix @ point_homogeneous
    return transformed_point


def distance_between_points(point1, point2):

    point1 = np.array(point1)
    point2 = np.array(point2)
    return np.linalg.norm(point1 - point2)
# Function to calculate the rotation matrix that aligns two vectors
def calculate_rotation_matrix(v1, v2):
    v1 = v1 / np.linalg.norm(v1)
    v2 = v2 / np.linalg.norm(v2)
    axis = np.cross(v1, v2)
    
    if np.linalg.norm(axis) < 1e-6:
        return np.eye(3)
    
    axis = axis / np.linalg.norm(axis)
    angle = np.arccos(np.dot(v1, v2))
    K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    R = np.eye(3) + np.sin(angle) * K + (1 - np.cos(angle)) * (K @ K)
    
    return R



# Function to transform the attached line after the bend is straightened
def transform_attached_line(bend_end_vertex, new_bend_end_vertex, plate2_COM, parent_direction,flatten = False):
    if flatten:
        child_direction = np.array([plate2_COM[0],plate2_COM[1],0]) - np.array([bend_end_vertex[0],bend_end_vertex[1],0])
    else:
        child_direction = np.array([plate2_COM[0],plate2_COM[1],plate2_COM[2]]) - np.array([bend_end_vertex[0],bend_end_vertex[1],bend_end_vertex[2]])

    if abs(sum(child_direction))>1e-6:
        new_direction = child_direction
    else:
        new_direction = parent_direction

    normalized_new_direction = new_direction/np.linalg.norm(new_direction)
    length_of_attached_line = distance_between_points(plate2_COM,bend_end_vertex)

    # translation_vector = new_bend_end_vertex - bend_end_vertex
    # bend_end_vertex_translated = np.array(bend_end_vertex) + translation_vector
    # Calculate the new plate2_COM position by moving along the normalized new direction
    plate2_COM_rotated = new_bend_end_vertex + normalized_new_direction * length_of_attached_line

    # plate2_COM_translated = np.array(plate2_COM) + translation_vector

    # attached_line_direction = np.array(plate2_COM) - np.array(bend_end_vertex)
    # attached_line_direction = attached_line_direction / np.linalg.norm(attached_line_direction)
    # rotation_matrix = calculate_rotation_matrix(attached_line_direction, new_direction)

    # bend_end_vertex_rotated = rotation_matrix @ (bend_end_vertex_translated - new_bend_end_vertex) + new_bend_end_vertex
    # plate2_COM_rotated = rotation_matrix @ (plate2_COM_translated - new_bend_end_vertex) + new_bend_end_vertex

    return plate2_COM_rotated



def unfold_vertices(plate1_COM, bend_edge, bend_start, bend_end, plate2_COM, bend_radius=2, bend_angle= 1.570796326794896,flatten = False):
    """
    This function combines the logic of straightening the bend and transforming the attached line.
    It handles both bend and planar surfaces based on the surface_type argument.
    """
    # Straighten the bend
    if flatten:
        child_direction = np.array([bend_end[0], bend_end[1], 0]) - np.array([bend_start[0], bend_start[1], 0])
    else:
        child_direction = np.array([bend_end[0], bend_end[1], bend_end[2]]) - np.array([bend_start[0], bend_start[1], bend_start[2]])

    if abs(sum(child_direction)):
        direction_vector = child_direction
    else:
        direction_vector = np.array(bend_start) - np.array(plate1_COM)
    
    direction_vector = direction_vector / np.linalg.norm(direction_vector)
    if flatten:
        bend_length = bend_radius * bend_angle  # Arc length
    else:
        bend_length = distance_between_points(bend_start,bend_end)
    new_bend_end_vertex = np.array(bend_start) + direction_vector * bend_length
    new_bend_end_0 = np.array(bend_edge[0]) +  direction_vector * bend_length
    new_bend_end_1 = np.array(bend_edge[1]) + + direction_vector * bend_length
    new_line_end_vertex = transform_attached_line(bend_end, new_bend_end_vertex, plate2_COM, direction_vector,flatten)
    transformed_plate2_edge = [list(new_bend_end_0),list(new_bend_end_1)]
    return new_bend_end_vertex, new_line_end_vertex,transformed_plate2_edge

def unfold_surfaces(plate1,bend,plate2):
    plate1_COM = plate1.COM
    bend_start_vertex = bend.vertexDict['center_after_transform']
    bend_end_vertex = plate2.vertexDict['center_after_transform']
    bend_angle = bend.bend_angle
    bend_radius = bend.inner_radius
    plate2_COM = plate2.COM  
    bend_axis = bend.axis
    bend_edge = bend.vertexDict['after_unfld']

    new_bend_end_vertex, transformed_plate2_com,transformed_plate2_edge = unfold_vertices(plate1_COM, bend_edge,bend_start_vertex, bend_end_vertex, plate2_COM,bend_radius,bend_angle,flatten=True)
    plate2.vertexDict["center_after_transform"] = new_bend_end_vertex
    plate2.COM = transformed_plate2_com
    translation_vector = transformed_plate2_com - plate2_COM
    apply_flatten_transformation(plate2,translation_vector,transformed_plate2_com,bend_angle,bend_axis)
    plate2.vertexDict['after_unfld'] = transformed_plate2_edge
    bend.flatten_edges = [bend_edge,transformed_plate2_edge]
    
def create_flatten_plate(bend,plate2,bend_radius,bend_angle):

    edge1 = bend.vertexDict['after_unfld']
    edge2 = plate2.vertexDict['after_unfld'] 

    b1 = edge1[0]
    b2 = edge2[0]
    # Calculate the arc length
    arc_length = bend_radius * bend_angle
    # Straightened b2' along the XY plane, using arc length
    direction_b1_b2 = np.array([b2[0] - b1[0], b2[1] - b1[1], 0])  # Flatten to XY plane
    direction_b1_b2_normalized = direction_b1_b2 / np.linalg.norm(direction_b1_b2)
    b2_0 = b1 + direction_b1_b2_normalized * arc_length

    b1 = edge1[1]
    b2 = edge2[1]
    # Calculate the arc length
    arc_length = bend_radius * bend_angle
    # Straightened b2' along the XY plane, using arc length
    direction_b1_b2 = np.array([b2[0] - b1[0], b2[1] - b1[1], 0])  # Flatten to XY plane
    direction_b1_b2_normalized = direction_b1_b2 / np.linalg.norm(direction_b1_b2)
    b2_1 = b1 + direction_b1_b2_normalized * arc_length

    edge2_t = [b2_0,b2_1]
    plate2.vertexDict['after_unfld'] = [b2_0,b2_1]

    p1 = gp_Pnt(edge1[0][0],edge1[0][1],edge1[0][2])
    p2 = gp_Pnt(edge1[1][0],edge1[1][1],edge1[1][2])
    p4 = gp_Pnt(edge2_t[0][0],edge2_t[0][1],edge2_t[0][2])
    p3 = gp_Pnt(edge2_t[1][0],edge2_t[1][1],edge2_t[1][2]) 


    # Calculate the arc length
    arc_length = bend_radius * bend_angle

        # Step 6: Create edges from these points
    edge1 = BRepBuilderAPI_MakeEdge(p1, p2).Edge()
    edge2 = BRepBuilderAPI_MakeEdge(p2, p3).Edge()
    edge3 = BRepBuilderAPI_MakeEdge(p3, p4).Edge()
    edge4 = BRepBuilderAPI_MakeEdge(p4, p1).Edge()

    # Step 7: Create the wire (closed loop of edges) for the planar face
    wire = BRepBuilderAPI_MakeWire(edge1, edge2, edge3, edge4).Wire()

    # Step 8: Create the planar face from the wire
    planar_face = BRepBuilderAPI_MakeFace(wire).Face()

    # Step 9: Replace the cylindrical face with the unwrapped planar face
    bend.face = planar_face
    bend.surface_type = "Flat"  # Mark the node as planar

def traverse_and_unfold(node):
    """
    Recursively traverse the tree to find all Flat -> Cylindrical -> Flat combinations
    and store them in triplet_list.

    Parameters:
    node (FaceNode): The current node in the tree.
    triplet_list (list): The list to store valid Flat -> Cylindrical -> Flat triplets.
    """
    count = 0
    # Check if the current node is a flat surface
    if node.surface_type == 'Flat': 
        # Traverse its children to find a cylindrical surface
        for child1 in node.children:
            if child1.surface_type == 'Cylindrical' and not child1.flatten:
                # Traverse the children of the cylindrical surface to find another flat surface
                for child2 in child1.children:
                    if child2.surface_type == 'Flat' and not child2.flatten:
                        # Check for common shared edges before adding to the triplet list
                        edge1 = bend_analysis.get_common_vertices(node, child1)
                        edge2 = bend_analysis.get_common_vertices(child1, child2)
                        if edge1 and edge2:
                            # Unfold the surfaces based on their parameters and common edges
                            # print('faces are {}, {}, {} with bend angle {}'.format(node.face_id, child1.face_id, child2.face_id, child1.bend_angle))
                            # print(f'and before unfold normals are:\n'
                            #     f'  {node.face_id}: X: {node.axis.X()}, Y: {node.axis.Y()}, Z: {node.axis.Z()}\n'
                            #     f'  {child1.face_id}: X: {child1.axis.X()}, Y: {child1.axis.Y()}, Z: {child1.axis.Z()}\n'
                            #     f'  {child2.face_id}: X: {child2.axis.X()}, Y: {child2.axis.Y()}, Z: {child2.axis.Z()}')     
                            unfold_surfaces(node, child1, child2)

                            # print(f'and after unfold normals are:\n'
                            #     f'  {node.face_id}: X: {node.axis.X()}, Y: {node.axis.Y()}, Z: {node.axis.Z()}\n'
                            #     f'  {child1.face_id}: X: {child1.axis.X()}, Y: {child1.axis.Y()}, Z: {child1.axis.Z()}\n'
                            #     f'  {child2.face_id}: X: {child2.axis.X()}, Y: {child2.axis.Y()}, Z: {child2.axis.Z()}')                           
                            # Mark the cylindrical and second flat node as flattened
                            child1.flatten = True
                            child2.flatten = True
                            count = count+1
                            # if count == 3:
                            #     return
                            # Recursively process child2 after unfolding
                            traverse_and_unfold(child2)  # Process further descendants of child2
                            # Add the triplet (Flat -> Cylindrical -> Flat) to the list
                            #triplet_list.append((node, child1, child2))
                        else:
                            print('No bend found between {}, {}, {}'.format(node.face_id,child1.face_id,child2.face_id))
    # Recursively traverse the children of the current node
    for child in node.children:
        if not child.flatten:
            traverse_and_unfold(child)
