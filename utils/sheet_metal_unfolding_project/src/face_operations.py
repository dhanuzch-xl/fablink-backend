# face_operations.py

from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.BRepExtrema import BRepExtrema_DistShapeShape
from OCC.Core.GProp import GProp_GProps
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.gp import gp_Trsf
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_FACE, TopAbs_EDGE
from OCC.Core.TopoDS import topods
from math import isclose
import math

# Centralize the BendNode class here for consistent use across the project
class BendNode:
    """
    Represents a node in the sheet metal structure for bend detection and analysis.
    Each node corresponds to a face or pair of faces, representing a bend.
    """
    def __init__(self, face):
        self.face = face
        self.edges = []  # Edges connected to the face
        self.surface_type = None  # Planar, Cylindrical
        self.children = []  # Faces related to this face (bend relationships)
        self.processed = False  # Whether this face has been processed
        self.parent = None  # Parent node
        self.bend_angle = None  # Angle between this face and its parent (if applicable)
        self.bend_type = None  # Type of connection: flat, cylindrical, or other

    def analyze_surface_type(self):
        """
        Determines whether the face is planar or cylindrical.
        """
        surf = BRepAdaptor_Surface(self.face)
        surf_type = surf.GetType()

        if surf_type == 0:  # Flat face (plane)
            self.surface_type = "Flat"
        elif surf_type == 1:  # Cylindrical face (typically a bend)
            self.surface_type = "Cylindrical"

    def analyze_edges(self):
        """
        Analyzes the edges of the face and stores them in the node.
        """
        exp = TopExp_Explorer(self.face, TopAbs_EDGE)
        while exp.More():
            edge = topods.Edge(exp.Current())
            self.edges.append(edge)
            exp.Next()

    def add_child(self, child_node, bend_angle=None, bend_type=None):
        """
        Adds a child node to this node, establishing the parent-child relationship.
        """
        self.children.append(child_node)
        child_node.parent = self
        child_node.bend_angle = bend_angle
        child_node.bend_type = bend_type

# ---------------------------------------------------------------
# Existing face extraction and transformation functions
def extract_faces(shape):
    """
    Extract all faces from the shape and classify them as flat or curved.
    """
    explorer = TopExp_Explorer(shape, TopAbs_FACE)
    faces = []
    while explorer.More():
        face = topods.Face(explorer.Current())
        faces.append(face)
        explorer.Next()
    return faces

def is_flat_face(face):
    """
    Determines if a given face is flat by checking if its surface is a plane.
    """
    surface = BRepAdaptor_Surface(face)
    return surface.GetType() == 0  # 0 represents a plane

def rotate_face(face, axis, angle_deg, center):
    """
    Rotates the given face around an axis by a specified angle.
    """
    angle_rad = math.radians(angle_deg)
    transformation = gp_Trsf()
    transformation.SetRotation(axis, angle_rad)
    rotated_face = BRepBuilderAPI_Transform(face, transformation).Shape()
    return rotated_face

def translate_face(face, translation_vec):
    """
    Translates a face by a given vector.
    """
    transformation = gp_Trsf()
    transformation.SetTranslation(translation_vec)
    translated_face = BRepBuilderAPI_Transform(face, transformation).Shape()
    return translated_face

def filter_faces_by_thickness(faces, thickness, tolerance=1e-6, min_area=300):
    """
    Filters the faces based on a specified thickness.
    """
    face_data = []
    for face in faces:
        surf = BRepAdaptor_Surface(face)
        if surf.GetType() == 0:  # Only consider flat faces
            props = GProp_GProps()
            brepgprop.SurfaceProperties(face, props)
            area = props.Mass()
            if area >= min_area:
                face_data.append({
                    "face": face,
                    "normal": surf.Plane().Axis().Direction(),
                    "area": area,
                    "processed": False
                })

    plates = []
    for i, data in enumerate(face_data):
        if data["processed"]:
            continue
        for j, other_data in enumerate(face_data):
            if i == j or other_data["processed"]:
                continue
            if data["normal"].IsParallel(other_data["normal"], tolerance):
                dist_shape_shape = BRepExtrema_DistShapeShape(data["face"], other_data["face"])
                face_thickness = dist_shape_shape.Value()
                if isclose(face_thickness, thickness, rel_tol=tolerance):
                    plates.append(data["face"])
                    data["processed"] = other_data["processed"] = True
                    print(f"Found face pair with thickness {thickness}: Faces {i+1} and {j+1}, Area: {data['area']}")
                    break
    return plates if plates else print(f"No plates found with the specified thickness {thickness}.")
