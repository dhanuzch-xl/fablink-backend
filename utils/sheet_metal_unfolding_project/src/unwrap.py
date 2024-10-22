from OCC.Core.gp import gp_Dir, gp_Vec, gp_Pnt, gp_Trsf, gp_Ax1
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.gp import gp_XYZ
from OCC.Core.GProp import GProp_GProps
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Trsf, gp_Dir, gp_Ax1, gp_Quaternion
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
import math
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
from OCC.Core.BRepTools import breptools
from OCC.Core.GeomAbs import GeomAbs_Cylinder, GeomAbs_Plane
from OCC.Core.gp import gp_Pnt,gp_Pnt2d
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeFace
import math
from OCC.Core.BRepTools import breptools
from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeVertex, BRepBuilderAPI_Transform
from OCC.Core.BRepTools import breptools
from OCC.Core.GeomAbs import GeomAbs_BSplineSurface

def get_cylinder_axis_and_base(cylinder):
    """
    Extract the axis direction and the base position from the cylinder.
    """
    cylinder_axis = cylinder.Axis().Direction()
    base_point = cylinder.Position().Location()
    return cylinder_axis, base_point

def compute_direct_transformation_matrix(cylinder):
    """
    Compute the full direct transformation matrix (rotation + translation) to move the origin to the cylinder's position
    and align the axis with the actual cylinder axis.
    """
    # Step 1: Extract cylinder axis and base point (position)
    cylinder_axis, base_point = get_cylinder_axis_and_base(cylinder)

    # Step 2: Define Z-axis
    z_axis = gp_Dir(0, 0, 1)

    # Step 3: Compute the axis of rotation (cross product) and rotation angle
    rotation_axis = gp_Vec(cylinder_axis.Crossed(z_axis))
    rotation_angle = math.acos(cylinder_axis.Dot(z_axis))

    # Step 4: Create the translation and rotation transformations
    transformation_trsf = gp_Trsf()

    # Correctly set translation from origin to base point
    translation_vec = gp_Vec(gp_Pnt(0, 0, 0), base_point)
    transformation_trsf.SetTranslation(translation_vec)

    # Create rotation transformation if necessary
    if rotation_axis.Magnitude() > 1e-6:
        rotation_trsf = gp_Trsf()
        rotation_trsf.SetRotation(gp_Ax1(base_point, gp_Dir(rotation_axis)), rotation_angle)
        # Combine rotation and translation
        transformation_trsf.Multiply(rotation_trsf)

    return transformation_trsf


def uv_to_3d_point(u, v, radius):
    """
    Convert UV coordinates to a 3D point on the unwrapped cylinder.
    """
    x = radius * u
    y = v
    z = 0  # Since this is unwrapped on a flat plane, z-coordinate is 0.
    return gp_Pnt(x, y, z)


def compute_uv_points(u_min, u_max, v_min, v_max, r, target_axis):
    """
    Compute four UV coordinates for a cylindrical surface, rotate them to align with an arbitrary axis.
    """
    # Step 1: Compute UV coordinates for the four corners (in local cylindrical coordinates)
    p1 = gp_Pnt(v_min, r * math.cos(u_min), r * math.sin(u_min))  # Bottom-left
    p2 = gp_Pnt(v_min, r * math.cos(u_max), r * math.sin(u_max))  # Bottom-right
    p3 = gp_Pnt(v_max, r * math.cos(u_max), r * math.sin(u_max))  # Top-right
    p4 = gp_Pnt(v_max, r * math.cos(u_min), r * math.sin(u_min))  # Top-left

    # Compute the rotation axis and angle (rotation from X-axis to the target axis)
    original_axis = gp_Vec(1, 0, 0)  # Cylinder initially along X-axis
    target_axis_vec = gp_Vec(target_axis.X(), target_axis.Y(), target_axis.Z())  # Convert target_axis to gp_Vec

    # Calculate the cross product to find the rotation axis
    rotation_axis = original_axis.Crossed(target_axis_vec)

    # Check if the vectors are collinear (i.e., the magnitude of the cross product is near zero)
    if rotation_axis.Magnitude() > 1e-6:
        # If not aligned, perform the rotation
        rotation_axis = rotation_axis.Normalized()
        rotation_angle = math.acos(original_axis.Dot(target_axis_vec.Normalized()))

        # Apply the rotation transformation
        height_center = (v_min + v_max) / 2
        trsf = gp_Trsf()
        trsf.SetRotation(gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(rotation_axis)), rotation_angle)

        # Rotate all four points
        p1_rotated = p1.Transformed(trsf)
        p2_rotated = p2.Transformed(trsf)
        p3_rotated = p3.Transformed(trsf)
        p4_rotated = p4.Transformed(trsf)
    else:
        # If the vectors are collinear, no rotation is needed
        p1_rotated, p2_rotated, p3_rotated, p4_rotated = p1, p2, p3, p4

    return p1_rotated, p2_rotated, p3_rotated, p4_rotated


