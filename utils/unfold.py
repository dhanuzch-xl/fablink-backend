import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Function to calculate the transformation matrix (4x4) from rotation matrix and translation vector
def create_transformation_matrix(rotation_matrix, translation_vector):
    transformation_matrix = np.eye(4)
    transformation_matrix[:3, :3] = rotation_matrix
    transformation_matrix[:3, 3] = translation_vector
    return transformation_matrix

# Function to calculate the straightened line's end point by extending along the original direction
def straighten_line(start_vertex, bend_start_vertex, bend_end_vertex):
    child_direction = np.array([bend_end_vertex[0],bend_end_vertex[1],0]) - np.array([bend_start_vertex[0],bend_start_vertex[1],0])
    if sum(child_direction):
        direction_vector = child_direction
    else:
        direction_vector = np.array(bend_start_vertex) - np.array(start_vertex)
    
    direction_vector = direction_vector / np.linalg.norm(direction_vector)  # Normalize the direction
    bend_radius = 5  
    bend_angle = np.radians(45)  
    bend_length = bend_radius * bend_angle  # Arc length
    straightened_end = np.array(bend_start_vertex) + direction_vector * bend_length
    return straightened_end, direction_vector

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
def transform_attached_line(bend_end_vertex, new_bend_end_vertex, attached_line_start, attached_line_end, parent_direction):
    child_direction = np.array([attached_line_end[0],attached_line_end[1],0]) - np.array([attached_line_start[0],attached_line_start[1],0])
    if sum(child_direction):
        new_direction = child_direction
    else:
        new_direction = parent_direction

    translation_vector = new_bend_end_vertex - bend_end_vertex
    attached_line_start_translated = np.array(attached_line_start) + translation_vector
    attached_line_end_translated = np.array(attached_line_end) + translation_vector

    attached_line_direction = np.array(attached_line_end) - np.array(attached_line_start)
    attached_line_direction = attached_line_direction / np.linalg.norm(attached_line_direction)
    rotation_matrix = calculate_rotation_matrix(attached_line_direction, new_direction)

    attached_line_start_rotated = rotation_matrix @ (attached_line_start_translated - new_bend_end_vertex) + new_bend_end_vertex
    attached_line_end_rotated = rotation_matrix @ (attached_line_end_translated - new_bend_end_vertex) + new_bend_end_vertex

    return attached_line_start_rotated, attached_line_end_rotated, rotation_matrix, translation_vector

# Main Code
start_vertex = np.array([0, 0, 0])  
bend_start_vertex = np.array([5, 5, 0])  
bend_end_vertex = np.array([8, 5, 3])  

attached_line_start = np.array([8, 5, 3])  
attached_line_end = np.array([8, 2, 12])  

new_bend_end_vertex, new_direction = straighten_line(start_vertex, bend_start_vertex, bend_end_vertex)

transformed_line_start, transformed_line_end, rotation_matrix, translation_vector = transform_attached_line(
    bend_end_vertex, new_bend_end_vertex, attached_line_start, attached_line_end, new_direction)

# Function to transform a 3D point using a 4x4 matrix
def apply_transformation(vertex, transformation_matrix):
    homogeneous_vertex = np.append(vertex, 1)  # Convert to homogeneous coordinates (x, y, z, 1)
    transformed_homogeneous_vertex = transformation_matrix @ homogeneous_vertex
    return transformed_homogeneous_vertex[:3]  # Return the transformed 3D vertex

# Create transformation matrices that include both rotation and translation
transformation_dict = {}

# 1. Bend Start Vertex (no rotation, only translation)
transformation_dict['bend_start'] = create_transformation_matrix(np.eye(3), bend_start_vertex)

# 2. Bend End Vertex (rotation + translation)
transformation_dict['bend_end'] = create_transformation_matrix(rotation_matrix, new_bend_end_vertex)

# 3. Attached Line Start Vertex (rotation + translation)
transformation_dict['attached_line_start'] = create_transformation_matrix(rotation_matrix, transformed_line_start)

# 4. Attached Line End Vertex (rotation + translation)
transformation_dict['attached_line_end'] = create_transformation_matrix(rotation_matrix, transformed_line_end)

# Apply transformations to original vertices
transformed_vertices = {
    'bend_start': apply_transformation(bend_start_vertex, transformation_dict['bend_start']),
    'bend_end': apply_transformation(bend_end_vertex, transformation_dict['bend_end']),
    'attached_line_start': apply_transformation(attached_line_start, transformation_dict['attached_line_start']),
    'attached_line_end': apply_transformation(attached_line_end, transformation_dict['attached_line_end'])
}
fig1 = plt.figure()
ax1 = fig1.add_subplot(111,projection='3d')
# Plot original vertices (in blue)
ax1.scatter(bend_start_vertex[0], bend_start_vertex[1], bend_start_vertex[2], color='b', label='Original Bend Start')
ax1.scatter(start_vertex[0], start_vertex[1], start_vertex[2], color='b', label='Original Start Vertex')
ax1.scatter(bend_end_vertex[0], bend_end_vertex[1], bend_end_vertex[2], color='b', label='Original Bend End')
ax1.scatter(attached_line_start[0], attached_line_start[1], attached_line_start[2], color='b', label='Original Line Start')
ax1.scatter(attached_line_end[0], attached_line_end[1], attached_line_end[2], color='b', label='Original Line End')

# 1Plot transformed vertices (in red)
ax1.scatter(transformed_vertices['bend_start'][0], transformed_vertices['bend_start'][1], transformed_vertices['bend_start'][2], color='r', label='Transformed Bend Start')
ax1.scatter(transformed_vertices['bend_end'][0], transformed_vertices['bend_end'][1], transformed_vertices['bend_end'][2], color='r', label='Transformed Bend End')
ax1.scatter(transformed_vertices['attached_line_start'][0], transformed_vertices['attached_line_start'][1], transformed_vertices['attached_line_start'][2], color='r', label='Transformed Line Start')
ax1.scatter(transformed_vertices['attached_line_end'][0], transformed_vertices['attached_line_end'][1], transformed_vertices['attached_line_end'][2], color='r', label='Transformed Line End')


# Visualize using Matplotlib
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the original line before the bend
ax.plot([start_vertex[0], bend_start_vertex[0]], [start_vertex[1], bend_start_vertex[1]], 
        [start_vertex[2], bend_start_vertex[2]], 'b-', label='Original Line')

# Plot the bend segment (for reference)
ax.plot([bend_start_vertex[0], bend_end_vertex[0]], [bend_start_vertex[1], bend_end_vertex[1]], 
        [bend_start_vertex[2], bend_end_vertex[2]], 'r--', label='Bend (Circular)')

# Plot the attached line before straightening
ax.plot([attached_line_start[0], attached_line_end[0]], [attached_line_start[1], attached_line_end[1]], 
        [attached_line_start[2], attached_line_end[2]], 'm-', label='Attached Line (Before Straightening)')

# Plot the straightened line
ax.plot([bend_start_vertex[0], new_bend_end_vertex[0]], [bend_start_vertex[1], new_bend_end_vertex[1]], 
        [bend_start_vertex[2], new_bend_end_vertex[2]], 'g-', label='Straightened Line')

# Plot the transformed attached line after straightening
ax.plot([transformed_line_start[0], transformed_line_end[0]], [transformed_line_start[1], transformed_line_end[1]], 
        [transformed_line_start[2], transformed_line_end[2]], 'c--', label='Attached Line (After Straightening)')




# Set labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Show the plot
plt.legend()
plt.show()



