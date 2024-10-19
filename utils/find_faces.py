from __future__ import print_function

import os
import sys

from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.IFSelect import IFSelect_RetDone, IFSelect_ItemsByEntity
from OCC.Core.GeomAbs import GeomAbs_Plane, GeomAbs_Cylinder
from OCC.Core.TopoDS import topods_Face
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Display.SimpleGui import init_display
from OCC.Extend.TopologyUtils import TopologyExplorer  # Ensure you import the correct class
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere  # Import for creating a sphere
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB  # Import for color handling
from OCC.Core.BRepGProp import brepgprop_SurfaceProperties
from OCC.Core.GProp import GProp_GProps

# Initialize the display only once
display, start_display, add_menu, add_function_to_menu = init_display()

# Global counts for planes and cylinders
plane_count = 0
cylinder_count = 0

def read_step_file(filename):
    """Read the STEP file and return the shape."""
    step_reader = STEPControl_Reader()
    status = step_reader.ReadFile(filename)

    if status == IFSelect_RetDone:  # Check status
        failsonly = False
        step_reader.PrintCheckLoad(failsonly, IFSelect_ItemsByEntity)
        step_reader.PrintCheckTransfer(failsonly, IFSelect_ItemsByEntity)
        step_reader.TransferRoot(1)
        return step_reader.Shape(1)
    else:
        print("Error: Can't read the file.")
        return None

def get_faces(shape):
    """Return the faces from `shape`."""
    explorer = TopologyExplorer(shape)  # Use TopologyExplorer here
    faces = [topods_Face(face) for face in explorer.faces()]  # Get faces from the explorer
    return faces

def visualize_plane_location(location):
    """Visualize the location of the plane with a yellow sphere."""
    sphere_radius = 5.0  # Fixed radius for the sphere
    sphere = BRepPrimAPI_MakeSphere(location, sphere_radius).Shape()  # Create a sphere at the location
    display.DisplayShape(sphere, update=True)  # Display the sphere

def get_face_area(face):
    """
    Compute and return the area of a given face.

    Parameters:
    - face: The TopoDS_Face object whose area is to be calculated.

    Returns:
    - area: The area of the face as a float.
    """
    props = GProp_GProps()
    brepgprop_SurfaceProperties(face, props)
    area = props.Mass()
    return area

def recognize_face(a_face):
    """Identify the nature of the face (plane, cylinder, etc.) and display normals."""
    global plane_count, cylinder_count  # Declare global counts
    surf = BRepAdaptor_Surface(a_face, True)
    surf_type = surf.GetType()
    if surf_type == GeomAbs_Plane:
        plane_count += 1  # Increment plane count
        # Get the properties of the plane
        gp_pln = surf.Plane()
        location = gp_pln.Location()  # A point on the plane
        normal = gp_pln.Axis().Direction()  # The plane normal
        # Print location and normal to the console output
        print("--> Plane detected")
        print(
            "--> Location (global coordinates)",
            location.X(),
            location.Y(),
            location.Z(),
        )
        print("--> Normal (global coordinates)", normal.X(), normal.Y(), normal.Z())

        # Visualize the plane location with a sphere
        visualize_plane_location(location)

    elif surf_type == GeomAbs_Cylinder:
        cylinder_count += 1  # Increment cylinder count
        # Get the properties of the cylinder
        gp_cyl = surf.Cylinder()
        location = gp_cyl.Location()  # A point on the cylinder's axis
        axis = gp_cyl.Axis().Direction()  # The cylinder axis
        # Print location and axis to the console output
        print("--> Cylinder detected")
        print(
            "--> Location (global coordinates)",
            location.X(),
            location.Y(),
            location.Z(),
        )
        print("--> Axis (global coordinates)", axis.X(), axis.Y(), axis.Z())
    else:
        print("--> Other type detected")

def on_face_selected(shapes):
    """This function is called whenever a face is selected in the UI."""
    for shape in shapes:
        if shape.ShapeType() == TopAbs_FACE:  # Ensure we're working with a face
            print("Face selected:")
            recognize_face(topods_Face(shape))  # Call the recognize_face function to print details

def main():
    # Load the fSTEP file (update the path as needed)
    filename = "/home/meher/xlogic/fablink-backend/models/WP-2.step"  # Change to your STEP file path
    shp = read_step_file(filename)

    if shp:  # Ensure the shape is valid before processing
        faces = get_faces(shp)  # Get all faces
        print(f"Number of faces detected: {len(faces)}")

        # Recognize each face and print normals
        for face in faces:
            recognize_face(face)

        # Display the shape
        display.DisplayShape(shp, update=True)
        display.SetSelectionModeFace()  # Switch to Face selection mode

        # Register the face selection callback
        display.register_select_callback(on_face_selected)

    # Start the display
    start_display()

if __name__ == "__main__":
    main()
