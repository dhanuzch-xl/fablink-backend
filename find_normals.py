from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.IFSelect import IFSelect_RetDone, IFSelect_ItemsByEntity
from OCC.Core.GeomAbs import GeomAbs_Plane, GeomAbs_Cylinder
from OCC.Core.TopAbs import TopAbs_FACE
from OCC.Core.TopoDS import topods_Face
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.BRep import BRep_Tool
from OCC.Display.SimpleGui import init_display
from OCC.Core.gp import gp_Dir
import math

display, start_display, add_menu, add_function_to_menu = init_display()


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
    topExp = TopExp_Explorer()
    topExp.Init(shape, TopAbs_FACE)
    faces = []

    while topExp.More():
        fc = topods_Face(topExp.Current())
        faces.append(fc)
        topExp.Next()

    return faces


def get_normal(surf):
    """Get the normal vector of the surface at a given point."""
    if surf.GetType() == GeomAbs_Plane:
        gp_pln = surf.Plane()
        return gp_pln.Axis().Direction()
    elif surf.GetType() == GeomAbs_Cylinder:
        gp_cyl = surf.Cylinder()
        return gp_cyl.Axis().Direction()
    else:
        return None


def calculate_folding_angle(face1, face2):
    """Calculate the folding angle between two faces."""
    surf1 = BRepAdaptor_Surface(face1, True)
    surf2 = BRepAdaptor_Surface(face2, True)

    normal1 = get_normal(surf1)
    normal2 = get_normal(surf2)

    if normal1 and normal2:
        angle = normal1.Angle(normal2) * 180 / math.pi  # Convert radians to degrees
        return angle
    return 0


def find_folds(shape):
    """Identify faces and calculate angles of folds at intersections."""
    faces = get_faces(shape)
    folds = []

    # Check pairs of faces to identify folds
    for i in range(len(faces)):
        for j in range(i + 1, len(faces)):
            # Calculate the folding angle
            angle = calculate_folding_angle(faces[i], faces[j])
            if angle > 0:  # Only consider valid angles
                folds.append((faces[i], faces[j], angle))

    return folds


def main():
    # Load the STEP file (update the path as needed)
    filename = "/home/meher/xlogic/fablink-backend/models/WP-2.step"  # Change this to your STEP file path
    shape = read_step_file(filename)

    if shape:
        # Get faces from the loaded shape
        faces = get_faces(shape)

        print(f"Number of faces: {len(faces)}")

        # Analyze each face for its geometrical nature
        for face in faces:
            surf = BRepAdaptor_Surface(face, True)
            surf_type = surf.GetType()
            if surf_type == GeomAbs_Plane:
                print("--> Plane detected")
            elif surf_type == GeomAbs_Cylinder:
                print("--> Cylinder detected")
            else:
                print("--> Other type detected")

        # Find folds and their angles
        folds = find_folds(shape)
        for face1, face2, angle in folds:
            print(f"Fold found between two faces with angle: {angle:.2f}°")

        # Display the shape
        display.DisplayShape(shape)
        display.FitAll()

    # Keep the display open
    start_display()


if __name__ == "__main__":
    main()
