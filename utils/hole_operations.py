from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCylinder
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCC.Core.gp import gp_Ax2, gp_Dir, gp_Pnt
from OCC.Extend.DataExchange import write_step_file, read_step_file_with_names_colors
from OCC.Extend.TopologyUtils import TopologyExplorer
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.GeomAbs import GeomAbs_Cylinder
from OCC.Core.gp import gp_Pnt
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepBndLib import brepbndlib
from OCC.Core.TopoDS import TopoDS_Face

# Function to recognize and extract all hole faces in batch mode
def recognize_hole_faces(step_file):
    big_shp_dict = read_step_file_with_names_colors(step_file)
    shapes = big_shp_dict.keys()

    holes = []
    for shape in shapes:
        for face in TopologyExplorer(shape).faces():
            hole_data = recognize_holes(face)
            if hole_data:
                holes.append(hole_data)
    return holes

def recognize_holes(a_face):
    if not isinstance(a_face, TopoDS_Face):
        return None

    # Check if the surface is cylindrical
    surf = BRepAdaptor_Surface(a_face, True)
    surf_type = surf.GetType()

    if surf_type != GeomAbs_Cylinder:
        return None

    # Extract cylinder information
    gp_cyl = surf.Cylinder()
    location = gp_cyl.Location()
    axis = gp_cyl.Axis().Direction()
    diameter = gp_cyl.Radius() * 2

    # Calculate the bounding box to get the cylinder's height
    bbox = Bnd_Box()
    brepbndlib.Add(a_face, bbox)
    xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
    height = zmax - zmin

    # Additional check: ensure the height is proportional to the diameter
    if abs(height - diameter) > 0.1 * diameter:  # Adjust tolerance as needed
        return None

    # Return the hole properties if the checks pass
    return {
        "position": {"x": location.X(), "y": location.Y(), "z": location.Z()},
        "diameter": diameter,
        "depth": height,  # Depth is now computed as height
        "axis": {"x": axis.X(), "y": axis.Y(), "z": axis.Z()}
    }



def modify_hole_size(shape, new_size, hole_data):
    # Use the locked/selected hole data directly from the request
    hole_position = hole_data['position']  # Extract position
    hole_axis = hole_data['axis']  # Extract axis
    hole_depth = hole_data['depth']  # Extract depth

    # Create a new cylinder with the updated size and correct axis
    new_hole_radius = new_size / 2.0
    hole_location = gp_Pnt(hole_position['x'], hole_position['y'], hole_position['z'])  # Use the hole's position
    hole_axis_direction = gp_Dir(hole_axis['x'], hole_axis['y'], hole_axis['z'])  # Use the hole's axis

    # Create a cylindrical axis (gp_Ax2) for the cutting cylinder
    cutting_axis = gp_Ax2(hole_location, hole_axis_direction)

    # Create the cylinder aligned with the hole's axis
    new_hole = BRepPrimAPI_MakeCylinder(cutting_axis, new_hole_radius, hole_depth).Shape()

    # No need for transformation if the cylinder is already aligned
    # Perform a boolean cut to replace the old hole with the new one
    modified_shape = BRepAlgoAPI_Cut(shape, new_hole).Shape()

    return modified_shape


from OCC.Core.TopoDS import TopoDS_Shape, topods
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_FACE
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.GeomAbs import GeomAbs_Cylinder
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepBndLib import brepbndlib
from OCC.Core.TopAbs import TopAbs_INTERNAL

def recognize_holes_new(a_shape):
    if not isinstance(a_shape, TopoDS_Shape):
        return None

    holes = []

    # Traverse all faces in the solid
    face_explorer = TopExp_Explorer(a_shape, TopAbs_FACE)
    while face_explorer.More():
        face = topods.Face(face_explorer.Current())

        # Check if the face has cylindrical geometry
        surface_adaptor = BRepAdaptor_Surface(face)
        surf_type = surface_adaptor.GetType()

        if surf_type == GeomAbs_Cylinder:
            # Extract cylinder information
            cylinder = surface_adaptor.Cylinder()
            location = cylinder.Location()
            axis = cylinder.Axis().Direction()
            radius = cylinder.Radius()

            # Calculate the bounding box to get the cylinder's height (depth of the hole)
            bbox = Bnd_Box()
            brepbndlib.Add(face, bbox)
            xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
            height = zmax - zmin  # Adjust according to the orientation

            # Store hole properties
            holes.append({
                "position": {"x": location.X(), "y": location.Y(), "z": location.Z()},
                "diameter": radius * 2,
                "depth": height,
                "axis": {"x": axis.X(), "y": axis.Y(), "z": axis.Z()}
            })

        face_explorer.Next()

    return holes if holes else None
