# tests/test_file_loader.py

from file_loader import load_step_file  # Import from src

def test_load_step_file():
    """
    Test loading a STEP file and verify the shape is successfully loaded.
    """
    # Hardcoded STEP file path for testing
    file_path = "data/WP-2.step"  # Update this to the correct path if needed

    # Attempt to load the STEP file
    shape = load_step_file(file_path)

    # Test if the shape is loaded successfully
    assert shape is not None, f"STEP file {file_path} failed to load."

    print(f"STEP file {file_path} loaded successfully!")


if __name__ == "__main__":
    test_load_step_file()
