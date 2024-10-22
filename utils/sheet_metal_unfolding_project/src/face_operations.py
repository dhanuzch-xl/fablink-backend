# face_operations.py

from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.BRepExtrema import BRepExtrema_DistShapeShape
from OCC.Core.GProp import GProp_GProps
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.gp import gp_Trsf
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_FACE
from OCC.Core.TopoDS import topods
from OCC.Core.GeomAbs import GeomAbs_Cylinder, GeomAbs_Plane,GeomAbs_Cone,GeomAbs_Sphere
from OCC.Core.GeomAbs import GeomAbs_Torus,GeomAbs_BSplineSurface
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Ax1, gp_Ax2, gp_Ax3, gp_Trsf, gp_Dir
from OCC.Core.BRepTools import breptools

from math import isclose
import math

num_samples = 10
      
# face extraction and transformation functions
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


def get_face_normal(face):
    """
    Get the normal vector of the surface at a given parametric point (U, V).
    This works for different surface types (planes, cylinders, cones, spheres, etc.).
    
    Args:
        face (TopoDS_Face): The face whose normal is to be computed.
        u (float): Parametric U value (for surfaces that require sampling, default is 0.5).
        v (float): Parametric V value (for surfaces that require sampling, default is 0.5).
    
    Returns:
        gp_Dir: The normal direction of the surface at the specified point, or None if not applicable.
    """
    surf = BRepAdaptor_Surface(face)
    surf_type = surf.GetType()
    
    
    if surf_type == GeomAbs_Plane:
        # Plane surface: return the normal vector from the plane's axis
        gp_pln = surf.Plane()
        return gp_pln.Axis().Direction()

    elif surf_type == GeomAbs_Cylinder:
        # Cylinder surface: normal can be computed from the axis at a given point
        gp_cyl = surf.Cylinder()
        return gp_cyl.Axis().Direction()

    elif surf_type == GeomAbs_Cone:
        # Cone surface: normal from the cone's axis
        gp_cone = surf.Cone()
        return gp_cone.Axis().Direction()

    elif surf_type == GeomAbs_Sphere:
        # Spherical surface: normal at any point is the vector from the center to the point on the surface
        gp_sphere = surf.Sphere()
        center = gp_sphere.Location()  # Center of the sphere
        u_min, u_max, v_min, v_max = breptools.UVBounds(face)  # Get parametric bounds for U and V
        point = gp_Pnt()
        surf.D0(u_min, v_min, point)  # Get the point at parametric (U, V)
        normal_vec = gp_Vec(center, point).Normalized()
        return gp_Dir(normal_vec)

    elif surf_type == GeomAbs_Torus:
        # Torus surface: return the axis of the torus
        gp_torus = surf.Torus()
        return gp_torus.Axis().Direction()

    elif surf_type == GeomAbs_BSplineSurface:
        # BSpline surface: normal must be calculated from the geometry at a given point (U, V)
        print("B-Spline surface: calculating average normal wuth 10 samples")
        return calculate_average_normal(face)

    else:
        try:
            # For revolved surfaces
            axis = surf.AxeOfRevolution()
            return axis.Direction()
        except AttributeError:
            # Handle non-revolution surfaces (like general cases or B-Splines)
            print("No axis of revolution available for this surface type.")
            return None

def calculate_average_normal(face, fixed_samples=None, num_samples=num_samples):
    """
    Calculate the average normal for a surface (planar, cylindrical, or BSpline) by sampling points 
    across the surface and averaging their normals. If fixed sampling points are provided, 
    the function will use them.
    
    Args:
        face (TopoDS_Face): The face to extract the surface and calculate the average normal.
        fixed_samples (List[Tuple[float, float]]): Optional list of fixed (U, V) sample points for consistency.
        num_samples (int): Number of samples to take in each parametric direction (U, V) if no fixed samples provided.
    
    Returns:
        gp_Dir: The average normal direction for the surface.
    """
    surface_adaptor = BRepAdaptor_Surface(face)
    u_min, u_max, v_min, v_max = breptools.UVBounds(face)

    total_normal = gp_Vec(0, 0, 0)  # Initialize with a zero vector

    if fixed_samples is None:
        fixed_samples = []

        # Step 1: Directly generate sample points in the U, V parametric space
        u_step = (u_max - u_min) / (num_samples - 1)
        v_step = (v_max - v_min) / (num_samples - 1)

        for i in range(num_samples):
            for j in range(num_samples):
                # Directly use parametric bounds without normalization
                u = u_min + i * u_step
                v = v_min + j * v_step
                fixed_samples.append((u, v))

    # Step 2: Sample points across the surface at the specified parametric points
    for (u, v) in fixed_samples:
        if u_min <= u <= u_max and v_min <= v <= v_max:
            point = gp_Pnt()
            tangent_u = gp_Vec()  # Tangent vector along U
            tangent_v = gp_Vec()  # Tangent vector along V

            # Get the point and normal at this (U, V) parameter on the surface
            surface_adaptor.D1(u, v, point, tangent_u, tangent_v)

            # Calculate the normal by taking the cross product of the tangent vectors
            normal_vec = tangent_u.Crossed(tangent_v).Normalized()

            # Convert gp_Dir (direction) to gp_Vec to accumulate normals
            normal_as_vec = gp_Vec(normal_vec.X(), normal_vec.Y(), normal_vec.Z())

            # Accumulate the normal as a vector
            total_normal.Add(normal_as_vec)

    # Step 3: Compute the average normal by normalizing the accumulated vector
    average_normal = gp_Dir(total_normal)

    return average_normal

