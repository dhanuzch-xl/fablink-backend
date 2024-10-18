import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from transform_node import apply_transformation_to_node_and_children,apply_flatten_transformation
from OCC.Core.gp import gp_Trsf, gp_Vec, gp_Quaternion, gp_Dir
from unfold import unfold_vertices
from OCC.Core.BRep import BRep_Tool
import bend_analysis
from face_operations import get_face_normal

# Function to calculate the transformation from old point P1, target point P2, and normal vector N1_vec (gp_Dir)
def get_transformation_matrix(P1, P2, N1_vec, target_axis=None):

    # Z-axis in Open CASCADE (gp_Dir for the Z-axis)
    if not target_axis:
        z_axis = gp_Dir(0, 0, 1)
    # else:
    # normalised target axis which is supposed to be normal of the line joining edge points.

    # Create a gp_Trsf object for the transformation
    trsf = gp_Trsf()

    # Rotation: Align N1 with the Z-axis using Rodrigues' rotation formula
    if not N1_vec.IsEqual(z_axis, 1e-6):  # Compare if the vectors are equal within a tolerance
        # Cross product for the rotation axis (using gp_Dir)
        rotation_axis_dir = N1_vec.Crossed(z_axis)  # Cross product returns a gp_Dir

        # Convert rotation_axis_dir to gp_Vec for normalization
        rotation_axis_vec = gp_Vec(rotation_axis_dir.X(), rotation_axis_dir.Y(), rotation_axis_dir.Z())
        rotation_axis_vec.Normalize()  # Normalize the rotation axis

        # Calculate the angle between N1 and the Z-axis
        angle = N1_vec.Angle(z_axis)

        # Create the rotation quaternion
        quat = gp_Quaternion()
        quat.SetVectorAndAngle(rotation_axis_vec, angle)

        # Set the rotation in the transformation
        trsf.SetRotation(quat)

    # Translation: Move the rotated P1 to P2
    translation_vector = gp_Vec(P2[0] - P1[0], P2[1] - P1[1], P2[2] - P1[2])

    # Set the translation in the transformation
    trsf.SetTranslation(translation_vector)

    return trsf



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
import numpy as np


def normalize(vector):
    """Helper function to normalize a vector."""
    return vector / np.linalg.norm(vector)

def calculate_rotation_matrix(v1, v2):
    """Calculate rotation matrix to rotate vector v1 to v2 using Rodrigues' formula."""
    # Normalize the vectors inside the rotation calculation
    v1 = normalize(v1)
    v2 = normalize(v2)

    # Cross product to get the axis of rotation
    axis = np.cross(v1, v2)
    axis_norm = np.linalg.norm(axis)

    if axis_norm == 0:  # If vectors are already aligned, return the identity matrix
        return np.eye(3)

    axis = axis / axis_norm  # Normalize the axis
    angle = np.arccos(np.clip(np.dot(v1, v2), -1.0, 1.0))  # Angle between v1 and v2

    # Rodrigues' rotation formula
    K = np.array([
        [0, -axis[2], axis[1]],
        [axis[2], 0, -axis[0]],
        [-axis[1], axis[0], 0]
    ])
    rotation_matrix = np.eye(3) + np.sin(angle) * K + (1 - np.cos(angle)) * (K @ K)

    return rotation_matrix

def transform_attached_line(bend_end_vertex, new_bend_end_vertex, plate2_COM, parent_direction, flatten=True):
    """
    Transform the attached line after the bend is straightened.
    This moves the plate2 direction to align with new_direction and translates the start to new_bend_end_vertex.
    """
    # Adjust bend direction depending on whether it's flattened (z = 0) or not
    flattened_direction = np.array(new_bend_end_vertex) - np.array(bend_end_vertex)
    if flatten:
        flattened_direction[2] = 0  # Set Z-coordinate to 0 if flattening

    # Use flattened_direction if it's non-zero, otherwise fall back to parent_direction
    new_direction = flattened_direction if np.any(flattened_direction) else parent_direction

    # Compute the plate2 direction (attached line direction) from old bend_end_vertex to plate2_COM
    attached_line_direction = np.array(plate2_COM) - np.array(bend_end_vertex)

    # Compute the rotation matrix to rotate attached_line_direction to new_direction
    rotation_matrix = calculate_rotation_matrix(attached_line_direction, new_direction)

    # Apply the rotation to the original attached_line_direction (no need for normalization)
    transformed_attached_line = rotation_matrix @ attached_line_direction

    # Translate it to start from new_bend_end_vertex
    new_plate2_COM = np.array(new_bend_end_vertex) + transformed_attached_line

    return new_plate2_COM


