from OCC.Extend.DataExchange import read_step_file, write_step_file
from OCC.Extend.TopologyUtils import TopologyExplorer
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCylinder
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.gp import gp_Trsf, gp_Vec, gp_Pnt, gp_Dir, gp_Ax2, gp_Quaternion, gp_Ax1
from OCC.Core.GeomAbs import GeomAbs_Cylinder

def insert_stud_with_proper_transform(sheet_metal_file, stud_file, output_file):
    # Read the STEP files
    sheet_metal_shape = read_step_file(sheet_metal_file)
    stud_shape = read_step_file(stud_file)

    # Search for the first hole and get its position and axis
    first_hole_position = None
    hole_diameter = None
    hole_axis = None
    explorer = TopologyExplorer(sheet_metal_shape)
    for face in explorer.faces():
        surface_adaptor = BRepAdaptor_Surface(face)
        if surface_adaptor.GetType() == GeomAbs_Cylinder:
            gp_cylinder = surface_adaptor.Cylinder()
            first_hole_position = gp_cylinder.Location()
            hole_diameter = gp_cylinder.Radius() * 2  # Diameter of the hole
            hole_axis = gp_cylinder.Axis().Direction()  # Extract hole axis
            break

    if first_hole_position is None or hole_diameter is None:
        print("No hole found in the sheet metal!")
        return

    # Scale the stud if necessary to fit the hole
    stud_diameter = 5.0  # Assume stud has this diameter, can extract dynamically from the stud model
    if hole_diameter > stud_diameter:
        scaling_factor = hole_diameter / stud_diameter
        scaling_trsf = gp_Trsf()
        scaling_trsf.SetScale(gp_Pnt(0, 0, 0), scaling_factor)  # Scale around origin
        stud_scaled = BRepBuilderAPI_Transform(stud_shape, scaling_trsf).Shape()
    else:
        stud_scaled = stud_shape

    # Apply axis alignment for the stud to match the hole's axis
    stud_axis = gp_Dir(0, 0, 1)  # Assume stud is initially aligned with the z-axis
    rotation_axis = gp_Ax1(first_hole_position, stud_axis.Crossed(hole_axis))
    rotation_angle = stud_axis.Angle(hole_axis)
    rotation = gp_Trsf()
    rotation.SetRotation(rotation_axis, rotation_angle)
    rotated_stud = BRepBuilderAPI_Transform(stud_scaled, rotation).Shape()

    # Translate the stud to the hole position
    translation_vector = gp_Vec(first_hole_position.X(), first_hole_position.Y(), first_hole_position.Z())
    translation = gp_Trsf()
    translation.SetTranslation(translation_vector)
    final_stud = BRepBuilderAPI_Transform(rotated_stud, translation, True).Shape()

    # Fuse the stud with the sheet metal
    fused_shape = BRepAlgoAPI_Fuse(sheet_metal_shape, final_stud).Shape()

    # Write the modified shape to a new STEP file
    write_step_file(fused_shape, output_file)

# File paths (use your actual file paths)
sheet_metal_file = "/home/meher/xlogic/fablink-backend/models/Plate_1.step"
stud_file = "/home/meher/xlogic/fablink-backend/models/test_stud.STEP"
output_file = "/home/meher/xlogic/fablink-backend/output/stud_modified.step"

# Test the functionality
insert_stud_with_proper_transform(sheet_metal_file, stud_file, output_file)