def unwrap_cylindrical_face(node):
    # Step 1: Identify the surface type
    surface_adaptor = BRepAdaptor_Surface(node.face)
    surface_type = surface_adaptor.GetType()

    if surface_type == GeomAbs_Cylinder:
        parent_node = node
        if parent_node and 'before_unfld' in parent_node.vertexDict:
            print('Unwrapping cylindrical surface...')

            common_vertices = parent_node.vertexDict['before_unfld']
            if len(common_vertices) >= 2:
                # Step 2: Extract cylindrical parameters (radius, height, etc.)
                cylinder = surface_adaptor.Cylinder()
                radius = cylinder.Radius()
                
                # Step 3: Get the parametric bounds of the cylindrical face
                u_min, u_max, v_min, v_max = breptools.UVBounds(node.face)
                
                # Compute rotated points based on UV parameters
                p1, p2, p3, p4 = compute_uv_points(u_min, u_max, v_min, v_max, radius, cylinder.Axis().Direction())

                # Convert common vertices to gp_Pnt objects if they are not already
                (parent_vertex1, child_vertex1) = common_vertices[0]
                (parent_vertex2, child_vertex2) = common_vertices[1]
                common_vertex1_pnt = gp_Pnt(*child_vertex1)
                common_vertex2_pnt = gp_Pnt(*child_vertex2)

                  # Translate each point to its respective common vertex
                # Using p1 -> common_vertex1, p2 -> common_vertex2, and so on
                p1_final = gp_Pnt(p1.X() + common_vertex1_pnt.X(), p1.Y() + common_vertex1_pnt.Y(), p1.Z() + common_vertex1_pnt.Z())
                p2_final = gp_Pnt(p2.X() + common_vertex2_pnt.X(), p2.Y() + common_vertex2_pnt.Y(), p2.Z() + common_vertex2_pnt.Z())
                p3_final = gp_Pnt(p3.X() + common_vertex2_pnt.X(), p3.Y() + common_vertex2_pnt.Y(), p3.Z() + common_vertex2_pnt.Z())
                p4_final = gp_Pnt(p4.X() + common_vertex1_pnt.X(), p4.Y() + common_vertex1_pnt.Y(), p4.Z() + common_vertex1_pnt.Z())

                # Print the translated points
                print(f"p1_final: X = {p1_final.X()}, Y = {p1_final.Y()}, Z = {p1_final.Z()}")
                print(f"p2_final: X = {p2_final.X()}, Y = {p2_final.Y()}, Z = {p2_final.Z()}")
                print(f"p3_final: X = {p3_final.X()}, Y = {p3_final.Y()}, Z = {p3_final.Z()}")
                print(f"p4_final: X = {p4_final.X()}, Y = {p4_final.Y()}, Z = {p4_final.Z()}")

                # Step 4: Create edges from the final points
                edge1 = BRepBuilderAPI_MakeEdge(p1_final, p2_final).Edge()
                edge2 = BRepBuilderAPI_MakeEdge(p2_final, p3_final).Edge()
                edge3 = BRepBuilderAPI_MakeEdge(p3_final, p4_final).Edge()
                edge4 = BRepBuilderAPI_MakeEdge(p4_final, p1_final).Edge()

                # Step 5: Create the wire (closed loop of edges) for the planar face
                wire = BRepBuilderAPI_MakeWire(edge1, edge2, edge3, edge4).Wire()

                # Step 6: Create the planar face from the wire
                planar_face = BRepBuilderAPI_MakeFace(wire).Face()

                # Step 7: Replace the cylindrical face with the unwrapped planar face
                node.face = planar_face
                node.surface_type = "Planar"  # Mark the node as planar
    
    # Recursively apply the same operation to all child nodes
    for child in node.children:
        unwrap_cylindrical_face(child)