def calculate_gp_trsf(bend_end_vertex, new_bend_end_vertex, plate2_COM, parent_direction, flatten=True):
    """
    Calculate the gp_Trsf transformation for plate2_COM that includes both rotation and translation.
    """
    # Step 1: Adjust the bend direction depending on whether flatten is True or False
    flattened_direction = np.array(new_bend_end_vertex) - np.array(bend_end_vertex)
    if flatten:
        flattened_direction[2] = 0  # Set Z-coordinate to 0 if flattening

        # Use the flattened direction if non-zero, otherwise use parent_direction
    tolerance = 1e-6
    new_direction = flattened_direction if np.any(np.abs(flattened_direction) > tolerance) else parent_direction

    # Compute the attached line direction from bend_end_vertex to plate2_COM
    attached_line_direction = np.array(plate2_COM) - np.array(bend_end_vertex)

    # Step 2: Normalize the vectors for rotation
    attached_line_direction_normalized = attached_line_direction / np.linalg.norm(attached_line_direction)
    new_direction_normalized = new_direction / np.linalg.norm(new_direction)

    # Step 3: Calculate the rotation quaternion (gp_Quaternion) between attached_line_direction and new_direction
    rotation_axis = np.cross(attached_line_direction_normalized, new_direction_normalized)
    rotation_axis_magnitude = np.linalg.norm(rotation_axis)

    if rotation_axis_magnitude != 0:  # If the vectors are not parallel
        rotation_axis = rotation_axis / rotation_axis_magnitude  # Normalize the rotation axis
        angle = np.arccos(np.clip(np.dot(attached_line_direction_normalized, new_direction_normalized), -1.0, 1.0))  # Angle between vectors

        # Create the quaternion for rotation
        quaternion = gp_Quaternion(gp_Vec(rotation_axis[0], rotation_axis[1], rotation_axis[2]), angle)
    else:
        # No rotation needed
        quaternion = gp_Quaternion()  # Identity quaternion (no rotation)

    # Step 4: Create the gp_Trsf for rotation
    trsf = gp_Trsf()
    trsf.SetRotation(quaternion)
    print(quaternion)
    # Step 5: Calculate the translation vector to move bend_end_vertex to new_bend_end_vertex
    translation_vector = new_bend_end_vertex - bend_end_vertex

    # Step 6: Set the translation in the gp_Trsf object
    trsf.SetTranslation(gp_Vec(translation_vector[0], translation_vector[1], translation_vector[2]))

    return trsf

def print_transformation_variables(plate1_COM, bend_start, bend_end, plate2_COM, bend_radius, bend_angle):
    """
    Print all transformation-related variables for debugging.
    """
    print("Transformation Variables:")
    print(f"plate1_COM: {plate1_COM}")
    print(f"bend_start: {bend_start}")
    print(f"bend_end: {bend_end}")
    print(f"plate2_COM: {plate2_COM}")
    print(f"bend_radius: {bend_radius}")
    print(f"bend_angle (in radians): {bend_angle}")
    print(f"bend_angle (in degrees): {bend_angle * 180 / np.pi}")

def transform_vertices(plate1_COM, bend_start, bend_end, plate2_COM, bend_radius, bend_angle,flatten = True):
    """
    This function combines the logic of straightening the bend and transforming the attached line.
    It handles both bend and planar surfaces based on the surface_type argument.
    """
    # Straighten the bend
    #print_transformation_variables(plate1_COM, bend_start, bend_end, plate2_COM, bend_radius, bend_angle)
    if flatten:
        bend_direction = np.array([bend_end[0], bend_end[1], 0]) - np.array([bend_start[0], bend_start[1], 0])
    else:
        bend_direction = np.array([bend_end[0], bend_end[1], bend_end[2]]) - np.array([bend_start[0], bend_start[1], bend_start[2]])

    if sum(bend_direction):
        direction_vector = bend_direction
    else:
        direction_vector = np.array(bend_start) - np.array(plate1_COM)
    
    direction_vector = direction_vector / np.linalg.norm(direction_vector)
    if flatten:
        bend_length = bend_radius * bend_angle  # Arc length
    else:
        bend_length = distance_between_points(bend_start,bend_end)
    new_bend_end_vertex = np.array(bend_start) + direction_vector * bend_length
    #new_line_end_vertex = transform_attached_line(bend_end, new_bend_end_vertex, plate2_COM, direction_vector,flatten)
    Tfm = calculate_gp_trsf(bend_end, new_bend_end_vertex, plate2_COM, direction_vector,flatten)

    return new_bend_end_vertex, Tfm


