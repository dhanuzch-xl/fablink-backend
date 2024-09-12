from utils import load_step_file
from compute_step_properties import compute_bounding_box_mm

def is_sheet_metal(file_path: str):
    length, breadth, thickness = get_revised_length_breadth_height(file_path)     

    # Step 2: Set the thickness threshold for sheet metal
    min_thickness = 0.3  # in mm # TODO: comes from the database #0.015 inch
    max_thickness = 12.7  # in mm # TODO: comes from the database #0.50 inch

    # Step 3: Check if the smallest dimension (thickness) is within the threshold
    if min_thickness <= thickness <= max_thickness:
        # Step 4: Ensure other dimensions are much larger than the thickness
        if length >= 10 * thickness and breadth >= 10 * thickness:
            return True  # The object is likely sheet metal
        else:
            return False  # The object is too thick relative to its other dimensions
    else:
        return False  # The object is not within the sheet metal thickness range

def get_revised_length_breadth_height(file_path: str):
    """
    Gives the smallest dimension as the thickness, and the other two as length and breadth.
    Returns:
        length, breadth, thickness
    """
    shape = load_step_file(file_path)
    length, breadth, height = compute_bounding_box_mm(shape)

    # Step 1: Identify the smallest dimension, assumed to be the thickness
    dimensions = sorted([length, breadth, height])
    thickness = dimensions[0]  # Smallest dimension is treated as the thickness
    length = dimensions[1]
    breadth = dimensions[2]

    return length, breadth, thickness

if __name__ == "__main__":
    file_path = "models/Plate_1.step"
    print(is_sheet_metal(file_path))
