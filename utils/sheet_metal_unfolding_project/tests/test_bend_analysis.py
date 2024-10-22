import os
from bend_analysis import detect_bends
from file_loader import load_step_file
from face_operations import extract_faces

def test_detect_bends():
    # Load the STEP file for testing
    step_file_path = os.path.join(os.getcwd(), "data/WP-2.step")
    shape = load_step_file(step_file_path)
    
    # Extract faces from the shape
    faces = extract_faces(shape)
    
    # Detect bends in the faces
    bends = detect_bends(faces, thickness=2.0)
    
    assert len(bends) > 0, "No bends detected."
    print(f"Detected {len(bends)} bends successfully!")

import os
from bend_analysis import detect_bends, calculate_bend_angle
from file_loader import load_step_file
from face_operations import extract_faces

def test_calculate_bend_angle():
    # Load the STEP file for testing
    step_file_path = os.path.join(os.getcwd(), "data/WP-2.step")
    shape = load_step_file(step_file_path)
    
    # Extract faces from the shape
    faces = extract_faces(shape)
    
    # Detect bends in the faces
    bends = detect_bends(faces, thickness=2.0)
    
    # Test the first bend pair
    node1, node2 = bends[0]
    
    # Calculate bend angle
    bend_angle, bend_direction = calculate_bend_angle(node1, node2, thickness=2.0)
    
    assert bend_angle > 0, "Bend angle calculation failed."
    print(f"Bend angle: {bend_angle} degrees, Direction: {bend_direction}")

import os
from bend_analysis import detect_bends
from file_loader import load_step_file
from face_operations import extract_faces
from sheet_tree import SheetTreeNode

def test_apply_transformation():
    # Load the STEP file for testing
    step_file_path = os.path.join(os.getcwd(), "data/WP-2.step")
    shape = load_step_file(step_file_path)
    
    # Extract faces from the shape
    faces = extract_faces(shape)
    
    # Detect bends in the faces
    bends = detect_bends(faces, thickness=2.0)
    
    # Test the first bend pair
    node1, node2 = bends[0]
    
    # Create a SheetTreeNode for testing transformation
    tree_node = SheetTreeNode(node2.face)
    
    # Apply transformation (unfold)
    tree_node.apply_transformation()
    
    # Ensure that the transformed face exists
    assert tree_node.transformed_face is not None, "Transformation was not applied."
    print(f"Transformation applied successfully to node {tree_node.transformed_face}.")

import os
from bend_analysis import detect_bends
from file_loader import load_step_file
from face_operations import extract_faces
from sheet_tree import SheetTreeNode

def test_track_vertices():
    # Load the STEP file for testing
    step_file_path = os.path.join(os.getcwd(), "data/WP-2.step")
    shape = load_step_file(step_file_path)
    
    # Extract faces from the shape
    faces = extract_faces(shape)
    
    # Detect bends in the faces
    bends = detect_bends(faces, thickness=2.0)
    
    # Test the first bend pair
    node1, node2 = bends[0]
    
    # Create a SheetTreeNode for testing vertex tracking
    tree_node = SheetTreeNode(node2.face)
    
    # Apply transformation (unfold)
    tree_node.apply_transformation()
    
    # Track vertices before and after transformation
    tree_node.track_vertices()
    
    assert len(tree_node.vertexDict) > 0, "Vertices were not tracked."
    print(f"Tracked {len(tree_node.vertexDict)} vertices successfully!")
