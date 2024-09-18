import ezdxf
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeFace
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCC.Core.gp import gp_Pnt, gp_Circ, gp_Ax2, gp_Dir, gp_Vec
from OCC.Display.SimpleGui import init_display
from OCC.Core.AIS import AIS_Shape
import math

def create_arc_edge(p1, p2, bulge):
    """Creates an arc edge between two points based on the bulge factor."""
    if bulge == 0:
        # If no bulge, it's a straight edge
        return BRepBuilderAPI_MakeEdge(p1, p2).Edge()

    # Compute chord length between p1 and p2
    chord_length = math.sqrt((p2.X() - p1.X()) ** 2 + (p2.Y() - p1.Y()) ** 2)

    # Compute the sagitta (height of the arc)
    sagitta = (bulge * chord_length) / 2.0

    # Compute the radius of the arc
    radius = abs(((chord_length ** 2) / (8 * sagitta)) + (sagitta / 2.0))

    # Midpoint of the chord
    mx = (p1.X() + p2.X()) / 2
    my = (p1.Y() + p2.Y()) / 2

    # Direction of the chord
    if bulge <0:
        dx = p2.X() - p1.X()
        dy = p2.Y() - p1.Y()
    else:
        dx = p1.X() - p2.X()
        dy = p1.Y() - p2.Y()

    # Distance from the chord to the arc center
    distance_to_center = math.sqrt(radius ** 2 - (chord_length / 2.0) ** 2)

    # Adjust the sign based on bulge's direction (bulge > 0 is counterclockwise, bulge < 0 is clockwise)
    if bulge > 0:
        cx = mx - (dy / chord_length) * distance_to_center
        cy = my + (dx / chord_length) * distance_to_center
    else:
        cx = mx + (dy / chord_length) * distance_to_center
        cy = my - (dx / chord_length) * distance_to_center

    # Create the arc with correct direction
    center_pnt = gp_Pnt(cx, cy, 0)
    if bulge <0:
        axis = gp_Ax2(center_pnt, gp_Dir(0, 0, -1))  # Corrected axis direction for arcs
    else:
        axis = gp_Ax2(center_pnt, gp_Dir(0, 0, 1))  # Corrected axis direction for arcs

    circ = gp_Circ(axis, radius)

    # Create only an arc, not a full circle
    return BRepBuilderAPI_MakeEdge(circ, p1, p2).Edge()