def sample_points_on_face(face, num_samples_u=5, num_samples_v=5):
    """
    Sample points across a surface (like a BSpline or planar surface) by sampling the parametric space.
    
    Args:
        face (TopoDS_Face): The face to sample points from.
        num_samples_u (int): Number of samples in the U direction.
        num_samples_v (int): Number of samples in the V direction.

    Returns:
        list: A list of sampled gp_Pnt points from the surface.
    """
    surface_adaptor = BRepAdaptor_Surface(face)
    u_min, u_max, v_min, v_max = breptools.UVBounds(face)
    points = []

    # Sample points across the U-V parametric space
    u_step = (u_max - u_min) / (num_samples_u - 1)
    v_step = (v_max - v_min) / (num_samples_v - 1)

    for i in range(num_samples_u):
        for j in range(num_samples_v):
            u = u_min + i * u_step
            v = v_min + j * v_step
            pt = gp_Pnt()
            surface_adaptor.D0(u, v, pt)  # Get point at (U, V)
            points.append(pt)

    return points


def find_faces_with_thickness(all_faces, thickness, min_area=300, tolerance=1e-6):
    """
    Args:
        thickness (float): Thickness to search for.
        min_area (float): Minimum area of faces to consider.
        tolerance (float): Tolerance for comparing thicknesses.

    Returns:
        list: List of faces with specified thickness.
    """
    faces = []
    for face in all_faces:
    # while exp.More():
    #     face = topods.Face(exp.Current())
        #print(len(faces))
        if not face.IsNull():
            normal = get_face_normal(face)
            if normal:
                # Calculate the face area
                props = GProp_GProps()
                brepgprop.SurfaceProperties(face, props)
                area = props.Mass()
                if area >= min_area:
                    surf = BRepAdaptor_Surface(face)
                    surf_type = surf.GetType()
                    faces.append({
                        "face": face,
                        "type": surf_type,
                        "normal": normal,
                        "area": area,
                        "processed": False
                    })
        else:
            print('face is null')    
    # Find plates with the specified thickness
    plates = []
    for i, data in enumerate(faces):
        if data["processed"]:
            continue
        for j, other_data in enumerate(faces):
            if i == j or other_data["processed"]:
                continue
            if data["normal"].IsParallel(other_data["normal"], tolerance):
                if data["type"] == 0:
                    dist_shape_shape = BRepExtrema_DistShapeShape(data["face"], other_data["face"])
                    face_thickness = dist_shape_shape.Value()
                else:
                    #Sample points from both faces
                    points1 = sample_points_on_face(data["face"], num_samples_u=num_samples, num_samples_v=num_samples)
                    points2 = sample_points_on_face(other_data["face"], num_samples_u=num_samples, num_samples_v=num_samples)

                    # Calculate the average distance between sampled points
                    distances = [pt1.Distance(pt2) for pt1, pt2 in zip(points1, points2)]
                    face_thickness = sum(distances) / len(distances)
                if isclose(face_thickness, thickness, rel_tol=tolerance):
                    #ToDo:find_top_face
                    plates.append((data["face"],other_data["face"]))
                    data["processed"] = other_data["processed"] = True
                    break

    if not plates:
        print("No plates found with the specified thickness.")
    return plates

def get_face_area(face):
    """
    Compute and return the area of a given face.
    """
    props = GProp_GProps()
    brepgprop.SurfaceProperties(face, props)
    area = props.Mass()
    return area
