# src/bend_analysis.py

from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.BRepExtrema import BRepExtrema_DistShapeShape
from math import isclose, acos, degrees
from face_operations import BendNode  # Moved BendNode to face_operations.py
import warnings
from math import acos, degrees

def detect_bends(faces, thickness, tolerance=1e-6):
    """
    Detects bends between faces by checking proximity and thickness.

    Args:
        faces: List of BendNode faces from the tree.
        thickness: Expected thickness of the sheet metal.
        tolerance: Tolerance for thickness comparison.

    Returns:
        list: List of tuples representing the bend relationships between nodes.
    """
    nodes = []
    # Create BendNode for each face and analyze its surface type and edges
    for face in faces:
        node = BendNode(face)
        node.analyze_surface_type()
        node.analyze_edges()
        nodes.append(node)
    
    # Now, check for adjacent face pairs that form a bend
    bends = []
    for i, node in enumerate(nodes):
        if node.processed:
            continue
        for j, other_node in enumerate(nodes):
            if i == j or other_node.processed:
                continue
            # Check if one face is flat and the other is cylindrical
            if node.surface_type == "Flat" and other_node.surface_type == "Cylindrical":
                dist = BRepExtrema_DistShapeShape(node.face, other_node.face).Value()
                if isclose(dist, thickness, rel_tol=tolerance):
                    bends.append((node, other_node))
                    node.children.append(other_node)
                    other_node.processed = True
                    print(f"Bend detected between face {i+1} and face {j+1}")
                    break
    return bends


def calculate_bend_angle(face1, face2):
    """
    Calculate the bend angle between two faces.
    
    Args:
        face1: The first face.
        face2: The second face.
    
    Returns:
        float: The bend angle in degrees or None if calculation fails.
    """
    # Extract surface normals from the faces
    surf1 = BRepAdaptor_Surface(face1)
    surf2 = BRepAdaptor_Surface(face2)

    # Ensure the surfaces are planar
    if surf1.GetType() != 0 or surf2.GetType() != 0:  # 0 represents a plane in BRepAdaptor_Surface
        import warnings
        warnings.warn("One or both of the faces are not planar. Bend angle calculation only works for planar surfaces.")
        return None

    normal1 = surf1.Plane().Axis().Direction()
    normal2 = surf2.Plane().Axis().Direction()

    # Compute the dot product between the two normal vectors
    dot_product = normal1.Dot(normal2)

    # Clamp the dot product to the valid range for acos
    dot_product = max(min(dot_product, 1.0), -1.0)

    # Calculate the angle between the normals
    angle_rad = acos(dot_product)
    angle_deg = degrees(angle_rad)

    return angle_deg