def unwrap_bspline_face(node):
    """
    Unwrap a BSpline face into a flat face, calculate the transformation (translation + rotation) 
    between the centroid of the BSpline face and the unwrapped planar face, and apply that transformation.
    
    Args:
        node (FaceNode): The node containing the BSpline face to unwrap.
    
    Returns:
        None: The function modifies the node's face directly.
    """
    # Step 1: Identify the surface type
    surface_adaptor = BRepAdaptor_Surface(node.face)
    surface_type = surface_adaptor.GetType()

    if surface_type == GeomAbs_BSplineSurface:
        print('Unwrapping BSpline surface...')
        
        # Step 2: Extract the BSpline surface and its properties
        bspline_surface = surface_adaptor.Surface().BSplineSurface()
        u_degree = bspline_surface.UDegree()
        v_degree = bspline_surface.VDegree()
        control_points = bspline_surface.Poles()
        u_knots = bspline_surface.UKnots()
        v_knots = bspline_surface.VKnots()

        # Step 3: Get the parametric bounds of the BSpline surface
        u_min, u_max, v_min, v_max = breptools.UVBounds(node.face)

        # Step 4: Generate unwrapped points in 2D (flatten in parametric space)
        points_2d = []
        for u in u_knots:
            for v in v_knots:
                pnt_3d = bspline_surface.Value(u, v)  # Get 3D point on surface
                points_2d.append(gp_Pnt2d(u, v))  # Flattened in U, V space

        # Step 5: Create edges for the unwrapped BSpline face (you might need to interpolate between points)
        edges = []
        for i in range(len(points_2d) - 1):
            p1 = gp_Pnt(points_2d[i].X(), points_2d[i].Y(), v_min)  # Bottom-left
            p2 = gp_Pnt(points_2d[i + 1].X(), points_2d[i + 1].Y(), v_min)  # Bottom-right
            edge = BRepBuilderAPI_MakeEdge(p1, p2).Edge()
            edges.append(edge)

        # Step 6: Create the wire (closed loop of edges) for the planar face
        wire = BRepBuilderAPI_MakeWire(*edges).Wire()

        # Step 7: Create the planar face from the wire
        planar_face = BRepBuilderAPI_MakeFace(wire).Face()

        # Step 8: Calculate centroid and normal of planar face (similarly to your cylindrical case)
        props = GProp_GProps()
        brepgprop.SurfaceProperties(planar_face, props)
        planar_centroid = props.CentreOfMass()

        # Step 9: Calculate the rotation and translation transformations (if needed)
        # For BSpline surfaces, rotation might not be as straightforward as cylindrical, so you can simplify
        # to a translation only if necessary or apply a more complex surface alignment technique.

        # Step 10: Replace the BSpline face with the transformed planar face
        node.face = planar_face
        node.surface_type = "Planar"  # Mark the node as planar

    # Recursively apply the same operation to all child nodes
    for child in node.children:
        unwrap_bspline_face(child)


