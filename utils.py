from OCC.Core.STEPControl import STEPControl_Reader

# Load the STEP file
def load_step_file(file_path: str):
    step_reader = STEPControl_Reader()
    step_reader.ReadFile(file_path)
    step_reader.TransferRoot()
    shape = step_reader.Shape()
    return shape

