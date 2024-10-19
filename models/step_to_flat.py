import FreeCAD
import FreeCADGui
import Part
import SheetMetalUnfolder

def flatten_with_freecad(step_file, output_dxf):
    doc = FreeCAD.newDocument()
    part = Part.Shape()
    part.read(step_file)
    Part.show(part)
    
    # Assuming the SheetMetal workbench is installed
    import SheetMetalCmd
    sheet_metal_obj = SheetMetalCmd.SheetMetalUnfold.Unfold(part)
    
    # Export the unfolded part
    unfolded_shape = sheet_metal_obj.Shape
    unfolded_shape.exportDXF(output_dxf)
    print("Flat pattern exported to DXF using FreeCAD.")

# Usage
flatten_with_freecad('your_sheet_metal_part.step', 'flat_pattern_freecad.dxf')
