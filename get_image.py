import sys
from OCC.Extend.DataExchange import read_step_file
from OCC.Display.OCCViewer import OffscreenRenderer

def initialize_renderer(step_file_path, bg_color1, bg_color2):
    try:
        # Read the shape from the STEP file
        my_shape = read_step_file(step_file_path)
        
        # Initialize the offscreen renderer
        renderer = OffscreenRenderer()
        
        # Ensure OffscreenRenderer is properly initialized
        if renderer is None:
            raise RuntimeError("OffscreenRenderer is not initialized.")
        
        # Set background color
        renderer.set_bg_gradient_color(bg_color1, bg_color2)
        
        # Remove the axis mark
        renderer.hide_triedron()
        
        return renderer, my_shape
    except Exception as e:
        print(f"Error during renderer initialization: {e}")
        sys.exit(1)

def export_to_PNG(renderer, shape, step_file_path, output_path="./test"):
    filename = f"{step_file_path.split('/')[-1].split('.')[0]}.png"
    try:
        renderer.DisplayShape(shape, dump_image_path=output_path, dump_image_filename=filename)
    except Exception as e:
        print(f"Error exporting to PNG: {e}")
        sys.exit(1)

def exit_gracefully(renderer):
    renderer._inited = False
    sys.exit()

if __name__ == "__main__":
    step_file_path = "models/Plate_1.step"
    bg_color1 = [0, 0, 0]
    bg_color2 = [0, 0, 0]
    
    renderer, my_shape = initialize_renderer(step_file_path, bg_color1, bg_color2)
    export_to_PNG(renderer, my_shape, step_file_path)
    exit_gracefully(renderer)
