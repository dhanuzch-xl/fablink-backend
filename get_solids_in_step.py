# Assuming necessary imports and initializations are done above
# from OCC.Core.STEPControl import STEPControl_Reader
# from OCC.Core.IFSelect import IFSelect_RetDone
# from xLogic_threejs_renderer import ThreejsRenderer

from OCC.Extend.DataExchange import read_step_file_with_names_colors
from OCC.Core.TopoDS import TopoDS_Solid

def get_shapes_in_step(file_path):
    shapes_labels_colors = read_step_file_with_names_colors(file_path)
    print("================================================")

    # Iterate over the shapes and display them
    for shp in shapes_labels_colors:
        if isinstance(shp, TopoDS_Solid):
            label, c = shapes_labels_colors[shp]
            print(f"Shape: {shp}, Label: {label}, Color: (R: {c.Red()}, G: {c.Green()}, B: {c.Blue()})")
    
    return shapes_labels_colors


if __name__ == "__main__":
    file_path = "models/suspension.stp"
    get_shapes_in_step(file_path)


# TODO: add logic in which if number of shapes at root is greater than 1, then it is not a sheet, but a part of a larger assembly.