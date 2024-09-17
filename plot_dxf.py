#!/usr/bin/env python3
# Copyright (c) 2020-2023, Matthew Broadway
# License: MIT License
import sys
import math
import json

import ezdxf
from ezdxf import recover
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.config import Configuration
from ezdxf.addons.drawing import json as ezdxfjson
import json

def calculate_angle(start, end):
    dx = end.x - start.x
    dy = end.y - start.y
    angle = math.degrees(math.atan2(dy, dx))
    return angle

def _main():
    if len(sys.argv) < 2:
        print("Usage: plot_dxf.py <cad_file>")
        sys.exit(1)

    cad_file = sys.argv[1]

    try:
        doc = ezdxf.readfile(cad_file)
    except IOError:
        print(f"Not a DXF file or a generic I/O error.")
        sys.exit(2)
    except ezdxf.DXFError:
        try:
            doc, auditor = recover.readfile(cad_file)
        except ezdxf.DXFStructureError:
            print(f"Invalid or corrupted DXF file: {cad_file}")
            sys.exit(3)
    else:
        auditor = doc.audit()

    if auditor.has_errors:
        # But is most likely good enough for rendering.
        print(f"Found {len(auditor.errors)} unrecoverable errors.")
        
    if auditor.has_fixes:
        print(f"Fixed {len(auditor.fixes)} errors.")

    try:
        layout = doc.layouts.get("Model")
    except KeyError:
        print(
            f'Could not find layout "Model". '
            f"Valid layouts: {[l.name for l in doc.layouts]}"
        )
        sys.exit(4)

    # List all layers
    layers = doc.layers
    print(f"Total number of layers: {len(layers)}")
    for layer in layers:
        print(f"Layer: {layer.dxf.name}")

    # List all circles with their radii and coordinates
    circles = layout.query('CIRCLE')
    print(f"Total number of circles: {len(circles)}")
    for circle in circles:
        center = circle.dxf.center
        radius = circle.dxf.radius
        print(f"Circle at ({center.x}, {center.y}, {center.z}) with radius {radius}")

    # List all bend lines with their start and end coordinates and additional properties
    bend_lines = layout.query('LINE[layer=="BEND"]')
    print(f"Total number of bend lines: {len(bend_lines)}")
    for line in bend_lines:
        start = line.dxf.start
        end = line.dxf.end
        length = math.sqrt((end.x - start.x) ** 2 + (end.y - start.y) ** 2)
        angle = calculate_angle(start, end)
        print(f"Bend line from ({start.x}, {start.y}, {start.z}) to ({end.x}, {end.y}, {end.z})")
        print(f"  Length: {length:.2f}")
        print(f"  Angle: {angle:.2f} degrees")

    # setup drawing add-on configuration
    config = Configuration()
    ctx = RenderContext(doc)
    out = ezdxfjson.CustomJSONBackend()  # Use the CustomJSONBackend
    Frontend(ctx, out, config=config).draw_layout(layout, finalize=True)
    
    # Output JSON data
    json_data = out.get_json_data()
    with open("output.json", "w") as json_file:
        json.dump(json_data, json_file, indent=2)

if __name__ == "__main__":
    _main()