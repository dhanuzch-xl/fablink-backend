import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from transform_node import apply_transformation_to_node_and_children

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

    if sum(child_direction):
        new_direction = child_direction
    else:
        new_direction = parent_direction

    translation_vector = new_bend_end_vertex - bend_end_vertex
    bend_end_vertex_translated = np.array(bend_end_vertex) + translation_vector
    plate2_COM_translated = np.array(plate2_COM) + translation_vector

    attached_line_direction = np.array(plate2_COM) - np.array(bend_end_vertex)
    attached_line_direction = attached_line_direction / np.linalg.norm(attached_line_direction)
    rotation_matrix = calculate_rotation_matrix(attached_line_direction, new_direction)

    bend_end_vertex_rotated = rotation_matrix @ (bend_end_vertex_translated - new_bend_end_vertex) + new_bend_end_vertex
    plate2_COM_rotated = rotation_matrix @ (plate2_COM_translated - new_bend_end_vertex) + new_bend_end_vertex

    return plate2_COM_rotated



def transform_vertices(plate1_COM, bend_start, bend_end, plate2_COM, bend_radius, bend_angle,flatten = False):
    """
    This function combines the logic of straightening the bend and transforming the attached line.
    It handles both bend and planar surfaces based on the surface_type argument.
    """
    # Straighten the bend
    if flatten:
        child_direction = np.array([bend_end[0], bend_end[1], 0]) - np.array([bend_start[0], bend_start[1], 0])
    else:
        child_direction = np.array([bend_end[0], bend_end[1], bend_end[2]]) - np.array([bend_start[0], bend_start[1], bend_start[2]])

    if sum(child_direction):
        direction_vector = child_direction
    else:
        direction_vector = np.array(bend_start) - np.array(plate1_COM)
    
    direction_vector = direction_vector / np.linalg.norm(direction_vector)
    if flatten:
        bend_length = bend_radius * bend_angle  # Arc length
    else:
        bend_length = distance_between_points(bend_start,bend_end)
    new_bend_end_vertex = np.array(bend_start) + direction_vector * bend_length
    new_line_end_vertex = transform_attached_line(bend_end, new_bend_end_vertex, plate2_COM, direction_vector,flatten)
    return new_bend_end_vertex, new_line_end_vertex


def unfold_surfaces(plate1,bend,plate2):
    plate1_COM = plate1.COM  
    common_edge_vertices = bend.vertexDict['before_unfld']
    bend_start_vertex = common_edge_vertices[0]
    bend_end_vertex = common_edge_vertices[1] 
    bend_angle = bend.bend_angle
    bend_radius = bend.inner_radius
    plate2_COM = plate2.COM  

    new_bend_end_vertex, transformed_plate2_com = transform_vertices(plate1_COM, bend_start_vertex, bend_end_vertex, plate2_COM,bend_radius,bend_angle,flatten=True)
    #create flatten face at the bend node using merge surface option in three JS or OCC
    transformation = get_transformation_matrix(plate2_COM,transformed_plate2_com,plate2.axis)
    apply_transformation_to_node_and_children(plate2,transformation)


# Main Code
def traverse_and_unfold(node):
    """
    Traverse the tree of face nodes to find the pattern Flat -> Cylindrical -> Flat
    and call unfold_surfaces(flatnode1, cylnode, flatnode2) whenever such a pattern is found.
    
    Parameters:
    node (FaceNode): The current node in the tree.
    """
    # Check if the current node is a flat surface and has not been flattened yet
    if node.surface_type == 'Flat' and not node.flatten:
        # Traverse its children to find a cylindrical surface
        for child1 in node.children:
            if child1.surface_type == 'Cylindrical' and not child1.flatten:
                # Traverse the children of the cylindrical surface to find another flat surface
                for child2 in child1.children:
                    if child2.surface_type == 'Flat' and not child2.flatten:
                        # We found the Flat -> Cylindrical -> Flat pattern, call unfold_surfaces
                        unfold_surfaces(node, child1, child2)
                        # Set flatten flag to True to avoid revisiting these nodes
                        node.flatten = True
                        child1.flatten = True
                        child2.flatten = True

                        return  # Exit after finding and processing this combination
    
    # If the pattern was not found, continue traversing the tree
    for child in node.children:
        traverse_and_unfold(child)


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