def unfold_surfaces(plate1,bend,plate2):
    plate1_COM = plate1.COM
    bend_start_vertex = bend.vertexDict['center_after_transform']
    bend_end_vertex = plate2.vertexDict['center_after_transform']
    bend_angle = bend.bend_angle
    bend_radius = bend.inner_radius
    plate2_COM = plate2.COM  
    new_bend_end_vertex, transformed_plate2_com = unfold_vertices(plate1_COM, bend_start_vertex, bend_end_vertex, plate2_COM,bend_radius,bend_angle,flatten=True)
    plate2.vertexDict["center_after_transform"] = new_bend_end_vertex
    plate2.COM = transformed_plate2_com
    # Step 5: Calculate the translation vector to move bend_end_vertex to new_bend_end_vertex
    translation_vector = transformed_plate2_com - plate2_COM
    apply_flatten_transformation(plate2,translation_vector,transformed_plate2_com)


def find_and_unfold_triplets(node):
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
                            unfold_surfaces(node, child1, child2)
                            print('found_triplets of {}, {}, {}'.format(node.face_id, child1.face_id, child2.face_id))
                            # Mark the cylindrical and second flat node as flattened
                            child1.flatten = True
                            child2.flatten = True
                            count = count+1
                            if count==1:
                                return
                            # Recursively process child2 after unfolding
                            find_and_unfold_triplets(child2)  # Process further descendants of child2
                            # Add the triplet (Flat -> Cylindrical -> Flat) to the list
                            #triplet_list.append((node, child1, child2))
                        else:
                            print('No bend found between {}, {}, {}'.format(node.face_id,child1.face_id,child2.face_id))
    # Recursively traverse the children of the current node
    for child in node.children:
        if not child.flatten:
            find_and_unfold_triplets(child)


def traverse_and_unfold(node):
    # Step 1: Find all Flat -> Cylindrical -> Flat combinations (triplets)
    triplet_list = []
    find_and_unfold_triplets(node)
    #print(triplet_list)


# # After processing children, return to the original root and traverse its other children (siblings)
# for sibling in original_node.children:
#     traverse_and_unfold(sibling)



# # Visualize using Matplotlib
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# # Plot the original line before the bend
# ax.plot([plate1_COM[0], bend_start_vertex[0]], [plate1_COM[1], bend_start_vertex[1]], 
#         [plate1_COM[2], bend_start_vertex[2]], 'b-', label='Original Line')

# # Plot the bend segment (for reference)
# ax.plot([bend_start_vertex[0], bend_end_vertex[0]], [bend_start_vertex[1], bend_end_vertex[1]], 
#         [bend_start_vertex[2], bend_end_vertex[2]], 'r--', label='Bend (Circular)')

# # Plot the attached line before straightening
# ax.plot([bend_end_vertex[0], plate2_COM[0]], [bend_end_vertex[1], plate2_COM[1]], 
#         [bend_end_vertex[2], plate2_COM[2]], 'm-', label='Attached Line (Before Straightening)')

# # Plot the straightened line
# ax.plot([bend_start_vertex[0], new_bend_end_vertex[0]], [bend_start_vertex[1], new_bend_end_vertex[1]], 
#         [bend_start_vertex[2], new_bend_end_vertex[2]], 'g-', label='Straightened Line')

# # Plot the transformed attached line after straightening
# ax.plot([new_bend_end_vertex[0], transformed_plate2_com[0]], [new_bend_end_vertex[1], transformed_plate2_com[1]], 
#         [new_bend_end_vertex[2], transformed_plate2_com[2]], 'c--', label='Attached Line (After Straightening)')




# # Set labels
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')

# # Show the plot
# plt.legend()
# plt.show()



