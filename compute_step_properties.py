from OCC.Core.GProp import GProp_GProps
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.TopoDS import topods, TopoDS_Shape, TopoDS_Face
from OCC.Core.TopAbs import TopAbs_EDGE, TopAbs_FACE
from OCC.Core.BRep import BRep_Tool
from OCC.Core.gp import gp_Pnt
from OCC.Core.BRepBndLib import brepbndlib
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopExp import topexp

from utils import load_step_file

# Conversion functions
def mm_to_cm(mm):
    return mm / 10

def mm_to_inches(mm):
    return mm / 25.4

def mm3_to_in3(mm3):
    return mm3 / 16387.064  # 1in3 = 16387.064mm3

def mm2_to_in2(mm2):
    return mm2 / 645.16  # 1in2 = 645.16mm2

# Function to compute volume using GProps
def compute_volume_mm3(shape: TopoDS_Shape):
    props = GProp_GProps()
    brepgprop.VolumeProperties(shape, props)
    volume = props.Mass()  # Volume in mm³
    return volume

# Function to compute the bounding box (length, breadth, height)
def compute_bounding_box_mm(shape: TopoDS_Shape):
    bbox = Bnd_Box()
    brepbndlib.Add(shape, bbox)
    xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
    length = xmax - xmin
    breadth = ymax - ymin
    height = zmax - zmin
    return length, breadth, height

# Function to get the largest face based on surface area
def get_largest_face_mm2(shape: TopoDS_Shape):
    explorer = TopExp_Explorer(shape, TopAbs_FACE)
    largest_face = None
    largest_area = 0.0
    
    while explorer.More():
        face = topods.Face(explorer.Current())
        area = compute_surface_area_mm2(face)
        
        if area > largest_area:
            largest_area = area
            largest_face = face
        
        explorer.Next()
    
    return largest_face, largest_area

# Function to compute surface area
def compute_surface_area_mm2(shape: TopoDS_Shape):
    props = GProp_GProps()
    brepgprop.SurfaceProperties(shape, props)
    area = props.Mass()  # Surface area in mm²
    return area

# Function to calculate the length of an edge
def compute_edge_length_mm(edge):
    props = GProp_GProps()
    brepgprop.LinearProperties(edge, props)
    return props.Mass()  # Mass here refers to the length of the edge

# Function to compute the perimeter along the breadth and height for one face
def compute_perimeter_of_face_mm(face: TopoDS_Face, tolerance=1e-3):
    total_perimeter = 0.0
    explorer = TopExp_Explorer(face, TopAbs_EDGE)
    
    # Iterate through all edges of the face
    while explorer.More():
        edge = topods.Edge(explorer.Current())
        edge_length = compute_edge_length_mm(edge)
        
        # Get the points of the edge
        vertex1 = topexp.FirstVertex(edge)
        p1 = BRep_Tool.Pnt(vertex1)
        vertex2 = topexp.LastVertex(edge)
        p2 = BRep_Tool.Pnt(vertex2)
        
        # Check if the edge lies along the Y-axis (breadth) or Z-axis (height)
        if abs(p1.X() - p2.X()) < tolerance:  # The edge runs along the YZ plane (perpendicular to X)
            total_perimeter += edge_length
        
        explorer.Next()

    return total_perimeter

# Function to compute the perimeter of the largest face
def compute_perimeter_of_largest_face_mm(shape: TopoDS_Shape, tolerance=1e-3):
    face, largest_area = get_largest_face_mm2(shape)
    if face is None:
        print("No face found in the shape!")
        return
    
    print(f"Largest face area: {largest_area:.2f} mm²")
    
    perimeter_mm = compute_perimeter_of_face_mm(face, tolerance)
    perimeter_in = mm_to_inches(perimeter_mm)
    
    print(f"Perimeter (Breadth and Height) for the largest face: {perimeter_mm:.2f} mm ({perimeter_in:.2f} inches)")

# Function to count the number of edges and faces
def count_edges_faces(shape: TopoDS_Shape):
    edge_count = 0
    face_count = 0
    
    explorer = TopExp_Explorer(shape, TopAbs_EDGE)
    while explorer.More():
        edge_count += 1
        explorer.Next()
    
    explorer = TopExp_Explorer(shape, TopAbs_FACE)
    while explorer.More():
        face_count += 1
        explorer.Next()
    
    return edge_count, face_count

# Function to compute the bounding box volume
def compute_bounding_box_volume_mm3(shape: TopoDS_Shape):
    length, breadth, height = compute_bounding_box_mm(shape)
    return length * breadth * height

# Main function to analyze the STEP file
def analyze_step_file(file_path: str):
    # Load STEP file
    shape = load_step_file(file_path)
    
    # Calculate length, breadth, and height
    length, breadth, height = compute_bounding_box_mm(shape)
    print(f"Length: {length:.2f} mm ({mm_to_cm(length):.2f} cm, {mm_to_inches(length):.2f} inches)")
    print(f"Breadth: {breadth:.2f} mm ({mm_to_cm(breadth):.2f} cm, {mm_to_inches(breadth):.2f} inches)")
    print(f"Height: {height:.2f} mm ({mm_to_cm(height):.2f} cm, {mm_to_inches(height):.2f} inches)")

    print("--------------------------------")
    
    # Calculate surface area
    surface_area_mm2 = compute_surface_area_mm2(shape)
    surface_area_in2 = mm2_to_in2(surface_area_mm2)
    print(f"Surface Area: {surface_area_mm2:.2f} mm² ({mm_to_cm(surface_area_mm2):.2f} cm², {surface_area_in2:.2f} in²)")

    print("--------------------------------")
    
    # Calculate volume
    volume_mm3 = compute_volume_mm3(shape)
    volume_in3 = mm3_to_in3(volume_mm3)
    print(f"Volume: {volume_mm3:.2f} mm³ ({mm_to_cm(volume_mm3):.2f} cm³, {volume_in3:.2f} in³)")

    print("--------------------------------")
    
    # Count edges and faces
    edge_count, face_count = count_edges_faces(shape)
    print(f"Number of Edges: {edge_count}, Number of Faces: {face_count}")

    print("--------------------------------")
    
    # Bounding box volume
    boundingbox_volume_mm3 = compute_bounding_box_volume_mm3(shape)
    boundingbox_volume_in3 = mm3_to_in3(boundingbox_volume_mm3)
    print(f"Bounding Box Volume: {boundingbox_volume_mm3:.2f} mm³, {mm_to_cm(boundingbox_volume_mm3):.2f} cm³, {boundingbox_volume_in3:.2f} inches³")
    print("--------------------------------")


if __name__ == "__main__":
    # Example usage
    file_path = 'models/Plate_2.step'  # Update with your file path
    analyze_step_file(file_path)
    compute_perimeter_of_largest_face_mm(load_step_file(file_path))
