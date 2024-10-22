# src/file_loader.py

from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.IFSelect import IFSelect_RetDone

def load_step_file(file_path):
    """
    Loads a STEP file and returns a shape object.
    Args:
        file_path (str): Path to the STEP file.
    Returns:
        shape (TopoDS_Shape): Loaded shape if successful, None otherwise.
    """

    # Initialize STEP file reader
    step_reader = STEPControl_Reader()

    # Read the STEP file
    status = step_reader.ReadFile(file_path)

    # Check if the file is read successfully
    if status != IFSelect_RetDone:
        print(f"Error: Unable to load STEP file: {file_path}")
        return None

    # Transfer the file contents to a shape
    step_reader.TransferRoots()
    shape = step_reader.OneShape()

    return shape

