from face_operations import extract_faces, is_flat_face, rotate_face, translate_face, filter_faces_by_thickness
from OCC.Core.gp import gp_Vec, gp_Pnt, gp_Ax1, gp_Dir
import os
from file_loader import load_step_file

def test_extract_faces():
    step_file_path = os.path.join(os.getcwd(), "data/WP-2.step")
    shape = load_step_file(step_file_path)
    
    faces = extract_faces(shape)
    assert len(faces) > 0, "No faces extracted from STEP file."
    print(f"Extracted {len(faces)} faces successfully!")

def test_face_transformations():
    step_file_path = os.path.join(os.getcwd(), "data/WP-2.step")
    shape = load_step_file(step_file_path)

    faces = extract_faces(shape)
    face = faces[0]

    # Rotate the face
    axis = gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1))  # Use gp_Dir instead of gp_Vec
    rotated_face = rotate_face(face, axis, 45.0, gp_Pnt(0, 0, 0))
    assert rotated_face is not None, "Rotation failed."

    
    # Translate the face
    translation_vec = gp_Vec(10, 0, 0)
    translated_face = translate_face(rotated_face, translation_vec)
    assert translated_face is not None, "Translation failed."
    print("Face transformation (rotation and translation) tests passed.")

def test_filter_faces_by_thickness():
    step_file_path = os.path.join(os.getcwd(), "data/WP-2.step")
    shape = load_step_file(step_file_path)
    
    faces = extract_faces(shape)
    filtered_faces = filter_faces_by_thickness(faces, thickness=2.0)
    assert len(filtered_faces) > 0, "No faces matched the specified thickness."
    print(f"Filtered {len(filtered_faces)} faces with thickness 2.0.")
