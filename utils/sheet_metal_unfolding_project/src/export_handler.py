# src/export_handler.py

from OCC.Core.STEPControl import STEPControl_Writer, STEPControl_AsIs

def export_unfolded(result_shape, folds, export_path):
    writer = STEPControl_Writer()
    writer.Transfer(result_shape, STEPControl_AsIs)
    status = writer.Write(export_path)
    
    if status != 1:
        print(f"Error exporting unfolded result to: {export_path}")
    else:
        print(f"Unfolded result exported successfully to: {export_path}")
