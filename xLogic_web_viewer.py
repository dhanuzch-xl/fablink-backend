import os
import sys

from OCC.Extend.DataExchange import read_step_file
from xLogic_threejs_renderer import ThreejsRenderer
from OCC.Core.TopoDS import TopoDS_Face
from OCC.Core.GeomAbs import GeomAbs_Plane, GeomAbs_Cylinder, GeomAbs_BSplineSurface
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Extend.TopologyUtils import TopologyExplorer
from OCC.Core.BRepGProp import brepgprop_VolumeProperties, brepgprop_SurfaceProperties
from OCC.Core.GProp import GProp_GProps
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepBndLib import brepbndlib_Add

from OCC.Extend.DataExchange import read_step_file_with_names_colors

# Load the STEP file
big_shp = read_step_file_with_names_colors(os.path.join("models", "Plate_1.step"))


# Function to recognize face geometry
def recognize_face(a_face):
    if not isinstance(a_face, TopoDS_Face):
        print("Please hit the 'G' key to switch to face selection mode")
        return False
    surf = BRepAdaptor_Surface(a_face, True)
    surf_type = surf.GetType()
    if surf_type == GeomAbs_Plane:
        print("Identified Plane Geometry")
        gp_pln = surf.Plane()
        location = gp_pln.Location()
        normal = gp_pln.Axis().Direction()
        print("--> Location (global coordinates)", location.X(), location.Y(), location.Z())
        print("--> Normal (global coordinates)", normal.X(), normal.Y(), normal.Z())
    elif surf_type == GeomAbs_Cylinder:
        print("Identified Cylinder Geometry")
        gp_cyl = surf.Cylinder()
        location = gp_cyl.Location()
        axis = gp_cyl.Axis().Direction()
        print("--> Location (global coordinates)", location.X(), location.Y(), location.Z())
        print("--> Axis (global coordinates)", axis.X(), axis.Y(), axis.Z())
    elif surf_type == GeomAbs_BSplineSurface:
        print("Identified BSplineSurface Geometry")
    else:
        print(surf_type, "recognition not implemented")

# Function to recognize clicked face
def recognize_clicked(face):
    print("Face selected: ", face)
    recognize_face(face)

# Function to recognize all faces in batch mode
def recognize_batch():
    for face in TopologyExplorer(big_shp).faces():
        recognize_face(face)
    print("============================")

# Function to calculate properties of a shape
def calculate_properties(shape):
    props = GProp_GProps()
    brepgprop_VolumeProperties(shape, props)
    volume = props.Mass()
    
    brepgprop_SurfaceProperties(shape, props)
    area = props.Mass()
    
    bbox = Bnd_Box()
    brepbndlib_Add(shape, bbox)
    xmin, ymin, zmin, xmax, ymax, zmax = bbox.Get()
    length = xmax - xmin
    breadth = ymax - ymin
    height = zmax - zmin
    
    return {
        "length": length,
        "breadth": breadth,
        "height": height,
        "area": area,
        "volume": volume
    }

# Function to get properties of all parts
def get_all_properties():
    properties = []
    for shape in TopologyExplorer(big_shp).solids():
        props = calculate_properties(shape)
        properties.append(props)
    return properties


# Main execution
if __name__ == "__main__":

    # Initialize the renderer
    my_renderer = ThreejsRenderer()
    for shp in big_shp:
        label, c = big_shp[shp]
        my_renderer.DisplayShape(
            shp, 
            color=(c.Red(), c.Green(), c.Blue()), 
            export_edges=False,
        )
    my_renderer.render()
    print("============================")
