from OCC.Core.gp import (
    gp_Pnt, gp_Vec, gp_Dir, gp_Ax1, gp_Ax3, gp_Trsf
)
from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepBuilderAPI import (
    BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire,
    BRepBuilderAPI_MakeFace, BRepBuilderAPI_Transform, BRepBuilderAPI_Sewing
)
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.TopAbs import TopAbs_FACE, TopAbs_EDGE, TopAbs_VERTEX
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopoDS import topods, TopoDS_Face, TopoDS_Edge
from OCC.Core.ShapeAnalysis import ShapeAnalysis_Surface
import math
from OCC.Core.GeomAbs import GeomAbs_Cylinder, GeomAbs_Plane,GeomAbs_Cone,GeomAbs_Sphere

def get_edge_vertices(edge):
    """Extract the vertices of an edge."""
    vertices = []
    explorer = TopExp_Explorer(edge, TopAbs_VERTEX)
    while explorer.More():
        vertex = topods.Vertex(explorer.Current())
        point = BRep_Tool.Pnt(vertex)
        vertices.append(point)
        explorer.Next()
    return vertices

def get_shared_edge(face1, face2):
    """Find the shared edge between two faces."""
    edges1 = []
    explorer1 = TopExp_Explorer(face1, TopAbs_EDGE)
    while explorer1.More():
        edge = topods.Edge(explorer1.Current())
        edges1.append(edge)
        explorer1.Next()

    edges2 = []
    explorer2 = TopExp_Explorer(face2, TopAbs_EDGE)
    while explorer2.More():
        edge = topods.Edge(explorer2.Current())
        edges2.append(edge)
        explorer2.Next()

    for edge1 in edges1:
        for edge2 in edges2:
            if edge1.IsSame(edge2):
                return edge1
    return None

def get_cylinder_parameters(cylindrical_face):
    """Extract the cylinder's parameters: radius, axis, and bend angle."""
    surface_adaptor = BRepAdaptor_Surface(cylindrical_face)
    if surface_adaptor.GetType() != GeomAbs_Cylinder:
        raise ValueError("Provided face is not cylindrical.")

    cylinder = surface_adaptor.Cylinder()
    radius = cylinder.Radius()
    axis = cylinder.Axis()
    axis_dir = axis.Direction()

    # Get parametric bounds to compute bend angle
    u_min, u_max, v_min, v_max = surface_adaptor.FirstUParameter(), surface_adaptor.LastUParameter(), surface_adaptor.FirstVParameter(), surface_adaptor.LastVParameter()
    bend_angle = u_max - u_min  # In radians

    # Height along the cylinder's axis
    height = v_max - v_min

    return radius, axis, axis_dir, bend_angle, height

def flatten_and_position_plate2(plate2_face, shared_edge, bend_angle, unwrapped_length):
    """Flatten Plate 2 and translate it to align with the unwrapped cylindrical face."""
    # Get the axis of rotation (shared edge)
    edge_vertices = get_edge_vertices(shared_edge)
    if len(edge_vertices) < 2:
        raise ValueError("Shared edge must have two vertices.")
    rotation_axis = gp_Ax1(edge_vertices[0], gp_Dir(gp_Vec(edge_vertices[0], edge_vertices[1])))

    # Create the rotation transformation
    rotation_trsf = gp_Trsf()
    rotation_trsf.SetRotation(rotation_axis, -bend_angle)  # Negative to flatten

    # Apply the rotation to Plate 2
    rotated_plate2 = BRepBuilderAPI_Transform(plate2_face, rotation_trsf, True).Shape()

    # Create the translation transformation along the X-axis by unwrapped_length
    translation_vec = gp_Vec(unwrapped_length, 0, 0)
    translation_trsf = gp_Trsf()
    translation_trsf.SetTranslation(translation_vec)

    # Apply the translation to the rotated Plate 2
    transformed_plate2 = BRepBuilderAPI_Transform(rotated_plate2, translation_trsf, True).Shape()

    return transformed_plate2

