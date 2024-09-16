import matplotlib.pyplot as plt
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_FACE, TopAbs_EDGE
from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepAdaptor import BRepAdaptor_Curve
from OCC.Core.GeomAbs import GeomAbs_Circle
from OCC.Core.gp import gp_Circ

# Load the STEP file
def load_step_file(file_path: str):
    step_reader = STEPControl_Reader()
    step_reader.ReadFile(file_path)
    step_reader.TransferRoot()
    shape = step_reader.Shape()
    return shape

def find_holes_in_step(shape):
    # Step 1: Explore all faces in the STEP file
    explorer_faces = TopExp_Explorer(shape, TopAbs_FACE)
    
    holes = []  # List to store hole data
    
    while explorer_faces.More():
        face = explorer_faces.Current()
        
        # Step 2: Explore edges within the face
        explorer_edges = TopExp_Explorer(face, TopAbs_EDGE)
        
        while explorer_edges.More():
            edge = explorer_edges.Current()
            
            # Use BRepAdaptor_Curve to adapt the edge into a curve
            curve_adaptor = BRepAdaptor_Curve(edge)
            
            # Check if the curve type is a circle
            if curve_adaptor.GetType() == GeomAbs_Circle:
                # Ensure the curve is a complete circle
                first_param = curve_adaptor.FirstParameter()
                last_param = curve_adaptor.LastParameter()
                full_circle_param_range = 2 * 3.141592653589793  # 2 * pi
                
                if abs(last_param - first_param - full_circle_param_range) < 1e-6:
                    # Extract the circle parameters
                    circle = curve_adaptor.Circle()
                    radius = circle.Radius()
                    center = circle.Location()
                    
                    # Store hole information (position and diameter)
                    hole_data = (
                        (center.X(), center.Y(), center.Z()),
                        2 * radius
                    )
                    holes.append(hole_data)
            
            explorer_edges.Next()
        
        explorer_faces.Next()
    
    if len(holes) == 0:
        raise ValueError("No holes found in the shape.")
    
    # Calculate the average absolute value for each coordinate
    sum_abs_values = [0, 0, 0]
    for center, _ in holes:
        for i, coord in enumerate(center):
            sum_abs_values[i] += abs(coord)
    
    avg_abs_values = [sum_val / len(holes) for sum_val in sum_abs_values]
    
    # Find the index of the coordinate with the smallest average absolute value
    min_index = avg_abs_values.index(min(avg_abs_values))
    
    # Remove the smallest average coordinate from each hole's center
    unique_holes_set = set()
    unique_holes = []
    removed_holes = []
    for center, diameter in holes:
        center_coords = list(center)
        removed_value = center_coords.pop(min_index)  # Remove the smallest average value
        hole_tuple = (tuple(center_coords), diameter)
        
        if hole_tuple not in unique_holes_set:
            unique_holes_set.add(hole_tuple)
            unique_holes.append({"center": tuple(center_coords), "diameter": diameter, "removed_value": removed_value})
        else:
            removed_holes.append({"center": tuple(center_coords), "diameter": diameter, "removed_value": removed_value})
    
    return unique_holes, removed_holes

def get_removed_holes(file_path: str):
    shape = load_step_file(file_path)
    _, removed_holes = find_holes_in_step(shape)
    return removed_holes

# Example Usage
file_path = "models/WP-15.step"    
shape = load_step_file(file_path)
unique_holes, removed_holes = find_holes_in_step(shape)

# Return the selected and rejected holes
print("Selected Holes:", len(unique_holes))
print("Rejected Holes:", len(removed_holes))
# Output all holes
print("Unique Holes:")
for hole in unique_holes:
    print(f"Hole at {hole['center']} with diameter {hole['diameter']:.2f} mm (removed value: {hole['removed_value']:.2f})")

# Plotting the unique holes
x_coords_unique = [hole['center'][0] for hole in unique_holes]
y_coords_unique = [hole['center'][1] for hole in unique_holes]
diameters_unique = [hole['diameter'] for hole in unique_holes]

# plt.figure(figsize=(10, 8))
# plt.scatter(x_coords_unique, y_coords_unique, s=diameters_unique, alpha=0.5)
# plt.xlabel('X Coordinate')
# plt.ylabel('Y Coordinate')
# plt.title('Unique Holes in Sheet Metal')
# plt.grid(True)
# plt.show()

# Plotting the removed holes
x_coords_removed = [hole['center'][0] for hole in removed_holes]
y_coords_removed = [hole['center'][1] for hole in removed_holes]
diameters_removed = [hole['diameter'] for hole in removed_holes]

# plt.figure(figsize=(10, 8))
# plt.scatter(x_coords_removed, y_coords_removed, s=diameters_removed, alpha=0.5, color='red')
# plt.xlabel('X Coordinate')
# plt.ylabel('Y Coordinate')
# plt.title('Removed Holes in Sheet Metal')
# plt.grid(True)
# plt.show()

# Plotting all detected holes
# print("All holes:", len(all_holes))
# for hole in all_holes:
#     print(hole)
# x_coords_all = [hole[0][0] for hole in all_holes]
# y_coords_all = [hole[0][1] for hole in all_holes]
# z_coords_all = [hole[0][2] for hole in all_holes]
# diameters_all = [hole[1] for hole in all_holes]

# plt.figure(figsize=(10, 8))
# plt.scatter(y_coords_all, z_coords_all, s=diameters_all, alpha=0.5, color='blue')
# plt.xlabel('Y Coordinate')
# plt.ylabel('Z Coordinate')
# plt.title('All Detected Holes in Sheet Metal')
# plt.grid(True)
# plt.show()

# Get and print removed holes using the new function
# removed_holes_only = get_removed_holes(file_path)
# print("\nRemoved Holes (using get_removed_holes function):")
# for hole in removed_holes_only:
#     print(f"Hole at {hole['center']} with diameter {hole['diameter']:.2f} mm (removed value: {hole['removed_value']:.2f})")