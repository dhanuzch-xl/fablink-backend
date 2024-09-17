import os
import ezdxf
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeFace
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCC.Core.gp import gp_Pnt, gp_Ax2, gp_Dir, gp_Vec, gp_Circ
from OCC.Display.SimpleGui import init_display
from OCC.Core.Quantity import Quantity_Color, Quantity_NOC_BLACK
from OCC.Core.AIS import AIS_Shape
from OCC.Extend.TopologyUtils import TopologyExplorer
from OCC.Core.BRep import BRep_Tool


def close_wire_if_needed(wire):
    """If the wire is open, close it by connecting the last vertex to the first."""
    explorer = TopologyExplorer(wire)
    vertices = list(explorer.vertices())
    
    if len(vertices) < 2:
        return wire  # Not enough vertices to form a valid wire

    first_vertex = BRep_Tool.Pnt(vertices[0])
    last_vertex = BRep_Tool.Pnt(vertices[-1])

    if not first_vertex.IsEqual(last_vertex, 1e-6):  # Check if the vertices are not the same
        # Create an edge between the last and first points to close the wire
        closing_edge = BRepBuilderAPI_MakeEdge(last_vertex, first_vertex).Edge()
        wire_maker = BRepBuilderAPI_MakeWire(wire)  # Create a new wire from the existing one
        wire_maker.Add(closing_edge)  # Add the closing edge
        return wire_maker.Wire()  # Return the closed wire
    return wire  # Return the original wire if already closed


def dxf_to_extruded_area_within_wireframe(dxf_filename, extrusion_height=2.0):
    # Open the DXF file using ezdxf
    dxf_doc = ezdxf.readfile(dxf_filename)

    # Prepare containers for DXF geometries (lines, polylines, circles)
    wire_edges = []
    circles = []

    # Iterate over all entities in modelspace
    msp = dxf_doc.modelspace()

    # Read DXF lines and polylines to form the wireframe
    for entity in msp:
        if entity.dxftype() == 'LINE':
            start_point = entity.dxf.start
            end_point = entity.dxf.end

            # Add to wireframe edges
            occ_start = gp_Pnt(start_point[0], start_point[1], 0)
            occ_end = gp_Pnt(end_point[0], end_point[1], 0)
            edge = BRepBuilderAPI_MakeEdge(occ_start, occ_end).Edge()
            wire_edges.append(edge)

        elif entity.dxftype() == 'LWPOLYLINE':
            points = entity.get_points()
            # Handle lightweight polylines, create edges from vertices
            polyline_edges = []
            for i in range(len(points) - 1):
                occ_start = gp_Pnt(points[i][0], points[i][1], 0)
                occ_end = gp_Pnt(points[i + 1][0], points[i + 1][1], 0)
                edge = BRepBuilderAPI_MakeEdge(occ_start, occ_end).Edge()
                polyline_edges.append(edge)
            # If polyline is closed, add the last segment
            if entity.is_closed:
                occ_start = gp_Pnt(points[-1][0], points[-1][1], 0)
                occ_end = gp_Pnt(points[0][0], points[0][1], 0)
                edge = BRepBuilderAPI_MakeEdge(occ_start, occ_end).Edge()
                polyline_edges.append(edge)

            # Add polyline edges to wireframe edges
            wire_edges.extend(polyline_edges)

        elif entity.dxftype() == 'CIRCLE':
            center = entity.dxf.center
            radius = entity.dxf.radius
            occ_center = gp_Pnt(-center[0], center[1], 0)  # Flip x-axis for circles
            axis = gp_Ax2(occ_center, gp_Dir(0, 0, 1))  # Circle in XY plane
            circle = gp_Circ(axis, radius)  # Create a gp_Circ geometry
            circle_edge = BRepBuilderAPI_MakeEdge(circle).Edge()  # Create the edge for the circle
            circles.append(circle_edge)  # Add to list of circles

    # Create a wire from the collected edges
    wire_maker = BRepBuilderAPI_MakeWire()
    for edge in wire_edges:
        wire_maker.Add(edge)

    # Check if the wire is closed, and if not, close it
    if wire_maker.IsDone():
        wire = wire_maker.Wire()
        wire = close_wire_if_needed(wire)
    else:
        raise RuntimeError("Failed to create a wire from the edges.")

    # Create a face from the closed wire
    face_maker = BRepBuilderAPI_MakeFace(wire)
    new_face = BRepBuilderAPI_MakeFace

    # Extrude the face to create a 3D solid
    extrusion_direction = gp_Vec(0, 0, extrusion_height)
    solid_shape = BRepPrimAPI_MakePrism(face_maker.Face(), extrusion_direction).Shape()

    # Initialize the viewer
    display, start_display, add_menu, add_function_to_menu = init_display()

    # Display the extruded solid
    ais_solid = AIS_Shape(solid_shape)
    display.Context.Display(ais_solid, True)

    # Display the circles (without extrusion)
    for circle_edge in circles:
        ais_circle = AIS_Shape(circle_edge)
        display.Context.Display(ais_circle, True)

    display.FitAll()

    print("Press ESC in the viewer window to exit.")

    # Start the viewer to display the shapes
    start_display()


# Example usage
dxf_filename = 'models/WP-2.dxf'
dxf_to_extruded_area_within_wireframe(dxf_filename)
