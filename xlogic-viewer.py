from OCC.Extend.DataExchange import read_step_file_with_names_colors
from xLogic_x3dom_renderer import XLogicX3DomRenderer

filename = "models/suspension.stp"
shapes_labels_colors = read_step_file_with_names_colors(filename)

# create the xlogic x3dom renderer
my_renderer = XLogicX3DomRenderer()

# traverse shapes, render in "face" mode
for shp in shapes_labels_colors:
    label, c = shapes_labels_colors[shp]
    my_renderer.DisplayShape(
        shp, 
        color=(c.Red(), c.Green(), c.Blue()), 
        export_edges=False,
        part_name=label  # Pass the part name here
    )

my_renderer.render()