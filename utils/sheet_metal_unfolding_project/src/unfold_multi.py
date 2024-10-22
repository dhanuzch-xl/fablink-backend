import numpy as np

# Function to compute rotation matrix around an arbitrary axis
def rotation_matrix_around_axis(axis, angle):
    axis = axis / np.linalg.norm(axis)  # Normalize the rotation axis
    cos_angle = np.cos(angle)
    sin_angle = np.sin(angle)
    ux, uy, uz = axis
    
    rotation_matrix = np.array([
        [cos_angle + ux**2 * (1 - cos_angle), ux*uy*(1 - cos_angle) - uz*sin_angle, ux*uz*(1 - cos_angle) + uy*sin_angle],
        [uy*ux*(1 - cos_angle) + uz*sin_angle, cos_angle + uy**2 * (1 - cos_angle), uy*uz*(1 - cos_angle) - ux*sin_angle],
        [uz*ux*(1 - cos_angle) - uy*sin_angle, uz*uy*(1 - cos_angle) + ux*sin_angle, cos_angle + uz**2 * (1 - cos_angle)]
    ])
    
    return rotation_matrix

# Function to apply the transformation to both b2 and c1
def straighten_arc(b1, b2, c1, bend_radius, bend_angle):
    # Calculate the arc length
    arc_length = bend_radius * bend_angle

    # Vector from b1 to b2
    vec_b1_b2 = b2 - b1

    # Straightened b2' along the XY plane, using arc length
    direction_b1_b2 = np.array([b2[0] - b1[0], b2[1] - b1[1], 0])  # Flatten to XY plane
    direction_b1_b2_normalized = direction_b1_b2 / np.linalg.norm(direction_b1_b2)
    b2_prime = b1 + direction_b1_b2_normalized * arc_length  # New b2'

    # Compute the rotation axis using the cross product of b1-b2 and b1-b2'
    rotation_axis = np.cross(vec_b1_b2, b2_prime - b1)
    
    # Use the bend angle as the rotation angle
    rotation_angle = bend_angle
    
    # Get the rotation matrix around the computed axis
    rotation_mat = rotation_matrix_around_axis(rotation_axis, rotation_angle)

    # Transform b2 to b2'
    b2_relative = b2 - b1
    b2_prime_transformed = b1 + rotation_mat @ b2_relative
    
    # Transform c1 to c1' using the same rotation matrix
    c1_relative = c1 - b1
    c1_prime_transformed = b1 + rotation_mat @ c1_relative

    return b2_prime_transformed, c1_prime_transformed

# Example coordinates for b1, b2, and c1
b1 = np.array([0, 0, 0])
b2 = np.array([5, 2, 3])  # Point b2 in 3D
c1 = np.array([7, 4, 2])  # Point c1 in 3D

bend_radius = 3  # Bend radius
bend_angle = np.pi / 4  # Bend angle (45 degrees)

# Compute the transformed points b2' and c1'
# b2_prime, c1_prime = straighten_arc(b1, b2, c1, bend_radius, bend_angle)
