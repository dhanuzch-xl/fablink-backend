from OCC.Core.gp import gp_Vec, gp_Pnt
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.TopoDS import topods  # Corrected the import here
from OCC.Core.TopAbs import TopAbs_EDGE
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Display.SimpleGui import init_display
from OCC.Core.gp import gp_Pnt
from OCC.Extend.ShapeFactory import get_aligned_boundingbox  # Import for getting bounding box

from OCC.Core.BRepAdaptor import BRepAdaptor_Curve

def get_edges(shape):
    """Return the edges from `shape`."""
    explorer = TopExp_Explorer(shape, TopAbs_EDGE)
    edges = []

    while explorer.More():
        edges.append(topods.Edge(explorer.Current()))
        explorer.Next()

    return edges

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

def distance_between_points(p1, p2):
    """Calculate the Euclidean distance between two 3D points."""
    vec = gp_Vec(gp_Pnt(p1['x'], p1['y'], p1['z']), gp_Pnt(p2['x'], p2['y'], p2['z']))
    return vec.Magnitude()

def are_edges_parallel(edge1_dict, edge2_dict):
    """Check if two edges are parallel based on their start and end points."""
    # Create vectors for the edges
    vec1 = gp_Vec(
        gp_Pnt(edge1_dict['start']['x'], edge1_dict['start']['y'], edge1_dict['start']['z']),
        gp_Pnt(edge1_dict['end']['x'], edge1_dict['end']['y'], edge1_dict['end']['z'])
    )
    vec2 = gp_Vec(
        gp_Pnt(edge2_dict['start']['x'], edge2_dict['start']['y'], edge2_dict['start']['z']),
        gp_Pnt(edge2_dict['end']['x'], edge2_dict['end']['y'], edge2_dict['end']['z'])
    )

    # Check if either of the vectors has a zero magnitude (degenerate edge)
    if vec1.Magnitude() == 0 or vec2.Magnitude() == 0:
        return False

    # Check if the vectors are parallel
    return vec1.IsParallel(vec2, 1e-6)
def calculate_sheet_metal_thickness_using_wires(shape):
    """Calculate the thickness of the sheet metal by comparing parallel edges."""
    edges = get_edges(shape)
    edge_dicts = [edge_to_dict(edge) for edge in edges]
     
    thickness_values = []
    processed_pairs = set()  # To track processed edge pairs

    # Compare each edge with the others to find parallel ones
    for i, edge1_dict in enumerate(edge_dicts):
        for j in range(i + 1, len(edge_dicts)):
            edge2_dict = edge_dicts[j]
            
            # Create a tuple of sorted edge ids to ensure uniqueness
            edge_pair = tuple(sorted([id(edge1_dict), id(edge2_dict)]))
            
            # Skip if this pair has already been processed
            if edge_pair in processed_pairs:
                continue
            
            # Mark this pair as processed
            processed_pairs.add(edge_pair)

            # Check if the edges are parallel
            if are_edges_parallel(edge1_dict, edge2_dict):
                # Calculate the distance between start points of the edges
                distance = distance_between_points(edge1_dict['start'], edge2_dict['start'])
                
                # Only add valid distances (e.g., within a threshold like <20mm and >0)
                if 1 < distance < 20:
                    thickness_values.append(distance)
    
    # Return or print the calculated thickness values (there may be multiple)
    if thickness_values:
        print(f"sheet metal thickness: {min(thickness_values):.6f} mm")
        return min(thickness_values)
    else:
        print("No parallel edges found.")
        return None
