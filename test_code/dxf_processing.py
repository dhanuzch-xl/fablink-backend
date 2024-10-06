import ezdxf

def detect_folds_and_holes(dxf_file_path):
    # Load the DXF file
    doc = ezdxf.readfile(dxf_file_path)
    modelspace = doc.modelspace()

    folds = []
    extended_folds = []
    holes = []

    # Define a threshold to differentiate between normal fold lines and extended fold lines
    fold_length_threshold = 100  # You can adjust this value based on your use case

    # Iterate through all entities in the modelspace
    for entity in modelspace:
        if entity.dxftype() == 'LINE':
            # Extract the start and end points of the line
            start_point = entity.dxf.start
            end_point = entity.dxf.end

            # Calculate the length of the line
            length = ((end_point.x - start_point.x) ** 2 + (end_point.y - start_point.y) ** 2) ** 0.5

            # Classify the line as fold or extended fold based on length
            if length > fold_length_threshold:
                extended_folds.append({
                    'start': (start_point.x, start_point.y, start_point.z),
                    'end': (end_point.x, end_point.y, end_point.z),
                    'length': length
                })
            else:
                folds.append({
                    'start': (start_point.x, start_point.y, start_point.z),
                    'end': (end_point.x, end_point.y, end_point.z),
                    'length': length
                })

        elif entity.dxftype() == 'CIRCLE':
            # For holes, extract the center point and radius
            center = entity.dxf.center
            radius = entity.dxf.radius
            holes.append({
                'center': (center.x, center.y, center.z),
                'radius': radius
            })

    # Return the data for folds, extended folds, and holes
    return {
        'folds': folds,
        'extended_folds': extended_folds,
        'holes': holes
    }

# Example usage:
dxf_file = 'WP-2.dxf'  # Replace with your DXF file path
data = detect_folds_and_holes(dxf_file)

# Print the detected data
print("Fold Lines:")
for fold in data['folds']:
    print(fold)

print("\nExtended Fold Lines:")
for extended_fold in data['extended_folds']:
    print(extended_fold)

print("\nHoles:")
for hole in data['holes']:
    print((hole))
