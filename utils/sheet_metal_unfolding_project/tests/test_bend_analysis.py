from bend_analysis import detect_bends, calculate_bend_angle
from file_loader import load_step_file
from face_operations import extract_faces
import os

def test_detect_bends():
    step_file_path = os.path.join(os.getcwd(), "data/WP-2.step")
    shape = load_step_file(step_file_path)
    
    faces = extract_faces(shape)
    bends = detect_bends(faces, thickness=2.0)
    
    assert len(bends) > 0, "No bends detected."
    print(f"Detected {len(bends)} bends successfully!")

def test_calculate_bend_angle():
    step_file_path = os.path.join(os.getcwd(), "data/WP-2.step")
    shape = load_step_file(step_file_path)
    
    faces = extract_faces(shape)
    
    for i in range(len(faces)):
        for j in range(i + 1, len(faces)):  # Avoid duplicate and self-pairing
            face1, face2 = faces[i], faces[j]
            angle = calculate_bend_angle(face1, face2)

            # Check if the angle is None and print appropriate messages
            if angle is None:
                print(f"Bend angle could not be calculated between face {i+1} and face {j+1}. One or both faces are not planar.")
            else:
                assert angle >= 0, f"Bend angle calculation failed between face {i+1} and face {j+1}."
                print(f"Calculated bend angle between face {i+1} and face {j+1}: {angle} degrees.")

    print("Bend angle calculations completed for all face pairs.")

