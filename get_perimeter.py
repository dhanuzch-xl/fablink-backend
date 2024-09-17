import math
import matplotlib.pyplot as plt
import numpy as np

def calculate_distance(point1, point2):
    """
    Calculate the distance between two points.
    
    Parameters:
    point1, point2 (tuple): (x, y) coordinates of the points.
    
    Returns:
    float: Distance between the points.
    """
    return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

def read_dxf_file(file_path):
    """
    Read a DXF file and extract the drawing coordinates.
    
    Parameters:
    file_path (str): Path to the DXF file.
    
    Returns:
    dict: Dictionary of layers with lists of entities representing the drawing.
    """
    drawing = {}
    current_layer = "0"
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    i = 0
    while i < len(lines):
        if lines[i].strip() == 'LAYER':
            i += 1
            while i < len(lines) and lines[i].strip() != '0':
                if lines[i].strip() == '2':
                    current_layer = lines[i + 1].strip()
                    if current_layer not in drawing:
                        drawing[current_layer] = []
                i += 2
        elif lines[i].strip() == 'LINE':
            start_x = start_y = end_x = end_y = None
            i += 1
            while i < len(lines) and lines[i].strip() != '0':
                if lines[i].strip() == '10':
                    start_x = float(lines[i + 1].strip())
                elif lines[i].strip() == '20':
                    start_y = float(lines[i + 1].strip())
                elif lines[i].strip() == '11':
                    end_x = float(lines[i + 1].strip())
                elif lines[i].strip() == '21':
                    end_y = float(lines[i + 1].strip())
                i += 2
            if start_x is not None and start_y is not None and end_x is not None and end_y is not None:
                drawing[current_layer].append((start_x, start_y, end_x, end_y))
        elif lines[i].strip() == 'CIRCLE':
            center_x = center_y = radius = None
            i += 1
            while i < len(lines) and lines[i].strip() != '0':
                if lines[i].strip() == '10':
                    center_x = float(lines[i + 1].strip())
                elif lines[i].strip() == '20':
                    center_y = float(lines[i + 1].strip())
                elif lines[i].strip() == '40':
                    radius = float(lines[i + 1].strip())
                i += 2
            if center_x is not None and center_y is not None and radius is not None:
                drawing[current_layer].append(('CIRCLE', (center_x, center_y), radius))
        elif lines[i].strip() == 'ARC':
            center_x = center_y = radius = start_angle = end_angle = None
            i += 1
            while i < len(lines) and lines[i].strip() != '0':
                if lines[i].strip() == '10':
                    center_x = float(lines[i + 1].strip())
                elif lines[i].strip() == '20':
                    center_y = float(lines[i + 1].strip())
                elif lines[i].strip() == '40':
                    radius = float(lines[i + 1].strip())
                elif lines[i].strip() == '50':
                    start_angle = math.radians(float(lines[i + 1].strip()))
                elif lines[i].strip() == '51':
                    end_angle = math.radians(float(lines[i + 1].strip()))
                i += 2
            if center_x is not None and center_y is not None and radius is not None and start_angle is not None and end_angle is not None:
                drawing[current_layer].append(('ARC', (center_x, center_y), radius, start_angle, end_angle))
        elif lines[i].strip() in ['POLYLINE', 'LWPOLYLINE']:
            points = []
            i += 1
            while i < len(lines) and lines[i].strip() != '0':
                if lines[i].strip() == 'VERTEX':
                    x = y = None
                    while i < len(lines) and lines[i].strip() != '0':
                        if lines[i].strip() == '10':
                            x = float(lines[i + 1].strip())
                        elif lines[i].strip() == '20':
                            y = float(lines[i + 1].strip())
                        i += 2
                    if x is not None and y is not None:
                        points.append((x, y))
                else:
                    i += 1
            for j in range(len(points) - 1):
                drawing[current_layer].append((points[j][0], points[j][1], points[j + 1][0], points[j + 1][1]))
            if len(points) > 1 and lines[i - 1].strip() == '70' and int(lines[i].strip()) & 1:
                drawing[current_layer].append((points[-1][0], points[-1][1], points[0][0], points[0][1]))
        else:
            i += 1

    return drawing

def calculate_perimeter(drawing):
    """
    Calculate the perimeter of a drawing.
    
    Parameters:
    drawing (dict): Dictionary of layers with lists of entities representing the drawing.
    
    Returns:
    float: Perimeter of the drawing.
    """
    if not drawing:
        return 0

    perimeter = 0
    for layer, entities in drawing.items():
        for entity in entities:
            if isinstance(entity, tuple) and len(entity) == 4:
                start_point = (entity[0], entity[1])
                end_point = (entity[2], entity[3])
                perimeter += calculate_distance(start_point, end_point)
            elif isinstance(entity, tuple) and entity[0] == 'CIRCLE':
                _, center, radius = entity
                perimeter += 2 * math.pi * radius
            elif isinstance(entity, tuple) and entity[0] == 'ARC':
                _, center, radius, start_angle, end_angle = entity
                arc_length = radius * abs(end_angle - start_angle)
                perimeter += arc_length

    return perimeter

def plot_drawing(drawing):
    """
    Plot the drawing using matplotlib.
    
    Parameters:
    drawing (dict): Dictionary of layers with lists of entities representing the drawing.
    """
    fig, ax = plt.subplots()
    colors = ['b', 'r', 'g', 'c', 'm', 'y', 'k']
    color_index = 0

    for layer, entities in drawing.items():
        color = colors[color_index % len(colors)]
        color_index += 1
        for entity in entities:
            if isinstance(entity, tuple) and len(entity) == 4:
                ax.plot([entity[0], entity[2]], [entity[1], entity[3]], color + '-')
            elif isinstance(entity, tuple) and entity[0] == 'CIRCLE':
                _, center, radius = entity
                circle = plt.Circle(center, radius, fill=False, edgecolor=color)
                ax.add_patch(circle)
            elif isinstance(entity, tuple) and entity[0] == 'ARC':
                _, center, radius, start_angle, end_angle = entity
                theta = np.linspace(start_angle, end_angle, 100)
                x_arc = center[0] + radius * np.cos(theta)
                y_arc = center[1] + radius * np.sin(theta)
                ax.plot(x_arc, y_arc, color + '-')

    ax.set_title("Drawing Perimeter")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True)
    ax.set_aspect('equal', adjustable='box')
    plt.show()

# Example usage
if __name__ == "__main__":
    file_path = "models/WP-2.dxf"
    drawing = read_dxf_file(file_path)
    perimeter = calculate_perimeter(drawing)
    print(f"Perimeter: {perimeter} mm")
    plot_drawing(drawing)