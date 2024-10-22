from bend_analysis import detect_bends, calculate_bend_angle
from file_loader import load_step_file
from face_operations import extract_faces
from sheet_tree import SheetTree
import os
def test_build_tree():
    step_file_path = os.path.join(os.getcwd(), "data/WP-2.step")
    shape = load_step_file(step_file_path)
    
    sheet_tree = SheetTree(shape)
    sheet_tree.build_tree()
    
    assert len(sheet_tree.nodes) > 0, "Tree construction failed."
    print(f"Tree constructed with {len(sheet_tree.nodes)} nodes.")


def test_bend_detection_in_tree():
    step_file_path = os.path.join(os.getcwd(), "data/WP-2.step")
    shape = load_step_file(step_file_path)
    
    sheet_tree = SheetTree(shape)
    sheet_tree.build_tree()
    
    # Extract the faces from the tree
    faces = [node.face for node in sheet_tree.nodes]
    
    # Call detect_bends on the faces
    bends = detect_bends(faces, thickness=2.0)
    
    assert len(bends) > 0, "No bends detected in the tree."
    print(f"Bends detected in the tree: {len(bends)}")
