from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.TopoDS import TopoDS_Shape, topods_Edge  # Corrected the import here
from OCC.Core.TopAbs import TopAbs_EDGE
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Display.SimpleGui import init_display
from OCC.Core.gp import gp_Pnt
from OCC.Extend.ShapeFactory import get_aligned_boundingbox  # Import for getting bounding box

# Initialize the display only once
display, start_display, add_menu, add_function_to_menu = init_display()

def read_step_file(filename):
    """Read the STEP file and return the shape."""
    step_reader = STEPControl_Reader()
    status = step_reader.ReadFile(filename)

    if status == IFSelect_RetDone:  # Check status
        step_reader.TransferRoot(1)
        return step_reader.Shape(1)
    else:
        print("Error: Can't read the file.")
        return None

def get_edges(shape):
    """Return the edges from `shape`."""
    explorer = TopExp_Explorer(shape, TopAbs_EDGE)
    edges = []

    while explorer.More():
        edges.append(topods_Edge(explorer.Current()))
        explorer.Next()

    return edges

def tag_edge(_edge, msg, _color=(1, 0, 0)):
    """Tag an edge."""
    center_pt = get_aligned_boundingbox(_edge)[0]
    display.DisplayMessage(center_pt, msg, message_color=_color)

def visualize_edges(shape):
    """Visualize edges of the shape."""
    edges = get_edges(shape)
    for n, edge in enumerate(edges):
        tag_edge(edge, f"Edge {n}")

def main():
    # Load the STEP file (update the path as needed)
    filename = "/home/meher/xlogic/fablink-backend/models/WP-2.step"  # Change to your STEP file path
    shp = read_step_file(filename)

    if shp:  # Ensure the shape is valid before processing
        visualize_edges(shp)  # Visualize the edges of the shape

        # Display the shape
        display.DisplayShape(shp, update=True)

    # Start the display
    start_display()

if __name__ == "__main__":
    main()
