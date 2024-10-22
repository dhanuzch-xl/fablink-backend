from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.TopoDS import topods  # Corrected the import here
from OCC.Core.TopAbs import TopAbs_EDGE
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Display.SimpleGui import init_display
from OCC.Core.gp import gp_Pnt
from OCC.Extend.ShapeFactory import get_aligned_boundingbox  # Import for getting bounding box
from OCC.Core.BRepAdaptor import BRepAdaptor_Curve

# # Initialize the display only once
# display, start_display, add_menu, add_function_to_menu = init_display()

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
        edges.append(topods.Edge(explorer.Current()))
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
        
from OCC.Core.BRepAdaptor import BRepAdaptor_Curve
from OCC.Core.gp import gp_Pnt

def edge_to_dict(edge):
    """Convert an edge into a dictionary containing the start and end points."""
    # Get the actual start and end points of the edge using BRepAdaptor_Curve
    curve_adaptor = BRepAdaptor_Curve(edge)

    # Get the curve's first and last parameters (t1, t2)
    t1 = curve_adaptor.FirstParameter()
    t2 = curve_adaptor.LastParameter()

    # Initialize points to store the start and end
    start_point = gp_Pnt()
    end_point = gp_Pnt()

    # Evaluate the curve at t1 (start) and t2 (end) to get the 3D points
    curve_adaptor.D0(t1, start_point)  # Evaluates at t1, stores in start_point
    curve_adaptor.D0(t2, end_point)    # Evaluates at t2, stores in end_point

    # Return the start and end points in dictionary format
    return {
        "start": {"x": start_point.X(), "y": start_point.Y(), "z": start_point.Z()},
        "end": {"x": end_point.X(), "y": end_point.Y(), "z": end_point.Z()}
    }



# def main():
#     # Load the STEP file (update the path as needed)
#     filename = "/home/meher/xlogic/fablink-backend/models/WP-2.step"  # Change to your STEP file path
#     shp = read_step_file(filename)

#     if shp:  # Ensure the shape is valid before processing
#         visualize_edges(shp)  # Visualize the edges of the shape

#         # Display the shape
#         display.DisplayShape(shp, update=True)

#     # Start the display
#     start_display()

# if __name__ == "__main__":
#     main()