def dxf_to_3d_shape(dxf_filename, extrusion_height=10.0):
    # Load the DXF file
    dxf_doc = ezdxf.readfile(dxf_filename)

    # Initialize containers for outer profile and circles
    outer_profile_edges = []
    interior_profile_wires = []
    circles = []

    # Extract the outer profile (LWPOLYLINE) and circles (CIRCLE)
    msp = dxf_doc.modelspace()

    for entity in msp:
        # Handle outer profiles (LWPOLYLINE on OUTER_PROFILES)
        if entity.dxftype() == 'LWPOLYLINE' and entity.dxf.layer == 'OUTER_PROFILES':
            points = entity.get_points('xyb')  # 'xyb' includes bulge values
            # Create edges for the outer profile, including arcs if bulge is present
            for i in range(len(points) - 1):
                p1 = gp_Pnt(points[i][0], points[i][1], 0)
                p2 = gp_Pnt(points[i + 1][0], points[i + 1][1], 0)
                bulge = points[i][2]  # Get the bulge value
                edge = create_arc_edge(p1, p2, bulge)
                outer_profile_edges.append(edge)

            # Close the profile by connecting the last point to the first
            p1 = gp_Pnt(points[-1][0], points[-1][1], 0)
            p2 = gp_Pnt(points[0][0], points[0][1], 0)
            bulge = points[-1][2]  # Handle bulge for the closing edge
            edge = create_arc_edge(p1, p2, bulge)
            outer_profile_edges.append(edge)

        # Handle interior profiles (LWPOLYLINE on INTERIOR_PROFILES)
        elif entity.dxftype() == 'LWPOLYLINE' and entity.dxf.layer == 'INTERIOR_PROFILES':
            points = entity.get_points('xyb')  # 'xyb' includes bulge values
            wire_maker = BRepBuilderAPI_MakeWire()  # Create wire for each interior profile
            # Create edges for the interior profile, including arcs
            for i in range(len(points) - 1):
                p1 = gp_Pnt(points[i][0], points[i][1], 0)
                p2 = gp_Pnt(points[i + 1][0], points[i + 1][1], 0)
                bulge = points[i][2]
                edge = create_arc_edge(p1, p2, bulge)
                wire_maker.Add(edge)

            # Close the interior profile by connecting the last point to the first
            p1 = gp_Pnt(points[-1][0], points[-1][1], 0)
            p2 = gp_Pnt(points[0][0], points[0][1], 0)
            bulge = points[-1][2]
            edge = create_arc_edge(p1, p2, bulge)
            wire_maker.Add(edge)

            if wire_maker.IsDone():
                interior_profile_wires.append(wire_maker.Wire())

        # Handle circles (CIRCLE on INTERIOR_PROFILES)
        elif entity.dxftype() == 'CIRCLE' and entity.dxf.layer == 'INTERIOR_PROFILES':
            center = entity.dxf.center
            radius = entity.dxf.radius
            # Remove negation if unnecessary for center.x
            circles.append((gp_Pnt(-center[0], center[1], 0), radius))

    # Create the wire from the outer profile edges
    wire_maker = BRepBuilderAPI_MakeWire()
    for edge in outer_profile_edges:
        wire_maker.Add(edge)

    if wire_maker.IsDone():
        wire = wire_maker.Wire()
        # Create a face from the outer wire
        face_maker = BRepBuilderAPI_MakeFace(wire)
        face = face_maker.Face()

        if face_maker.IsDone():
            face = face_maker.Face()

            # Extrude the face to create a 3D shape
            extrusion_direction = gp_Vec(0, 0, extrusion_height)
            solid_shape = BRepPrimAPI_MakePrism(face, extrusion_direction).Shape()

            # Initialize the viewer
            display, start_display, add_menu, add_function_to_menu = init_display()

            # Cut circular holes in the extruded shape
            for center, radius in circles:
                axis = gp_Ax2(center, gp_Dir(0, 0, -1))  # Correct axis direction for circular holes
                circle_edge = BRepBuilderAPI_MakeEdge(gp_Circ(axis, radius)).Edge()
                circle_wire = BRepBuilderAPI_MakeWire(circle_edge).Wire()
                circle_face = BRepBuilderAPI_MakeFace(circle_wire).Face()
                # Extrude the circle face through the solid shape
                circle_cut_shape = BRepPrimAPI_MakePrism(circle_face, extrusion_direction).Shape()
                # Subtract the circular cutout from the solid shape
                solid_shape = BRepAlgoAPI_Cut(solid_shape, circle_cut_shape).Shape()
            
            # Cut interior profiles (LWPOLYLINE from INTERIOR_PROFILES) in the extruded shape
            for hole_wire in interior_profile_wires:
                hole_face = BRepBuilderAPI_MakeFace(hole_wire).Face()
                hole_cut_shape = BRepPrimAPI_MakePrism(hole_face, extrusion_direction).Shape()
                solid_shape = BRepAlgoAPI_Cut(solid_shape, hole_cut_shape).Shape()
            # Display the final 3D shape with holes
            ais_solid = AIS_Shape(solid_shape)
            display.Context.Display(ais_solid, True)
            display.FitAll()

            print("Press ESC in the viewer window to exit.")
            # Start the viewer
            start_display()

        else:
            raise RuntimeError("Failed to create the face with holes.")
    else:
        raise RuntimeError("Failed to create the outer profile wire.")

# Example usage
dxf_filename = 'models/WP-6.dxf'  # Replace with your DXF file path
dxf_to_3d_shape(dxf_filename)
