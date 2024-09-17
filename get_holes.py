import ezdxf
import os

# Specify the path to your DXF file
dxf_file_path = 'models/WP-2.dxf'  # Replace with the actual file path

# Check if the file exists
if not os.path.isfile(dxf_file_path):
    print(f"File not found: {dxf_file_path}")
    exit(1)

# Read the DXF document from the file
try:
    doc = ezdxf.readfile(dxf_file_path)
except IOError:
    print(f"Not a DXF file or a generic I/O error.")
    exit(2)
except ezdxf.DXFStructureError:
    print(f"Invalid or corrupted DXF file.")
    exit(3)

# Access the modelspace where entities are stored
msp = doc.modelspace()

# Query all CIRCLE entities (holes)
circles = msp.query('CIRCLE')

# Extract and print coordinates and dimensions of the holes
for circle in circles:
    center = circle.dxf.center  # (x, y, z)
    radius = circle.dxf.radius
    layer = circle.dxf.layer
    print(f"Hole found on layer '{layer}': Center=({center[0]}, {center[1]}), Radius={radius}")

# Print the total count of circles
print(f"Total number of circles: {len(circles)}")