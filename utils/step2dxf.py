import os
import ezdxf
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepAdaptor import BRepAdaptor_Curve
from OCC.Core.TopoDS import TopoDS_Iterator
from OCC.Core.GeomAbs import GeomAbs_Line, GeomAbs_Circle, GeomAbs_Ellipse, GeomAbs_BSplineCurve, GeomAbs_Hyperbola, GeomAbs_Parabola
from OCC.Core.gp import gp_Pnt

def step_to_dxf(step_file, dxf_file):
    # Initialize the STEP reader
    step_reader = STEPControl_Reader()

    # Read the STEP file
    status = step_reader.ReadFile(step_file)

    # Check if the file was successfully read
    if status != IFSelect_RetDone:
        raise Exception(f"Error: Cannot read the STEP file: {step_file}")

    # Transfer the contents of the STEP file to the TopoDS_Shape
    step_reader.TransferRoots()
    shape = step_reader.OneShape()

    # Create a new DXF document
    dxf_doc = ezdxf.new('R2010')
    dxf_msp = dxf_doc.modelspace()

    # Iterate over the shapes (edges) and convert them to DXF format
    def convert_shape_to_dxf(shape):
        it = TopoDS_Iterator(shape)
        while it.More():
            current_shape = it.Value()
            if current_shape.ShapeType() == 1:  # Check if it's an edge
                edge = BRep_Tool.Edge(current_shape)
                curve = BRepAdaptor_Curve(edge)
                curve_type = curve.GetType()

                # Handle different curve types
                if curve_type == GeomAbs_Line:  # Line
                    p1 = curve.Value(0)
                    p2 = curve.Value(1)
                    dxf_msp.add_line((p1.X(), p1.Y()), (p2.X(), p2.Y()))

                elif curve_type == GeomAbs_Circle:  # Circle
                    circle = curve.Circle()
                    center = circle.Location()
                    radius = circle.Radius()
                    normal = circle.Axis().Direction()
                    dxf_msp.add_circle((center.X(), center.Y()), radius)

                elif curve_type == GeomAbs_BSplineCurve:  # Spline (for complex curves)
                    num_points = curve.NbPoles()
                    points = [curve.Pole(i + 1) for i in range(num_points)]
                    dxf_msp.add_spline([(p.X(), p.Y()) for p in points])

                elif curve_type == GeomAbs_Ellipse:  # Ellipse
                    ellipse = curve.Ellipse()
                    center = ellipse.Location()
                    major_radius = ellipse.MajorRadius()
                    minor_radius = ellipse.MinorRadius()
                    normal = ellipse.Axis().Direction()
                    dxf_msp.add_ellipse((center.X(), center.Y()), major_radius, minor_radius)

                # Handle other curve types if necessary
            it.Next()

    # Convert the STEP shape to DXF entities
    convert_shape_to_dxf(shape)

    # Save the DXF file
    dxf_doc.saveas(dxf_file)
    print(f"DXF file saved to {dxf_file}")

# Example usage
step_file = "/home/meher/xlogic/fablink-backend/models/WP-2.step"
dxf_file = "/home/meher/xlogic/fablink-backend/output/WP-2.dxf"
step_to_dxf(step_file, dxf_file)
