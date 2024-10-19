import sys
import math
from OCC.Core.TopoDS import topods, TopoDS_Shape, TopoDS_Face
from OCC.Core.TopAbs import TopAbs_FACE, TopAbs_EDGE
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.GeomAbs import GeomAbs_Cylinder, GeomAbs_Plane
from OCC.Core.BRep import BRep_Tool_Surface
from OCC.Core.BRepBndLib import brepbndlib_Add
from OCC.Core.BRepGProp import brepgprop_SurfaceProperties, brepgprop_VolumeProperties, brepgprop_LinearProperties
from OCC.Core.GProp import GProp_GProps
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.BRepTools import breptools_Read
from OCC.Core.gp import gp_Pnt, gp_Dir
from OCC.Extend.TopologyUtils import TopologyExplorer
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.BRepExtrema import BRepExtrema_DistShapeShape

from OCC.Core.gp import gp_Dir
import math


# Function to get the dimensions of the bounding box
def get_bounding_box_dimensions(shape):
    """
    Compute the dimensions of the bounding box of the shape.
    Returns (x_min, y_min, z_min, x_max, y_max, z_max).
    """
    bbox = Bnd_Box()
    brepbndlib_Add(shape, bbox)
    x_min, y_min, z_min, x_max, y_max, z_max = bbox.Get()
    return x_min, y_min, z_min, x_max, y_max, z_max

# Function to determine if the shape is a sheet metal part
def is_sheet_metal(shape, thickness_threshold=5.0):
    """
    Determine if the shape is a sheet metal part.
    A simplistic approach: if the average thickness is less than the threshold percentage of the smallest bounding box dimension.
    """
    # Compute the volume and total surface area
    props = GProp_GProps()
    brepgprop_VolumeProperties(shape, props)
    volume = props.Mass()
    brepgprop_SurfaceProperties(shape, props)
    surface_area = props.Mass()

    # Compute the bounding box dimensions
    x_min, y_min, z_min, x_max, y_max, z_max = get_bounding_box_dimensions(shape)
    dims = [x_max - x_min, y_max - y_min, z_max - z_min]
    min_dim = min(dims)

    # Estimate the average thickness: Volume divided by surface area
    if surface_area == 0:
        return False  # Avoid division by zero
    average_thickness = volume / surface_area

    # Check if the average thickness is less than a threshold percentage of the minimum dimension
    threshold = (thickness_threshold / 100.0) * min_dim
    if average_thickness < threshold:
        return True
    else:
        return False

# Function to get the normal of a face
def get_face_normal(face):
    """
    Get the normal vector of a face.
    Returns a gp_Dir object representing the normal vector.
    """
    from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
    from OCC.Core.GeomAbs import GeomAbs_Plane
    from OCC.Core.GeomLProp import GeomLProp_SLProps

    # Create an adaptor for the face
    surf_adaptor = BRepAdaptor_Surface(face)
    surf_type = surf_adaptor.GetType()

    if surf_type == GeomAbs_Plane:
        # For planar surfaces, get the plane and normal
        plane = surf_adaptor.Plane()
        normal = plane.Axis().Direction()
        return normal
    else:
        # For non-planar surfaces, compute the normal at a point
        u_min, u_max, v_min, v_max = surf_adaptor.FirstUParameter(), surf_adaptor.LastUParameter(), surf_adaptor.FirstVParameter(), surf_adaptor.LastVParameter()
        u_mid = (u_min + u_max) / 2
        v_mid = (v_min + v_max) / 2

        props = GeomLProp_SLProps(surf_adaptor.Surface().GetHandle(), u_mid, v_mid, 1, 0.01)
        if props.IsNormalDefined():
            normal_vec = props.Normal()
            return normal_vec
        else:
            return None

# Function to check if two faces are adjacent
def are_faces_adjacent(face1, face2):
    """
    Check if two faces share an edge (i.e., they are adjacent).
    Returns True if they share an edge, False otherwise.
    """
    from OCC.Core.TopExp import TopExp_Explorer
    from OCC.Core.TopAbs import TopAbs_EDGE

    # Get the edges of face1
    edges1 = set()
    exp1 = TopExp_Explorer(face1, TopAbs_EDGE)
    while exp1.More():
        edge = exp1.Current()
        edges1.add(edge.__hash__())
        exp1.Next()

    # Get the edges of face2
    edges2 = set()
    exp2 = TopExp_Explorer(face2, TopAbs_EDGE)
    while exp2.More():
        edge = exp2.Current()
        edges2.add(edge.__hash__())
        exp2.Next()

    # Check for shared edges
    shared_edges = edges1.intersection(edges2)
    return len(shared_edges) > 0

# Function to estimate the sheet thickness
def get_sheet_thickness(shape, angle_tolerance=5.0, distance_tolerance=1e-3):
    """
    Estimate the sheet thickness of a sheet metal part.

    Parameters:
    - shape: The TopoDS_Shape object representing the part.
    - angle_tolerance: The angle tolerance in degrees to consider faces as parallel.
    - distance_tolerance: The minimal distance to consider (to avoid numerical issues).

    Returns:
    - thickness: The estimated sheet thickness.
    """

    faces = [face for face in TopologyExplorer(shape).faces()]
    num_faces = len(faces)
    angle_tolerance_rad = math.radians(angle_tolerance)

    thicknesses = []

    for i in range(num_faces):
        face1 = faces[i]
        normal1 = get_face_normal(face1)
        if normal1 is None:
            continue

        for j in range(i+1, num_faces):
            face2 = faces[j]
            if are_faces_adjacent(face1, face2):
                continue

            normal2 = get_face_normal(face2)
            if normal2 is None:
                continue

            # Compute angle between normals
            angle = normal1.AngleWithRef(normal2, gp_Dir(0, 0, 1))
            angle = min(angle, math.pi - angle)  # Ensure angle is between 0 and pi/2

            if angle <= angle_tolerance_rad:
                # Faces are approximately parallel
                # Compute minimal distance between the faces
                dist_shape_shape = BRepExtrema_DistShapeShape(face1, face2)
                dist_shape_shape.Perform()
                if dist_shape_shape.IsDone() and dist_shape_shape.Value() > distance_tolerance:
                    distance = dist_shape_shape.Value()
                    thicknesses.append(distance)

    if thicknesses:
        estimated_thickness = min(thicknesses)
        return estimated_thickness
    else:
        return None  # Unable to estimate thickness