def create_unwrapped_cylindrical_face(unwrapped_length, height):
    """Create the unwrapped cylindrical face as a flat rectangle."""
    # Define points in the XZ plane (since Plate 1 is in XZ plane)
    p1 = gp_Pnt(0, 0, 0)
    p2 = gp_Pnt(unwrapped_length, 0, 0)
    p3 = gp_Pnt(unwrapped_length, 0, height)
    p4 = gp_Pnt(0, 0, height)

    # Create edges
    edge1 = BRepBuilderAPI_MakeEdge(p1, p2).Edge()
    edge2 = BRepBuilderAPI_MakeEdge(p2, p3).Edge()
    edge3 = BRepBuilderAPI_MakeEdge(p3, p4).Edge()
    edge4 = BRepBuilderAPI_MakeEdge(p4, p1).Edge()

    # Create wire
    wire_maker = BRepBuilderAPI_MakeWire()
    wire_maker.Add(edge1)
    wire_maker.Add(edge2)
    wire_maker.Add(edge3)
    wire_maker.Add(edge4)
    wire = wire_maker.Wire()

    # Create the planar face
    flat_face = BRepBuilderAPI_MakeFace(wire).Face()

    return flat_face

def assemble_flattened_plate(plate1_face, unwrapped_cyl_face, transformed_plate2_face):
    """Assemble the flattened components into a single shape."""
    sewing = BRepBuilderAPI_Sewing()
    sewing.Add(plate1_face)
    sewing.Add(unwrapped_cyl_face)
    sewing.Add(transformed_plate2_face)
    sewing.Perform()

    flattened_plate = sewing.SewedShape()
    return flattened_plate

def flatten_bent_plate(plate1, bend, plate2):
    """Main function to flatten the bent plate."""
    # Ensure plate1 is in the XZ plane
    # Plate 1 is assumed to be already in the XZ plane

    # Get the shared edges
    plate1_face = plate1.face
    cylindrical_face = bend.face
    plate2_face = plate2.face

    edge1 = bend.vertexDict['after_unfld']
    edge2 = plate2.vertexDict['after_unfld'] 
    p1 = gp_Pnt(edge1[0][0],edge1[0][1],edge1[0][2])
    p2 = gp_Pnt(edge1[1][0],edge1[1][1],edge1[1][2])
    p4 = gp_Pnt(edge2[0][0],edge2[0][1],edge2[0][2])
    p3 = gp_Pnt(edge2[1][0],edge2[1][1],edge2[1][2]) 

    shared_edge1 = BRepBuilderAPI_MakeEdge(p1, p2).Edge()
    shared_edge2 = BRepBuilderAPI_MakeEdge(p3, p4).Edge()

    # shared_edge1 = get_shared_edge(plate1_face, cylindrical_face)
    # shared_edge2 = get_shared_edge(cylindrical_face, plate2_face)

    if shared_edge1 is None or shared_edge2 is None:
        raise ValueError("Shared edges between faces could not be found.")

    # Get cylinder parameters
    radius, axis, axis_dir, bend_angle, height = get_cylinder_parameters(cylindrical_face)

    # Calculate unwrapped length
    unwrapped_length = bend_angle * radius

    # Unwrap the cylindrical face
    unwrapped_cyl_face = create_unwrapped_cylindrical_face(unwrapped_length, height)

    # Flatten and position Plate 2
    transformed_plate2_face = flatten_and_position_plate2(plate2_face, shared_edge2, bend_angle, unwrapped_length)

    # Assemble the flattened components
    flattened_plate = assemble_flattened_plate(plate1_face, unwrapped_cyl_face, transformed_plate2_face)
    bend.face = unwrapped_cyl_face
    plate2.face = transformed_plate2_face
    return flattened_plate

# Example usage:

# Assuming plate1, cylinder, and plate2 are provided as TopoDS_Face objects

# flattened_plate = flatten_bent_plate(plate1, cylinder, plate2)

# Now, flattened_plate contains the assembled flattened shape
