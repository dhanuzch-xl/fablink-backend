import os
import json
from OCC.Extend.DataExchange import read_step_file_with_names_colors
from OCC.Core.TopoDS import TopoDS_Face
from OCC.Core.GeomAbs import GeomAbs_Cylinder
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepBndLib import brepbndlib_Add
from OCC.Extend.TopologyUtils import TopologyExplorer

# Load the STEP file and extract the shapes
step_file_path = os.path.join('..', 'models', 'WP-2.step')
big_shp_dict = read_step_file_with_names_colors(step_file_path)

# Extract the shapes (keys are TopoDS_Shape objects)
shapes = big_shp_dict.keys()

# Function to recognize face geometry and extract hole properties
def recognize_face(a_face):
    if not isinstance(a_face, TopoDS_Face):
        print("Please hit the 'G' key to switch to face selection mode")
        return False
    surf = BRepAdaptor_Surface(a_face, True)
    surf_type = surf.GetType()

    if surf_type == GeomAbs_Cylinder:
        gp_cyl = surf.Cylinder()
        location = gp_cyl.Location()
        axis = gp_cyl.Axis().Direction()
        diameter = gp_cyl.Radius() * 2

        # Calculate the bounding box to get the cylinder's height
        bbox = Bnd_Box()
        brepbndlib_Add(a_face, bbox)
        xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
        height = zmax - zmin

        return {
            "position": {"x": location.X(), "y": location.Y(), "z": location.Z()},
            "diameter": diameter,
            "depth": height,  # Depth is now computed as height
            "axis": {"x": axis.X(), "y": axis.Y(), "z": axis.Z()}
        }
    return None

# Function to recognize and extract all hole faces in batch mode
def recognize_hole_faces():
    holes = []
    for shape in shapes:  # Loop through each shape in the dictionary
        for face in TopologyExplorer(shape).faces():
            hole_data = recognize_face(face)
            if hole_data:
                holes.append(hole_data)
    return holes

# Main execution
if __name__ == "__main__":
    holes = recognize_hole_faces()
    output_path = os.path.join('..', 'app', 'hole_data.json')
    with open(output_path, 'w') as f:
        json.dump(holes, f, indent=4)
    print(f"Hole data exported to {output_path}")
