import sys
import math
from OCC.Core.TopoDS import topods_Face
from OCC.Core.TopAbs import TopAbs_FACE
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.GeomAbs import GeomAbs_Cylinder
from OCC.Core.BRep import BRep_Tool_Surface
from OCC.Core.BRepBndLib import brepbndlib
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.GProp import GProp_GProps
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.BRepTools import breptools_Read
from OCC.Core.gp import gp_Pnt
from OCC.Extend.TopologyUtils import TopologyExplorer
from OCC.Display.SimpleGui import init_display


# user libraries
from find_sheet_thickness import get_sheet_thickness
# Function to get all faces from a shape
def get_faces(shape):
    """
    Return the faces from `shape`.
    """
    explorer = TopologyExplorer(shape)
    faces = [face for face in explorer.faces()]
    return faces

# Function to compute the area of a face
def get_face_area(face):
    """
    Compute and return the area of a given face.
    """
    props = GProp_GProps()
    brepgprop.SurfaceProperties(face, props)
    area = props.Mass()
    return area


# Function to get the dimensions of the bounding box
def get_bounding_box_dimensions(shape):
    """
    Compute the dimensions of the bounding box of the shape.
    Returns (x_min, y_min, z_min, x_max, y_max, z_max).
    """
    bbox = Bnd_Box()
    brepbndlib.Add(shape, bbox)
    x_min, y_min, z_min, x_max, y_max, z_max = bbox.Get()
    return x_min, y_min, z_min, x_max, y_max, z_max

# Function to determine if the shape is a sheet metal part
def is_sheet_metal(shape, thickness_threshold=5.0):
    """
    Determine if the shape is a sheet metal part.
    A simplistic approach: if the maximum thickness is less than the threshold percentage of the smallest bounding box dimension.
    """
    # Compute the volume and total surface area
    props = GProp_GProps()
    brepgprop.VolumeProperties(shape, props)
    volume = props.Mass()
    brepgprop.SurfaceProperties(shape, props)
    surface_area = props.Mass()

    # Compute the bounding box dimensions
    x_min, y_min, z_min, x_max, y_max, z_max = get_bounding_box_dimensions(shape)
    dims = [x_max - x_min, y_max - y_min, z_max - z_min]
    min_dim = min(dims)

    # Estimate the thickness: Volume divided by surface area approximates the average thickness
    if surface_area == 0:
        return False  # Avoid division by zero
    average_thickness = volume / surface_area

    # Check if the average thickness is less than a threshold percentage of the minimum dimension
    threshold = (thickness_threshold / 100.0) * min_dim
    if average_thickness < threshold:
        return True
    else:
        return False


# Function to calculate the length of a TopoDS_Edge
def calculate_edge_length(edge):
    """
    Calculate the length of an edge.
    """
    props = GProp_GProps()
    brepgprop.LinearProperties(edge, props)
    length = props.Mass()
    return length

# Function to calculate the circumference of a hole
def calculate_hole_circumference(hole):
    """
    Calculate the circumference of a hole.
    """
    diameter = hole["diameter"]
    circumference = math.pi * diameter
    return circumference

# Function to calculate the total laser travel length
def calculate_total_laser_length(edges, holes_data, include_hole_depth=False):
    """
    Calculate the total laser travel length along edges and holes.

    Parameters:
    - shape: The TopoDS_Shape object representing the geometry.
    - holes_data: List of hole dictionaries.
    - include_hole_depth: Boolean indicating whether to include hole depth in the calculation.

    Returns:
    - total_length: Total laser travel length.
    """
    # Calculate total edge length
    total_edge_length = 0.0
    for index, edge in enumerate(edges, start=1):
        length = calculate_edge_length(edge)
        total_edge_length += length
        print(f"Edge {index} length: {length}")

    # Calculate total hole length
    total_hole_length = 0.0
    for index, hole in enumerate(holes_data, start=1):
        circumference = calculate_hole_circumference(hole)
        hole_length = circumference
        if include_hole_depth:
            # If the laser drills down the depth of the hole
            depth = hole["depth"]
            hole_length += depth
            print(f"Hole {index} at {hole['position']} circumference: {circumference}, depth: {depth}")
        else:
            print(f"Hole {index} at {hole['position']} circumference: {circumference}")
        total_hole_length += hole_length

    total_length = total_edge_length + total_hole_length
    print(f"Total edge length: {total_edge_length}")
    print(f"Total hole length: {total_hole_length}")
    print(f"Total laser travel length: {total_length}")

    return total_length


def count_cylindrical_surfaces_from_faces(faces):
    """
    Count the number of cylindrical surfaces in the list of faces.
    """
    count = 0
    for face in faces:
        # Create an adaptor for the face's surface
        adaptor = BRepAdaptor_Surface(face, True)
        # Get the type of the surface
        surf_type = adaptor.GetType()
        # Check if it is a cylindrical surface
        if surf_type == GeomAbs_Cylinder:
            count += 1
    return count

# Main function to process the shape
def process_shape(shape,edges,holes_data):
    # Sum of areas of all faces
    faces = get_faces(shape)
    total_area = 0.0
    for face in faces:
        area = get_face_area(face)
        total_area += area
    print(f"Total surface area: {total_area} square units")


    # Number of cylindrical surfaces
    num_cylinders = len(holes_data)
    print('------------number of holes', num_cylinders)

    num_bends = count_cylindrical_surfaces_from_faces(faces)
    num_bends = (num_bends-num_cylinders)/2
    print('------------------number of bends',num_bends)

    # Determine if it is a sheet metal part
    is_sheet = is_sheet_metal(shape)
    print(' -------------is sheeet', is_sheet)
    if is_sheet:
        thickness =2#= get_sheet_thickness(shape, angle_tolerance=5.0, distance_tolerance=1e-3)
        print('----------------thickens',thickness)
    # Dimensions of the bounding box
    x_min, y_min, z_min, x_max, y_max, z_max = get_bounding_box_dimensions(shape)

    print('bounding box', x_min, y_min, z_min, x_max, y_max, z_max)
    if is_sheet:
        print("The shape is considered a sheet metal part.")
    else:
        print("The shape is not considered a sheet metal part.")
    
    perimeter = 500#calculate_total_laser_length(edges, holes_data, include_hole_depth=False)
    print('-----------perimeters', perimeter)
    params = list()
    params = {'flat_area':1000,'perimeter':perimeter,'num_holes':num_cylinders,'box_dim':[x_max-x_min,y_max-y_min,z_max-z_min],'is_sheet':is_sheet,'area':total_area, 'num_bends':num_bends,'thickness':thickness}
    print(params)
    return params