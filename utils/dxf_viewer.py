import ezdxf
from OCC.Core.gp import gp_Pnt, gp_Circ, gp_Ax2
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
from OCC.Display.SimpleGui import init_display
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge2d

def dxf_to_occ(dxf_file):
    # Initialize the display
    display, start_display, add_menu, add_function_to_menu = init_display()

    # Load the DXF file using ezdxf
    doc = ezdxf.readfile(dxf_file)
    modelspace = doc.modelspace()

    # Iterate over the entities in the DXF file
    for entity in modelspace:
        if entity.dxftype() == 'LINE':
            # Handle line entities
            start_point = entity.dxf.start
            end_point = entity.dxf.end
            p1 = gp_Pnt(start_point[0], start_point[1], 0)
            p2 = gp_Pnt(end_point[0], end_point[1], 0)
            edge = BRepBuilderAPI_MakeEdge(p1, p2).Edge()
            display.DisplayShape(edge, update=True)

        elif entity.dxftype() == 'CIRCLE':
            # Handle circle entities
            center = entity.dxf.center
            radius = entity.dxf.radius
            circ = gp_Circ(gp_Ax2(gp_Pnt(center[0], center[1], 0), gp_Pnt(0, 0, 1).XYZ()), radius)
            edge = BRepBuilderAPI_MakeEdge(circ).Edge()
            display.DisplayShape(edge, update=True)

        elif entity.dxftype() == 'ARC':
            # Handle arc entities
            center = entity.dxf.center
            radius = entity.dxf.radius
            start_angle = entity.dxf.start_angle  # In degrees
            end_angle = entity.dxf.end_angle      # In degrees

            # Define the circle and extract the arc segment
            circ = gp_Circ(gp_Ax2(gp_Pnt(center[0], center[1], 0), gp_Pnt(0, 0, 1).XYZ()), radius)
            edge = BRepBuilderAPI_MakeEdge2d(circ, start_angle * 3.14159 / 180.0, end_angle * 3.14159 / 180.0).Edge()
            display.DisplayShape(edge, update=True)

        elif entity.dxftype() == 'POLYLINE':
            # Handle polyline entities
            points = [(v.dxf.x, v.dxf.y, 0) for v in entity.vertices]
            edges = []
            for i in range(len(points) - 1):
                p1 = gp_Pnt(*points[i])
                p2 = gp_Pnt(*points[i + 1])
                edge = BRepBuilderAPI_MakeEdge(p1, p2).Edge()
                display.DisplayShape(edge, update=True)

    # Start the OCC display
    start_display()

# Example usage:
dxf_file = "output_flat.dxf"
dxf_to_occ(dxf_file)
