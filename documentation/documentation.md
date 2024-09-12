# Project Documentation

This documentation provides an overview of the functionality of each Python file in the folder.

## core_meshDS_numpy_node_colors.py

This Python code is an example of how to create and visualize a triangular mesh using the `OCC` (Open CASCADE Technology) library, with the mesh data derived from NumPy arrays. Below is a detailed breakdown of the code's purpose and functionality:

### Purpose:
The code generates a 3D triangular mesh from a mathematical function, colors the mesh based on the Z-values of its vertices, and visualizes the mesh using the Open CASCADE Technology library.

### Functionality:

1. **Imports and Dependencies:**
   - The code imports necessary modules from `numpy`, `scipy.spatial`, and various components of the `OCC` library.
   - The `init_display` function from `OCC.Display.SimpleGui` is used to set up the display window.

2. **Mesh Generation (`getMesh` function):**
   - The `getMesh` function creates a grid of points in the XY plane using `numpy.linspace` and `numpy.meshgrid`.
   - It calculates the Z-values of these points using a mathematical function \( \frac{\sin(x^2 + y^2)}{x^2 + y^2} \).
   - The function returns the vertices and faces of the mesh. The faces are generated using the Delaunay triangulation of the XY coordinates.

3. **Data Source Creation:**
   - The vertices and faces are passed to `MeshDS_DataSource`, which is an OCC data structure that holds mesh data.

4. **Mesh Visualization Setup:**
   - A `MeshVS_Mesh` object is created to handle the visualization of the mesh.
   - A `MeshVS_NodalColorPrsBuilder` is used to color the mesh nodes based on their Z-values. The colors are interleaved between the nodes.

5. **Color Mapping:**
   - An `Aspect_SequenceOfColor` object is prepared to hold the color map. Colors like purple, blue, green, and orange are added to this map.
   - A `TColStd_DataMapOfIntegerReal` object is used to map the normalized Z-values of the vertices to color intensities.

6. **Color Assignment:**
   - The Z-values of the vertices are normalized to a range of [0, 1].
   - These normalized values are bound to the vertices using the `aScaleMap` object.

7. **Mesh Customization:**
   - The color map and scale values are applied to the `node_builder`.
   - The edges of the mesh are turned off for visualization purposes using `mesh_drawer.SetBoolean(MeshVS_DA_ShowEdges, False)`.

8. **Displaying the Mesh:**
   - The `init_display` function initializes the display context.
   - The mesh is added to the display context and the view is fitted to show the entire mesh.
   - The `start_display` function starts the GUI event loop to display the mesh window.

### Summary:
The code demonstrates how to create a 3D triangular mesh from a mathematical function using NumPy, apply color mapping based on Z-values, and visualize the mesh using the Open CASCADE Technology library. The mesh is displayed without edges, and the colors are interpolated between vertices to reflect their Z-values.

## core_display_dont_show_edges.py

This Python code is an example script that demonstrates the basic functionality of the `pythonOCC` library, which is a set of Python bindings for the Open CASCADE Technology (OCCT), a software development platform for 3D CAD, CAM, CAE, etc.

### Purpose:
The script serves as a basic test to ensure that the `pythonOCC` library is installed correctly, a GUI manager (such as wxPython or PyQt/PySide) is available for rendering, and the OpenGL graphics driver is functioning properly.

### Functionality:
1. **Imports Required Modules:**
   - `init_display` from `OCC.Display.SimpleGui` to initialize the display.
   - `BRepPrimAPI_MakeBox` from `OCC.Core.BRepPrimAPI` to create a 3D box shape.

2. **Initialize the Display:**
   - Calls `init_display()` to set up the display environment, which returns several functions:
     - `display`: The display object used to render shapes.
     - `start_display`: A function to start the display loop.
     - `add_menu`: A function to add a menu to the GUI.
     - `add_function_to_menu`: A function to add functionality to the menu.

3. **Create a 3D Box:**
   - `my_box` is created using `BRepPrimAPI_MakeBox(10.0, 20.0, 30.0).Shape()`, which generates a box with dimensions 10x20x30 units.

4. **Configure and Display the Shape:**
   - `display.default_drawer.SetFaceBoundaryDraw(False)`: Configures the display settings to not draw face boundaries.
   - `display.DisplayShape(my_box, update=True)`: Renders the created box shape in the display.

5. **Start the Display Loop:**
   - `start_display()`: Starts the GUI event loop to keep the display window open and responsive.

### Summary:
This script is a simple example to verify the installation and basic functionality of the `pythonOCC` library and its ability to render 3D shapes using a graphical user interface. It creates and displays a 3D box, ensuring that the necessary components (such as the GUI manager and OpenGL) are working correctly.

## core_mesh_data_source.py

The provided Python code is a script that uses the `pythonOCC` library to read, display, and manipulate a 3D mesh from an STL file. Here is a concise description of its purpose and functionality:

1. **Imports and License**:
   - The script begins with a comment block that includes licensing information under the GNU Lesser General Public License.
   - It imports necessary modules from the `pythonOCC` library, which is a set of Python bindings for the Open Cascade Technology (OCCT) 3D modeling library.

2. **File Path Setup**:
   - The script sets up the path to the STL file (`fan.stl`) located in the `../assets/models/` directory relative to the script's location.

3. **STL File Reading**:
   - The STL file is read using `rwstl.ReadFile`, which loads the 3D mesh data into the variable `a_stl_mesh`.

4. **Data Source Creation**:
   - A `MeshDS_DataSource` object is created from the STL mesh data, which acts as a data source for the mesh visualization.

5. **Mesh Presentation Setup**:
   - A `MeshVS_Mesh` object (`a_mesh_prs`) is created to represent the mesh.
   - A `MeshVS_MeshPrsBuilder` object (`a_builder`) is created to build the visual representation of the mesh.
   - The builder is added to the mesh presentation object.

6. **Nodal Color Builder**:
   - Another builder, `MeshVS_NodalColorPrsBuilder`, is set up to handle nodal color data and texture mapping for the mesh.

7. **Display Initialization**:
   - The script initializes the display using `init_display` from `OCC.Display.SimpleGui`.

8. **Mesh Display**:
   - The mesh is displayed in the initialized display context.
   - The view is fitted to show the entire mesh.
   - The display loop is started to render the mesh.

In summary, this script reads a 3D mesh from an STL file, prepares it for visualization with color and texture, and displays it using the `pythonOCC` library's graphical user interface tools.

## core_geometry_splinecage.py

This Python script is part of the `pythonOCC` library, which is a set of Python bindings for the Open CASCADE Technology (OCCT), a software development platform for 3D CAD, CAM, CAE. The script's primary purpose is to create a surface from a network of curves, similar to the "curve network surfacing" command in Rhino, a 3D computer graphics and CAD application.

Here's a breakdown of the script's functionality:

1. **Imports and Initialization**:
   - The script imports various modules from the `OCC` library for handling curves, points, surfaces, and display functionalities.
   - Initializes the display environment using `init_display()` from `OCC.Display.SimpleGui`.

2. **Helper Functions**:
   - `random_color()`: Generates a random RGB color.
   - `length_from_edge(edg)`: Computes the length of a given edge.
   - `divide_edge_by_nr_of_points(edg, n_pts)`: Divides an edge into a specified number of points and returns a list of parameters and points.
   - `hash_edge_length_to_face(faces)`: Creates dictionaries that map edge lengths to faces and edges.

3. **Main Function**:
   - `build_curve_network(event=None, enforce_tangency=True)`: This is the core function that:
     - Reads a STEP file containing a spline cage model.
     - Extracts faces and edges from the model.
     - Maps edge lengths to corresponding faces and edges.
     - Filters edges that are not part of any face.
     - Creates a `BRepOffsetAPI_MakeFilling` object to build the surface.
     - Adds constraints and support faces to the surface builder.
     - Optionally enforces tangency constraints for higher surface quality.
     - Adds points along edges without adjacent faces to the surface builder.
     - Builds and displays the resulting surface if successful.

4. **Execution Block**:
   - When run as the main program, the script calls `build_curve_network()`, fits the display to show all objects, and starts the display loop.

### Purpose:
The purpose of this script is to demonstrate how to create a surface from a network of curves using the `pythonOCC` library. It reads a spline cage from a STEP file, processes the edges and faces, and constructs a surface while optionally enforcing tangency constraints for a smoother result.

### Usage:
- This script is intended to be run in an environment where `pythonOCC` is installed.
- The STEP file path (`../assets/models/splinecage.stp`) should be updated to point to a valid file location.

### Note:
The script contains a TODO comment about needing examples where tangency to constraining faces is respected, indicating that this is a potential area for further development or testing.

## core_export_step_header_section.py

This Python code is a script designed to create a 3D box shape and export it to a STEP (Standard for the Exchange of Product model data) file format with a detailed header. It utilizes the `pythonOCC` library, which is a set of Python bindings for the Open CASCADE Technology (OCCT) framework, commonly used for 3D CAD, CAM, CAE, etc.

Here is a breakdown of its functionality:

1. **Imports Required Libraries:**
   - Imports various modules from `OCC.Core` for creating shapes and handling STEP file operations.
   - Imports `datetime` from the standard library to add a timestamp to the STEP file header.

2. **Create a 3D Box Shape:**
   - Uses `BRepPrimAPI_MakeBox` to create a 3D box shape with dimensions 10x20x30 units.

3. **Initialize STEP Exporter:**
   - Initializes a `STEPControl_Writer` object to handle the STEP file writing process.
   - Sets the STEP schema to "AP203" using `Interface_Static_SetCVal`.

4. **Transfer Shape and Write File:**
   - Transfers the box shape to the STEP writer.
   - Sets the product name to "Box".

5. **Set STEP Header:**
   - Clears any existing header information in the STEP model.
   - Creates a new header using `APIHeaderSection_MakeHeader`.
   - Sets various header fields such as name, author, authorization, description, organization, originating system, implementation level, schema identifiers, preprocessor version, and a timestamp.

6. **Add Header Entities:**
   - Adds the header entities to the STEP model.

7. **Write the STEP File:**
   - Writes the STEP file to "box_header.stp".
   - Checks the status of the write operation and raises an error if the write operation fails.

### Summary
The script's purpose is to demonstrate how to create a simple 3D box shape and export it to a STEP file with a comprehensive header using the `pythonOCC` library. The header contains metadata such as the model name, author, description, organization, and a timestamp, ensuring that the exported STEP file is well-documented.

## core_visualization_graphic3d_custom_opengl.py

This Python code is designed to create and render a large number of 3D lines using the Open CASCADE Technology (OCCT) library for 3D CAD, CAM, CAE, etc. Here’s a breakdown of its purpose and functionality:

### Purpose:
The main goal of the script is to efficiently render a large number of 3D lines in a display window, leveraging OpenGL for better performance. This approach is significantly faster than using traditional methods provided by OCCT for rendering individual shapes.

### Functionality:

1. **Imports and Dependencies:**
   - The script imports necessary modules from OCCT, as well as standard Python libraries like `random` and `warnings`.
   - It attempts to import `numpy` for efficient random number generation. If `numpy` is not available, it falls back to a slower method using Python's `random` module.

2. **Function Definitions:**
   - `create_ogl_group(display)`: Initializes an OpenGL group for rendering.
   - `generate_points(spread, n)`: Generates `n` random 3D points within a specified spread. It uses `numpy` if available; otherwise, it falls back to using `random`.
   - `draw_lines(pnt_list, nr_of_points, display)`: Draws lines between pairs of points from the provided list. It uses a more direct OpenGL approach for faster rendering.

3. **Main Execution:**
   - The script initializes the display using `init_display()`.
   - It defines the number of points (`nr_of_points`) and the spread for random point generation.
   - It calls `draw_lines()` with the generated points to render the lines in the display.
   - Finally, it starts the display loop with `start_display()`.

### Detailed Steps:

1. **Creating an OpenGL Group:**
   - `create_ogl_group(display)` sets up a structure to store an OpenGL buffer for rendering.

2. **Generating Points:**
   - `generate_points(spread, n)` yields random 3D points within the specified spread. If `numpy` is available, it uses `numpy.random.uniform` for efficient point generation. Otherwise, it uses `random.uniform` and warns the user about the potential slowness.

3. **Drawing Lines:**
   - `draw_lines(pnt_list, nr_of_points, display)`:
     - Initializes an OpenGL group and sets up line attributes (color, style).
     - Creates an array to store the vertices of the lines.
     - Iterates through the points, adding vertices and lines to the array.
     - Adds the array to the OpenGL group and displays it.

4. **Running the Script:**
   - The script initializes the display, generates points, draws the lines, and starts the display loop.

### Key Points:
- The script uses OCCT for 3D rendering and leverages OpenGL for performance.
- It efficiently generates and renders a large number of 3D lines.
- It handles the absence of `numpy` gracefully, with a warning about performance.

This approach is particularly useful for applications requiring the visualization of a large number of points or lines, such as scientific simulations or complex CAD models.

## core_hlr_outliner.py

This Python script is designed to read a BREP (Boundary Representation) file of a cylinder head, perform hidden line removal (HLR) on the 3D shape, and then display the resulting outline using a graphical user interface (GUI). Here is a detailed breakdown of its functionality:

1. **Imports**: The script imports various modules from the `OCC` (Open CASCADE Technology) library, which is used for 3D CAD, CAM, CAE, etc.
   - `init_display` from `OCC.Display.SimpleGui` for initializing the display window.
   - `BRepPrimAPI_MakeBox` from `OCC.Core.BRepPrimAPI` for creating primitive shapes (not used in the script).
   - `HLRTopoBRep_OutLiner` from `OCC.Core.HLRTopoBRep` for handling HLR outlines.
   - `breptools_Read` from `OCC.Core.BRepTools` for reading BREP files.
   - `TopoDS_Shape` from `OCC.Core.TopoDS` for representing topological shapes.
   - `BRep_Builder` from `OCC.Core.BRep` for constructing BREP shapes.
   - `HLRBRep_Algo` and `HLRBRep_HLRToShape` from `OCC.Core.HLRBRep` for HLR algorithms and converting HLR results to shapes.

2. **Shape Initialization**:
   - `cylinder_head` and `outt` are initialized as `TopoDS_Shape` objects.
   - `builder` is initialized as a `BRep_Builder` object.

3. **Reading the BREP File**:
   - The `breptools_Read` function reads the BREP file `../assets/models/cylinder_head.brep` and stores the shape in `cylinder_head`.

4. **HLR Algorithm**:
   - `myAlgo` is an instance of `HLRBRep_Algo`, which is used to perform HLR.
   - The `cylinder_head` shape is added to `myAlgo`.
   - The `Update` method is called on `myAlgo` to process the HLR.

5. **Conversion to Shape**:
   - The `HLRBRep_HLRToShape` class is used to convert the HLR results into a shape.
   - `aHLRToShape` is an instance of `HLRBRep_HLRToShape` initialized with `myAlgo`.
   - The `OutLineVCompound3d` method is called on `aHLRToShape` to get the 3D outline shape, which is stored in `o`.

6. **Displaying the Shape**:
   - `init_display` initializes the display window and returns several functions for controlling the display.
   - The `DisplayShape` method is used to display the shape `o` in the initialized display window.
   - `start_display` starts the GUI event loop to render the display.

In summary, this script reads a 3D model from a BREP file, processes it to remove hidden lines, and displays the resulting outline using a GUI.

## core_display_callbacks.py

This Python code is part of the `pythonOCC` library, a set of Python bindings for the Open CASCADE Technology (OCCT) 3D modeling library. The code's primary purpose is to create and display 3D geometric shapes (a box and a torus) and compute their bounding boxes when selected in the graphical display. Here is a concise breakdown of its functionality:

1. **Imports**:
   - `BRepPrimAPI_MakeBox`, `BRepPrimAPI_MakeTorus`: Functions to create 3D shapes (a box and a torus).
   - `Bnd_Box`: Class to define a bounding box.
   - `brepbndlib_Add`: Function to compute the bounding box of a shape.
   - `init_display`: Function to initialize the display window.

2. **Function Definitions**:
   - `print_xy_click(shp, *kwargs)`: Callback function that prints the selected shape(s) and additional arguments.
   - `compute_bbox(shp, *kwargs)`: Callback function that computes and prints the bounding box dimensions and center for the selected shape(s).

3. **Display Initialization**:
   - `display, start_display, add_menu, add_function_to_menu = init_display()`: Initializes the display window and retrieves functions to control it.

4. **Callback Registration**:
   - `display.register_select_callback(print_xy_click)`: Registers `print_xy_click` to be called when a shape is selected.
   - `display.register_select_callback(compute_bbox)`: Registers `compute_bbox` to be called when a shape is selected.

5. **Shape Creation**:
   - `my_torus = BRepPrimAPI_MakeBox(10.0, 20.0, 30.0).Shape()`: Creates a box with dimensions 10x20x30.
   - `my_box = BRepPrimAPI_MakeTorus(30.0, 5.0).Shape()`: Creates a torus with a major radius of 30 and a minor radius of 5.

6. **Shape Display**:
   - `display.DisplayShape(my_torus)`: Displays the created box.
   - `display.DisplayShape(my_box, update=True)`: Displays the created torus and updates the display.

7. **Start Display Loop**:
   - `start_display()`: Starts the GUI event loop to display the shapes and handle user interactions.

In summary, this script initializes a graphical display, creates a box and a torus, displays them, and sets up callbacks to print information and compute the bounding box of these shapes when they are selected.

## core_display_quality.py

This Python script, part of the `pythonOCC` library, demonstrates how to adjust the display quality of 3D shapes in a graphical interface. Here's a concise breakdown of its functionality:

1. **Imports and Initialization**:
   - The script imports necessary modules from the `OCC` library, which is a set of Python bindings for the Open CASCADE Technology (OCCT), a software development platform for 3D CAD, CAM, CAE.
   - It initializes a 3D display using `init_display()` from `OCC.Display.SimpleGui`.

2. **Retrieve and Print Default Display Quality Settings**:
   - The script retrieves the current display quality settings for the `AISInteractiveContext` (which manages the display of interactive objects) using `DeviationCoefficient()` and `DeviationAngle()` methods.
   - It prints these default settings to the console.

3. **Improve Display Quality**:
   - The script improves the display quality by reducing the deviation coefficient and deviation angle by a factor of 10. This means the shapes will be rendered with higher precision, but at the cost of increased memory usage.

4. **Create and Display a Cylinder**:
   - A cylinder is created using `BRepPrimAPI_MakeCylinder` with a radius and height of 50 units.
   - The cylinder shape is displayed in the initialized 3D viewer.

5. **Adjust Hidden Line Removal (HLR) Quality**:
   - The script retrieves and prints the current deviation angle for HLR.
   - It then improves the HLR quality by reducing this angle by the same factor of 10.

6. **Display Settings and Loop**:
   - The view is set to an isometric view and all displayed objects are fitted within the view.
   - The script enters the main display loop using `start_display()`.

### Summary
The script essentially sets up a 3D viewer, improves the display quality settings for rendering 3D shapes, creates and displays a cylinder, and adjusts the hidden line removal quality before entering the display loop. The improvements in quality result in more precise rendering at the expense of higher memory consumption.

## core_topology_holes_in_face.py

This Python code uses the `pythonOCC` library, which is a set of Python bindings for the Open CASCADE Technology (OCCT) 3D modeling library. The primary purpose of this code is to create a planar face with three circular holes and display it using a simple graphical user interface.

Here's a breakdown of its functionality:

1. **Imports**: The code imports necessary classes and functions from the `OCC.Core` and `OCC.Display.SimpleGui` modules.

2. **Initialization of Display**: `init_display()` initializes the display window and returns functions for controlling the display.

3. **Function `holes_in_face`**:
    - Creates a plane (`gp_Pln`).
    - Defines three circles (`gp_Circ`) on the plane and sets their locations to specific points.
    - Converts these circles into edges using `BRepBuilderAPI_MakeEdge`.
    - Converts these edges into wires using `BRepBuilderAPI_MakeWire`.
    - Creates a rectangular face on the plane using `BRepBuilderAPI_MakeFace`.
    - Adds the wires (representing circles) as holes in the face by reversing the wires before adding them to the face.
    - Checks if the face creation is successful and returns the resulting shape.

4. **Main Execution**:
    - Calls the `holes_in_face` function to create the face with holes.
    - Displays the face using the `display.DisplayShape` function.
    - Starts the display loop with `start_display()` to visualize the shape.

### Summary
The code constructs a rectangular planar face with three circular holes, each located at specified coordinates, and displays this face using a simple GUI. It demonstrates the use of geometric primitives, shape construction, and visualization capabilities provided by the `pythonOCC` library.

## core_load_iges.py

This Python code is designed to read and display a 3D model from an IGES file using the pythonOCC library, which is a set of Python bindings for the Open CASCADE Technology (OCCT) CAD kernel.

Here's a step-by-step breakdown of its functionality:

1. **License Information**: The initial comments provide licensing information, indicating that the code is part of pythonOCC and is distributed under the GNU Lesser General Public License.

2. **Imports**:
   - `from __future__ import print_function`: Ensures compatibility with both Python 2 and 3 by using the print function from Python 3.
   - `from OCC.Display.SimpleGui import init_display`: Imports the `init_display` function from the `OCC.Display.SimpleGui` module, which is used to initialize the display window.
   - `from OCC.Extend.DataExchange import read_iges_file`: Imports the `read_iges_file` function from the `OCC.Extend.DataExchange` module, which is used to read IGES files.

3. **Reading the IGES File**:
   - `shapes = read_iges_file("../../pythonocc-core/test/test_io/example_45_faces.iges")`: Reads the IGES file located at the specified path and stores the resulting shapes in the `shapes` variable.

4. **Initializing the Display**:
   - `display, start_display, add_menu, add_function_to_menu = init_display()`: Initializes the display window and assigns the returned functions to variables. `display` is used to control the display, `start_display` starts the display loop, `add_menu` and `add_function_to_menu` are for adding menus and functions to the GUI, but they are not used in this script.

5. **Displaying the Shape**:
   - `display.DisplayShape(shapes, update=True)`: Displays the shapes read from the IGES file in the initialized display window. The `update=True` argument ensures that the display is updated immediately.

6. **Starting the Display Loop**:
   - `start_display()`: Starts the display loop, which keeps the window open and responsive to user interactions.

In summary, this script reads a 3D model from an IGES file and displays it in a graphical window using the pythonOCC library.

## core_display_set_edge_color.py

This Python script utilizes the `pythonOCC` library to create and display a 3D box with specific visual properties in an interactive graphical window. Here's a breakdown of its functionality and purpose:

1. **License Information**:
   - The script includes comments about the GNU Lesser General Public License, under which the `pythonOCC` library is distributed. This section informs users about their rights to redistribute and modify the software.

2. **Imports**:
   - The script imports various modules from the `OCC` package, which is part of the `pythonOCC` library. These modules provide functions for creating geometric shapes, managing their display, and setting visual attributes.

3. **Initialization**:
   - `init_display()` is called to initialize the display window and retrieve functions to control the display (e.g., `start_display`, `add_menu`).

4. **Box Creation**:
   - A 3D box with dimensions 60x60x50 units is created using `BRepPrimAPI_MakeBox(60, 60, 50).Shape()`.

5. **Display Context**:
   - The display context is retrieved via `display.Context`, which is used to manage how shapes are shown in the display.

6. **Shape Display**:
   - An `AIS_Shape` object is created to represent the box in the display context.
   - The shape is displayed using `context.Display(aisShape, True)`.

7. **Visual Properties**:
   - **Transparency**: The shape's transparency is set to 0.6 (60%) using `context.SetTransparency(aisShape, 0.6, True)`.
   - **Color**: The shape's color is set to red using `context.SetColor(aisShape, col, True)`, where `col` is a `Quantity_Color` object initialized to red.
   - **Highlighting**: The shape is highlighted with the specified color using `context.HilightWithColor(aisShape, drawer, True)`.

8. **View Configuration**:
   - The display is set to an isometric view using `display.View_Iso()`.
   - The view is adjusted to fit the entire shape within the display window using `display.FitAll()`.

9. **Start Display**:
   - The interactive display is started with `start_display()`, allowing the user to interact with the 3D window.

In summary, this script demonstrates how to create a 3D box, set its transparency and color, and display it in an interactive window using the `pythonOCC` library.

## core_display_colorscale.py

The provided Python code is a script that utilizes the `pythonOCC` library, which is a set of Python bindings for the OpenCASCADE Technology (OCCT) CAD kernel. The purpose and functionality of this script can be summarized as follows:

1. **License Information**: The script starts with a shebang line and comments specifying that it is part of the `pythonOCC` project, which is distributed under the GNU Lesser General Public License (LGPL).

2. **Imports**: The script imports various modules from the `OCC.Core` package, which are necessary for creating 3D shapes, displaying color scales, and managing graphical transformations. It also imports the `init_display` function from `OCC.Display.SimpleGui` to initialize the display window.

3. **Initialization**: The `init_display` function is called to initialize the display window and retrieve several functions (`display`, `start_display`, `add_menu`, `add_function_to_menu`) for managing the display.

4. **Creating a 3D Box**: A 3D box shape (`myBox`) is created using the `BRepPrimAPI_MakeBox` function with dimensions 60x60x50.

5. **Color Scale Setup**:
   - An `AIS_ColorScale` object (`colorscale`) is instantiated.
   - Various properties of the color scale are retrieved, such as minimum and maximum range, number of intervals, text height, label position, and title.
   - The size of the color scale is set to 300x300.
   - The range of the color scale is set from 0.0 to 10.0 with 10 intervals.
   - The Z-layer of the color scale is set to -5.
   - A transformation persistence is applied to the color scale to keep it in the lower left corner of the display.
   - The color scale is marked to update its display.

6. **Displaying the Color Scale and Box**:
   - The color scale is displayed using `display.Context.Display`.
   - The 3D box shape (`myBox`) is displayed using `display.DisplayShape`.

7. **Starting the Display Loop**: The `start_display()` function is called to start the display loop, allowing the user to interact with the graphical window.

### Summary
The script creates a 3D box and a color scale, configures their properties, and displays them in a graphical window. The color scale is positioned in the lower left corner of the window and is set to update its display properties. The script uses the `pythonOCC` library to handle the creation and display of the 3D objects and graphical elements.

## core_geometry_ellipsoid.py

This Python code leverages the `pythonOCC` library, which is a set of Python bindings for the Open CASCADE Technology (OCCT), a software development platform for 3D CAD, CAM, CAE, etc. The purpose of this code is to create and display a 3D geometric model involving a boolean intersection operation between an ellipsoid and a box. Here is a step-by-step breakdown of its functionality:

1. **Imports**:
   - The code imports several classes and functions from the `OCC.Core` module for creating geometric shapes, transformations, and performing boolean operations.
   - It also imports functions for initializing and managing the display window from `OCC.Display.SimpleGui`.

2. **Initialization**:
   - The display window and related functions (`display`, `start_display`, `add_menu`, `add_function_to_menu`) are initialized using `init_display()`.

3. **Sphere Creation**:
   - A sphere is created with a center at the origin `(0.0, 0.0, 0.0)` and a radius of `50.0` units using `BRepPrimAPI_MakeSphere`.

4. **Ellipsoid Creation**:
   - The sphere is transformed into an ellipsoid using a general transformation (`gp_GTrsf`) that scales the sphere along the x, y, and z axes by factors `17.1`, `17.1`, and `3.5` respectively, and translates it along the y-axis by `112.2` units.

5. **Box Creation**:
   - A box is created with opposite corners at `(-1000, -1000, -1000)` and `(1000, 112.2, 1000)` using `BRepPrimAPI_MakeBox`.

6. **Boolean Intersection**:
   - A boolean intersection operation is performed between the ellipsoid and the box using `BRepAlgoAPI_Common`. This results in a shape that is the common volume of the ellipsoid and the box.
   - The code checks if the resulting shape (`common`) is null, raising an `AssertionError` if it is.

7. **Display**:
   - The box, ellipsoid, and the resulting intersection shape are displayed in the initialized display window with specified colors (`BLACK`) and transparency (`0.8` for the box and ellipsoid, `0.8` with update for the common shape).

8. **Start Display**:
   - The display loop is started using `start_display()` to render the shapes and allow user interaction.

In summary, the code creates a sphere, transforms it into an ellipsoid, intersects this ellipsoid with a box, and displays the resulting shapes using the `pythonOCC` library.

## core_display_camera_projection.py

This Python code is part of the `pythonOCC` library, which is used for 3D CAD (Computer-Aided Design) modeling and visualization. The primary purpose of this script is to display a 3D model of a motor and provide various camera projection modes for viewing the model. Here's a detailed breakdown of its functionality:

1. **Imports**: The code imports necessary modules from the `pythonOCC` library and the `sys` module for system-specific parameters and functions.

2. **Camera Projection Functions**: 
   - `perspective(event=None)`: Sets the camera to perspective projection and fits the view to display all objects.
   - `orthographic(event=None)`: Sets the camera to orthographic projection and fits the view.
   - `anaglyph_red_cyan(event=None)`: Sets the camera to anaglyph red-cyan mode (simple) and fits the view.
   - `anaglyph_red_cyan_optimized(event=None)`: Sets the camera to anaglyph red-cyan mode (optimized) and fits the view.
   - `anaglyph_yellow_blue(event=None)`: Sets the camera to anaglyph yellow-blue mode and fits the view.
   - `anaglyph_green_magenta(event=None)`: Sets the camera to anaglyph green-magenta mode and fits the view.
   - `exit(event=None)`: Exits the application.

3. **Main Script Execution**:
   - Initializes the display using `init_display()`, which sets up the GUI elements needed for visualization.
   - Loads a 3D model of a motor from a file (`Motor-c.brep`) using `breptools.Read()` and displays it.
   - Adds a menu titled "camera projection" with various camera projection modes and an exit option.
   - Starts the display loop with `start_display()` to render the GUI and handle user interactions.

In summary, this script sets up a 3D viewer for a motor model with multiple camera projection options, allowing the user to switch between different viewing modes (perspective, orthographic, and various anaglyph modes) and exit the application.

## core_topology_splitter.py

This Python code is a part of the `pythonOCC` library, which is a set of Python bindings for the Open Cascade Technology (OCCT), a software development platform for 3D CAD, CAM, CAE, etc. The purpose of this code is to demonstrate how to use the `BOPAlgo_Splitter` class to split geometric shapes (faces and edges) using the `pythonOCC` library. It provides two main functionalities: splitting a face with an edge and splitting an edge with a face, and visualizing the results.

Here is a detailed breakdown of the code:

1. **Imports and Initialization**:
   - Imports necessary modules from `OCC.Core` and `OCC.Extend`.
   - Initializes the display using `init_display()` from `OCC.Display.SimpleGui`.

2. **Function Definitions**:
   - `split_face_with_edge(event=None)`: 
     - Creates a plane face and an edge.
     - Uses `BOPAlgo_Splitter` to split the face with the edge.
     - Displays the resulting faces in the viewer.
   - `split_edge_with_face(event=None)`:
     - Creates a plane face and an edge.
     - Uses `BOPAlgo_Splitter` to split the edge with the face.
     - Displays the resulting edges in the viewer with different colors.
   - `exit(event=None)`: Exits the application.

3. **Main Execution Block**:
   - Adds a menu titled "BOPAlgo Splitter Example" to the display.
   - Adds the functions `split_face_with_edge`, `split_edge_with_face`, and `exit` to the menu.
   - Starts the display loop with `start_display()`.

**Functionality Summary**:
- **split_face_with_edge**: Creates a face and an edge, splits the face using the edge, and displays the resulting faces.
- **split_edge_with_face**: Creates a face and an edge, splits the edge using the face, and displays the resulting edges in different colors.
- **exit**: Exits the application.

The code is designed to be run as a standalone script, providing a graphical user interface to visualize the results of splitting operations on geometric shapes.

## core_webgl_mesh_quality.py

This Python script is designed to create and render 3D models of tori (doughnut-shaped objects) using the `pythonOCC` library, which is a set of Python bindings for the Open CASCADE Technology (OCCT) framework. The script utilizes the `threejs_renderer` to visualize the tori in a web browser using Three.js, a popular JavaScript library for 3D graphics.

Here is a breakdown of the script's functionality:

1. **Import Statements**:
   - `from __future__ import print_function`: Ensures compatibility of the print function with Python 2 and 3.
   - Imports necessary modules from `pythonOCC` for rendering (`threejs_renderer`), creating tori (`BRepPrimAPI_MakeTorus`), and manipulating shapes (`gp_Vec`, `translate_shp`).

2. **Renderer Initialization**:
   - `my_ren = threejs_renderer.ThreejsRenderer()`: Initializes the Three.js renderer.

3. **Creating Tori**:
   - Three tori are created using `BRepPrimAPI_MakeTorus(20, 5).Shape()`, which defines tori with a major radius of 20 and a minor radius of 5.
   - The second and third tori are translated along the x-axis by 60 units and -60 units respectively using the `translate_shp` function and `gp_Vec`.

4. **Rendering Tori with Different Mesh Qualities**:
   - The first torus (`torus_shp1`) is rendered with default mesh quality and colored red.
   - The second torus (`torus_shp2`) is rendered with better mesh quality (more triangles, higher computational cost) and colored green.
   - The third torus (`torus_shp3`) is rendered with worse mesh quality (fewer triangles, lower computational cost) and colored blue.

5. **Output and Rendering**:
   - The script prints messages to the console indicating the quality of each torus being computed.
   - `my_ren.render()`: Finalizes the rendering process and displays the tori in a web browser.

In summary, the script demonstrates how to create and render 3D tori with varying mesh qualities using the `pythonOCC` library and Three.js renderer.

## core_shape_properties.py

This Python script utilizes the `pythonOCC` library to create and analyze 3D shapes, specifically focusing on computing inertia properties of a cube and surface areas of a box's faces. Here's a breakdown of its purpose and functionality:

### Purpose:
The script performs geometric computations on 3D shapes using the `pythonOCC` library, which is a set of Python bindings for the OpenCASCADE geometric modeling kernel. It specifically:

1. **Computes and displays the inertia properties of a cubic shape.**
2. **Computes and displays the surface area of each face of a rectangular box.**

### Functionality:

#### 1. `cube_inertia_properties()`:
- **Purpose:** Computes and displays the inertia properties (mass, center of gravity, and matrix of inertia) of a cubic box with dimensions 50x50x50 units.
- **Steps:**
  1. Creates a cubic box shape with dimensions 50x50x50 units.
  2. Computes the volume properties of the cube.
  3. Retrieves the mass, center of gravity, and inertia matrix from the computed properties.
  4. Prints the mass, center of gravity coordinates, and the matrix of inertia.

#### 2. `shape_faces_surface()`:
- **Purpose:** Computes and displays the surface area of each face of a rectangular box with dimensions 50x30x10 units.
- **Steps:**
  1. Creates a rectangular box shape with dimensions 50x30x10 units.
  2. Iterates over each face of the box.
  3. Computes the surface properties of each face.
  4. Retrieves and prints the surface area for each face.

### Execution:
- When the script is executed as the main module, it calls both `cube_inertia_properties()` and `shape_faces_surface()` functions to perform the described computations and print the results.

### Libraries and Modules:
- **`OCC.Core.BRepPrimAPI`**: Used for creating primitive shapes like boxes.
- **`OCC.Core.GProp`**: Used for handling geometric properties.
- **`OCC.Core.BRepGProp`**: Used for computing geometric properties like volume and surface area.
- **`OCC.Extend.TopologyUtils`**: Used for exploring the topology of shapes (e.g., iterating over faces).

### Summary:
The script is a demonstration of how to use the `pythonOCC` library to create 3D shapes, compute their physical properties, and print these properties to the console. It focuses on a cubic box for inertia properties and a rectangular box for surface area computations of its faces.

## core_display_qt5_app.py

This Python code creates a graphical user interface (GUI) application using PyQt5 and pythonOCC, a set of Python bindings for the Open CASCADE Technology (OCCT) 3D CAD kernel. The application allows users to display and erase a 3D box shape within the GUI. Here is a detailed breakdown of its functionality:

1. **Imports**:
   - Imports necessary modules from `os`, `sys`, `PyQt5`, and `OCC.Core`.
   - Loads the PyQt5 backend for the OCC display.

2. **Class Definition (`App`)**:
   - Inherits from `QDialog` to create a dialog window.
   - Initializes the main window with a title, size, and position.
   - Sets up the user interface (UI) components.

3. **UI Initialization (`initUI`)**:
   - Sets the window title and geometry.
   - Creates a horizontal layout containing buttons and a 3D viewer.
   - Adds the horizontal layout to the main window layout.
   - Initializes the 3D viewer (`qtDisplay.qtViewer3d`).
   - Sets up the display driver and resizes the canvas.

4. **Creating the Horizontal Layout (`createHorizontalLayout`)**:
   - Creates a group box to contain the layout.
   - Adds two buttons: "Display Box" and "Erase Box".
   - Connects the buttons to their respective methods (`displayBOX` and `eraseBOX`).
   - Adds the 3D viewer to the layout and sets the layout to the group box.

5. **Displaying the Box (`displayBOX`)**:
   - Creates a 3D box shape using `BRepPrimAPI_MakeBox`.
   - Displays the box shape in the 3D viewer.
   - Adjusts the view to fit the entire box.

6. **Erasing the Box (`eraseBOX`)**:
   - Erases the displayed box from the 3D viewer.

7. **Main Execution Block**:
   - Creates an instance of `QApplication`.
   - Instantiates the `App` class to create the GUI.
   - Runs the application event loop unless the `APPVEYOR` environment variable is set.

Overall, this code sets up a simple PyQt5 application with buttons to display and erase a 3D box using the pythonOCC library.

## core_shape_pickling.py

This Python script is designed to create a 3D box shape using the `pythonOCC` library, serialize it into a string using the `pickle` module, and then deserialize it back into a box shape. Here is a detailed breakdown of its functionality:

1. **Shebang Line**: 
   ```python
   #! /usr/bin/python
   ```
   This indicates that the script should be run using the Python interpreter.

2. **License Information**: 
   The script includes a block of comments providing licensing information, indicating that it is part of the `pythonOCC` project and is distributed under the GNU Lesser General Public License.

3. **Imports**: 
   ```python
   from __future__ import print_function
   from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
   import pickle
   ```
   - The `print_function` import ensures compatibility with Python 3's `print` function.
   - `BRepPrimAPI_MakeBox` is imported from the `OCC.Core.BRepPrimAPI` module, which is part of the `pythonOCC` library used for creating 3D shapes.
   - The `pickle` module is used for serializing and deserializing Python objects.

4. **Create Shape**: 
   ```python
   box1 = BRepPrimAPI_MakeBox(10.0, 10.0, 10.0).Shape()
   ```
   This line creates a 3D box shape with dimensions 10x10x10 units.

5. **Serialize Shape**: 
   ```python
   box_dump_string = pickle.dumps(box1)
   print("Box (10,10,10) dump:\n", box_dump_string)
   ```
   The `box1` object is serialized into a string using `pickle.dumps()`. The serialized string is then printed to the console.

6. **Deserialize Shape**: 
   ```python
   box2 = pickle.loads(box_dump_string)
   assert not box2.IsNull()
   print("Box successfully loaded.")
   ```
   The serialized string is deserialized back into a `box2` object using `pickle.loads()`. An assertion checks that the deserialized object is not null, and a message is printed to confirm successful loading.

In summary, this script demonstrates how to create a 3D box using `pythonOCC`, serialize it with `pickle`, and then deserialize it back into a shape, ensuring that the deserialized shape is valid.

## core_geometry_geomplate.py

The provided Python code is a script that utilizes the `pythonOCC` library, which is a set of Python bindings for the Open CASCADE Technology (OCCT) library. The script is designed for creating and manipulating complex geometric shapes and surfaces, specifically focusing on building n-sided patches, plate surfaces, and solving for surfaces with specific radius constraints.

### Key Functionalities:

1. **Initialization and Imports:**
   - The script imports various modules from `pythonOCC` and other dependencies such as `scipy` (if available) for optimization tasks.
   - It initializes a display window using `init_display()` from `OCC.Display.SimpleGui`.

2. **Utility Functions:**
   - `make_n_sided(edges, points, continuity)`: Creates an n-sided patch surface constrained by given edges and points, with a specified level of continuity.
   - `make_closed_polygon(*args)`: Constructs a closed polygon from a list of points.
   - `build_plate(polygon, points)`: Builds a surface from constraining polygons and points using `GeomPlate_BuildPlateSurface`.
   - `radius_at_uv(face, u, v)`: Calculates the mean radius at a given u,v coordinate on a surface.
   - `uv_from_projected_point_on_face(face, pt)`: Projects a point onto a face and returns the corresponding u,v coordinates.

3. **Main Functionalities:**
   - `geom_plate(event=None)`: Demonstrates the creation of a geometric plate by constructing a closed polygon and a face constrained by a point.
   - `solve_radius(event=None)`: Uses `scipy.optimize.fsolve` to adjust the height of a point constraining a plate to achieve a desired radius at that point.
   - `build_geom_plate(edges)`: Builds a plate surface from a network of edges.
   - `build_curve_network(event=None)`: Mimics the curve network surfacing command from Rhino by importing an IGES file, building a geometric plate from its edges, and displaying the result.

4. **Class:**
   - `RadiusConstrainedSurface`: A class that constructs a surface with a specific radius at a given point. It uses an iterative method to adjust the surface until the target radius is achieved.

5. **Menu and Event Handling:**
   - The script adds menu items for different functionalities (`geom_plate`, `solve_radius`, `build_curve_network`, `exit`) and binds them to corresponding functions.
   - The `start_display()` function initiates the graphical display loop.

### Usage:
- The script can be run directly. It initializes a graphical display and provides a menu to interact with the different functionalities.
- It demonstrates advanced geometric modeling techniques and is useful for tasks requiring precise control over surface properties and constraints.

### Dependencies:
- `pythonOCC`: The main library for geometric modeling.
- `scipy`: Used for optimization tasks (optional, but required for `solve_radius` functionality).

This script is particularly useful for engineers, designers, and developers working with 3D geometric modeling, CAD applications, and related fields.

## core_webgl_threejs_torus.py

This Python script is designed to create and render a 3D torus using the `pythonOCC` library, which is a set of Python bindings for the Open CASCADE Technology (OCCT) framework. Here's a step-by-step breakdown of its functionality:

1. **Shebang and License Information**:
   - The script starts with a shebang line (`#!/usr/bin/env python`) to indicate that it should be run using the Python interpreter.
   - It includes license information, specifying that the code is part of the `pythonOCC` project and is distributed under the GNU Lesser General Public License (LGPL).

2. **Imports**:
   - `from OCC.Display.WebGl import threejs_renderer`: Imports the `threejs_renderer` module, which is used for rendering 3D shapes in a web browser using the Three.js library.
   - `from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeTorus`: Imports the `BRepPrimAPI_MakeTorus` class, which is used to create a 3D torus shape.

3. **Create a Torus**:
   - `torus_shp = BRepPrimAPI_MakeTorus(20.0, 10.0).Shape()`: Creates a torus shape with a major radius of 20.0 units and a minor radius of 10.0 units.

4. **Renderer Initialization**:
   - `my_renderer = threejs_renderer.ThreejsRenderer()`: Initializes a renderer object that uses Three.js to display the shape.

5. **Display and Render the Shape**:
   - `my_renderer.DisplayShape(torus_shp)`: Adds the torus shape to the renderer for display.
   - `my_renderer.render()`: Renders the shape, generating the necessary output to visualize the torus in a web browser.

In summary, the script's purpose is to create a 3D torus and render it in a web browser using the `pythonOCC` library and Three.js.

## core_topology_prism.py

This Python code is designed to create and display a 3D geometric object using the pythonOCC library, which is a set of Python bindings for the Open CASCADE Technology (OCCT) 3D modeling library. Here's a breakdown of its functionality:

1. **Import Statements**:
    - The code imports necessary modules from the `OCC.Core` package to handle geometric points, vectors, B-spline curves, and basic 3D shapes.
    - It also imports the `init_display` function from `OCC.Display.SimpleGui` to initialize the display window.

2. **Initialization**:
    - The `init_display()` function sets up the display environment and returns several functions (`display`, `start_display`, `add_menu`, `add_function_to_menu`) for managing the display.

3. **Prism Function**:
    - **B-Spline Profile**:
        - An array of 5 points (`gp_Pnt` objects) is created to define a B-spline curve.
        - These points are used to generate a B-spline curve (`GeomAPI_PointsToBSpline`), which is then converted into an edge (`BRepBuilderAPI_MakeEdge`).
    - **Linear Path**:
        - Two points (`gp_Pnt`) define the start and end of a linear path.
        - A vector (`gp_Vec`) is created from the starting point to the end point.
        - An edge representing this path is created (`BRepBuilderAPI_MakeEdge`).
    - **Extrusion**:
        - The B-spline profile is extruded along the vector to create a 3D prism shape (`BRepPrimAPI_MakePrism`).
    - **Display**:
        - The profile, starting point, end point, path, and the resulting prism are displayed in the 3D viewer.

4. **Main Execution**:
    - When the script is run directly, the `prism()` function is called to create and display the 3D prism.
    - The `start_display()` function is called to start the display loop, allowing the user to interact with the 3D viewer.

In summary, this code creates a 3D prism by extruding a B-spline curve along a linear path and displays the result using the pythonOCC library's visualization tools.

## core_display_material_shape.py

This Python script is designed to create and display a series of cylinders, each with a different material appearance. It uses the `pythonOCC` library, which is a set of Python wrappers for the OpenCASCADE geometric modeling kernel.

### Detailed Breakdown:

1. **Shebang and Licensing Information:**
   - The script starts with a shebang (`#!/usr/bin/env python`) to indicate that it should be run using the Python interpreter.
   - It includes comments about licensing, indicating that the code is part of `pythonOCC` and is distributed under the GNU Lesser General Public License.

2. **Imports:**
   - The script imports various modules and classes from the `OCC.Core` package, which is part of `pythonOCC`.
   - It imports material constants from `OCC.Core.Graphic3d`.
   - It imports geometric and shape manipulation classes from `OCC.Core.gp` and `OCC.Core.BRepPrimAPI`.
   - It imports display initialization functions from `OCC.Display.SimpleGui`.

3. **Display Initialization:**
   - The `init_display()` function is called to initialize the display environment. This function returns several objects used to manage the display (`display`, `start_display`, `add_menu`, `add_function_to_menu`).

4. **Material List:**
   - A list named `available_materials` is defined, containing various material constants that can be applied to shapes.

5. **Cylinder Creation and Display:**
   - A base cylinder shape (`s`) is created using the `BRepPrimAPI_MakeCylinder` function, with a specified radius of 30 units and a height of 200 units.
   - A loop iterates over each material in the `available_materials` list:
     - The base cylinder `s` is translated along the x-axis by `delta_x` units to create a new shape `s2`.
     - The new shape `s2` is displayed with the current material using the `display.DisplayShape` method.
     - The `delta_x` value is incremented to position the next cylinder without overlapping the previous one.

6. **Final Display Adjustment:**
   - The `display.FitAll()` method is called to adjust the view to fit all displayed shapes within the viewport.
   - The `start_display()` function is called to start the interactive display loop.

### Purpose:
The primary purpose of this script is to demonstrate the visualization of different material appearances on a simple geometric shape (a cylinder) using the `pythonOCC` library. It showcases how to create shapes, apply different materials, and display them in a 3D viewer. This can be useful for applications in CAD, CAM, or other fields requiring 3D visualization and modeling.

## core_meshDS_numpy_material.py

This Python code is designed to generate and visualize a 3D triangular mesh using the Open CASCADE Technology (OCCT) library, along with NumPy and SciPy for mesh generation. Here is a clear, concise description of its purpose and functionality:

1. **Imports Libraries**:
   - `numpy` and `scipy.spatial.Delaunay` for mesh generation.
   - Various modules from `OCC.Core` and `OCC.Display` for handling mesh data, visualization, and display.

2. **Mesh Generation Function (`getMesh`)**:
   - Generates a 2D grid of points using `numpy.linspace` and `numpy.meshgrid`.
   - Computes a 3D surface using a mathematical function involving sine and inverse square.
   - Uses Delaunay triangulation to create a mesh from the 2D points.
   - Returns the vertices and faces of the mesh.

3. **Mesh Data Preparation**:
   - Calls `getMesh` to obtain vertices and faces of the mesh.

4. **Mesh Data Source**:
   - Creates a `MeshDS_DataSource` object with the generated vertices and faces.

5. **Mesh Visualizer**:
   - Creates a `MeshVS_Mesh` object to visualize the mesh.
   - Associates the mesh visualizer with the mesh data source.

6. **Presentation Builder**:
   - Creates a `MeshVS_MeshPrsBuilder` to build the visual presentation of the mesh.
   - Sets up material properties using `Graphic3d_PBRMaterial` and `Graphic3d_MaterialAspect` with a green color.
   - Configures the visual appearance of the mesh (e.g., disabling edges and nodes display).
   - Adds the presentation builder to the mesh visualizer.

7. **Display Setup**:
   - Initializes the display using `init_display`.
   - Displays the mesh visualizer in the graphical context.
   - Fits the view to show the entire mesh.
   - Starts the display loop to render the visualization.

In summary, this code generates a 3D triangular mesh from a mathematical function, sets up its visual properties, and displays it using the OCCT library's visualization tools.

## core_gfa.py

The provided Python code is a script that leverages the `pythonOCC` library to create and display 3D shapes using OpenCASCADE Technology (OCCT). Here's a clear and concise description of its purpose and functionality:

### Purpose:
The script is designed to create two 3D box shapes, perform a Boolean operation to combine them, and display the resulting shape in a graphical window.

### Functionality:
1. **Import Libraries:**
   - `init_display` from `OCC.Display.SimpleGui` to initialize the display window.
   - `BRepPrimAPI_MakeBox` from `OCC.Core.BRepPrimAPI` to create box shapes.
   - `BOPAlgo_Builder` from `OCC.Core.BOPAlgo` to perform Boolean operations on shapes.

2. **Initialize Display:**
   - The `init_display()` function initializes the display and returns several functions (`display`, `start_display`, `add_menu`, `add_function_to_menu`) for manipulating the graphical window.

3. **Create Box Shapes:**
   - `my_box1` is created as a box with dimensions 10.0 x 20.0 x 30.0.
   - `my_box2` is created as a box with dimensions 20.0 x 1.0 x 30.0.

4. **Boolean Operation:**
   - An instance of `BOPAlgo_Builder` is created to perform Boolean operations.
   - Both boxes (`my_box1` and `my_box2`) are added as arguments to the builder.
   - The builder is set to run in parallel mode for potentially improved performance.
   - The `Perform()` method is called to execute the Boolean operation.
   - If the builder encounters any errors, an assertion error is raised with the error details.

5. **Display Result:**
   - The resulting shape from the Boolean operation is retrieved using `builder.Shape()`.
   - This result is then displayed in the initialized graphical window using `display.DisplayShape(result, update=True)`.

6. **Start Display Loop:**
   - The `start_display()` function is called to start the event loop for the graphical window, allowing the user to interact with the displayed shape.

### Summary:
The script demonstrates how to use the `pythonOCC` library to create and manipulate 3D shapes through Boolean operations and visualize the results in a graphical interface.

## core_load_step_ap203.py

This Python code is part of the `pythonOCC` library, which is a set of Python bindings for the Open CASCADE Technology (OCCT) framework, used for 3D CAD, CAM, CAE, etc. The script specifically focuses on importing and displaying 3D models from STEP files.

Here is a concise description of its functionality:

1. **Imports and Initialization**:
   - The script imports necessary modules and functions from `pythonOCC`, including tools for handling colors, displaying GUI, exploring topology, and reading STEP files.
   - It also imports standard Python libraries like `random`, `os`, and `sys`.

2. **Function Definitions**:
   - `import_as_one_shape(event=None)`: This function reads a STEP file (`as1_pe_203.stp` located in the `../assets/models/` directory) and displays it as a single shape in the viewer. It clears any existing shapes before displaying the new one.
   - `import_as_multiple_shapes(event=None)`: This function reads the same STEP file but displays each solid in the compound STEP file as individual shapes with random colors. It uses the `TopologyExplorer` to iterate over the solids in the compound.
   - `exit(event=None)`: This function exits the application by calling `sys.exit()`.

3. **Main Execution**:
   - The script initializes the display using `init_display()`, which returns the display control functions.
   - It adds a menu named "STEP import" with two options: one to import the STEP file as a single shape and another to import it as multiple shapes.
   - The script then starts the display loop with `start_display()`, which keeps the GUI running and responsive to user interactions.

**Purpose**:
The purpose of this script is to provide a simple GUI-based application for importing and visualizing 3D models from STEP files using the `pythonOCC` library. It demonstrates how to read STEP files, manipulate and display 3D shapes, and interact with the graphical display.

## core_mesh_gmsh.py

This Python script is designed to create a 3D torus shape, convert it into a mesh using Gmsh, and display the resulting mesh using the pythonOCC library. Here's a breakdown of its functionality:

1. **Licensing and Imports**:
   - The script starts with a shebang and licensing information.
   - Essential modules and functions are imported, including those from the `OCC` library, which is used for 3D CAD modeling.

2. **Function Definition**:
   - `mesh_shape(a_topods_shape)`: This function takes a BRep shape (a CAD file format) as input and performs the following steps:
     - Writes the shape to a BRep file named `shape.brep`.
     - Creates a Gmsh `.geo` file with specific mesh characteristics.
     - Calls Gmsh to generate an STL file (`shape.stl`) from the `.geo` file.
     - Reads and returns the STL file if Gmsh successfully creates it; otherwise, it prints an error message and exits.

3. **Main Script Execution**:
   - A torus shape is created using `BRepPrimAPI_MakeTorus` with specified dimensions (major radius 40.0 and minor radius 10.0).
   - The `mesh_shape` function is called to convert the torus shape into a mesh.
   - The `init_display` function is used to set up the display environment.
   - The mesh shape is displayed using the `display.DisplayShape` function.
   - The display event loop is started with `start_display`.

### Detailed Steps:
1. **Creating the Torus**:
   - `BRepPrimAPI_MakeTorus(40.0, 10.0).Shape()` creates a torus shape with a major radius of 40.0 and a minor radius of 10.0.

2. **Writing the Shape to a BRep File**:
   - `breptools_Write(a_topods_shape, "shape.brep")` writes the shape to a file named `shape.brep`.

3. **Generating the Gmsh .geo File**:
   - A string containing Gmsh commands is written to `shape.geo`, specifying mesh characteristics and referencing the `shape.brep` file.

4. **Calling Gmsh**:
   - `os.system("gmsh shape.geo -2 -o shape.stl -format stl")` runs Gmsh to generate an STL file from the `.geo` file.

5. **Reading the STL File**:
   - If Gmsh succeeds, the STL file is read using `read_stl_file("shape.stl")`.

6. **Displaying the Mesh**:
   - The mesh shape is displayed using the `init_display` and `display.DisplayShape` functions from the `OCC.Display.SimpleGui` module.

### Dependencies:
- The script relies on the `pythonOCC` library for CAD operations and display.
- Gmsh must be installed and available in the system's PATH for mesh generation.

### Summary:
The script demonstrates how to create a 3D torus shape, convert it to a mesh using Gmsh, and visualize the mesh using the `pythonOCC` library. It integrates CAD modeling with mesh generation and visualization seamlessly.

## core_webgl_x3dom_bigfile_multipleshapes.py

The provided Python script is designed to read and display a 3D model from a STEP file using the `pythonOCC` library, which is a set of Python bindings for the Open CASCADE Technology (OCCT) framework. Here's a breakdown of its purpose and functionality:

1. **License and Metadata**:
   - The script includes comments at the beginning that specify its licensing under the GNU Lesser General Public License and credits the author, Thomas Paviot.

2. **Imports**:
   - The script imports necessary modules: `os` and `sys` for file and system operations, and several modules from the `OCC` package for handling STEP files and rendering 3D models.

3. **File Path Setup**:
   - The script constructs a path to a STEP file (`3864470050F1.stp`) located in a relative directory (`../assets/models/`).

4. **File Existence Check**:
   - It checks if the specified STEP file exists. If the file is not found, it prompts the user to unzip the corresponding ZIP file and then terminates the script.

5. **STEP File Reading**:
   - If the file exists, the script reads the STEP file using the `read_step_file` function from the `OCC.Extend.DataExchange` module, storing the resulting shape in the `big_shp` variable.

6. **Topology Exploration**:
   - The script uses the `TopologyExplorer` class to explore the topology of the loaded shape (`big_shp`) and extracts all solid subshapes.

7. **Rendering Setup**:
   - An instance of `X3DomRenderer` from the `OCC.Display.WebGl` module is created to handle rendering.

8. **Shape Rendering**:
   - The script iterates over each solid subshape and uses the `DisplayShape` method of the renderer to prepare each shape for display.

9. **Render Call**:
   - Finally, the script calls the `render` method of the renderer to display the shapes in a web-based 3D viewer using X3DOM.

### Summary
In essence, this script reads a 3D model from a STEP file, extracts its solid components, and renders them in a web-based 3D viewer using the X3DOM framework. It ensures that the STEP file is available before proceeding and provides user feedback if the file is missing.

## core_geometry_curves2d_from_curve.py

This Python script is designed to create and display a 2D B-spline curve using the `pythonOCC` library, which is a set of Python wrappers for the Open CASCADE Technology (OCCT) CAD kernel. Here is a breakdown of its functionality:

1. **Imports and Initialization:**
   - It imports various modules from the `OCC.Core` package to handle geometric constructions and conversions.
   - It also imports `init_display` from `OCC.Display.SimpleGui` to initialize the display environment.

2. **Display Initialization:**
   - `init_display()` initializes the display and provides functions to control it (`display`, `start_display`, etc.).

3. **Function Definition (`curves2d_from_curves`):**
   - The function `curves2d_from_curves` performs the following steps:
     1. **Ellipse Creation:**
        - Defines the major and minor radii of an ellipse.
        - Uses `gp_OX2d()` to create a 2D coordinate system axis.
        - Creates an ellipse using `GCE2d_MakeEllipse` with the defined axis and radii.
     2. **Curve Trimming:**
        - Trims the ellipse to a specific parameter range (-1 to 2) using `Geom2d_TrimmedCurve`.
     3. **B-Spline Conversion:**
        - Converts the trimmed curve to a B-spline curve using `geom2dconvert_CurveToBSplineCurve`.
     4. **Display:**
        - Displays the B-spline curve using `display.DisplayShape`.

4. **Main Execution:**
   - If the script is run as the main program, it calls `curves2d_from_curves` to create and display the B-spline curve.
   - It then starts the display loop using `start_display()` to render the curve in a GUI window.

### Purpose:
The purpose of this script is to demonstrate the creation and visualization of a 2D B-spline curve derived from an ellipse using the `pythonOCC` library. It showcases basic geometric operations, curve trimming, and conversion, followed by rendering the result in a graphical user interface.

## core_display_line_properties.py

This Python script uses the `pythonOCC` library to create and display 3D lines in a graphical window. Here is a clear and concise breakdown of its purpose and functionality:

1. **Imports and Initialization**:
    - The script imports necessary modules from `pythonOCC` for geometry creation (`gp_Pnt`, `gp_Dir`, `Geom_Line`), visualization (`AIS_Line`, `Prs3d_LineAspect`, `Prs3d_Drawer`), and color handling (`Quantity_Color`).
    - It initializes a display window using `init_display` from `OCC.Display.SimpleGui`.

2. **Line Creation and Visualization**:
    - The `line` function creates and displays 3D lines:
        - A primary line is created using a point (`gp_Pnt`) and a direction (`gp_Dir`), and then visualized using `AIS_Line`.
        - The appearance of the line can be customized using `Prs3d_Drawer` to set attributes like color, width, and style.
        - The script then enters a loop to create additional lines with varying positions and directions, each with unique visual attributes.
        - Each line's attributes are set using `Prs3d_LineAspect`, which takes parameters for color, type, and width.
        - The lines are displayed in the graphical window using `display.Context.Display`.

3. **Program Execution**:
    - The `line` function is called when the script is executed directly (`if __name__ == "__main__":`).
    - An `exit` function is defined to handle program termination, though it is not used in this script.

4. **License Information**:
    - The script includes a header with licensing information, indicating it is part of `pythonOCC` and distributed under the GNU Lesser General Public License.

### Summary
The script's primary purpose is to demonstrate how to create and display 3D lines with customizable attributes (color, width, style) using the `pythonOCC` library. It initializes a display window, creates lines with specified geometric properties, applies visual attributes, and renders them in the window.

## core_simple_mesh.py

The provided Python code is a script that uses the `pythonOCC` library to create and display a 3D mesh of a fused geometric shape. Here's a breakdown of its purpose and functionality:

### Purpose
The script demonstrates how to create, mesh, and display a 3D model composed of a box and a sphere that are fused together. It also shows how to generate and display the edges of the mesh triangles derived from the fused shape.

### Functionality
1. **Imports:** The script imports various modules from the `pythonOCC` library, which is a set of Python bindings for the Open CASCADE Technology (OCCT), a software development platform for 3D CAD, CAM, CAE.

2. **Display Initialization:** 
   - `init_display()` initializes the display context and returns functions to control the display (`display`, `start_display`, `add_menu`, `add_function_to_menu`).
   - `display.SetSelectionModeVertex()` sets the selection mode to vertices.

3. **Mesh Generation (`simple_mesh` function):**
   - **Shape Creation:**
     - `theBox` is created as a box with dimensions 200x60x60.
     - `theSphere` is created as a sphere with a radius of 80, centered at point (100, 20, 20).
     - `shape` is the result of fusing `theBox` and `theSphere`.
   
   - **Mesh Creation:**
     - `BRepMesh_IncrementalMesh(shape, 0.8)` meshes the `shape` with a deflection of 0.8.
     - A `BRep_Builder` object and a `TopoDS_Compound` object are created to store the mesh edges.
   
   - **Triangle Extraction and Edge Creation:**
     - `TopExp_Explorer` is used to iterate over the faces of the `shape`.
     - For each face, the triangulation data is retrieved using `BRep_Tool().Triangulation(face, location)`.
     - For each triangle in the triangulation, edges are created between the triangle's vertices using `BRepBuilderAPI_MakeEdge`.
     - These edges are added to the compound shape `comp`.
   
   - **Display:**
     - `display.EraseAll()` clears the display.
     - `display.DisplayShape(shape)` displays the original fused shape.
     - `display.DisplayShape(comp, update=True)` displays the mesh edges.

4. **Main Execution:**
   - If the script is run as the main module, `simple_mesh()` is called to generate and display the mesh, and `start_display()` starts the display loop.

### Summary
The script creates a 3D model by fusing a box and a sphere, meshes the resulting shape, extracts the mesh triangles, converts them into edges, and displays both the original shape and the mesh edges using the `pythonOCC` library.

## core_display_offscreen_renderer.py

The provided Python code utilizes the `pythonOCC` library, which is a set of Python bindings for the Open CASCADE Technology (OCCT), a software development platform for 3D CAD, CAM, CAE, etc. Here is a clear and concise description of the code's purpose and functionality:

1. **Importing Modules:**
   - `BRepPrimAPI_MakeBox` from `OCC.Core.BRepPrimAPI` is used to create a box shape.
   - `OffscreenRenderer` from `OCC.Display.OCCViewer` is used for rendering shapes offscreen.

2. **Creating a Box Shape:**
   - A box shape with dimensions 10x20x30 units is created using `BRepPrimAPI_MakeBox(10, 20, 30).Shape()`, and the resulting shape is stored in the variable `a_box_shape`.

3. **Rendering the Box Shape Offscreen:**
   - An instance of `OffscreenRenderer` named `my_renderer` is created.
   - The box shape (`a_box_shape`) is displayed using `my_renderer.DisplayShape(a_box_shape)`.

4. **Rendering and Saving Images:**
   - Another instance of `OffscreenRenderer` named `my_renderer2` is created.
   - The box shape is displayed and saved as an image in three different formats:
     - PNG format, saved as `my_capture.png`.
     - PPM format, saved as `my_capture.ppm`.
     - JPG format, saved as `my_capture.jpg`.
   - The images are saved in the current directory (`"."`).

In summary, the code demonstrates how to create a 3D box shape using `pythonOCC`, render it offscreen, and save the rendered images in different formats.

## core_topology_heightmap.py

The provided Python code is a script that uses the `pythonOCC` library to generate and display 3D surfaces based on mathematical equations or heightmap images. Here's a breakdown of its purpose and functionality:

### Purpose:
The script is designed to create and visualize 3D surfaces using different methods:
1. **Mathematical Equations**: It generates surfaces based on user-defined mathematical functions.
2. **Heightmap Images**: It creates surfaces from grayscale images where pixel intensity represents height.

### Functionality:

1. **Imports and Dependencies**:
    - Imports necessary modules from `pythonOCC` for 3D geometry creation and manipulation.
    - Imports `math` for mathematical functions.
    - Attempts to import `PIL` (Python Imaging Library) for image processing. If not available, it disables the image-based heightmap functionality.

2. **Functions**:
    - `x2_y2(event=None)`: Defines a mathematical function \( z = x^2 - y^2 \) and calls `heightmap_from_equation` to create a surface.
    - `cosxsinxcosysiny(event=None)`: Defines a mathematical function \( z = 5 \cdot \cos(x) \cdot \sin(x) \cdot \sin(y) \cdot \cos(y) \) and calls `heightmap_from_equation` to create a surface.
    - `heightmap_from_equation(f, x_min=-1, x_max=1, y_min=-1, y_max=1)`: Generates a B-Spline surface from a given mathematical function `f(x, y)`. It calculates points on a grid, creates a point cloud, and converts it into a B-Spline surface which is then displayed.
    - `boundary_curve_from_2_points(p1, p2)`: Creates a boundary curve between two points, used for defining the edges of surfaces.
    - `heightmap_from_image(event=None)`: Creates a surface from a grayscale image. It reads pixel values, converts them into height values, and constructs a 3D surface using these heights. This function is only available if `PIL` is installed.

3. **Main Execution**:
    - Initializes the display using `init_display` from `pythonOCC`.
    - Adds menu options for the different heightmap generation functions (`x2_y2`, `cosxsinxcosysiny`, and `heightmap_from_image` if `PIL` is available).
    - Starts the display loop to interact with the user.

### Summary:
The script provides an interactive tool for generating and visualizing 3D surfaces based on mathematical equations or grayscale images. It leverages the `pythonOCC` library for creating complex geometries and displaying them in a graphical window.

## core_topology_face.py

The provided Python code is a script that uses the pythonOCC library to create and display various 3D geometric shapes and faces in a graphical window. Here's a concise breakdown of its purpose and functionality:

### Purpose:
The script demonstrates the creation of different 3D faces and edges using the Open CASCADE Technology (OCCT) through the pythonOCC library. It then displays these shapes in a graphical window.

### Functionality:
1. **Initialization**:
   - Imports necessary modules from pythonOCC for geometric and topological operations.
   - Initializes the display window using `init_display()`.

2. **Function `face()`**:
   - Creates multiple geometric shapes and faces:
     - **Green Face**: A spherical face.
     - **Red Face**: A B-Spline surface face created from a set of 3D points.
     - **Brown Face**: A face bounded by a wire consisting of a circular edge and two linear edges.
     - **Pink Face**: Another B-Spline surface face with additional 2D lines projected onto it to create edges and a wire.
   - Displays these shapes in different colors using the `display.DisplayColoredShape()` method.

3. **Main Execution**:
   - Calls the `face()` function to create and display the shapes.
   - Starts the display loop with `start_display()` to render the shapes in the graphical window.

### Key Components:
- **Geometric Primitives**:
  - `gp_Pnt`, `gp_Sphere`, `gp_Circ`, etc., are used to define points, spheres, circles, and other geometric entities.
- **B-Spline Surface**:
  - Created using `GeomAPI_PointsToBSplineSurface` from a grid of points.
- **Faces and Edges**:
  - Constructed using `BRepBuilderAPI_MakeFace` and `BRepBuilderAPI_MakeEdge`.
- **Wire**:
  - Created using `BRepBuilderAPI_MakeWire` to combine multiple edges.
- **Display**:
  - Uses `init_display()` and related methods from `OCC.Display.SimpleGui` to render the shapes in a window.

### Example Shapes:
- **Green Face**: A spherical segment.
- **Red Face**: A B-Spline surface defined by six points.
- **Brown Face**: A face created from a semi-circular edge and two linear edges.
- **Pink Face**: A B-Spline surface with additional 2D lines projected onto it to form edges and a wire.

### Usage:
- To run the script, execute it in a Python environment with pythonOCC installed. The script will open a graphical window displaying the created shapes.

This script serves as a practical example for using pythonOCC to create and visualize complex 3D geometries.

## core_export_ply_single_shape.py

This Python code is a simple script that uses the `pythonOCC` library to create a 3D model of a sphere and export it to a PLY file format. Here is a breakdown of its functionality:

1. **Imports**:
   - `BRepPrimAPI_MakeSphere` from `OCC.Core.BRepPrimAPI`: This is a function used to create a primitive shape, specifically a sphere in this case.
   - `write_ply_file` from `OCC.Extend.DataExchange`: This function is used to write or export a shape to a PLY (Polygon File Format or Stanford Triangle Format) file.

2. **Sphere Creation**:
   - The line `shp = BRepPrimAPI_MakeSphere(60.0).Shape()` creates a sphere with a radius of 60.0 units. The `BRepPrimAPI_MakeSphere` function generates the sphere, and `.Shape()` retrieves the shape object.

3. **Export to PLY**:
   - The line `write_ply_file(shp, "sphere.ply")` exports the created sphere shape (`shp`) to a file named `sphere.ply` in the PLY format.

In summary, this script creates a 3D sphere with a radius of 60 units and saves it as a PLY file named "sphere.ply".

## core_display_manipulator.py

The provided Python code is a script that uses the `pythonOCC` library to create and display a 3D box with interactive manipulation capabilities. Here's a detailed breakdown of its purpose and functionality:

1. **Imports:**
   - `init_display` from `OCC.Display.SimpleGui`: Initializes the display window and returns functions to control the display.
   - `BRepPrimAPI_MakeBox` from `OCC.Core.BRepPrimAPI`: Provides functionality to create a 3D box shape.
   - `AIS_Manipulator` from `OCC.Core.AIS`: Allows for interactive manipulation of shapes in the display.

2. **Initialization:**
   - `display, start_display, add_menu, add_function_to_menu = init_display()`: Initializes the display window and sets up functions to control the display, such as starting the display loop and adding menus.

3. **Shape Creation:**
   - `my_box = BRepPrimAPI_MakeBox(10.0, 20.0, 30.0).Shape()`: Creates a 3D box with dimensions 10x20x30 units.

4. **Display Setup:**
   - `display.View.TriedronErase()`: Removes the triedron (coordinate system axes) from the display.
   - `ais_shp = display.DisplayShape(my_box, update=True)[0]`: Displays the 3D box shape in the display window and retrieves the displayed shape object.

5. **Manipulator Attachment:**
   - `manip = AIS_Manipulator()`: Creates an instance of `AIS_Manipulator` for interactive manipulation.
   - `manip.Attach(ais_shp)`: Attaches the manipulator to the displayed shape, enabling interactive manipulation (e.g., translation, rotation).

6. **Start Display:**
   - `start_display()`: Starts the display loop, allowing the user to interact with the 3D box in the graphical window.

### Summary
The script initializes a graphical display window, creates a 3D box with specified dimensions, displays the box, attaches an interactive manipulator to the box, and starts the display loop for user interaction. The manipulator allows the user to interactively move and rotate the box within the display window.

## core_parallel_slicer.py

This Python script is designed to perform parallel slicing of a 3D shape using the `pythonOCC` library, which is a set of Python bindings for Open CASCADE, a 3D CAD modeling library. Here's a detailed breakdown of its purpose and functionality:

1. **Imports and Setup**:
    - The script imports necessary modules from `pythonOCC`, `multiprocessing`, and other standard libraries.
    - The shebang `#!/usr/bin/env python` indicates that the script should be run using the Python interpreter.

2. **Helper Functions**:
    - `drange(start, stop, step)`: Mimics NumPy's `arange` function to generate a list of floating-point numbers from `start` to `stop` with a given `step`.
    - `get_brep()`: Reads a BREP (Boundary Representation) file of a 3D model (specifically a cylinder head) and returns it as a `TopoDS_Shape` object.

3. **Main Slicing Function**:
    - `vectorized_slicer(li)`: Takes a list containing z-values and a shape, then slices the shape at each z-value using planes parallel to the XY-plane. It returns a list of section shapes resulting from these slices.

4. **Parallel Execution**:
    - `run(n_procs, compare_by_number_of_processors=False)`: The main function that orchestrates the slicing process.
        - It retrieves the 3D shape.
        - Computes the bounding box of the shape to determine the slicing range.
        - Defines helper functions to distribute z-coordinates among processors (`get_z_coords_for_n_procs`) and prepare arguments for multiprocessing (`arguments`).
        - Depending on the `compare_by_number_of_processors` flag, it either slices using a specified number of processors or runs a comparison test with different numbers of processors.
        - Uses the `multiprocessing` library to parallelize the slicing process across multiple CPU cores.

5. **Visualization**:
    - After slicing, the script uses `init_display` from `pythonOCC` to visualize the original shape and the resulting slices.

6. **Execution**:
    - The script is designed to be run as a standalone program. In the `__main__` block, it determines the number of CPU cores available and calls the `run` function with this number, unless overridden by the `compare_by_number_of_processors` flag.

**Usage**:
- The script slices a 3D model (cylinder head) into multiple cross-sections parallel to the XY-plane and visualizes these slices.
- It leverages multiprocessing to speed up the slicing process by distributing the workload across available CPU cores.
- The script can also compare the performance of slicing with different numbers of processors.

**Example Command**:
```bash
python script_name.py
```
Replace `script_name.py` with the actual filename of the script.

**Dependencies**:
- `pythonOCC`
- `multiprocessing`
- Other Python standard libraries such as `time` and `sys`.

**Note**:
- Ensure that the BREP file (`cylinder_head.brep`) is available at the specified path (`../assets/models/cylinder_head.brep`). Adjust the path as necessary.
- The script includes licensing information for `pythonOCC` under the GNU Lesser General Public License.

## core_meshDS_numpy_face_colors.py

This Python code provides an example of creating and visualizing a triangular mesh using the `OCC` (Open CASCADE Technology) library, `numpy`, and `scipy`. The mesh is colored based on the mean z-values of its vertices. Below is a detailed breakdown of the code's purpose and functionality:

1. **Import Libraries:**
   - `numpy` and `scipy.spatial.Delaunay` for numerical operations and Delaunay triangulation.
   - `matplotlib.cm` for colormap handling.
   - `OCC` modules for mesh data handling and visualization.
   - `OCC.Display.SimpleGui` for initializing the display.

2. **Define `getMesh` Function:**
   - Generates a grid of points in the x-y plane.
   - Computes z-values using a mathematical function (`sin(xx**2 + yy**2) / (xx**2 + yy**2)`).
   - Creates a triangular mesh using Delaunay triangulation on the x-y coordinates.
   - Returns the vertices and faces of the mesh.

3. **Generate Mesh Data:**
   - Calls `getMesh` to obtain vertices and faces of the mesh.

4. **Compute Face Colors:**
   - Uses the 'viridis' colormap to map mean z-values of the faces to colors.
   - Normalizes these z-values to fit within the colormap range.

5. **Create Data Source:**
   - Initializes `MeshDS_DataSource` with vertices and faces, which are converted to contiguous arrays.

6. **Create Mesh Visualizer:**
   - Initializes `MeshVS_Mesh` and sets the data source.
   - Creates an `ElementalColorPrsBuilder` for coloring the mesh elements.
   - Assigns colors to each face based on the normalized z-values.

7. **Disable Edges:**
   - Configures the mesh drawer to hide edges for a cleaner visualization.

8. **Display the Mesh:**
   - Initializes the display using `init_display`.
   - Adds the mesh visualizer to the display context.
   - Fits the display to show all elements.
   - Starts the display loop.

This code effectively demonstrates how to create a 3D triangular mesh, color it based on vertex attributes, and visualize it using the Open CASCADE library.

## core_load_step_ap203_ocaf.py

This Python code is designed to read and display a 3D STEP file using the `pythonOCC` library, which is a set of Python bindings for the Open CASCADE Technology (OCCT) framework. Here is a breakdown of its purpose and functionality:

1. **Imports**:
   - The code imports various modules from `OCC.Core` for handling documents, reading STEP files, and managing different attributes such as colors, layers, and materials.
   - It also imports `init_display` from `OCC.Display.SimpleGui` to set up a graphical display for the 3D shapes.

2. **File and Variable Initialization**:
   - The STEP file to be read is specified by the `filename` variable.
   - An empty list `_shapes` is initialized to store the shapes extracted from the STEP file.

3. **Document Creation**:
   - A document object `doc` is created to hold the data read from the STEP file.

4. **Tool Initialization**:
   - Several tools are initialized to manage shapes, colors, layers, and materials within the document:
     - `shape_tool` for shapes
     - `l_colors` for colors
     - `l_layers` for layers
     - `l_materials` for materials

5. **STEP File Reading**:
   - A `STEPCAFControl_Reader` object `step_reader` is created and configured to read colors, layers, names, and materials from the STEP file.
   - The STEP file is read using `ReadFile(filename)`, and if successful (`IFSelect_RetDone`), the data is transferred to the document.

6. **Extracting Shapes and Colors**:
   - The root shapes (free shapes) are extracted using `GetFreeShapes(labels)`, and the number of root shapes is printed.
   - For each root shape, it checks if the shape is an assembly and extracts its sub-shapes, printing the number of sub-shapes.
   - The colors used in the document are extracted using `GetColors(color_labels)`, and the number of colors is printed. Each color is then printed using `Dump()`.

7. **Storing Shapes**:
   - For each root shape, the shape itself is retrieved and added to the `_shapes` list.

8. **Displaying Shapes**:
   - The shapes stored in `_shapes` are displayed using the `init_display` function, which sets up the graphical display.
   - The `start_display()` function is called to start the graphical user interface (GUI) and display the shapes.

In summary, this script reads a 3D STEP file, extracts and prints information about the shapes and colors present in the file, and then displays the 3D shapes using a GUI.

## core_font_register.py

This Python code is designed to render a piece of text as a 3D shape using the `pythonOCC` library, which is a set of Python bindings for the Open CASCADE Technology (OCCT), a software development platform for 3D CAD, CAM, CAE, etc. Here's a breakdown of its purpose and functionality:

1. **License and Imports**:
   - The initial comments specify the license under which the code is distributed (GNU Lesser General Public License) and include the author's information.
   - Required modules are imported, specifically `os`, and several components from `OCC` (Open CASCADE Community) including `Display`, `Core.Addons`, and `SimpleGui`.

2. **Initialization**:
   - `init_display()` is called to initialize the display window and functionalities. This function returns several objects/functions (`display`, `start_display`, `add_menu`, `add_function_to_menu`).

3. **Font Registration**:
   - The `register_font` function is used to register a custom font located at `../assets/fonts/Respective.ttf`.

4. **Text Definition**:
   - A multiline string containing a poem by Paul Verlaine is defined. This text will be converted into a 3D shape.

5. **Text to BREP Conversion**:
   - The `text_to_brep` function converts the text into a BREP (Boundary Representation) 3D shape using the registered font ("Respective"), a standard font style (`Font_FA_Regular`), a font size of 12.0, and a flag set to `True` indicating that the text should be bold.

6. **Displaying the Text**:
   - The `display.DisplayColoredShape` method is used to display the generated BREP shape in the initialized display window.
   - `start_display()` is called to start the event loop of the display window, making it interactive.

In summary, this script converts a piece of text into a 3D shape using a specific font and displays it in a 3D viewer window.

## core_animation.py

This Python script is designed to create and display a 3D cube using the pythonOCC library, which is a set of Python bindings for the Open CASCADE Technology (OCCT) 3D modeling library. The script includes functionality to animate the rotation of the cube around one or two axes. Here's a breakdown of its purpose and functionality:

1. **Imports and Initialization**:
   - The script imports necessary modules, including time, math functions, and various components from the pythonOCC library.
   - It initializes the display using `init_display()` from the `OCC.Display.SimpleGui` module.

2. **Shape Building Function**:
   - `build_shape()`: This function creates a 3D box (cube) with dimensions 50x50x50 units using `BRepPrimAPI_MakeBox` and displays it. It returns the displayed shape object.

3. **Single-Axis Rotation Animation**:
   - `rotating_cube_1_axis(event=None)`: This function animates the rotation of the cube around the Z-axis.
     - It erases any existing shapes from the display.
     - It calls `build_shape()` to create and display a new cube.
     - It sets up a rotation axis (`gp_Ax1`) along the Z-axis.
     - It iterates 200 times, incrementing the rotation angle each time and updating the cube's position using `SetRotation` and `SetLocation`.
     - It prints the time taken for the 200 rotations.

4. **Two-Axis Rotation Animation**:
   - `rotating_cube_2_axis(event=None)`: This function animates the rotation of the cube around both the Z-axis and Y-axis.
     - Similar to the single-axis rotation, it erases existing shapes and creates a new cube.
     - It sets up two rotation axes (`gp_Ax1`), one along the Z-axis and one along the Y-axis.
     - It iterates 200 times, applying rotations around both axes and updating the cube's position.
     - It prints the time taken for the 200 rotations.

5. **Main Execution**:
   - The script adds menu items for the animations and links them to the respective functions.
   - It starts the display loop, allowing the user to interact with the 3D viewer and trigger the animations through the menu.

Overall, the script demonstrates the use of pythonOCC to create and manipulate 3D shapes and provides a simple example of animating a cube's rotation in a 3D viewer.

## core_mesh_data_source_color_map.py

The provided Python code is designed to read an STL (stereolithography) file, create a mesh from it, apply color mapping based on randomly generated values, and display the resulting mesh using the `pythonOCC` library, which is a set of Python bindings for the Open CASCADE Technology (OCCT) framework.

Here's a breakdown of the code's purpose and functionality:

1. **Imports**: The code imports various modules from the `pythonOCC` library, which are necessary for handling mesh data, reading STL files, applying colors, and displaying the mesh.

2. **STL File Path**: The path to the STL file (`fan.stl`) is defined. It is assumed to be located in a directory structure relative to the script.

3. **Read STL File**: The STL file is read using the `rwstl.ReadFile` function, which returns a mesh object.

4. **Create Data Source**: A `MeshDS_DataSource` object is created from the mesh data, which serves as the data source for the mesh visualization.

5. **Create Mesh**: A `MeshVS_Mesh` object is instantiated, and the data source is assigned to it.

6. **Assign Nodal Builder**: A `MeshVS_NodalColorPrsBuilder` is created and assigned to the mesh. This builder is responsible for defining how the nodes of the mesh are colored. The builder is configured to use texture mapping.

7. **Prepare Color Map**: An `Aspect_SequenceOfColor` object is created to hold the color map. Two colors (red and blue) are added to the map.

8. **Assign Color Scale Map Values**: A `TColStd_DataMapOfIntegerReal` object is created to map node IDs to color scale values (ranging from 0 to 1). The code iterates through a range of node IDs (0 to 999) and assigns a random value between 0 and 1 to each node.

9. **Set Color Map and Texture Coordinates**: The color map and the scale values are assigned to the nodal builder. An invalid color (black) is also specified for nodes that do not have a valid color mapping.

10. **Add Builder to Mesh**: The nodal builder is added to the mesh, enabling the mesh to use the color mapping defined.

11. **Display Mesh**: The `init_display` function initializes the display context, and the mesh is displayed. The `start_display` function starts the GUI event loop to render the mesh on the screen.

In summary, this code reads an STL file, creates a mesh from it, applies a random color mapping to the mesh nodes, and displays the colored mesh using the `pythonOCC` library.

## core_export_gltf_single_shape.py

This Python code demonstrates the creation and export of a 3D sphere model using the `pythonOCC` library, which is a set of Python bindings for the Open CASCADE Technology (OCCT) 3D modeling library. The code performs the following steps:

1. **Import Necessary Modules**: The script imports various modules from the `OCC.Core` package, which provides tools for creating and manipulating 3D shapes, as well as for exporting these shapes in different formats.

2. **Create a Sphere Shape**:
   - Uses `BRepPrimAPI_MakeSphere` to create a 3D sphere with a radius of 60 units.

3. **Create a Document**:
   - Initializes a `TDocStd_Document` object to store the shape.
   - Retrieves tools for managing shapes and layers within the document using `XCAFDoc_DocumentTool_ShapeTool` and `XCAFDoc_DocumentTool_LayerTool`.

4. **Mesh the Shape**:
   - Cleans the shape using `breptools_Clean`.
   - Triangulates the shape using `BRepMesh_IncrementalMesh`, which prepares the shape for export by converting it into a mesh.

5. **Add Shape to Document**:
   - Adds the meshed shape to the document using `shape_tool.AddShape`.

6. **GLTF Export Options**:
   - Sets the format for transformations (`RWGltf_WriterTrsfFormat_Compact`).
   - Forces UV export to ensure texture coordinates are included.

7. **Add Metadata**:
   - Creates an indexed data map for metadata and adds an author entry ("pythonocc").

8. **Export the Shape in Binary GLTF Format**:
   - Configures a `RWGltf_CafWriter` for binary export (GLB format).
   - Sets the transformation format and forces UV export.
   - Performs the export, writing the binary GLTF file (`box.glb`).

9. **Export the Shape in ASCII GLTF Format**:
   - Configures another `RWGltf_CafWriter` for ASCII export (GLA format).
   - Sets the transformation format and forces UV export.
   - Performs the export, writing the ASCII GLTF file (`box.gla`).

In summary, this script creates a 3D sphere, converts it into a mesh, and exports it into both binary (GLB) and ASCII (GLA) GLTF formats, including metadata about the author.

## core_mesh_data_source_numpy.py

This Python code is designed to create and visualize a 3D mesh using the `pythonOCC` library, which is a set of Python bindings for Open CASCADE Technology (OCCT), a software development platform for 3D CAD, CAM, CAE, etc. Here's a step-by-step breakdown of its purpose and functionality:

1. **Import Statements**:
   - Imports necessary classes and functions from the `pythonOCC` library and `numpy` for numerical operations.
   
2. **Vertex and Face Data Creation**:
   - Defines the coordinates of 8 vertices (`v1` to `v8`) which form the corners of a cube.
   - Defines 12 faces (`f1` to `f12`) using the indices of the vertices. Each face is represented as a triangle.

3. **Data Conversion**:
   - Converts the vertex and face data into NumPy arrays (`vertices` and `faces`) with appropriate data types (`float32` for vertices and `int32` for faces).

4. **Mesh Data Source Creation**:
   - Creates a `MeshDS_DataSource` object (`a_data_source`) using the vertex and face data.

5. **Mesh Presentation Setup**:
   - Initializes a `MeshVS_Mesh` object (`a_mesh_prs`), which represents the mesh to be visualized.
   - Sets the data source for the mesh using `SetDataSource`.
   - Creates a `MeshVS_MeshPrsBuilder` object (`a_builder`) to build the mesh presentation and adds it to the mesh using `AddBuilder`.

6. **Nodal Color Presentation**:
   - Creates a `MeshVS_NodalColorPrsBuilder` object (`a_builder`) to handle nodal color data presentation.
   - Configures the builder to use textures with `UseTexture(True)`.

7. **Display Initialization**:
   - Initializes the display context using `init_display` and assigns the returned functions to `display`, `start_display`, `add_menu`, and `add_function_to_menu`.

8. **Mesh Display**:
   - Displays the mesh in the graphical context with `display.Context.Display(a_mesh_prs, True)`.
   - Fits the view to show the entire mesh using `display.FitAll()`.
   - Starts the display loop with `start_display()`.

### Summary
The code demonstrates how to create a simple 3D cube mesh using vertex and face data, set up the mesh with `pythonOCC`, and visualize it using a graphical display. The mesh is displayed with nodal color data and texture support, providing a visual representation of the 3D object.

## core_geometry_airfoil.py

This Python script is designed to create a 3D solid model of an airfoil using data from the UIUC Airfoil Coordinates Database. Here's a detailed breakdown of its functionality:

1. **Imports and Dependencies**: 
   - It imports various modules from the `OCC` library, which is used for 3D CAD modeling.
   - It also imports modules for handling SSL and HTTP requests.

2. **Class Definition**: 
   - The `UiucAirfoil` class is defined to represent an airfoil with a specified chord, span, and profile name. The profile name corresponds to a specific airfoil data file hosted on the UIUC website.

3. **Initialization and Data Retrieval**:
   - The `__init__` method initializes the airfoil's chord, span, and profile attributes and calls the `make_shape` method to construct the 3D model.
   - The `make_shape` method fetches the airfoil data from the UIUC database. It constructs the URL for the data file and retrieves it using `urllib2`.

4. **Data Processing**:
   - The method processes the retrieved data to extract 2D points representing the airfoil's cross-sectional shape. These points are scaled by the chord length.

5. **Spline Creation**:
   - A B-spline curve is created from the 2D points using the `Geom2dAPI_PointsToBSpline` class.
   - The 2D spline is converted to a 3D spline using the `geomapi.To3d` function.

6. **Face and Solid Creation**:
   - The script attempts to create a trailing edge segment. If successful, it combines the spline and trailing edge into a wire and then a face.
   - If the trailing edge creation fails (due to points being too close), it creates a face directly from the spline.
   - The face is then extruded along the span direction to create a 3D solid model of the airfoil.

7. **Helper Functions**:
   - `point2d_list_to_TColgp_Array1OfPnt2d` and `_Tcol_dim_1` are utility functions for converting a list of 2D points into the format required by the OCC library.

8. **Main Execution**:
   - When run as a standalone script, it creates an instance of `UiucAirfoil` with specified chord, span, and profile parameters.
   - It initializes the OCC display, renders the 3D airfoil shape, and starts the display loop.

### Summary
This script fetches airfoil coordinate data from the UIUC database, processes it to create a 3D B-spline curve, constructs a face from the curve, and extrudes the face to generate a 3D solid model of the airfoil. It uses the `pythonOCC` library for 3D CAD operations and provides a visualization of the created airfoil model.

## core_geometry_faircurve.py

This Python script is a graphical application that uses the `pythonOCC` library to generate and display a "fair curve"—a smooth curve with minimal variation—between two points in 2D space. Here's a breakdown of its purpose and functionality:

1. **Imports and Initialization**:
    - The script imports necessary modules from `pythonOCC` for geometry creation and display.
    - It initializes a graphical display using `init_display()` from the `OCC.Display.SimpleGui` module.

2. **Error Code Mapping**:
    - The `error_code` function maps integer error codes to their corresponding descriptive strings for the `FairCurve_MinimalVariation` computations.

3. **Batten Curve Generation**:
    - The `batten_curve` function creates a fair curve between two 2D points (`pt1` and `pt2`) with specified height, slope, and angles at the endpoints.
    - The function configures the fair curve constraints and computes the curve, printing any error messages if the computation does not converge properly.
    - It returns the computed curve.

4. **Fair Curve Visualization**:
    - The `faircurve` function sets up the initial points and height for the curve.
    - It iterates over a range of slope values, generating and displaying the fair curve for each slope.
    - The display is updated in a loop, erasing the previous curve and showing the new one with a slight delay (`time.sleep(0.21)`).

5. **Exit Function**:
    - The `exit` function provides a way to gracefully exit the application.

6. **Main Execution Block**:
    - Adds a menu item "fair curve" to the display.
    - Associates the `faircurve` and `exit` functions with the menu.
    - Starts the graphical display loop.

### Key Functional Points:
- **Fair Curve Calculation**: Uses `FairCurve_MinimalVariation` to compute smooth curves based on constraints.
- **Dynamic Visualization**: Iteratively displays curves with varying slopes, updating the graphical display in real-time.
- **User Interaction**: Provides a menu interface for users to start the curve generation and exit the application.

### Usage:
- Run the script to start the graphical interface.
- Use the menu to generate and visualize fair curves dynamically.
- Exit the application using the provided menu option.

This script is particularly useful in CAD applications where smooth and aesthetically pleasing curves are required, such as in ship hull design, automotive design, or any other field requiring precise curve control.

## core_offscreen_rendering.py

This Python code uses the `pythonOCC` library, which is a set of Python bindings for the OpenCASCADE Technology (OCCT) framework. The primary purpose of the code is to create a 3D box shape, render it using an offscreen renderer, and export the rendered images at different resolutions.

Here is a step-by-step breakdown of the functionality:

1. **Imports**:
   - `BRepPrimAPI_MakeBox` from `OCC.Core.BRepPrimAPI` to create a 3D box shape.
   - `Graphic3d_BufferType` from `OCC.Core.Graphic3d` for specifying the buffer type when exporting image data.
   - `Viewer3d` from `OCC.Display.OCCViewer` to create an offscreen renderer for rendering 3D shapes.

2. **Renderer Initialization**:
   - An offscreen renderer (`Viewer3d`) is created and initialized with default settings (640x480 resolution and shaded mode).

3. **Shape Creation**:
   - A 3D box shape (`my_box`) with dimensions 10x20x30 units is created using `BRepPrimAPI_MakeBox`.

4. **Rendering the Shape**:
   - The created box shape is displayed in the offscreen renderer.

5. **Image Data Export**:
   - The rendered image data is exported at two different resolutions:
     - 640x480 pixels.
     - 1024x768 pixels.
   - The exported data uses the depth buffer type (`Graphic3d_BT_Depth`).

6. **Image Export**:
   - The rendered view is dumped to a JPEG file at 640x480 resolution.
   - The renderer is resized to 1024x768 resolution, and the view is dumped again to a JPEG file at the new resolution.

7. **Note**:
   - The code comments highlight that exporting image data at a higher resolution without resizing the renderer results in a zoomed-in image of the lower resolution. A better quality image is obtained by resizing the renderer before exporting.

In summary, the code demonstrates how to create and render a 3D box shape using `pythonOCC`, and how to export the rendered images at different resolutions while emphasizing the importance of resizing the renderer for better image quality.

## core_export_stl.py

This Python code is part of the `pythonOCC` library, which is used for 3D CAD modeling. The code specifically creates a 3D torus shape and exports it to STL files with different resolutions. Here is a detailed breakdown of its functionality:

1. **Imports**:
   - `os`: A standard library module for interacting with the operating system.
   - `BRepPrimAPI_MakeTorus` from `OCC.Core.BRepPrimAPI`: A function to create a torus shape.
   - `write_stl_file` from `OCC.Extend.DataExchange`: A function to write shapes to STL files.

2. **Creating the Torus Shape**:
   - The code uses `BRepPrimAPI_MakeTorus` to create a torus with a major radius of 20.0 units and a minor radius of 10.0 units.
   - The resulting shape is stored in the variable `my_torus`.

3. **Setting the Output Directory**:
   - The code defines the directory where the STL files will be saved, which is located at `../assets/models` relative to the script's location.
   - The directory path is made absolute using `os.path.abspath`.

4. **Directory Validation**:
   - The code checks if the specified output directory exists using `os.path.isdir`.
   - If the directory does not exist, an `AssertionError` is raised with the message "wrong path provided".

5. **Exporting the Torus to STL Files**:
   - The code first exports the torus to an STL file with default resolution. The file is named `torus_default_resolution.stl` and saved in the specified directory.
   - The function `write_stl_file` is used to write the shape to the STL file.

6. **Exporting with High Resolution**:
   - The code then exports the torus to another STL file, this time with higher resolution and in binary format.
   - The file is named `torus_high_resolution.stl` and saved in the same directory.
   - The `write_stl_file` function is called again, but this time with additional parameters `mode="binary"`, `linear_deflection=0.5`, and `angular_deflection=0.3` to control the mesh resolution and format.

In summary, the code creates a 3D torus shape and exports it to two STL files: one with default resolution and one with higher resolution in binary format. It ensures the output directory exists before attempting to write the files.

## core_geometry_project_point_on_curve.py

The provided Python code is a script that utilizes the `pythonOCC` library, which is a set of Python bindings for the OpenCASCADE geometry and modeling kernel. The script's primary purpose is to demonstrate how to project a point onto a curve (specifically, a circle) and visualize the results using a graphical display.

Here's a concise breakdown of its functionality:

1. **Imports and Initialization**:
   - The script imports necessary modules from `OCC.Core` for geometric operations and from `OCC.Display.SimpleGui` for visualization.
   - It initializes the display system with `init_display()`.

2. **Function: `project_point_on_curve`**:
   - **Create a Point and Circle**:
     - A point (`gp_Pnt`) with coordinates (1.0, 2.0, 3.0) is defined.
     - A circle (`Geom_Circle`) with a radius of 5.0 units centered at the origin is created.
   - **Display Shapes**:
     - The circle and the point are displayed in the graphical window.
     - A label "P" is displayed at the point's location.
   - **Project Point onto Circle**:
     - The point is projected onto the circle using `GeomAPI_ProjectPointOnCurve`.
     - The nearest point on the circle to the given point is obtained.
     - The number of possible projection results is retrieved and printed.
     - The nearest projected point is displayed with a message indicating the distance from the original point.
   - **Handle Multiple Results**:
     - If there are multiple projection results, each result is displayed along with the distance from the original point.

3. **Main Execution**:
   - The `project_point_on_curve` function is called.
   - The graphical display is started with `start_display()`.

### Key Points:
- **Visualization**: The script uses `pythonOCC` to create and display geometric shapes (a point and a circle) and project a point onto the circle.
- **Projection**: It demonstrates the use of `GeomAPI_ProjectPointOnCurve` to find and display the projection of a point onto a curve.
- **User Interaction**: The results, including the number of projections and their distances, are displayed graphically and printed to the console.

This script is useful for educational purposes or for developers who need to understand how to perform geometric projections and visualize the results using the `pythonOCC` library.

## core_visualization_glsl.py

This Python code is a script that utilizes the `pythonOCC` library, which is a set of Python bindings for the Open CASCADE Technology (OCCT) 3D modeling and visualization library. The purpose of this script is to create a 3D sphere, apply custom vertex and fragment shaders to it, and display the sphere in a graphical window.

Here is a step-by-step breakdown of the functionality:

1. **Imports and Initialization**:
    - The script imports necessary classes and functions from the `OCC.Core` and `OCC.Display` modules.
    - `init_display()` is called to initialize the display environment, returning handles for display functions.

2. **Sphere Creation**:
    - A sphere with a radius of 100 units is created using `BRepPrimAPI_MakeSphere`.
    - This sphere is wrapped in an `AIS_Shape` object, which is used for interactive 3D shape visualization.

3. **Shader Definitions**:
    - Two shaders are defined using GLSL (OpenGL Shading Language):
        - **Fragment Shader (`fs`)**: Sets the fragment color to green (`vec4(0.0, 1.0, 0, 1.0)`).
        - **Vertex Shader (`vs`)**: Computes the position of each vertex using transformation matrices (`occProjectionMatrix`, `occWorldViewMatrix`, `occModelWorldMatrix`, `occVertex`).

4. **Shader Compilation and Attachment**:
    - The vertex and fragment shaders are compiled from their source code using `Graphic3d_ShaderObject.CreateFromSource`.
    - A shader program (`Graphic3d_ShaderProgram`) is created, and the compiled shaders are attached to it.
    - The shader program is then attached to the shading aspect of the `AIS_Shape` object representing the sphere.

5. **Assertions and Display**:
    - The script checks if the shader program is valid and successfully attached.
    - The sphere is redisplayed with the new shader applied using `display.Context.Redisplay`.
    - The display is fitted to show the entire sphere using `display.FitAll`.
    - The graphical display loop is started with `start_display()`.

In summary, this script demonstrates how to create a 3D sphere, apply custom shaders to it, and visualize it using the `pythonOCC` library. The shaders modify the appearance of the sphere, with the vertex shader handling transformations and the fragment shader setting the color.

## core_topology_revolved_shape.py

This Python code is a script that demonstrates how to use the pythonOCC library, which is a set of Python bindings for the Open CASCADE Technology (OCCT) library. The script specifically showcases how to create a revolved shape from a wireframe edge. Here is a detailed breakdown of its purpose and functionality:

1. **Imports**: 
   - Imports necessary modules from the `OCC.Core` package for creating geometrical shapes and performing operations on them.
   - Imports `init_display` from `OCC.Display.SimpleGui` to initialize the graphical display.

2. **Display Initialization**:
   - Initializes the display environment using `init_display()`, which returns display control functions: `display`, `start_display`, `add_menu`, and `add_function_to_menu`.

3. **Function `revolved_shape`**:
   - **Purpose**: Demonstrates how to create a 3D revolved shape from a 2D edge.
   - **Steps**:
     1. **Define Points**: Creates a list of points (`edg_points`) that form the vertices of a hexagonal shape.
     2. **Create Wire**: Uses `BRepBuilderAPI_MakeWire` to aggregate edges formed between consecutive points into a wireframe.
     3. **Create Face**: Converts the wire into a face using `BRepBuilderAPI_MakeFace`.
     4. **Revolve Face**: Revolves the face around the Z-axis by 90 degrees to create a 3D shape using `BRepPrimAPI_MakeRevol`.
     5. **Display Shapes**: Renders the original wire and the revolved shape using `display.DisplayShape` and fits them to the display window using `display.FitAll`.
     6. **Start Display**: Initiates the graphical display loop with `start_display`.

4. **Main Execution**:
   - The `revolved_shape` function is called within the `if __name__ == "__main__":` block to execute when the script is run directly.

**Summary**:
The script demonstrates the creation of a 3D revolved shape from a 2D hexagonal wireframe using the pythonOCC library. It initializes a display, defines a set of points to form a hexagon, converts these points into a wireframe, creates a face from the wireframe, revolves this face around an axis to form a 3D shape, and finally displays the wireframe and the revolved shape in a graphical window.

## core_display_z_order_transparency.py

The provided Python code is a script that uses the `pythonOCC` library, which is a set of Python wrappers for the OpenCASCADE Technology (OCCT) 3D modeling library. This script demonstrates basic 3D shape creation and manipulation, as well as rendering these shapes in a graphical window. Here's a breakdown of its purpose and functionality:

1. **Imports**: The script imports necessary modules from `pythonOCC` for creating shapes, displaying them, and performing geometric transformations.
    - `BRepPrimAPI_MakeBox` and `BRepPrimAPI_MakeSphere` are used to create basic 3D shapes (a box and a sphere).
    - `init_display` initializes the display window.
    - `gp_Vec` and `gp_Pnt` are used for geometric points and vectors.
    - `translate_shp` is a utility function to translate (move) shapes.

2. **Display Initialization**: The `init_display()` function initializes the display environment and returns several functions used to control the display (`display`, `start_display`, `add_menu`, `add_function_to_menu`).

3. **Shape Creation**:
    - A box is created with dimensions 200x60x60 units.
    - A sphere is created with a center at point (100, 20, 20) and a radius of 80 units.

4. **Shape Transformation**:
    - The sphere is translated (moved) by a vector (0.0, -200.0, 0.0), effectively shifting it 200 units down along the Y-axis.

5. **Shape Display**:
    - The box is displayed with a slight transparency (0.1).
    - The moved sphere is displayed with a blue color and high transparency (0.9).

6. **Fit and Start Display**:
    - `display.FitAll()` adjusts the view to fit all displayed shapes within the window.
    - `start_display()` starts the interactive display loop, allowing users to view and interact with the rendered shapes.

In summary, the script creates a 3D box and a sphere, moves the sphere, and then displays both shapes in a graphical window with specified colors and transparency levels.

## core_2d_fillet.py

This Python code is a script that utilizes the `pythonOCC` library, which is a set of Python bindings for the OpenCASCADE geometric modeling kernel. The script's purpose is to create and display a 2D fillet between two edges. Here's a step-by-step breakdown of its functionality:

1. **Imports and Initial Setup:**
   - The script imports several classes and functions from the `OCC` module, which is part of the `pythonOCC` library.
   - It also imports a function to initialize a display window from `OCC.Display.SimpleGui`.

2. **Initialize the Display:**
   - The `init_display` function is called to set up the display environment, returning several objects for managing the display (`display`, `start_display`, `add_menu`, `add_functionto_menu`).

3. **Define Points:**
   - Three points (`p1`, `p2`, `p3`) are defined using the `gp_Pnt` class, which represents points in 3D space.

4. **Create Edges:**
   - Two edges (`ed1`, `ed2`) are created using the `BRepBuilderAPI_MakeEdge` class, which constructs edges between pairs of points.

5. **Create a 2D Fillet:**
   - An instance of `ChFi2d_AnaFilletAlgo` is created to handle the fillet creation.
   - The `Init` method initializes the fillet algorithm with the two edges and a plane (`gp_Pln`).
   - The `Perform` method is called with a specified radius (1.0) to create the fillet.
   - The `Result` method produces the fillet shape between the two edges.

6. **Create a Wire:**
   - The `make_wire` function is used to create a wire (a connected sequence of edges) from the list of edges and the fillet.

7. **Display the Wire:**
   - The `display.DisplayShape` method is called to display the wire.
   - The `start_display` function is invoked to start the display loop, allowing the user to view the created geometry.

In summary, this script demonstrates how to use the `pythonOCC` library to create a simple geometric construction involving two edges and a fillet, and then visualize the result in a graphical window.

## core_load_brep.py

This Python code is designed to read and display a 3D model from a BREP (Boundary Representation) file using the `pythonOCC` library. Here's a detailed breakdown of its purpose and functionality:

1. **Import Statements**:
    - `init_display` from `OCC.Display.SimpleGui`: Initializes the display window for rendering 3D shapes.
    - `breptools_Read` from `OCC.Core.BRepTools`: Reads BREP files and converts them into `TopoDS_Shape` objects.
    - `TopoDS_Shape` from `OCC.Core.TopoDS`: Represents a topological shape in OpenCASCADE.
    - `BRep_Builder` from `OCC.Core.BRep`: Provides tools to build BREP shapes.

2. **Shape Initialization**:
    - `cylinder_head = TopoDS_Shape()`: Creates an empty `TopoDS_Shape` object to hold the 3D model.
    - `builder = BRep_Builder()`: Initializes a `BRep_Builder` object, which is used in conjunction with `breptools_Read` to construct the shape.

3. **Reading the BREP File**:
    - `breptools_Read(cylinder_head, "../assets/models/cylinder_head.brep", builder)`: Reads the BREP file located at `../assets/models/cylinder_head.brep` and stores the resulting shape in the `cylinder_head` object using the `builder`.

4. **Display Initialization**:
    - `display, start_display, add_menu, add_function_to_menu = init_display()`: Initializes the display window and returns functions to control it.

5. **Displaying the Shape**:
    - `display.DisplayShape(cylinder_head, update=True)`: Renders the `cylinder_head` shape in the display window.
    - `start_display()`: Starts the display loop, which keeps the window open and responsive to user interactions.

In summary, this script reads a 3D model from a specified BREP file and displays it in a graphical window using the `pythonOCC` library.

## core_geometry_recognize_feature.py

This Python code is part of the `pythonOCC` library, which is used for 3D CAD modeling and analysis. The purpose of this script is to load a STEP file, identify the geometrical nature of each face in the 3D model (such as planes, cylinders, and BSpline surfaces), and display the properties of these faces either interactively or in batch mode. Below is a detailed breakdown of its functionality:

### Key Functionalities:
1. **Loading and Displaying STEP File:**
   - The script reads a STEP file (`as1_pe_203.stp`) using the `read_step_file` function.
   - It initializes a 3D display window using the `init_display` function from `OCC.Display.SimpleGui`.

2. **Face Recognition:**
   - The `recognize_face` function identifies whether a face is a plane, cylinder, or BSpline surface.
     - If the face is a plane, it prints the location and normal vector.
     - If the face is a cylinder, it prints the location and axis vector.
     - If the face is a BSpline surface, it identifies it but does not print specific properties (as the example STEP file does not contain BSpline surfaces).

3. **Interactive Mode:**
   - Users can click on faces in the 3D window to identify them. The `recognize_clicked` function is called upon clicking a face, which in turn calls `recognize_face` to print the face's properties.

4. **Batch Mode:**
   - Users can process all faces in the model at once by selecting a menu item. The `recognize_batch` function iterates over all faces in the model and calls `recognize_face` for each one.

5. **Menu and Event Handling:**
   - The script sets up a menu item for batch processing.
   - It registers a callback for face selection and defines an exit function to terminate the script.

### Main Components:
- **Imports:**
  - Various modules from `OCC.Core` for geometry and topology operations.
  - `init_display`, `read_step_file`, and `TopologyExplorer` from `OCC.Extend`.

- **Functions:**
  - `recognize_face(a_face)`: Identifies and prints properties of a face.
  - `recognize_clicked(shp, *kwargs)`: Handles face selection in the 3D view.
  - `recognize_batch(event=None)`: Processes all faces in the model.
  - `exit(event=None)`: Exits the application.

- **Main Execution:**
  - Initializes the display and sets it to face selection mode.
  - Loads and displays the STEP file.
  - Adds a menu for batch recognition.
  - Starts the display loop.

### Usage:
- **Interactive Mode:**
  - Click on faces in the 3D window to see their properties in the console.

- **Batch Mode:**
  - Select the menu item to analyze all faces in the model and print their properties.

This script is a useful tool for analyzing the geometry of 3D models in STEP files, particularly for identifying and understanding the types of surfaces present in the model.

## core_webgl_threejs_cylinderhead_faces.py

This Python script is designed to load and render a 3D shape from a BREP (Boundary Representation) file using the pythonOCC library, which is a set of Python bindings for the OpenCASCADE Technology (OCCT), a software development platform for 3D CAD, CAM, CAE, etc.

Here is a concise breakdown of its functionality:

1. **Library Imports**: The script imports necessary modules from the `pythonOCC` library, which include tools for displaying 3D shapes using WebGL, managing BREP shapes, and exploring the topology of these shapes.

2. **Loading the BREP Shape**:
   - A `TopoDS_Shape` object named `cylinder_head` is created to hold the 3D shape.
   - A `BRep_Builder` object named `builder` is instantiated to assist in constructing the shape.
   - The `breptools_Read` function is used to read the BREP file (`cylinder_head.brep`) from the specified path (`../assets/models/cylinder_head.brep`) and load it into the `cylinder_head` object using the `builder`.

3. **Rendering the Shape**:
   - A `ThreejsRenderer` object named `my_renderer` is created to facilitate rendering the shape in a web-based 3D viewer using the Three.js library.
   - The `TopologyExplorer` class is used to extract all the faces of the `cylinder_head` shape.
   - Each face is displayed individually using the `DisplayShape` method of the `my_renderer` object.
   - Finally, the `render` method of the `my_renderer` object is called to render the complete shape in the viewer.

In summary, this script reads a 3D model from a BREP file and renders it in a web-based 3D viewer using the Three.js library through the pythonOCC bindings.

## core_webgl_threejs_random_toruses.py

This Python script generates and displays 100 randomly positioned, oriented, and colored toruses using the `pythonOCC` library, which is a set of Python bindings for the OpenCASCADE geometry kernel. Here’s a breakdown of its functionality:

1. **Imports:**
   - `print_function` from `__future__` ensures compatibility with Python 3's print function.
   - Standard library `random` module for generating random numbers.
   - `threejs_renderer` from `OCC.Display.WebGl` to render shapes using WebGL.
   - `BRepPrimAPI_MakeTorus` from `OCC.Core.BRepPrimAPI` to create torus shapes.
   - `gp_Vec` from `OCC.Core.gp` for vector operations.
   - `translate_shp` and `rotate_shp_3_axis` from `OCC.Extend.ShapeFactory` for transforming shapes.

2. **Renderer Initialization:**
   - `my_ren = threejs_renderer.ThreejsRenderer()`: Initializes the WebGL renderer.

3. **Torus Generation Loop:**
   - `n_toruses = 100`: Specifies the number of toruses to generate.
   - A loop runs 100 times to create, transform, and display each torus:
     - `BRepPrimAPI_MakeTorus(10 + random.random() * 10, random.random() * 10).Shape()`: Creates a torus with random inner and outer radii.
     - Random angles (`angle_x`, `angle_y`, `angle_z`) are generated for rotation.
     - `rotate_shp_3_axis` rotates the torus around the x, y, and z axes by the generated angles.
     - Random translation values (`tr_x`, `tr_y`, `tr_z`) are generated.
     - `translate_shp` translates the rotated torus by the generated vector.
     - Random color (`rnd_color`) and transparency are generated.
     - `my_ren.DisplayShape` displays the transformed torus with the specified color and transparency.
     - Progress is printed to the console.

4. **Rendering:**
   - `my_ren.render()`: Renders the scene with all the generated toruses.

### Summary
The script creates and visually displays 100 toruses with random sizes, positions, orientations, colors, and transparencies using the `pythonOCC` library and WebGL for rendering.

## core_geometry_project_point_on_wire.py

This Python script is designed to read a BREP (Boundary Representation) wire file, discretize the wire, interpolate it using a C2 continuous curve, and project a given point onto the approximated curve. Here is a step-by-step breakdown of its functionality:

1. **Imports and License Information**:
   - The script begins with importing necessary modules and libraries from the `pythonOCC` package, which is used for working with CAD data.
   - License information is provided as comments.

2. **Reading the Wire File**:
   - The script constructs the file path for the wire file (`wire.brep`) located in the `../assets/models/` directory.
   - It initializes a `TopoDS_Shape` object and a `BRep_Builder` object.
   - The wire shape is read from the file using `breptools.Read` and converted to a `TopoDS_Wire`.

3. **Discretizing and Interpolating the Wire**:
   - A `BRepAdaptor_CompCurve` object is created to adapt the wire for further processing.
   - The wire is approximated to a C2 continuous curve using `Approx_Curve3d`.
   - The approximation process considers a tolerance (`tol`), maximum number of segments (`max_segments`), and maximum degrees (`max_degrees`).

4. **Projecting a Point onto the Curve**:
   - A point (`gp_Pnt(1.0, 2.0, 3.0)`) is defined for projection onto the approximated curve.
   - Two methods are used to project the point onto the curve:
     - **Using `GeomAPI_ProjectPointOnCurve`**:
       - The point is projected, and the nearest point on the curve is obtained.
       - The number of possible projection results and the distance to the nearest point are printed.
     - **Using `ShapeAnalysis_Curve().Project`**:
       - The point is projected using `ShapeAnalysis_Curve().Project`.
       - The distance and parameter of the projection are obtained and printed.

In summary, this script reads a wire from a BREP file, approximates it to a smooth curve, and demonstrates two methods of projecting a point onto this curve, outputting the results of these projections.

## core_load_step_ap203_ocaf_from_string.py

This Python code is designed to read and display a 3D model from a STEP file using the pythonOCC library, which is a set of Python bindings for the Open CASCADE Technology (OCCT) CAD kernel. Here's a step-by-step breakdown of its functionality:

1. **Importing Libraries**:
   - Several modules from the `OCC.Core` package are imported, which are essential for handling documents, reading STEP files, and interacting with shapes, colors, layers, and materials.
   - The `init_display` function from `OCC.Display.SimpleGui` is imported to handle the visualization of the 3D model.

2. **Reading the STEP File**:
   - The STEP file path is specified (`filename = "../assets/models/as1_pe_203.stp"`).
   - The file is opened and read into a string (`step_file_as_string`).

3. **Document and Tools Setup**:
   - A document handle is created (`doc = TDocStd_Document("pythonocc-doc")`).
   - Tools for handling shapes, colors, layers, and materials are initialized using the document (`shape_tool`, `l_colors`, `l_layers`, `l_materials`).

4. **STEP File Reader Configuration**:
   - A `STEPCAFControl_Reader` is instantiated and configured to read colors, layers, names, and materials from the STEP file (`step_reader`).
   - The STEP file content is read into the document (`status = step_reader.ReadStream("pyocc_stream", step_file_as_string)`), and if successful (`IFSelect_RetDone`), the data is transferred to the document.

5. **Extracting Shapes and Colors**:
   - Free shapes (root shapes) are retrieved from the document (`shape_tool.GetFreeShapes(labels)`).
   - The number of root shapes is printed.
   - For each root shape, it checks if the shape is an assembly and prints the number of sub-shapes.
   - Colors associated with the shapes are retrieved and printed.

6. **Storing Shapes**:
   - For each root shape, the shape is retrieved and added to the `_shapes` list.

7. **Displaying the Shapes**:
   - The display is initialized (`display, start_display, add_menu, add_function_to_menu = init_display()`).
   - The shapes stored in `_shapes` are displayed (`display.DisplayShape(_shapes, update=True)`).
   - The display loop is started to visualize the shapes (`start_display()`).

In summary, this code reads a STEP file, extracts the shapes, colors, and other attributes, and then visualizes the 3D model using the pythonOCC library.

## core_display_background_image.py

This Python code is a script that utilizes the `pythonOCC` library, which is a set of Python bindings for the Open CASCADE Technology (OCCT) CAD kernel. The script's primary purpose is to create a 3D box shape and display it within a graphical window, with a background image set for the display.

Here's a breakdown of the code's functionality:

1. **Imports:**
   - `init_display` from `OCC.Display.SimpleGui`: Initializes the display window and provides functions to manage it.
   - `BRepPrimAPI_MakeBox` from `OCC.Core.BRepPrimAPI`: Used to create a box primitive.

2. **Initialize the display:**
   - `init_display()` initializes the graphical display environment and returns several functions:
     - `display`: The display object used to control the rendering.
     - `start_display`: A function to start the display loop.
     - `add_menu` and `add_function_to_menu`: Functions to add menus and functions to menus in the display window (not used in this script).

3. **Create a 3D box shape:**
   - `my_box = BRepPrimAPI_MakeBox(10.0, 20.0, 30.0).Shape()`: Creates a box with dimensions 10x20x30 units.

4. **Set the background image:**
   - `display.SetBackgroundImage("../assets/images/nevers-pont-de-loire.jpg", stretch=True)`: Sets a background image for the display window, stretching it to fit the window size.

5. **Display the 3D box:**
   - `display.DisplayShape(my_box, update=True)`: Renders the created box shape in the display window.

6. **Start the display loop:**
   - `start_display()`: Starts the display loop, which keeps the window open and responsive to user interactions.

In summary, this script sets up a graphical display with a background image, creates a 3D box, and renders it in the display window using the `pythonOCC` library.

## core_geometry_quaternion.py

The provided Python script is designed to visualize quaternion rotations and interpolations using the `pythonOCC` library, which is a set of Python bindings for the Open CASCADE Technology (OCCT) CAD kernel.

### Key Components and Functionality:

1. **Imports and Initialization:**
   - The script imports necessary modules from `pythonOCC` for display (`init_display`), geometric primitives (`gp_Quaternion`, `gp_Vec`, `gp_Pnt`), and shape creation (`make_edge`).
   - It initializes the display window and sets up the necessary functions for interacting with the GUI.

2. **Helper Function:**
   - `as_pnt(a_gp_Vec)`: Converts a `gp_Vec` object to a `gp_Pnt` object, which is necessary for displaying points in the 3D viewer.

3. **Rotation Visualization (`rotate` function):**
   - Clears the display and sets up the origin and vectors `vX`, `vY`, and `v45`.
   - Creates a quaternion `q1` for the rotation from `vX` to `vY`.
   - Computes the endpoints of vectors transformed by the quaternion and creates edges (lines) between these points and the origin.
   - Displays the original and transformed edges in different colors (original in red, transformed in green) and adds labels to the points and vectors.

4. **Interpolation Visualization (`interpolate` function):**
   - Clears the display and sets up the origin and vectors `vX`, `vY`, and `v45`.
   - Creates a spherical linear interpolation (`SLerp`) between two quaternions (identity and a quaternion rotating `vX` to `vY`).
   - Iteratively interpolates between the quaternions and displays the interpolated vectors as white edges, slightly displaced to avoid obstruction.
   - Adds labels to the interpolated points.

5. **Float Range Function (`frange`):**
   - A utility function to generate a range of floating-point numbers, used to control the interpolation steps.

6. **Main Execution:**
   - Adds a menu named "quaternion" to the display window.
   - Adds the `rotate` and `interpolate` functions to the menu.
   - Starts the display loop, allowing user interaction with the visualization.

### Purpose:
The script is intended for educational and demonstration purposes, showcasing how quaternions can be used for rotations and interpolations in 3D space. It visualizes these transformations in a 3D viewer, providing an intuitive understanding of quaternion operations.

## core_geometry_bounding_box.py

This Python script is designed to compute and print the bounding boxes of three different 3D shapes: a box, a cylinder, and a torus. It utilizes the `pythonOCC` library, which is a set of Python bindings for the OpenCASCADE CAD kernel.

### Key Components and Functionality:

1. **Imports:**
   - The script imports necessary classes and functions from the `OCC.Core` module, which is part of the `pythonOCC` library. These include:
     - `Bnd_Box` for bounding box representation.
     - `brepbndlib_Add` to add shapes to the bounding box.
     - `BRepPrimAPI_MakeBox`, `BRepPrimAPI_MakeCylinder` for creating box and cylinder shapes.
     - `BRepMesh_IncrementalMesh` for meshing the shapes to improve bounding box accuracy.

2. **Function `get_boundingbox`:**
   - This function computes the bounding box of a given shape (`TopoDS_Shape` or its subclass).
   - **Parameters:**
     - `shape`: The shape for which the bounding box is to be computed.
     - `tol`: Tolerance for the bounding box computation (default is `1e-6`).
     - `use_mesh`: A boolean flag indicating whether to mesh the shape before computing the bounding box (default is `True`).
   - **Process:**
     - Initializes a bounding box `bbox` with a specified gap tolerance.
     - If `use_mesh` is `True`, it meshes the shape to improve accuracy.
     - Adds the shape to the bounding box.
     - Retrieves the minimum and maximum coordinates of the bounding box along the x, y, and z axes.
     - Returns the coordinates and the dimensions of the bounding box.

3. **Main Script Execution:**
   - **Box Bounding Box Computation:**
     - Creates a box shape with dimensions 10.0 x 20.0 x 30.0.
     - Computes and prints the bounding box of the box shape.
   - **Cylinder Bounding Box Computation:**
     - Creates a cylinder shape with a radius of 10.0 and height of 20.0.
     - Computes and prints the bounding box of the cylinder shape.
   - **Torus Bounding Box Computation:**
     - This part of the script seems to have a mistake: it attempts to create a torus but uses `BRepPrimAPI_MakeCylinder` instead. The correct API for a torus should be used (e.g., `BRepPrimAPI_MakeTorus`).
     - Computes and prints the bounding box of the supposed torus shape.

### Summary:
The script demonstrates how to use the `pythonOCC` library to create 3D shapes and compute their bounding boxes. It highlights the importance of meshing for accurate bounding box computation and provides a reusable function for this purpose. However, there is a mistake in the torus creation part, which should be corrected for accurate torus bounding box computation.

## core_dimensions.py

This Python script is designed to create and display a 3D graphical representation of a circle using the pythonOCC library, which is a set of Python bindings for the Open CASCADE Technology (OCCT) 3D CAD modeling library. Here's a breakdown of its purpose and functionality:

1. **Licensing Information**: The script begins with a shebang (`#!/usr/bin/env python`) and a block of comments that provide licensing information, indicating that the code is part of the pythonOCC project and is distributed under the GNU Lesser General Public License.

2. **Imports**: The script imports several modules from the `OCC.Core` package, which are necessary for creating geometric shapes, displaying them, and setting their properties:
    - `gp_Dir`, `gp_Ax2`, `gp_Circ`, `gp_Pnt` for defining geometric primitives.
    - `AIS_Shape` for creating an interactive shape.
    - `PrsDim_RadiusDimension` for creating a radius dimension annotation.
    - `Quantity_Color`, `Quantity_NOC_BLACK` for color definitions.
    - `Prs3d_DimensionAspect` for setting dimension properties.
    - `BRepBuilderAPI_MakeEdge` for creating edges from geometric shapes.
    - `init_display` for initializing the display window.

3. **Display Initialization**: The display window is initialized using `init_display()`, which returns several functions:
    - `display` for managing the display context.
    - `start_display` for starting the display event loop.
    - `add_menu` and `add_function_to_menu` for adding menus and functions to the GUI (not used in this script).

4. **Circle Creation**:
    - A circle (`gp_Circ`) is defined with a center at the point `(200.0, 200.0, 0.0)` and a radius of `80` units. The circle lies in a plane defined by the axis `gp_Ax2` with a direction `gp_Dir(0.0, 0.0, 1.0)` (pointing along the z-axis).
    - An edge (`ec`) is created from this circle using `BRepBuilderAPI_MakeEdge`.

5. **Shape Display**:
    - An interactive shape (`AIS_Shape`) is created from the edge and displayed in the context using `display.Context.Display(ais_shp, True)`.

6. **Radius Dimension Annotation**:
    - A radius dimension (`PrsDim_RadiusDimension`) is created for the edge.
    - A dimension aspect (`Prs3d_DimensionAspect`) is created and its color is set to black using `Quantity_Color(Quantity_NOC_BLACK)`.
    - The dimension aspect is applied to the radius dimension using `rd.SetDimensionAspect(the_aspect)`.
    - The radius dimension is displayed in the context using `display.Context.Display(rd, True)`.

7. **Final Display Setup**:
    - The display is fitted to show all objects using `display.FitAll()`.
    - The display event loop is started with `start_display()`.

In summary, the script creates a 3D graphical representation of a circle with a radius dimension annotation and displays it using the pythonOCC library.

## core_geometry_point_from_curve.py

This Python script is designed to use the `pythonOCC` library, a set of Python bindings for Open CASCADE Technology (OCCT), which is a software development platform for 3D CAD, CAM, CAE. The script demonstrates how to create a 2D circle, sample points along the circle at uniform intervals, and display both the circle and the sampled points in a graphical window.

Here's a breakdown of its functionality:

1. **Imports**:
   - Various classes and functions from `OCC.Core` modules for geometric and display operations.
   - `init_display` from `OCC.Display.SimpleGui` to initialize the graphical display.

2. **Display Initialization**:
   - `init_display()` is called to set up the display environment, returning `display`, `start_display`, `add_menu`, and `add_function_to_menu`.

3. **Function `points_from_curve`**:
   - **Circle Creation**: A 2D circle is created using `Geom2d_Circle` with a radius of 5.0 units.
   - **Curve Adaptation**: The circle is adapted to a 2D curve using `Geom2dAdaptor_Curve`.
   - **Uniform Sampling**: Points along the curve are sampled at uniform intervals (abscissa of 3.0 units) using `GCPnts_UniformAbscissa`.
   - **Point Extraction**: If the sampling is successful (`ua.IsDone()`), the sampled points are extracted and stored in a list `a_sequence`.
   - **Display Circle**: The circle is displayed using `display.DisplayShape`.
   - **Display Points**: Each sampled point is converted to a 3D point (`gp_Pnt`) for display purposes, and both the point and its corresponding parameter value are displayed.

4. **Main Execution Block**:
   - When the script is run as the main module, it calls `points_from_curve()` to perform the operations and then starts the display loop with `start_display()`.

### Purpose and Functionality:
- **Purpose**: To demonstrate the creation and sampling of a 2D circle using `pythonOCC`, and to visualize the circle and the sampled points in a graphical window.
- **Functionality**: 
  - Creates a 2D circle.
  - Samples points along the circle at uniform intervals.
  - Displays the circle and the sampled points along with their parameter values in a 3D graphical window.

This script serves as an example of how to use `pythonOCC` for basic geometric operations and visualization.

## core_geometry_medial_axis_offset.py

This Python script uses the `pythonOCC` library, which is a set of Python bindings for the OpenCASCADE CAD kernel. The script's purpose is to create a geometric shape, generate offset contours from it, and display these shapes using a graphical interface.

Here's a breakdown of the script's functionality:

1. **Imports**: The script imports various modules from the `pythonOCC` library for creating and manipulating geometric shapes and for displaying these shapes.

2. **Helper Functions**:
   - `boolean_cut(shapeToCutFrom, cuttingShape)`: Performs a boolean cut operation between two shapes and returns the resulting shape.
   - `make_face_to_contour_from()`: Creates a complex face shape made up of multiple vertices and edges. It also performs a boolean cut to create a hole in the face and returns the resulting face.
   - `create_offsets(face, nr_of_counters, distance_between_contours)`: Generates multiple offset contours from a given face. It initializes an offset operation and iteratively performs the offset to create a series of contours at specified distances.

3. **Main Execution**:
   - The script first creates a complex face shape by calling `make_face_to_contour_from()`.
   - It then displays this initial face shape.
   - The script generates 50 offset contours from the initial face, each 0.12 units apart, using the `create_offsets` function.
   - Each generated contour is displayed.
   - Finally, the display is fitted to show all shapes, and the graphical interface is started to allow user interaction.

### Summary

The script demonstrates how to use `pythonOCC` to create a geometric face, generate multiple offset contours from this face, and display them using a graphical interface. This can be particularly useful in CAD applications where offsetting contours is a common operation, such as in CNC machining or creating tool paths.

## core_geometry_curves2d_from_offset.py

The provided Python code is a script that utilizes the pythonOCC library to create and display 2D B-spline curves and their offset curves. Here is a detailed breakdown of its purpose and functionality:

1. **Imports and Initialization**:
   - The script imports necessary modules from the pythonOCC library, which is a set of Python bindings for Open CASCADE Technology (OCCT), a software development platform for 3D CAD, CAM, CAE, etc.
   - It initializes a display window using the `init_display` function from `OCC.Display.SimpleGui`.

2. **Function Definition**:
   - The function `curves2d_from_offset` is defined to create and display 2D B-spline curves and their offset curves.
   - Inside this function:
     - A `TColgp_Array1OfPnt2d` array is created and filled with five 2D points.
     - A B-spline curve (`spline_1`) is generated from these points using `Geom2dAPI_PointsToBSpline`.
     - Two offset curves (`offset_curve1` and `offset_curve2`) are created at distances of 1 and 1.5 units from the original B-spline curve, respectively.
     - The continuity of these offset curves is checked using the `IsCN` method, and the results are printed to the console.
     - The original B-spline curve and its offset curves are displayed in the initialized display window with different colors (yellow and blue).

3. **Main Execution Block**:
   - When the script is executed, the `curves2d_from_offset` function is called to create and display the curves.
   - The `start_display` function is called to start the display loop, allowing the user to interact with the graphical window.

### Summary
The script demonstrates how to use the pythonOCC library to:
- Create a 2D B-spline curve from a set of points.
- Generate offset curves from the original B-spline curve.
- Check the continuity of the offset curves.
- Display the original and offset curves in a graphical window with different colors.

This script is useful for visualizing and analyzing 2D B-spline curves and their offsets in a CAD-like environment.

## core_topology_draft_angle.py

This Python code is a script that uses the `pythonOCC` library to create a 3D model of a box and apply a draft angle to its faces. Here’s a detailed breakdown of its purpose and functionality:

### Purpose
The main purpose of the script is to demonstrate how to create a 3D box and apply a draft angle to its faces using the `pythonOCC` library. This is typically used in CAD (Computer-Aided Design) applications to add taper to the faces of a 3D model, which is often required in manufacturing processes like injection molding.

### Functionality Breakdown

1. **Imports**:
    - Various modules from `OCC.Core` are imported to handle geometric shapes, transformations, and display functionalities.
    - `math` is imported for mathematical operations.

2. **Display Initialization**:
    - `init_display()` is called to set up the display environment for visualizing the 3D model. It returns several functions for managing the display.

3. **`draft_angle` Function**:
    - This function is defined to create a box and apply a draft angle to its faces.
    - `BRepPrimAPI_MakeBox(200.0, 300.0, 150.0).Shape()` creates a 3D box with dimensions 200x300x150 units.
    - `BRepOffsetAPI_DraftAngle(S)` initializes the draft angle operation on the box `S`.
    - `TopExp_Explorer` is used to iterate over the faces of the box.
    - For each face, it checks if the face is normal to the Z-axis (`gp_Dir(0, 0, 1)`) using `IsNormal`.
    - If the face is normal, it adds a draft angle of 15 degrees to the face using `adraft.Add`.
    - `adraft.Build()` finalizes the draft angle operation.
    - `display.DisplayShape(adraft.Shape(), update=True)` displays the modified shape.

4. **Main Execution**:
    - When the script is run directly, it calls `draft_angle()` to perform the draft angle operation.
    - `start_display()` is called to start the interactive display window where the 3D model can be viewed.

### Summary
The script creates a 3D box and applies a 15-degree draft angle to all faces that are normal to the Z-axis. It uses the `pythonOCC` library for CAD operations and visualization. The result is displayed in an interactive window where users can view the modified 3D model.

## core_visualization_ais_coloredshape.py

This Python code is part of the pythonOCC library, which is a set of Python bindings for the OpenCASCADE 3D CAD, CAM, CAE system. The code's primary purpose is to create a 3D box, color its faces randomly, and display it in a graphical viewer. Here is a breakdown of its functionality:

1. **License Information**: The initial comments provide information about the licensing under the GNU Lesser General Public License.

2. **Imports**:
   - `from __future__ import print_function`: Ensures compatibility with Python 2 and 3.
   - `from random import random`: Imports the `random` function to generate random colors.
   - Various imports from the `OCC` module to handle 3D shapes, colors, and display functionalities.

3. **Display Initialization**:
   - `init_display()` initializes the display window and returns the display objects needed for rendering.

4. **Box Creation**:
   - `my_box = BRepPrimAPI_MakeBox(10.0, 20.0, 30.0).Shape()`: Creates a 3D box with dimensions 10x20x30 units.

5. **Shape Coloring**:
   - `ais_shp = AIS_ColoredShape(my_box)`: Wraps the box shape in an `AIS_ColoredShape` to allow for custom coloring.
   - A loop iterates over each face of the box, using `TopologyExplorer(my_box).faces()`.
   - For each face, `ais_shp.SetCustomColor(fc, rgb_color(random(), random(), random()))` assigns a random color.

6. **Display**:
   - `display.Context.Display(ais_shp, True)`: Adds the colored shape to the display context.
   - `display.FitAll()`: Adjusts the view to fit the entire shape within the display window.
   - `start_display()`: Starts the display loop, rendering the window and allowing user interaction.

In summary, this script uses pythonOCC to create a 3D box, assigns random colors to each of its faces, and displays it in a graphical window.

## core_topology_local_ops.py

This Python script is a set of functions designed for performing various 3D geometric operations using the pythonOCC library, which is a set of Python bindings for the Open CASCADE Technology (OCCT) CAD kernel. The script includes functions for creating and manipulating 3D shapes, such as boxes, extrusions, offsets, and revolutions, and then displaying these shapes using a graphical interface.

Here's a concise description of the key components and functionality:

1. **Imports and Initialization**:
   - The script imports necessary modules from the `OCC` library to handle 3D geometric operations.
   - It initializes the display using `init_display` from the `OCC.Display.SimpleGui` module.

2. **Function Definitions**:
   - **`extrusion`**: Creates a box, selects a face, creates a 2D sketch on that face, and extrudes the sketch to form a protrusion.
   - **`brepfeat_prism`**: Creates a box, selects a face, draws a circle on it, and extrudes the circle to form a prism.
   - **`thick_solid`**: Creates a box and thickens its faces to form a solid with a specified wall thickness.
   - **`offset_cube`**: Creates a box and offsets its faces inward to create a hollow shape.
   - **`split_shape`**: Creates a box and splits it using a plane.
   - **`brep_feat_rib`**: Creates a prism and adds a rib feature to it.
   - **`brep_feat_local_revolution`**: Creates a box and performs a local revolution around an axis.
   - **`brep_feat_extrusion_protrusion`**: Demonstrates both extrusion and protrusion operations on a box.
   - **`exit`**: Exits the application.

3. **Menu and Event Handling**:
   - The script adds a menu called "topology local operations" with various geometric operations as menu items.
   - Each menu item is linked to the corresponding function.
   - The `start_display` function is called to start the graphical interface and display the menu.

4. **Execution**:
   - When the script is executed, it sets up the menu and event handlers and then starts the display loop, allowing users to select and execute different geometric operations interactively.

Overall, the script serves as a demonstration and interactive tool for performing and visualizing various 3D geometric operations using the pythonOCC library.

## core_geometry_bisector.py

This Python code is a part of the `pythonOCC` library, which is used for 3D CAD modeling and visualization. The primary purpose of this script is to demonstrate the calculation and visualization of bisectors between different geometric entities, such as lines, circles, and points, in a 2D space. Here's a detailed breakdown of its functionality:

1. **Imports**: The code imports various modules and classes from the `OCC` library, which provide functions for creating and manipulating geometric shapes, as well as for displaying them in a GUI.

2. **GUI Initialization**: The `init_display` function initializes a simple graphical user interface (GUI) for displaying the shapes.

3. **Functions for Bisector Calculations**:
    - `bisect_lineline(event=None)`: Calculates and displays the bisectors between two lines.
    - `bisect_linecircle(event=None)`: Calculates and displays the bisector between a line and a circle.
    - `bisect_pnt(event=None)`: Calculates and displays the bisector between two points.
    - `bisect_crvcrv(event=None)`: Calculates and displays the bisector between a circle and a line.

4. **Visualization**:
    - Each function uses the `display` object to erase any previous shapes and then display new ones.
    - Shapes are created using the `gp_Lin2d`, `gp_Circ2d`, `gp_Pnt2d`, and other geometric classes.
    - Bisectors are calculated using the `GccAna_Lin2dBisec`, `GccAna_CircLin2dBisec`, `GccAna_Pnt2dBisec`, and `Bisector_BisecCC` classes.
    - The calculated bisectors are displayed in different colors for visual distinction.

5. **Main Execution**:
    - The `__main__` block adds a menu named "bisector" to the GUI.
    - It associates the bisector calculation functions with menu items.
    - The `start_display()` function launches the GUI.

In summary, this script is a demonstration tool for visualizing the bisectors between various geometric entities using the `pythonOCC` library. It provides an interactive GUI where users can select different bisector calculations and see the results displayed graphically.

## core_meshDS_numpy.py

This Python code demonstrates how to create and visualize a triangular mesh using the `MeshDS_DataSource` from the Open CASCADE Technology (OCC) library. Here is a step-by-step description of its purpose and functionality:

1. **Imports**:
   - `numpy` for numerical operations.
   - `Delaunay` from `scipy.spatial` for generating a Delaunay triangulation.
   - Various components from the OCC library for mesh data handling and visualization.
   - `init_display` from `OCC.Display.SimpleGui` for setting up the display window.

2. **Function `getMesh(X=100, Y=100)`**:
   - Generates a grid of points using `numpy.linspace` and `numpy.meshgrid` within the range of -5 to 5 for both `x` and `y` dimensions.
   - Computes `z` values based on a mathematical function involving sine and division.
   - Flattens the `xx`, `yy`, and `z` arrays and stacks them into a single array `xyz` representing vertices.
   - Uses `Delaunay` to generate a triangulation of the `x` and `y` coordinates, returning the vertices and the simplices (triangles).

3. **Mesh Data Preparation**:
   - Calls `getMesh()` to generate vertices and faces (triangles) for the mesh.

4. **Mesh Data Source**:
   - Creates a `MeshDS_DataSource` object using the vertices and faces. This object serves as the data source for the mesh.

5. **Mesh Visualizer**:
   - Creates a `MeshVS_Mesh` object, which is a visualizer for the mesh data.
   - Sets the data source for the visualizer using `SetDataSource`.

6. **Presentation Builder**:
   - Creates a `MeshVS_MeshPrsBuilder` object, which is responsible for building the presentation of the mesh.
   - Adds the presentation builder to the visualizer using `AddBuilder`.

7. **Display Setup**:
   - Initializes the display using `init_display`, which returns functions to control the display.
   - Displays the mesh visualizer using `display.Context.Display`.
   - Fits the displayed mesh to the view using `display.FitAll`.
   - Starts the display loop with `start_display`.

This code effectively creates a 3D plot of a mathematical surface using a triangular mesh and visualizes it in a graphical window. The mesh is generated from a grid of points and triangulated using Delaunay triangulation. The OCC library is used to handle and visualize the mesh data.

## core_modeling_bool_demo.py

The provided Python code is a script that utilizes the `pythonOCC` library, which is a set of Python bindings for the Open CASCADE Technology (OCCT) CAD kernel. The script demonstrates various CAD operations, including creating and manipulating 3D shapes, performing boolean operations, and transforming geometries. Here is a concise description of its purpose and functionality:

1. **Initialization and Imports**: The script imports necessary modules from `pythonOCC` and initializes the display for visualizing the 3D shapes.

2. **Shape Generation**:
   - **`generate_shape`**: Creates a basic sphere with specific angular constraints.
   - **`add_feature`**: Adds a cylindrical hole through the sphere, modifying its geometry.
   - **`boolean_cut`**: Creates a cylinder and performs repeated boolean cut operations to subtract the cylinder from the base shape at various positions.
   - **`boolean_fuse`**: Creates a torus and fuses it with the base shape.
   - **`revolved_cut`**: Defines a set of points to create a hexagonal face, revolves this face around an axis to form a solid, and then subtracts this revolved shape from the base shape.

3. **Demo Generation**:
   - **`generate_demo`**: Combines all the above steps to generate a complex shape by sequentially applying the operations defined in the previous functions.

4. **Main Execution**:
   - If the script is run as the main program, it generates the demo shape and displays it using the initialized display functions.

The script effectively demonstrates how to create, modify, and visualize complex 3D geometries using the `pythonOCC` library.

## core_load_step_with_colors.py

This Python script is designed to read and display 3D models from STEP files using the pythonOCC library, which is a set of Python bindings for the OpenCASCADE 3D CAD modeling library. Here's a breakdown of its functionality:

1. **Importing Required Modules:**
   - `read_step_file_with_names_colors` from `OCC.Extend.DataExchange`: Reads a STEP file and extracts shapes, names, and colors.
   - `Quantity_Color` and `Quantity_TOC_RGB` from `OCC.Core.Quantity`: Used for color representation.
   - `init_display` from `OCC.Display.SimpleGui`: Initializes the graphical display.

2. **Setting the Filename:**
   - The script specifies the path to the STEP file to be read. The filename is set to `"../assets/models/as1-oc-214.stp"`. There are also commented-out lines for other STEP files that could be used instead.

3. **Reading the STEP File:**
   - `shapes_labels_colors = read_step_file_with_names_colors(filename)`: This function reads the STEP file and returns a dictionary where keys are shapes, and values are tuples containing labels and colors.

4. **Initializing the Display:**
   - `display, start_display, add_menu, add_function_to_menu = init_display()`: Initializes the graphical display environment and returns functions to control the display.

5. **Displaying Shapes with Colors:**
   - The script iterates over the `shapes_labels_colors` dictionary. For each shape, it retrieves the associated label and color.
   - `display.DisplayColoredShape(shpt_lbl_color, color=Quantity_Color(c.Red(), c.Green(), c.Blue(), Quantity_TOC_RGB))`: Displays each shape in the graphical window with its corresponding color.

6. **Starting the Display:**
   - `start_display()`: Starts the graphical display loop, allowing the user to interact with the 3D model.

### Summary
The purpose of this script is to read a 3D model from a STEP file, extract the shapes and their associated colors, and display them in a graphical window using the pythonOCC library. The script is set up to be flexible, allowing different STEP files to be used by changing the filename variable.

## core_webgl_threejs_bigfile_multipleshapes.py

The provided Python code is designed to read and render a 3D model from a STEP file using the `pythonOCC` library, which is a set of Python wrappers for the OpenCASCADE library, a software development platform for 3D CAD, CAM, CAE. Here is a clear and concise description of the code's purpose and functionality:

### Purpose:
The code loads a STEP file, which is a common file format for 3D models, and renders it in a web browser using a WebGL-based renderer.

### Functionality:
1. **Import Libraries:**
   - Imports necessary modules from `os`, `sys`, `zipfile`, and `pythonOCC` libraries.

2. **Define File Paths:**
   - Constructs the path to the STEP file (`stp_file`) and checks if it exists.
   - If the STEP file does not exist, it assumes that the file is compressed in a ZIP file (`zip_file_path`) and extracts it.

3. **Read STEP File:**
   - Uses the `read_step_file` function from `OCC.Extend.DataExchange` to read the STEP file and obtain a shape object (`big_shp`).

4. **Explore Topology:**
   - Uses `TopologyExplorer` from `OCC.Extend.TopologyUtils` to extract all solid subshapes from the main shape.

5. **Render the Model:**
   - Initializes a `ThreejsRenderer` object from `OCC.Display.WebGl`.
   - Iterates over each solid subshape and displays it using the renderer.
   - Finally, calls the `render` method to display the 3D model in a web browser.

### Summary:
This script automates the process of loading a 3D model from a STEP file, extracting its components, and rendering them using a web-based 3D viewer. This can be particularly useful for visualizing complex assemblies in a browser without needing specialized CAD software.

## core_geometry_oriented_bounding_box.py

The provided Python script is designed to demonstrate the use of the pythonOCC library for 3D CAD modeling. Specifically, it focuses on computing and displaying oriented bounding boxes (OBBs) for a set of randomly generated points and a 3D model loaded from a BREP file. Here is a detailed breakdown of its purpose and functionality:

1. **License and Imports**:
   - The script starts with a license header indicating that it is part of the pythonOCC project and is distributed under the GNU Lesser General Public License.
   - Various modules from the pythonOCC library are imported to handle 3D CAD operations, such as creating shapes, computing bounding boxes, and displaying the results.

2. **Display Initialization**:
   - The `init_display` function initializes the display environment for rendering 3D shapes.

3. **Function Definition**:
   - `convert_bnd_to_shape(the_box)`: This function takes an oriented bounding box (`the_box`) as input and converts it into a 3D box shape using the BRepPrimAPI_MakeBox function. It calculates the center, directions, and half-sizes of the bounding box to create the corresponding box shape.

4. **Compute OBB for Random Points**:
   - An empty oriented bounding box (`obb1`) is initialized.
   - A loop generates a specified number (`num_points`) of random points within a given range (100 to 500 in each coordinate).
   - Each point is added to the display and included in the bounding box computation using `brepbndlib.AddOBB`.
   - The resulting bounding box (`obb1`) is converted to a shape using the `convert_bnd_to_shape` function and displayed with transparency.

5. **Compute OBB for Loaded BREP Model**:
   - A 3D shape (`cylinder_head`) is initialized and loaded from a BREP file located at `../assets/models/cylinder_head.brep`.
   - An empty oriented bounding box (`obb2`) is initialized.
   - The BREP model is added to the bounding box computation with additional parameters to optimize the bounding box.
   - The resulting bounding box (`obb2`) is converted to a shape and displayed with transparency alongside the original BREP model.

6. **Start Display**:
   - The `start_display` function is called to begin the interactive display loop, allowing the user to view the 3D shapes and their bounding boxes.

In summary, this script demonstrates the creation and visualization of oriented bounding boxes for both randomly generated points and a pre-existing 3D model using the pythonOCC library. It showcases the process of computing bounding boxes, converting them to shapes, and rendering them in a 3D display environment.

## core_geometry_overlap.py

This Python script is designed to detect and visualize the overlapping regions between two 3D box shapes using the pythonOCC library, which is a set of Python bindings for the OpenCASCADE CAD kernel. Here's a detailed breakdown of its functionality:

1. **Imports and Initialization**:
   - The script imports necessary modules from the pythonOCC library, including classes for creating points (`gp_Pnt`), boxes (`BRepPrimAPI_MakeBox`), meshing (`BRepMesh_IncrementalMesh`), and shape proximity detection (`BRepExtrema_ShapeProximity`).
   - It also imports functions for initializing a display window (`init_display`).

2. **Display Initialization**:
   - The `init_display` function is called to initialize the display window and related functions (`display`, `start_display`, `add_menu`, and `add_function_to_menu`).

3. **Create and Mesh Boxes**:
   - Two intersecting box shapes are created using `BRepPrimAPI_MakeBox` with specified corner points:
     - `box1` spans from (0, 0, 0) to (20, 20, 20).
     - `box2` spans from (10, 10, 10) to (30, 30, 30).
   - These boxes are then meshed using `BRepMesh_IncrementalMesh` with a specified deflection value of `1e-3`.

4. **Perform Shape Proximity Check**:
   - A proximity check is performed between the two boxes using `BRepExtrema_ShapeProximity` with a tolerance of `0.1`.
   - The `Perform` method is called to execute the proximity detection algorithm.

5. **Retrieve and Store Overlapping Faces**:
   - The script retrieves the indices of the overlapping faces from both shapes using `OverlapSubShapes1` and `OverlapSubShapes2`.
   - For each index, the corresponding face is fetched using `GetSubShape1` and `GetSubShape2` and stored in lists (`shape_1_faces` and `shape_2_faces`).

6. **Visualization**:
   - The two box shapes are displayed with a transparency of 0.5.
   - The overlapping faces from both shapes are displayed in red.
   - The `FitAll` method is called to adjust the view to fit all displayed shapes, and `start_display` is called to start the interactive display loop.

### Summary
This script creates two intersecting 3D boxes, checks for overlapping regions between them, and visually highlights these regions in a display window. It uses the pythonOCC library for CAD operations and visualization. The overlapping faces are displayed in red to clearly indicate the intersecting areas.

## core_visualization_camera_2.py

The provided Python code is a script designed for 3D visualization using the `pythonOCC` library, which is a set of Python bindings for the Open Cascade Technology (OCC) CAD kernel. Here is a clear and concise description of its purpose and functionality:

1. **Initialization and Imports**:
    - The script starts by importing necessary modules from the `pythonOCC` library.
    - `BRepPrimAPI_MakeBox` is used to create a 3D box shape.
    - `init_display` initializes the display window for rendering the 3D shapes.

2. **Display Initialization**:
    - The `init_display` function is called, which returns several functions: `display`, `start_display`, `add_menu`, and `add_function_to_menu`.
    - `display` is used to manage the rendering of shapes.
    - `start_display` starts the display loop.
    - `add_menu` and `add_function_to_menu` are used to add a menu and associated functions to the display window.

3. **Shape Creation and Display**:
    - A 3D box shape with dimensions 300x200x100 is created using `BRepPrimAPI_MakeBox`.
    - This shape is then displayed in the rendering window using `display.DisplayShape`.

4. **Animation Function**:
    - The `animate_viewpoint` function is defined to animate the camera viewpoint.
    - It retrieves the current camera (`cam`) and its eye position (`eye`).
    - The camera's eye position is modified in a loop to create a simple animation effect, moving the camera's Y-coordinate incrementally.
    - After each modification, the viewer is updated to reflect the new camera position.

5. **Menu and Function Binding**:
    - A menu named "camera" is added to the display window.
    - The `animate_viewpoint` function is bound to the "camera" menu, allowing the user to trigger the animation from the menu.

6. **Start Display Loop**:
    - The `start_display` function is called to start the display loop, rendering the 3D shape and providing an interactive window with the "camera" menu.

In summary, this script sets up a 3D visualization environment using `pythonOCC`, displays a 3D box, and provides a menu option to animate the camera viewpoint around the displayed shape.

## core_topology_pipe.py

This Python script uses the pythonOCC library, which is a set of Python bindings for the OpenCASCADE CAD kernel. The primary purpose of the script is to create and display a 3D pipe shape using B-spline curves for both the profile and the path of the pipe.

Here is a detailed breakdown of its functionality:

1. **Imports and Initialization**:
    - The script imports necessary modules from the `OCC` library to create geometric shapes and display them.
    - The `init_display` function initializes the display environment for visualizing the 3D shapes.

2. **Function `pipe()`**:
    - **Path Creation**:
        - A B-spline curve is created to serve as the path of the pipe. This is done by defining three 3D points and using `GeomAPI_PointsToBSpline` to generate the curve.
        - The curve is then converted into an edge and subsequently into a wire, which is necessary for creating the pipe.
    - **Profile Creation**:
        - Another B-spline curve is created to serve as the profile of the pipe. This involves defining five 3D points and generating the curve in a similar manner as the path.
        - The profile curve is converted into an edge.
    - **Pipe Creation**:
        - The `BRepOffsetAPI_MakePipe` function is used to create a pipe shape by sweeping the profile edge along the path wire.
    - **Display**:
        - The profile edge, path wire, and resulting pipe shape are displayed using the initialized display environment.

3. **Main Execution**:
    - If the script is executed directly (not imported as a module), the `pipe()` function is called to create and display the pipe.
    - The `start_display()` function is called to start the GUI event loop, allowing the user to interact with the 3D visualization.

### Summary
The script creates a 3D pipe by sweeping a B-spline curve profile along a B-spline curve path and displays the resulting shape using the pythonOCC library's visualization tools.

## core_load_step_ap214_with_materials.py

This Python code is designed to read a STEP file, extract material information from it, and print out the details of each material found. It utilizes the `pythonOCC` library, which is a set of Python bindings for the Open CASCADE Technology (OCCT) framework, commonly used for 3D CAD, CAM, and CAE.

Here is a step-by-step description of the code's functionality:

1. **Import necessary modules from `pythonOCC`**:
   - `TDocStd_Document` for creating a document handle.
   - `XCAFDoc_DocumentTool_MaterialTool` for accessing material tools.
   - `STEPCAFControl_Reader` for reading STEP files.
   - `IFSelect_RetDone` for checking the status of the STEP file reading process.
   - `TDF_LabelSequence` for handling sequences of labels.

2. **Specify the STEP file to be read**:
   - The file path is set to `../assets/models/eight_cyl.stp`.

3. **Create a document handle**:
   - A new document is created with the identifier `"pythonocc-doc"`.

4. **Initialize the material tool**:
   - The material tool is obtained from the document's main assembly.

5. **Read the STEP file**:
   - A `STEPCAFControl_Reader` object is created.
   - The STEP file specified by `filename` is read.
   - If the file is successfully read (`status == IFSelect_RetDone`), the data is transferred to the document.

6. **Extract material labels**:
   - A `TDF_LabelSequence` object is created to store material labels.
   - The material tool retrieves the material labels and stores them in `material_labels`.

7. **Iterate through the material labels and print material properties**:
   - For each material label, the material properties are retrieved using `mat_tool.GetMaterial()`.
   - The properties include:
     - `material_name`
     - `material_description`
     - `material_density`
     - `material_densname`
     - `material_densvaltype`
   - These properties are printed to the console.

In summary, this script reads a STEP file, extracts material information, and prints the details of each material found in the file. It leverages the `pythonOCC` library to handle the STEP file and extract the necessary information.

## core_inherit_topods_shape.py

This Python code demonstrates how to create a custom class that inherits from the `TopoDS_Edge` class, which is a part of the Open CASCADE Technology (OCCT) library used for 3D CAD, CAM, CAE, etc. The code specifically shows how to extend the functionality of a `TopoDS_Edge` object and how to visualize it using the pythonOCC library.

### Key Components and Functionality:

1. **Imports**:
   - The code imports necessary modules from the `OCC.Core` package for creating and manipulating geometric shapes (`BRepBuilderAPI_MakeEdge`, `TopoDS_Edge`, `gp_Pnt`, `BRep_Tool`).
   - It also imports the `init_display` function from `OCC.Display.SimpleGui` for visualization purposes.

2. **InheritEdge Class**:
   - The `InheritEdge` class inherits from `TopoDS_Edge`.
   - The `__init__` method initializes the inherited edge by copying the base shape's properties (TShape, Location, Orientation) to the new object.
   - The `get_curve` method uses the `BRep_Tool.Curve` function to retrieve the geometric curve associated with the edge.

3. **Main Execution**:
   - The main block of the code:
     - Creates a base edge using `BRepBuilderAPI_MakeEdge` with two points `(0,0,0)` and `(100,0,0)`.
     - Instantiates an `InheritEdge` object from the base edge.
     - Prints the curve associated with the `inherited_edge`.
     - Initializes the display window, displays the inherited edge, and starts the display loop.

### Purpose:
The main purpose of this code is to demonstrate how to extend the `TopoDS_Edge` class in pythonOCC, copy an existing edge's properties to a new object, and retrieve its geometric curve. Additionally, it shows how to visualize the edge using the pythonOCC's display functionalities.

### Visualization:
- The `init_display` function sets up the visualization environment.
- The `display.DisplayShape` method is used to render the `inherited_edge`.
- The `start_display` function starts the interactive display loop, allowing the user to view and interact with the rendered shape.

This example is useful for developers working with 3D geometric modeling who need to extend and manipulate basic shapes provided by the OCCT library and visualize the results.

## core_load_stl.py

This Python script is designed to read and display a 3D model from an STL file using the `pythonOCC` library, which is a set of Python bindings for the Open CASCADE Technology (OCCT) framework. Here is a detailed breakdown of its purpose and functionality:

1. **Copyright and Licensing Information:**
   - The script begins with a block comment that includes copyright information and licensing terms under the GNU Lesser General Public License. This indicates that the script is part of the `pythonOCC` project and outlines the terms under which it can be used and modified.

2. **Import Statements:**
   - The script imports necessary modules:
     - `os`: A standard library module for interacting with the operating system, used here to construct file paths.
     - `init_display` from `OCC.Display.SimpleGui`: A function to initialize the display window for rendering the 3D model.
     - `read_stl_file` from `OCC.Extend.DataExchange`: A function to read STL files and convert them into shapes that can be displayed.

3. **File Path Construction:**
   - The script constructs the path to the STL file (`fan.stl`) which is assumed to be located in the `../assets/models/` directory relative to the script's location. This is done using `os.path.join`.

4. **Reading the STL File:**
   - The `read_stl_file` function is called with the constructed file path as an argument. This function reads the STL file and returns a shape object (`stl_shp`) that represents the 3D model.

5. **Initializing Display:**
   - The `init_display` function is called to set up the display window. This function returns four objects:
     - `display`: The main display object used to render shapes.
     - `start_display`: A function to start the display loop.
     - `add_menu` and `add_function_to_menu`: Functions for adding menus and menu items to the display window, although they are not used in this script.

6. **Displaying the Shape:**
   - The `DisplayShape` method of the `display` object is called with the shape (`stl_shp`) as an argument and `update=True` to render the 3D model in the display window.

7. **Starting the Display Loop:**
   - The `start_display` function is called to start the display loop, which keeps the window open and responsive to user interactions.

In summary, this script reads a 3D model from an STL file and displays it in a graphical window using the `pythonOCC` library.

## core_display_point_cloud.py

This Python script is designed to visualize point cloud data using the `pythonOCC` library, which is a set of Python bindings for the Open CASCADE Technology (OCCT) 3D modeling library. The script provides functionalities to display random points, a predefined "bunny" model, and a "tabletop" model from Point Cloud Data (PCD) files.

### Key Components and Functionality:

1. **Imports and Initialization**:
    - Imports necessary modules from `pythonOCC` and standard Python libraries.
    - Initializes a display window using `init_display()` from `OCC.Display.SimpleGui`.

2. **Function Definitions**:
    - **`pcd_get_number_of_vertices(pcd_filename)`**:
        - Reads a PCD file header to determine the number of vertices (points) in the file.

    - **`random_points(event=None)`**:
        - Generates a random set of 500,000 3D points within a specified range.
        - Creates and displays a point cloud of these random points.

    - **`bunny(event=None)`**:
        - Loads a "bunny" model from a PCD file.
        - Reads the number of vertices from the file.
        - Creates a point cloud from the vertices and displays it.

    - **`tabletop(event=None)`**:
        - Loads a "tabletop" model from a PCD file.
        - Reads the vertices and their RGB color values.
        - Creates a colored point cloud from the vertices and displays it.

    - **`unpackRGB(rgb)`**:
        - Converts a packed RGB float value into individual red, green, and blue components.

3. **Main Execution**:
    - Adds a menu named "pointcloud" to the display window.
    - Adds the functions `random_points`, `bunny`, and `tabletop` to the menu.
    - Starts the display loop with `start_display()`.

### Purpose:
The script is primarily used for visualizing point cloud data. It can display:
- A large set of randomly generated points.
- A predefined "bunny" model loaded from a PCD file.
- A "tabletop" model with color information loaded from a PCD file.

This tool can be useful for developers and researchers working with 3D point cloud data, providing a way to visualize and interact with the data using the `pythonOCC` library.

## core_display_background_gradient_color.py

This Python code is a script that uses the `pythonOCC` library, which is a set of Python bindings for the OpenCASCADE technology, a software development platform for 3D CAD, CAM, CAE, etc. Here's a clear and concise description of the code's purpose and functionality:

### Purpose:
The script creates a 3D visualization of a box using the `pythonOCC` library and displays it in a graphical window with a gradient background.

### Functionality:
1. **Library Imports**:
   - `init_display` from `OCC.Display.SimpleGui`: Initializes the display window.
   - `BRepPrimAPI_MakeBox` from `OCC.Core.BRepPrimAPI`: Used to create a box shape.
   - Various color-related classes and constants from `OCC.Core.Quantity`: For setting the background gradient colors.

2. **Display Initialization**:
   - `display, start_display, add_menu, add_function_to_menu = init_display()`: Initializes the display window and sets up functions to interact with it.

3. **Box Creation**:
   - `my_box = BRepPrimAPI_MakeBox(10.0, 20.0, 30.0).Shape()`: Creates a box shape with dimensions 10x20x30 units.

4. **Background Gradient Setup**:
   - `display.View.SetBgGradientColors(...)`: Sets the background gradient of the display window from `ALICEBLUE` to `ANTIQUEWHITE`.

5. **Display and Render**:
   - `display.Repaint()`: Refreshes the display to apply the background gradient.
   - `display.DisplayShape(my_box, update=True)`: Displays the created box in the display window.
   - `start_display()`: Starts the display loop, allowing the window to remain open and interactive.

### Summary:
The script uses `pythonOCC` to create and display a 3D box with specified dimensions in a window that has a gradient background. It initializes the display, creates the box, sets the background colors, and then renders the box in the display window.

## core_webgl_x3dom_cylinderhead.py

This Python script is designed to load and render a BREP (Boundary Representation) shape using the pythonOCC library, which is a set of Python bindings for the Open CASCADE Technology (OCCT) library. Here’s a breakdown of its functionality:

1. **Shebang and Licensing Information:**
   - The script starts with a shebang line (`#!/usr/bin/env python`) to indicate that it should be executed using the Python interpreter.
   - It includes a copyright notice and licensing information for the pythonOCC library, specifying that it is distributed under the GNU Lesser General Public License (LGPL).

2. **Imports:**
   - `x3dom_renderer` from `OCC.Display.WebGl`: This module is used for rendering shapes using the x3dom framework, which allows for web-based 3D visualization.
   - `BRep_Builder`, `TopoDS_Shape` from `OCC.Core.BRep` and `OCC.Core.TopoDS`: These classes are used for constructing and representing BREP shapes.
   - `breptools_Read` from `OCC.Core.BRepTools`: This function is used to read BREP files and load them into a shape object.

3. **Loading the BREP Shape:**
   - A `TopoDS_Shape` object named `cylinder_head` is created to hold the geometry of the shape.
   - A `BRep_Builder` object named `builder` is created to assist in constructing the shape.
   - The `breptools_Read` function is called to read the BREP file located at `"../assets/models/cylinder_head.brep"` and load its contents into the `cylinder_head` object using the `builder`.

4. **Rendering the Shape:**
   - An `X3DomRenderer` object named `my_renderer` is created to handle the rendering of the shape.
   - The `DisplayShape` method of `my_renderer` is called with `cylinder_head` as an argument to prepare the shape for rendering.
   - The `render` method of `my_renderer` is called to render the shape in an x3dom viewer, which will produce a web-based 3D visualization of the cylinder head.

In summary, this script loads a BREP file representing a cylinder head, constructs the shape using the pythonOCC library, and renders it using the x3dom framework for web-based visualization.

## core_display_customize_linewidth.py

This Python script uses the `pythonOCC` library to create and display a 3D box shape. Here’s a detailed breakdown of its purpose and functionality:

1. **License and Metadata**:
   - The script begins with a shebang (`#!/usr/bin/env python`) indicating it should be run using the Python interpreter.
   - It includes a copyright notice and licensing information for `pythonOCC`, which is an open-source library for 3D CAD development.

2. **Imports**:
   - `AIS_Shape` from `OCC.Core.AIS`: Used to create an interactive shape.
   - `BRepPrimAPI_MakeBox` from `OCC.Core.BRepPrimAPI`: Used to create a box primitive.
   - `init_display` from `OCC.Display.SimpleGui`: Used to initialize the display window and related functions.

3. **Display Initialization**:
   - `display, start_display, add_menu, add_function_to_menu = init_display()`: Initializes the display window and gets functions to control the display.

4. **Box Creation**:
   - `s = BRepPrimAPI_MakeBox(200, 100, 50).Shape()`: Creates a box with dimensions 200x100x50 units and stores the shape in `s`.

5. **Interactive Shape Creation**:
   - `ais_shp = AIS_Shape(s)`: Wraps the box shape `s` into an `AIS_Shape` object for interactive display.
   - `ais_shp.SetWidth(4)`: Sets the line width of the shape to 4 units.
   - `ais_shp.SetTransparency(0.10)`: Sets the transparency of the shape to 10%.

6. **Display the Shape**:
   - `ais_context = display.GetContext()`: Retrieves the display context.
   - `ais_context.Display(ais_shp, True)`: Displays the interactive shape in the context.

7. **View and Fit**:
   - `display.View_Iso()`: Sets the view to an isometric perspective.
   - `display.FitAll()`: Adjusts the view to fit all displayed objects within the window.

8. **Start Display Loop**:
   - `start_display()`: Starts the display loop, keeping the window open and interactive.

### Summary

The script creates a 3D box with specified dimensions, wraps it into an interactive shape, sets its visual properties (line width and transparency), and displays it in an isometric view within a GUI window. This is a basic example of using `pythonOCC` for 3D CAD visualization.

## core_display_material_compound_subshape.py

This Python script is designed to create and display 3D shapes using the pythonOCC library, which is a set of Python bindings for the OpenCASCADE Technology (OCCT) 3D modeling kernel. Below is a clear and concise description of its purpose and functionality:

### Purpose:
The script generates two cylinders with different materials, positions them side by side, and displays them in a 3D viewer.

### Functionality:
1. **Import Libraries**: 
   - Imports various modules from the pythonOCC library to handle shapes, materials, colors, transformations, and 3D visualization.

2. **Define Materials**:
   - Defines a list of available materials (`Graphic3d_NOM_ALUMINIUM` and `Graphic3d_NOM_STEEL`).

3. **Create Cylinder**:
   - Creates a cylinder with a specified radius (30 units) and height (200 units).

4. **Translate and Store Cylinders**:
   - Translates the cylinder along the x-axis to position them side by side.
   - Stores the translated cylinders in a list.

5. **Create Compound Shape**:
   - Initializes a compound shape and a builder to combine multiple shapes into one.
   - Adds the translated cylinders to the compound shape.

6. **Assign Colors**:
   - Assigns custom colors to the individual cylinders within the compound shape based on their materials.

7. **Display Setup**:
   - Initializes the 3D viewer using `init_display`.
   - Displays the compound shape with the custom colors.
   - Fits the view to encompass all displayed objects.
   - Starts the display loop to render the 3D viewer.

### Execution Flow:
1. **Initialization**:
   - The script sets up the environment and imports necessary modules.

2. **Shape Creation and Transformation**:
   - A cylinder is created and then duplicated, with each copy being translated along the x-axis.

3. **Compound Shape Creation**:
   - The translated cylinders are combined into a single compound shape.

4. **Color Assignment**:
   - Each cylinder in the compound is assigned a specific color corresponding to its material.

5. **Display**:
   - The compound shape is displayed in a 3D viewer, and the view is adjusted to fit all objects.

This script is a typical example of how to use pythonOCC to create, manipulate, and visualize 3D geometric shapes with different materials and colors.

## core_visualization_3d_to_2d_screen_coordinates.py

This Python code is designed to work with the `pythonOCC` library, which is a set of Python bindings for the Open CASCADE Technology (OCCT), a software development platform for 3D CAD, CAM, CAE, etc. The script specifically focuses on selecting a vertex in a 3D model and displaying its coordinates in both 3D space and 2D screen space.

Here is a concise description of its purpose and functionality:

1. **Initialization**:
   - The script imports necessary modules from `pythonOCC` for display, handling vertices, and reading STEP files.
   - It initializes the display environment using `init_display()`.

2. **Vertex Selection Callback**:
   - Defines a function `vertex_clicked` that is triggered whenever a vertex is selected in the 3D viewer.
   - Inside this function, it iterates over the selected shapes (vertices), retrieves the 3D coordinates of the vertex using `BRep_Tool.Pnt`, and prints these coordinates.
   - Converts the 3D coordinates to 2D screen coordinates using `display.View.Convert` and prints these as well.

3. **Loading and Displaying a STEP File**:
   - Loads a STEP file located at `../assets/models/as1_pe_203.stp` using `read_step_file`.
   - Displays the loaded shape in the viewer.

4. **Interactive Display Setup**:
   - Registers the `vertex_clicked` function as a callback for vertex selection events using `display.register_select_callback`.
   - Sets the selection mode to vertex selection with `display.SetSelectionModeVertex`.
   - Starts the display loop with `start_display()` to keep the viewer interactive.

In summary, this script allows a user to interactively select vertices in a 3D model loaded from a STEP file and view their 3D and 2D screen coordinates in the console.

## core_display_export_to_image.py

This Python script uses the `pythonOCC` library to create a graphical user interface (GUI) for displaying a 3D box and provides functionality to capture and save screenshots of the display in various image formats. Here is a breakdown of its purpose and functionality:

1. **Imports**:
    - `sys`: Standard Python library for system-specific parameters and functions.
    - `init_display` from `OCC.Display.SimpleGui`: Initializes the display window and GUI components.
    - `BRepPrimAPI_MakeBox` from `OCC.Core.BRepPrimAPI`: Used to create a 3D box shape.

2. **Display Initialization**:
    - `init_display()` is called to initialize the display and GUI components, returning the display object and functions to start the display, add menus, and add functions to menus.

3. **3D Box Creation**:
    - `BRepPrimAPI_MakeBox(10.0, 20.0, 30.0).Shape()` creates a 3D box with dimensions 10x20x30 units.
    - `display.DisplayShape(my_box, update=True)` displays the created box in the initialized display window.

4. **Screenshot Export Functions**:
    - Several functions (`export_to_BMP`, `export_to_PNG`, `export_to_JPEG`, `export_to_TIFF`) are defined to capture and save the current view of the display window in different image formats (BMP, PNG, JPEG, TIFF).
    - Each function uses `display.View.Dump(filename)` to save the screenshot to the specified file.

5. **Exit Function**:
    - `exit(event=None)`: Exits the application using `sys.exit()`.

6. **Main Execution**:
    - When the script is run directly (`if __name__ == "__main__":`), it adds a menu named "screencapture" to the GUI.
    - Functions for exporting screenshots and exiting the application are added to the "screencapture" menu.
    - `start_display()` is called to start the GUI event loop, displaying the window and enabling interaction.

**Summary**: The script creates a GUI application that displays a 3D box and provides menu options to capture and save screenshots of the display in BMP, PNG, JPEG, and TIFF formats. It uses the `pythonOCC` library for 3D modeling and rendering.

## core_display_raytracing.py

This Python script is part of the `pythonOCC` library and is used to create and display a 3D scene with specific geometric shapes and lighting. Here is a structured breakdown of its purpose and functionality:

1. **Imports and Initialization:**
   - The script imports various modules from the `pythonOCC` library, which is a set of Python bindings for the Open CASCADE Technology (OCCT) 3D modeling library.
   - It also imports the `sys` module for system-level operations.

2. **Geometry Creation:**
   - A rectangular box (representing a table) is created and translated to a specific position.
   - Two cones are created: one representing the outer shape of a glass and another slightly translated cone representing the inner shape of the glass. The inner cone is subtracted from the outer cone to create a hollow glass shape.
   - The glass is then translated to a specific position.

3. **Display Initialization:**
   - The `init_display` function is called to initialize the display window and related functionalities.

4. **Lighting:**
   - A spotlight is created and positioned in the scene. The light is added to the viewer and turned on.

5. **Shape Display:**
   - The `bottle` shape (imported from `core_classic_occ_bottle`) is displayed with an aluminum material.
   - The table is displayed with a plastic material and coral color.
   - The glass is displayed with a plastic material, brown color, and some transparency.

6. **Menu and Event Handling:**
   - Functions are defined to handle different display modes: raytracing with default depth, raytracing with depth 8, rasterization, and exit.
   - A menu named "raytracing" is added to the display, and the defined functions are linked to this menu.

7. **Main Execution:**
   - If the script is run as the main module, the menu is set up, and the display loop is started.

**Purpose:**
The script is designed to create a 3D scene with specific geometric objects (a table, a glass, and a bottle), set up lighting, and provide interactive options to switch between different rendering modes (raytracing and rasterization). It demonstrates the capabilities of the `pythonOCC` library in creating and manipulating 3D shapes and rendering them with various materials and lighting effects.

## core_topology_tetrahedron.py

This Python script uses the `pythonOCC` library, which is a set of Python bindings for the OpenCASCADE Technology (OCCT) framework, to create and display a 3D geometric shape. Specifically, it constructs a tetrahedron, which is a polyhedron with four triangular faces. Here is a step-by-step breakdown of its functionality:

1. **Imports**:
   - The script imports necessary classes and functions from the `pythonOCC` library to create geometric points, edges, wires, faces, and to display the resulting shape.

2. **Creating Vertices**:
   - Four 3D points (`gp_Pnt`) are defined, representing the vertices of the tetrahedron:
     - `v1` at (1, 0, 0)
     - `v2` at (0, 1, 0)
     - `v3` at (0, 0, 1)
     - `v4` at (0, 0, 0)

3. **Creating Edges**:
   - Edges are created between these points using `BRepBuilderAPI_MakeEdge`:
     - `e0` from `v1` to `v4`
     - `e1` from `v4` to `v2`
     - `e2` from `v4` to `v3`
     - `e3` from `v2` to `v1`
     - `e4` from `v3` to `v2`
     - `e5` from `v3` to `v1`

4. **Creating Wires**:
   - Wires are created by combining the edges using `BRepBuilderAPI_MakeWire`:
     - `w0` combines `e5`, `e3`, and `e4`
     - `w1` combines `e1`, `e3`, and `e0`
     - `w2` combines `e0`, `e5`, and `e2`
     - `w3` combines `e2`, `e4`, and `e1`

5. **Creating Faces**:
   - Faces are created from the wires using `BRepBuilderAPI_MakeFace`:
     - `f0` from `w0`
     - `f1` from `w1`
     - `f2` from `w2`
     - `f3` from `w3`

6. **Sewing Faces Together**:
   - The faces are sewn together to form a shell using `BRepBuilderAPI_Sewing`:
     - The faces (`f0`, `f1`, `f2`, `f3`) are added to the sewing object.
     - `sew.Perform()` performs the sewing operation.
     - `tetrahedron_shell` is the resulting sewed shape.

7. **Displaying the Result**:
   - The script initializes a display using `init_display` and displays the resulting tetrahedron shell.
   - `display.DisplayShape(tetrahedron_shell, update=True)` displays the shape.
   - `start_display()` starts the GUI event loop to render the display.

In summary, the script constructs a tetrahedron by defining its vertices, creating edges between these vertices, forming triangular faces from these edges, sewing the faces together into a shell, and finally displaying the 3D tetrahedron using the `pythonOCC` library.

## core_geometry_bspline.py

This Python script is designed to create and display B-spline curves using the pythonOCC library, which is a set of Python bindings for the Open CASCADE Technology (OCCT) 3D modeling library. Below is a detailed description of its purpose and functionality:

### Purpose:
The script demonstrates how to create and visualize 2D B-spline curves using predefined points. It uses the pythonOCC library to handle the geometric operations and the display functionalities.

### Functionality:
1. **Library Imports**:
   - `from __future__ import print_function`: Ensures compatibility with Python 2 and 3.
   - Various modules from the `OCC.Core` are imported to handle geometric points (`gp_Pnt2d`), B-spline interpolation (`Geom2dAPI_Interpolate` and `Geom2dAPI_PointsToBSpline`), and array structures (`TColgp_HArray1OfPnt2d`, `TColgp_Array1OfPnt2d`).
   - `init_display` from `OCC.Display.SimpleGui` is imported to initialize the display window.

2. **Display Initialization**:
   - `display, start_display, add_menu, add_function_to_menu = init_display()`: Initializes the display window and related functions.

3. **B-spline Function (`bspline`)**:
   - **First B-spline**:
     - Creates an array of 5 2D points (`TColgp_Array1OfPnt2d`).
     - Sets the coordinates of these points.
     - Generates a B-spline curve (`bspline_1`) from these points using `Geom2dAPI_PointsToBSpline`.
   
   - **Second B-spline**:
     - Creates a handle array of 5 2D points (`TColgp_HArray1OfPnt2d`).
     - Sets the coordinates of these points.
     - Uses `Geom2dAPI_Interpolate` to create an interpolated B-spline (`bspline_2`) from these points.
   
   - **Third B-spline**:
     - Creates another handle array of 5 2D points with different coordinates.
     - Uses `Geom2dAPI_Interpolate` with periodic interpolation enabled to create another B-spline (`bspline_3`).

   - **Display Points and B-splines**:
     - Iterates through the points in the arrays and displays them.
     - Displays the three B-spline curves with different colors (`bspline_1` in default color, `bspline_2` in green, `bspline_3` in blue).

4. **Main Execution**:
   - When the script is run directly, it calls the `bspline()` function to create and display the B-splines.
   - `start_display()` is called to start the display loop, allowing the user to interact with the graphical window.

### Summary:
The script is a demonstration of how to create and visualize 2D B-spline curves using the pythonOCC library. It sets up a graphical display, creates three different B-spline curves from predefined points, and visualizes these curves along with their defining points. Each B-spline curve is generated using different methods provided by the OCCT library, showcasing the flexibility and capabilities of pythonOCC for geometric modeling and visualization.

## core_exception.py

The provided Python code is a small script that demonstrates the use of the `gp_Dir` class from the `OCC.Core.gp` module, which is part of the pythonOCC library, a Python wrapper for the Open CASCADE Technology (OCCT) 3D modeling library.

Here's a breakdown of the code's purpose and functionality:

1. **Importing the Required Class**:
   ```python
   from OCC.Core.gp import gp_Dir
   ```
   This line imports the `gp_Dir` class, which represents a direction in 3D space, from the `OCC.Core.gp` module.

2. **Creating a Direction Object**:
   ```python
   d = gp_Dir(0, 0, 1)
   ```
   This line creates an instance of the `gp_Dir` class, representing a direction vector along the Z-axis (0, 0, 1).

3. **Exception Handling**:
   ```python
   try:
       d.Coord(-1)  # should raise Standard_OutOfRange
   except RuntimeError:
       print("Exception successfully raised.")
   ```
   - The `try` block attempts to call the `Coord` method of the `gp_Dir` instance `d` with an invalid argument `-1`. The `Coord` method is used to access the coordinates of the direction vector, and valid indices are typically 1, 2, or 3 (corresponding to X, Y, and Z).
   - The invalid index `-1` is expected to raise a `RuntimeError` (which corresponds to the `Standard_OutOfRange` exception in the underlying C++ library).
   - The `except` block catches the `RuntimeError` and prints a message indicating that the exception was successfully raised.

**Summary**:
The script demonstrates how to create a direction vector using the `gp_Dir` class from the pythonOCC library and shows how to handle an exception when accessing an invalid coordinate index. The primary purpose is to validate that the `Coord` method correctly raises an exception for out-of-range indices.

## core_modeling_sprocket.py

The provided Python script is a detailed and comprehensive program for generating a 3D model of a sprocket using the OpenCASCADE library. The script's main functionalities and purpose can be summarized as follows:

### Purpose:
To create a 3D model of a sprocket based on user-defined parameters like roller diameter, pitch, number of teeth, and chain width. The model includes detailed features such as teeth profile, rounded edges, center hole, mounting holes, and cut-outs for weight reduction.

### Key Functionalities:

1. **Imports and Setup**:
   - Imports necessary modules from OpenCASCADE and other libraries.
   - Defines sprocket parameters such as roller diameter, pitch, number of teeth, chain width, and dimensions derived from these inputs.

2. **Teeth Construction**:
   - `build_tooth()`: Constructs the 2D profile of a single sprocket tooth and extrudes it to create a 3D wedge-shaped tooth.

3. **Tooth Rounding**:
   - `round_tooth(wedge)`: Adds rounded edges to the tooth for a smoother profile by creating and applying a rounding cut.

4. **Tooth Cloning**:
   - `clone_tooth(base_shape)`: Duplicates the rounded tooth around the sprocket's circumference to form the complete sprocket teeth.

5. **Center Hole**:
   - `center_hole(base)`: Cuts a central hole in the sprocket for fitting onto an axle.

6. **Mounting Holes**:
   - `mounting_holes(base)`: Adds mounting holes around the sprocket for attachment purposes.

7. **Cut-Outs**:
   - `cut_out(base)`: Creates cut-outs between the mounting holes to reduce the sprocket's weight while maintaining structural integrity.

8. **Sprocket Assembly**:
   - `build_sprocket()`: Assembles the complete sprocket by integrating all the above components (teeth, center hole, mounting holes, and cut-outs).

9. **Display**:
   - Uses the `init_display` function from the OpenCASCADE library to visualize the final sprocket model.

### Execution:
- The script calculates various geometric properties and creates the sprocket model by combining multiple 2D and 3D shapes.
- Finally, it displays the 3D model using OpenCASCADE's visualization tools.

### Example Parameters:
- `roller_diameter = 10.2`
- `pitch = 15.875`
- `num_teeth = 40`
- `chain_width = 6.35`

### Visualization:
- The script initializes a display window and shows the constructed sprocket model, allowing the user to visualize and inspect the sprocket.

### Summary:
This script is a powerful tool for generating and visualizing a custom sprocket model, leveraging the OpenCASCADE library's capabilities for 3D CAD modeling. It demonstrates advanced usage of geometric construction, transformations, and Boolean operations to create a detailed and functional mechanical part.

## core_load_gltf_ocaf.py

This Python code is designed to load and display a 3D model from a GLTF file using the pythonOCC library, which is a set of Python bindings for the Open CASCADE Technology (OCCT) framework. Here is a detailed breakdown of its purpose and functionality:

1. **Imports:**
   - `TDocStd_Document` from `OCC.Core.TDocStd`: Manages documents in OCCT.
   - `Message_ProgressRange` from `OCC.Core.Message`: Handles progress messages.
   - `RWGltf_CafReader` from `OCC.Core.RWGltf`: Reads GLTF files.
   - `IFSelect_RetDone` from `OCC.Core.IFSelect`: Indicates successful operations.
   - Functions for initializing the display from `OCC.Display.SimpleGui`.

2. **File Path:**
   - Specifies the GLTF file to be loaded: `"../assets/models/2CylinderEngine.glb"`.

3. **Document Creation:**
   - Creates a new OCCT document: `doc = TDocStd_Document("pythonocc-doc")`.

4. **GLTF Reader Setup:**
   - Instantiates a GLTF reader: `gltf_reader = RWGltf_CafReader()`.
   - Sets the document for the reader: `gltf_reader.SetDocument(doc)`.

5. **File Reading:**
   - Reads the GLTF file and checks if the operation was successful: 
     ```python
     status = gltf_reader.Perform(filename, Message_ProgressRange())
     assert status == IFSelect_RetDone
     ```

6. **Shape Extraction:**
   - Extracts the shape from the GLTF reader: `shp = gltf_reader.SingleShape()`.

7. **Display Setup:**
   - Initializes the display window and related functions: 
     ```python
     display, start_display, add_menu, add_function_to_menu = init_display()
     ```

8. **Shape Display:**
   - Displays the extracted shape in the initialized display window:
     ```python
     display.DisplayShape(shp, update=True)
     start_display()
     ```

### Summary
This script loads a 3D model from a GLTF file, processes it into an OCCT document, extracts the shape, and then displays it using the pythonOCC library's visualization tools. The code includes several commented-out options for customizing the GLTF reader's behavior, such as setting the coordinate system, enabling parallel processing, and more.

## core_display_erase_shape.py

The provided Python code is a script for creating and displaying 3D geometric shapes using the `pythonOCC` library, which is a set of Python bindings for the OpenCASCADE (OCC) CAD kernel. Here's a clear and concise description of its purpose and functionality:

### Purpose:
The script's purpose is to create and visualize three different 3D shapes (a box, a sphere, and a cylinder) in a graphical window, and to provide functionality to erase these shapes from the display through a menu.

### Functionality:
1. **Imports**: The script imports necessary modules from the `OCC.Core` for creating shapes and transformations, and from `OCC.Display.SimpleGui` for initializing the display.

2. **Shape Creation**:
   - A box is created at the origin with dimensions 10x20x30.
   - A sphere is created with a radius of 10 and translated along the x-axis by 50 units.
   - A cylinder is created with a radius of 10 and height of 40, and translated along the x-axis by -50 units.

3. **Display Initialization**:
   - The `init_display` function initializes the display window and returns functions for controlling the display and adding menu items.

4. **Display Shapes**:
   - The created shapes (box, sphere, and cylinder) are displayed in the graphical window using the `display.DisplayShape` method. The returned display objects are stored in variables `ais_box`, `ais_sphere`, and `ais_cylinder`.

5. **Erase Functions**:
   - Three functions (`erase_box`, `erase_cylinder`, and `erase_sphere`) are defined to erase the respective shapes from the display when called.

6. **Menu Setup**:
   - A menu titled "Erase Shapes" is added to the graphical window.
   - Menu items are added to the "Erase Shapes" menu to call the erase functions for the box, cylinder, and sphere.

7. **Main Execution**:
   - If the script is run as the main module, the menu is set up, the display is fitted to show all shapes, and the display loop is started to render the window and handle user interactions.

### Summary:
The script demonstrates how to create and manipulate 3D shapes using `pythonOCC`, display them in a graphical window, and interact with them through a menu to erase the shapes. This is useful for applications involving CAD modeling, visualization, and interactive geometry manipulation.

## core_export_step_ap203.py

This Python script is designed to create a 3D box shape and export it to a STEP file format using the pythonOCC library, which is a set of Python bindings for the Open CASCADE Technology (OCCT) 3D modeling library. Here's a detailed breakdown of its functionality:

1. **Header and License Information**:
   - The script starts with a shebang (`#!/usr/bin/env python`) to specify the interpreter.
   - It includes a copyright notice and licensing information, indicating that the code is part of pythonOCC and is licensed under the GNU Lesser General Public License.

2. **Imports**:
   - The `from __future__ import print_function` statement ensures compatibility with Python 3's print function in Python 2.x.
   - Various modules from pythonOCC are imported:
     - `BRepPrimAPI_MakeBox` for creating a box shape.
     - `STEPControl_Writer` and `STEPControl_AsIs` for exporting the shape to a STEP file.
     - `Interface_Static_SetCVal` for setting export parameters.
     - `IFSelect_RetDone` for checking the status of the export operation.

3. **Creating a 3D Box Shape**:
   - `box_s = BRepPrimAPI_MakeBox(10, 20, 30).Shape()` creates a box with dimensions 10x20x30 units and stores the shape in `box_s`.

4. **Initializing the STEP Exporter**:
   - `step_writer = STEPControl_Writer()` initializes a STEP file writer.
   - `dd = step_writer.WS().TransferWriter().FinderProcess()` retrieves the transfer process and prints it for debugging purposes.

5. **Setting Export Parameters**:
   - `Interface_Static_SetCVal("write.step.schema", "AP203")` sets the STEP schema to AP203, a standard for 3D CAD data exchange.

6. **Transferring the Shape and Writing the File**:
   - `step_writer.Transfer(box_s, STEPControl_AsIs)` transfers the box shape to the STEP writer.
   - `status = step_writer.Write("box.stp")` writes the transferred shape to a file named `box.stp`.

7. **Error Handling**:
   - The script checks if the writing process was successful by comparing `status` to `IFSelect_RetDone`.
   - If the status indicates failure, an `AssertionError` is raised with the message "load failed".

In summary, this script creates a 3D box shape with specified dimensions and exports it to a STEP file named `box.stp` using the pythonOCC library. It includes error handling to ensure the export process completes successfully.

## core_visualization_overpaint_viewer.py

The provided Python code demonstrates how to create an application that integrates an OpenGL viewer with a Qt interface, specifically using the pythonOCC library to render 3D graphics. Here's a detailed breakdown of its purpose and functionality:

### Purpose

The primary purpose of this script is to showcase the overpainting of an OpenGL viewport with Qt widgets. This technique allows for dynamic and interactive overlays on top of the OpenGL-rendered scene, enabling the creation of sophisticated user interfaces.

### Functionality

1. **Imports and Setup:**
   - The script imports necessary modules from `OCC` and `Qt` libraries.
   - It ensures that a Qt backend is loaded and retrieves the required Qt modules.
   - It defines several constants representing different actions that can trigger the OpenGL viewport to be redrawn (e.g., zoom, pan, select).

2. **Bubble Class:**
   - Represents a bubble with properties such as position, radius, velocity, and colors.
   - Contains methods to update its appearance, draw itself using a `QPainter`, and move within a bounding box.

3. **GLWidget Class:**
   - Inherits from `qtViewer3d` and serves as the main OpenGL widget.
   - Initializes various states and GUI parameters.
   - Handles mouse and keyboard events to interact with the OpenGL viewport (e.g., zooming, rotating, panning).
   - Manages the creation and animation of bubbles that are overpainted on the OpenGL viewport.
   - Contains methods to handle the painting and overpainting of the viewport, including drawing bubbles and instructional text.

4. **Main Application:**
   - The `TestOverPainting` function sets up the main application window using `QtWidgets.QWidget`.
   - It initializes the `GLWidget` and integrates it into the main layout.
   - The application runs an event loop to handle user interactions.

### Key Features

- **OpenGL Context Sharing:** The script demonstrates how to share the OpenGL context with Qt to allow for overpainting.
- **Interactive Overlays:** Implements interactive overlays such as bubbles that move and change appearance based on user interactions.
- **Event Handling:** Captures and processes various user inputs (mouse clicks, movements, wheel events, and key presses) to interact with the 3D scene.
- **Dynamic Redrawing:** Ensures that the OpenGL viewport is redrawn synchronously with the overpainting actions to avoid visual artifacts.

### Usage

To run the script, execute the `TestOverPainting` function in the `__main__` block. This will create a window with an OpenGL viewport and interactive bubbles overlayed on top of it. Users can interact with the viewport using mouse and keyboard inputs to see the dynamic updates and overpainting effects.

This example serves as a foundation for more complex applications that require integrating 3D graphics with rich, interactive user interfaces using Qt and OpenGL.

## core_topology_vertex_filleting.py

This Python script is designed to demonstrate how to generate and manipulate 3D geometry using the `pythonOCC` library, specifically focusing on creating a simple cubic shape and adding fillets to its vertices. 

### Key Functionalities:

1. **Importing Required Modules:**
   The script imports various classes and functions from the `OCC` (Open CASCADE Technology) library, which is a powerful 3D CAD modeling library. These imports include tools for creating shapes, exploring topology, and displaying the geometry.

2. **Initializing Display:**
   The script initializes a 3D display window using `init_display()` from the `OCC.Display.SimpleGui` module. This sets up the GUI environment for visualizing the 3D shapes.

3. **Creating a Cube:**
   A cube of dimensions 100x100x100 units is created using `BRepPrimAPI_MakeBox`.

4. **Exploring Vertices:**
   The script uses `TopExp_Explorer` to iterate over the vertices of the cube. It retrieves two vertices (`vertA` and `vertB`) for further processing.

5. **Filleting Function:**
   The core functionality is in the `vertex_fillet` function, which applies a fillet to the edges incident on a given vertex. 
   - It initializes a fillet operation using `BRepFilletAPI_MakeFillet`.
   - It maps edges connected to the specified vertex using `topexp_MapShapesAndAncestors`.
   - It iterates over these edges, adding a fillet to each edge based on its orientation.
   - The fillet radius is set to 20 units.
   - The function returns the filleted shape if the fillet operation is successful.

6. **Applying Fillet and Displaying:**
   The `vertex_fillet` function is called for `vertA`, and the resulting filleted shape is displayed in the initialized 3D display window.

7. **Starting the Display Loop:**
   The script enters the display loop with `start_display()`, allowing the user to interact with the 3D visualization.

### Summary:
The script demonstrates how to create a basic 3D shape (a cube), explore its vertices, and apply fillets to the edges incident on a specific vertex using the `pythonOCC` library. Finally, it visualizes the resulting geometry in a 3D display window. This example serves as a basic introduction to 3D geometric modeling and manipulation using `pythonOCC`.

## core_boolean_fuzzy_cut_emmenthaler.py

This Python script utilizes the `pythonOCC` library, which is a set of Python bindings for the Open CASCADE Technology (OCCT) framework, to create and manipulate 3D shapes. The script specifically demonstrates how to perform boolean operations on shapes, particularly the "cut" operation, with some added randomness to the shapes' parameters. Here's a detailed breakdown of its purpose and functionality:

1. **Imports**:
   - Imports various modules from `pythonOCC` for creating and manipulating 3D shapes (`BRepPrimAPI_MakeBox`, `BRepPrimAPI_MakeCylinder`, etc.).
   - Imports `random` for generating random numbers.
   - Imports `time` for measuring execution time.
   - Imports `sys` for system-specific parameters and functions.
   - Imports display-related functions from `OCC.Display.SimpleGui`.

2. **Display Initialization**:
   - Initializes the display using `init_display`, which sets up the GUI for visualizing the 3D shapes.

3. **Helper Functions**:
   - `random_pnt()`: Generates a random point within a unit cube.
   - `random_vec()`: Generates a random vector with components in the range [-1, 1].

4. **Boolean Operation Function**:
   - `fuzzy_cut(shape_A, shape_B, tol=5e-5, parallel=False)`: Performs a boolean cut operation (subtracts `shape_B` from `shape_A`) with a specified tolerance and option for parallel execution. Returns the resulting shape.

5. **Main Function (`emmenthaler`)**:
   - Creates a box shape (`box`) with dimensions 200x200x200.
   - Defines an inner function `do_cyl()` that creates a randomly positioned and oriented cylinder with a random radius between 8 and 36.
   - Iteratively performs `fuzzy_cut` operations to subtract randomly generated cylinders from the box shape for a specified number of iterations (`nb_iter` = 40).
   - Measures and prints the time taken for each cut operation and the total execution time.
   - Displays the final shape using the initialized display.

6. **Exit Function**:
   - `exit(event=None)`: Exits the script.

7. **Main Execution Block**:
   - Adds a menu item "fuzzy boolean operations" to the display.
   - Associates the `emmenthaler` function with the menu item.
   - Starts the display loop.

### Summary
The script creates a 3D box and iteratively subtracts randomly positioned and oriented cylinders from it using a fuzzy boolean cut operation. The resulting shape, which resembles a block of Emmental cheese with holes, is displayed in a GUI. The script also includes timing measurements for performance analysis.

## core_geometry_surface_from_curves.py

The provided Python code is a script that demonstrates the creation and visualization of B-Spline surfaces using the `pythonOCC` library, which is a set of Python bindings for the Open CASCADE Technology (OCCT) CAD kernel. Here's a breakdown of its purpose and functionality:

### Purpose:
The script's primary purpose is to create three different B-Spline surfaces by interpolating between pairs of B-Spline curves using different filling styles (`StretchStyle`, `CoonsStyle`, and `CurvedStyle`). It then visualizes these surfaces using a graphical display.

### Functionality:
1. **Imports and Initialization**:
   - The script imports necessary modules from `pythonOCC` and initializes the display using `init_display` from `OCC.Display.SimpleGui`.

2. **Surface Creation Function (`surface_from_curves`)**:
   - This function creates three pairs of B-Spline curves and generates a B-Spline surface for each pair using different interpolation styles.
   
   - **First Pair of B-Spline Curves**:
     - A list of points is defined and converted into a B-Spline curve (`SPL1`).
   
   - **Second Pair of B-Spline Curves**:
     - Another list of points is defined and converted into a second B-Spline curve (`SPL2`).

   - **Filling Styles**:
     - `GeomFill_StretchStyle`: Creates a B-Spline surface (`aGeomFill1`) by interpolating between `SPL1` and `SPL2`.
     - `GeomFill_CoonsStyle`: Creates another B-Spline surface (`aGeomFill2`) by interpolating between `SPL3` and `SPL4` (translated versions of `SPL1` and `SPL2`).
     - `GeomFill_CurvedStyle`: Creates a third B-Spline surface (`aGeomFill3`) by interpolating between `SPL5` and `SPL6` (further translated versions of `SPL1` and `SPL2`).

   - **Surface Visualization**:
     - The surfaces are converted into displayable shapes using `make_face` and displayed using `display.DisplayShape`.

3. **Main Execution Block**:
   - The `surface_from_curves` function is called.
   - The `start_display` function is called to start the graphical display loop.

### Summary:
The script demonstrates how to create and visualize B-Spline surfaces using different interpolation styles with the `pythonOCC` library. It sets up the display environment, defines B-Spline curves, generates surfaces using various filling styles, and visualizes the results in a graphical window.

## core_display_signal_slots.py

This Python script leverages the Open CASCADE Technology (OCCT) library to create a simple 3D viewer application using the PyQt5 framework. The script's primary purpose is to display a cube and a sphere in a 3D viewer and provide functionality to calculate and display the linear properties of selected shapes. Here's a detailed breakdown of its functionality:

1. **Imports and Initialization**:
   - The script imports necessary modules from OCCT for creating shapes, calculating properties, and handling the display.
   - It initializes the display using PyQt5, setting up the required modules and the 3D viewer.

2. **Helper Functions**:
   - `get_occ_viewer()`: Retrieves the OCC viewer instance from the Qt application, ensuring that the viewer is correctly initialized.
   - `location_from_vector(x, y, z)`: Creates a translation transformation based on the given vector (x, y, z) and returns the corresponding location object.

3. **Event Handlers**:
   - `on_select(shapes)`: This function is triggered when shapes are selected in the viewer. It calculates and prints the linear properties (mass, center of mass, and static moments) for each selected shape.
   - `also_on_select(shapes)`: Another selection handler that prints the type of each selected shape (solid, edge, or face).

4. **Shape Creation and Display**:
   - The script creates a cube and a sphere using `BRepPrimAPI_MakeBox` and `BRepPrimAPI_MakeSphere` respectively.
   - The sphere is moved 500 units along the x-axis to separate it from the cube.
   - Both shapes are displayed in the viewer.

5. **Viewer Configuration**:
   - The script connects the selection signal of the viewer (`sig_topods_selected`) to the `on_select` and `also_on_select` functions to handle shape selection events.
   - It fits all displayed shapes within the viewer's view and starts the display loop.

In summary, this script sets up a 3D viewer with a cube and a sphere, and it provides functionality to interactively calculate and display geometric properties of selected shapes within the viewer.

## core_topology_through_sections.py

This Python code is a script that uses the `pythonOCC` library to create and display 3D shapes through a process called "lofting" or "through sections." Here's a breakdown of its purpose and functionality:

### Purpose
The script demonstrates how to create 3D shapes by lofting through multiple circular sections (wires) using the `pythonOCC` library, which is a set of Python bindings for the Open CASCADE Technology (OCCT), a powerful 3D CAD modeling library. The script creates two different lofted shapes and visualizes them using a simple graphical user interface.

### Functionality
1. **Library Imports**:
   - The script imports necessary classes and functions from the `OCC.Core` modules for geometric and topological operations.
   - It also imports the `init_display` function from `OCC.Display.SimpleGui` to initialize the display window.

2. **Display Initialization**:
   - `init_display()` initializes the display window and provides functions to start the display loop and add menus.

3. **through_sections Function**:
   - This function creates two lofted shapes using circular sections:
     - **First Lofted Shape (Ruled)**:
       - Four circles (`circle_1`, `circle_2`, `circle_3`, `circle_4`) are defined at different positions.
       - Each circle is converted into a wire using `BRepBuilderAPI_MakeWire`.
       - A `BRepOffsetAPI_ThruSections` object (`generatorA`) is created to generate a lofted shape through the wires. The `False, True` parameters indicate that the shape should be ruled (not smoothed) and that the wires should not be closed.
       - The wires are added to the generator using a loop.
       - The lofted shape is built and displayed.
     - **Second Lofted Shape (Smooth)**:
       - Another set of four circles (`circle_1b`, `circle_2b`, `circle_3b`, `circle_4b`) are defined at different positions.
       - These circles are also converted into wires.
       - Another `BRepOffsetAPI_ThruSections` object (`generatorB`) is created with `True, False` parameters, indicating that the shape should be smooth and the wires should not be closed.
       - The wires are added to the generator using a loop.
       - The lofted shape is built and displayed.

4. **Main Execution**:
   - The `through_sections` function is called to create and display the lofted shapes.
   - `start_display()` starts the display loop, allowing the user to interact with the 3D visualization.

### Summary
The script creates and visualizes two 3D lofted shapes (one ruled and one smooth) through a series of circular sections using the `pythonOCC` library. It demonstrates the use of geometric and topological operations to generate complex 3D shapes and provides a simple graphical interface for viewing them.

## core_display_point_properties.py

This Python code is a script designed to create and display a grid of 3D points using various visual aspects (shapes) in a 3D viewer. The script leverages the `pythonOCC` library, which is a set of Python bindings for the Open CASCADE Technology (OCCT), a software development platform for 3D CAD, CAM, CAE, etc.

Here's a breakdown of its functionality:

1. **Imports**: The script imports necessary modules from the `OCC.Core` package to create points, define colors, and set visual aspects. It also imports functions to initialize and manage the 3D display.

2. **Initialization**: The `init_display()` function initializes the 3D viewer and returns functions to control the display (`display`, `start_display`, `add_menu`, and `add_function_to_menu`).

3. **Aspect Types**: A list `ALL_ASPECTS` is defined, containing various point aspect types (shapes like points, pluses, stars, rings, etc.).

4. **Point Creation Function (`pnt`)**:
    - The function `pnt()` generates a grid of points in a 3D space.
    - It uses three nested loops to create points at different coordinates (x, y, z).
    - Each point's position is determined by the loop indices (`idx`, `idy`, `idz`).
    - For each point, a `Geom_CartesianPoint` object is created using `gp_Pnt`.
    - A color is assigned to each point based on its x and z coordinates.
    - An `AIS_Point` object is created for each point, which is used for visualization.
    - The point's visual aspect is set using a `Prs3d_PointAspect` object, which defines the shape and color of the point.
    - The point is then displayed in the 3D viewer using `display.Context.Display`.

5. **Display Management**:
    - After creating all points, `display.FitAll()` is called to adjust the view to fit all the points.
    - `start_display()` is called to start the interactive 3D viewer.

6. **Exit Function**: A simple `exit()` function is defined to exit the script when called.

7. **Main Execution**: The script's main block calls the `pnt()` function to execute the point creation and display process when the script is run directly.

In summary, the script generates a 10x10x13 grid of 3D points, each with a different visual aspect and color, and displays them in an interactive 3D viewer.

## core_webgl_threejs_helix.py

This Python script is designed to create and display a 3D helical shape using the pythonOCC library, which is a set of Python bindings for the Open CASCADE Technology (OCCT), a software development platform for 3D CAD, CAM, CAE, etc.

Here's a step-by-step breakdown of the script's functionality:

1. **Import Statements**: The script imports necessary modules and classes from the `math` library and various `OCC` (Open CASCADE) core libraries, as well as a renderer from `OCC.Display.WebGl`.

2. **Creating a Cylindrical Surface**:
   - A cylindrical surface (`aCylinder`) is created using the `Geom_CylindricalSurface` class, with a radius of 6.0 units and aligned with the `gp_Ax3` axis system.

3. **Defining a 2D Line and Segment**:
   - A 2D line (`aLine2d`) is defined using the `gp_Lin2d` class, starting from the origin point `(0.0, 0.0)` and directed along `(1.0, 1.0)`.
   - A 2D segment (`aSegment`) is created from this line, spanning from `0.0` to `2π` (one full rotation).

4. **Creating a Helical Edge**:
   - A helical edge (`helix_edge`) is constructed using the `BRepBuilderAPI_MakeEdge` class, which takes the 2D segment and maps it onto the cylindrical surface, creating a 3D helical shape that spans `6π` units in height.

5. **Rendering the Helical Edge**:
   - An instance of `threejs_renderer.ThreejsRenderer` is created to handle the rendering.
   - The helical edge is displayed with a red color `(1, 0, 0)` and a line width of `1.0`.
   - The `render()` method is called to display the shape in a WebGL-enabled environment.

In summary, this script builds a 3D helical shape on a cylindrical surface and displays it using a WebGL renderer. The helix is defined by a 2D line segment wrapped around the cylinder, creating a spiral shape.

## core_topology_fillet.py

This Python script is part of a 3D CAD application built using the `pythonOCC` library, which is a set of Python wrappers for the OpenCASCADE Technology (OCCT) library. The script provides a graphical user interface (GUI) to perform various topology operations, specifically focusing on creating and manipulating fillets on 3D shapes. Below is a detailed breakdown of the script's purpose and functionality:

### Purpose:
The script demonstrates how to create and manipulate fillets (rounded edges) on various 3D shapes such as boxes and cylinders. It provides interactive functions to visualize these operations using the `pythonOCC` library's display capabilities.

### Functionality:

1. **Imports and Initialization:**
   - The script imports necessary modules from `pythonOCC` and standard Python libraries.
   - It initializes the display using `init_display` from `OCC.Display.SimpleGui`.

2. **Fillet Functions:**
   - **`fillet(event=None):`**
     - Creates a box and applies a uniform fillet of radius 20 to all edges.
     - Creates two boxes, fuses them together, and applies variable fillets based on edge lengths.
     - Displays the resulting shapes.

   - **`rake(event=None):`**
     - Creates a box and applies a variable fillet to one specific edge.
     - Displays the resulting shape if the fillet operation is successful.

   - **`fillet_cylinder(event=None):`**
     - Creates a cylinder and attempts to apply a fillet using a set of 2D points.
     - Displays the original and potentially filleted cylinder.

   - **`variable_filleting(event=None):`**
     - Creates a box and applies a variable fillet to one specific edge using a set of predefined 2D points.
     - Displays the resulting shape if the fillet operation is successful.

3. **Exit Function:**
   - **`exit(event=None):`**
     - Exits the application by calling `sys.exit()`.

4. **Main Execution:**
   - Adds a menu titled "topology fillet operations" to the GUI.
   - Adds the defined functions (`fillet`, `rake`, `variable_filleting`, `fillet_cylinder`, and `exit`) to the menu.
   - Starts the display loop to allow user interaction.

### Summary:
The script is a demonstration of how to use `pythonOCC` to create and manipulate 3D shapes with fillets. It provides several interactive functions to apply different types of fillets to boxes and cylinders, and it visualizes the results using a GUI. The script serves as an educational tool or a starting point for more complex CAD applications using `pythonOCC`.

## core_display_zlayer.py

This Python code is a script that uses the pythonOCC library, which is a set of Python bindings for the Open CASCADE Technology (OCCT) 3D modeling library. The script's purpose is to create and display a 3D box and a 3D sphere in a graphical window, each on a separate Z-layer, which allows for different rendering settings for each shape.

### Detailed Functionality:

1. **Importing Modules:**
   - `BRepPrimAPI_MakeBox` and `BRepPrimAPI_MakeSphere` are imported to create 3D box and sphere shapes.
   - `Graphic3d_ZLayerSettings` is imported to manage Z-layer settings for rendering.
   - `init_display` from `OCC.Display.SimpleGui` is imported to initialize the display.

2. **Initializing Display:**
   - `init_display()` initializes the display and returns functions for managing the display: `display`, `start_display`, `add_menu`, and `add_function_to_menu`.

3. **Creating Shapes:**
   - A box (`myBox`) with dimensions 60x60x50 units is created.
   - A sphere (`mySphere`) with a radius of 30 units is created.

4. **Viewer Initialization:**
   - The viewer object is retrieved from the display and printed.

5. **Creating Z-Layers:**
   - Two Z-layers are created using `Graphic3d_ZLayerSettings()`.
   - Each layer creation is confirmed with a print statement, displaying the layer ID.

6. **Displaying Shapes:**
   - The box is displayed using `display.DisplayShape(myBox)` and assigned to the first Z-layer.
   - The sphere is displayed using `display.DisplayShape(mySphere)` and assigned to the second Z-layer.

7. **Fitting and Starting Display:**
   - `display.FitAll()` adjusts the view to fit all displayed shapes.
   - `start_display()` starts the graphical display loop.

### Summary:
The script demonstrates how to use pythonOCC to create and render 3D shapes (a box and a sphere) in a graphical window, assigning each shape to different Z-layers for potentially different rendering settings. This can be useful for managing complex 3D scenes where different objects may require different rendering properties.

## core_topology_uv_to_cartesian_coordinates.py

This Python script utilizes the `pythonOCC` library to create and display a B-spline surface and a network of points on that surface. Here's a detailed breakdown of its purpose and functionality:

### Purpose
The script is designed to:
1. Construct a B-spline surface from a set of predefined points.
2. Generate a network of points on the created B-spline surface.
3. Display the B-spline surface and the network of points using a graphical user interface.

### Functionality

1. **Imports**:
   - Various modules from the `OCC` (Open CASCADE) library are imported for geometric and surface operations.
   - `init_display` from `OCC.Display.SimpleGui` is used to initialize the display for visualizing the shapes.

2. **Initialization**:
   - `init_display` initializes the display and provides functions to start the display and add shapes to it.

3. **`build_surf` Function**:
   - Defines six 3D points (`gp_Pnt`).
   - Creates a 2x3 array (`TColgp_Array2OfPnt`) to hold these points.
   - Populates the array with the defined points.
   - Generates a B-spline surface (`GeomAPI_PointsToBSplineSurface`) using the points array.
   - Returns the created B-spline surface.

4. **`build_points_network` Function**:
   - Accepts a B-spline surface as input.
   - Creates a face from the B-spline surface (`BRepBuilderAPI_MakeFace`).
   - Retrieves the UV parameter bounds of the face (`shapeanalysis_GetFaceUVBounds`).
   - Iterates over the UV parameter space within the bounds to sample points on the surface (`ShapeAnalysis_Surface.Value`).
   - Prints the UV coordinates and corresponding XYZ coordinates of each point.
   - Collects and returns the sampled points as a list.

5. **Main Execution Block**:
   - Calls `build_surf` to create the B-spline surface.
   - Displays the B-spline surface using `display.DisplayShape`.
   - Calls `build_points_network` to generate the network of points on the surface.
   - Iterates over the generated points and displays each one using `display.DisplayShape`.
   - Refreshes the display (`display.Repaint`).
   - Starts the display loop (`start_display`).

### Summary
This script is a practical example of using the `pythonOCC` library to create, manipulate, and visualize geometric shapes. Specifically, it constructs a B-spline surface from a set of points, samples points on this surface, and visually displays both the surface and the sampled points in a graphical user interface.

## core_font_helloworld.py

This Python script is part of the `pythonOCC` library, which is a set of Python bindings for the Open CASCADE Technology (OCCT), a software development platform for 3D CAD, CAM, CAE, etc. The script's main purpose is to create and display a 3D representation of a string of text using the `pythonOCC` library.

Here is a step-by-step breakdown of its functionality:

1. **Imports**: The script imports necessary modules from the `pythonOCC` library:
   - `init_display` from `OCC.Display.SimpleGui` for initializing the display window.
   - `text_to_brep` and `Font_FontAspect_Bold` from `OCC.Core.Addons` for creating a 3D representation of text.

2. **Initialize Display**: The `init_display()` function is called to set up the display environment. This function returns four objects: `display`, `start_display`, `add_menu`, and `add_function_to_menu`.

3. **Create 3D Text**: The `text_to_brep` function is used to create a 3D BREP (Boundary Representation) object from a string. The parameters provided to `text_to_brep` are:
   - The text string: `"pythonocc rocks !"`.
   - The font name: `"Arial"`.
   - The font aspect: `Font_FontAspect_Bold` (indicating bold text).
   - The font size: `12.0`.
   - A boolean value: `True` (likely indicating whether the text should be mirrored or some other attribute).

4. **Display the Text**: The `display.DisplayShape` method is called to render the 3D text in the display window. The `update=True` parameter ensures that the display is refreshed to show the new shape.

5. **Start Display Loop**: The `start_display()` function is called to start the GUI event loop, which keeps the display window open and responsive to user interactions.

In summary, this script initializes a display window, creates a 3D representation of the text "pythonocc rocks !" using a bold Arial font, and displays it in the window.

## core_geometry_point_from_intersection.py

The provided Python code is a script that uses the `pythonOCC` library, which is a set of Python bindings for the Open CASCADE Technology (OCCT) framework. This framework is commonly used for 3D CAD, CAM, CAE, etc. The script performs the following tasks:

1. **Initialization and Importing Modules:**
   - The script imports necessary modules from `pythonOCC` for geometric operations and display functionalities.

2. **Display Initialization:**
   - It initializes the display environment using `init_display()`, which sets up the display window and related functionalities.

3. **Function Definition (`points_from_intersection`):**
   - The function `points_from_intersection()` is defined to create and visualize the intersection points between a plane and an ellipse.
   - A plane is created using the `gp_Pln` class with the `gp_XOY` coordinate system.
   - An ellipse is defined in the `gp_YOZ` plane with specified major and minor radii.
   - The `IntAna_IntConicQuad` class is used to compute the intersection between the ellipse and the plane.
   - A rectangular trimmed surface is created from the plane and displayed.
   - The ellipse is also displayed.
   - If the intersection computation is successful (`IsDone()`), the number of intersection points is retrieved, and each point is displayed along with a label.

4. **Main Execution Block:**
   - The script calls `points_from_intersection()` to perform the intersection and visualization tasks.
   - It starts the display loop with `start_display()`, which keeps the display window open and interactive.

### Summary
The script's primary purpose is to demonstrate the intersection of a plane and an ellipse using the `pythonOCC` library. It visualizes the plane, the ellipse, and their intersection points in a 3D display window. The display is initialized and managed using functions provided by `pythonOCC`.

## core_json_serializer.py

The provided Python code is designed to handle JSON serialization and deserialization for the `gp_Pnt` class from the Open CASCADE Technology (OCCT) library, which represents a point in 3D space.

Here's a breakdown of its functionality:

1. **Imports**:
   - `json`: The standard library module for working with JSON data.
   - `gp_Pnt` from `OCC.Core.gp`: The class representing a 3D point in OCCT.

2. **Initialization**:
   - A `gp_Pnt` object, `p_1`, is created with coordinates (1.0, 3.14, -3.0).

3. **OCCT JSON Dump**:
   - The `DumpJson` method of `gp_Pnt` is used to generate a JSON string representation of the point. However, this method produces a non-conformant JSON string.
   - The code attempts to parse this JSON string using `json.loads()`, but it is expected to fail, resulting in a `Json decode error` message.

4. **Custom JSON Serialization/Deserialization**:
   - **`encode_json_gp_Pnt(p)`**: A custom function to serialize a `gp_Pnt` object into a JSON string. It creates a dictionary with the point's type and coordinates (`x`, `y`, `z`), and then converts it to a JSON string using `json.dumps()`.
   - **`decode_json_gp_Pnt(s)`**: A custom function to deserialize a JSON string back into a `gp_Pnt` object. It parses the JSON string to extract the coordinates and then creates a new `gp_Pnt` object with those values.

5. **Usage of Custom Functions**:
   - The custom `encode_json_gp_Pnt` function is used to serialize `p_1` into a JSON string `ss`.
   - The custom `decode_json_gp_Pnt` function is then used to deserialize the JSON string `ss` back into a `gp_Pnt` object `p_2`.

In summary, the code demonstrates how to handle JSON serialization and deserialization for `gp_Pnt` objects from the OCCT library by implementing custom functions to work around issues with the library's built-in JSON methods.

## core_visualization_camera.py

This Python code is designed to load and display a 3D model from a STEP file using the `pythonOCC` library, which is a set of Python bindings for the Open CASCADE Technology (OCCT) CAD kernel. Additionally, it includes functionality to animate the viewpoint of the displayed 3D model.

Here's a breakdown of the code's purpose and functionality:

1. **Initialization and Imports:**
   - The script starts with a shebang (`#!/usr/bin/env python`) indicating that it should be run using the Python interpreter.
   - It imports necessary functions from `OCC.Display.SimpleGui` and `OCC.Extend.DataExchange`.

2. **Display Initialization:**
   - `init_display()` initializes the display window and returns several functions: `display`, `start_display`, `add_menu`, and `add_function_to_menu`.

3. **Loading and Displaying the STEP File:**
   - `read_step_file("../assets/models/as1_pe_203.stp")` reads a STEP file located at `../assets/models/as1_pe_203.stp` and returns the shape.
   - `display.DisplayShape(the_shape)` displays the loaded shape in the initialized display window.

4. **Animating the Viewpoint:**
   - The function `animate_viewpoint()` is defined to animate the camera's viewpoint.
     - It fits the entire shape into the view and updates the viewer.
     - It retrieves the camera object and its current center and eye positions.
     - It then animates the camera by incrementally moving the eye position along the Y-axis and the center position along the Z-axis over 100 iterations each, updating the viewer after each change.

5. **Menu and Animation Integration:**
   - `add_menu("camera")` adds a menu named "camera" to the display window.
   - `add_function_to_menu("camera", animate_viewpoint)` adds the `animate_viewpoint` function as an option in the "camera" menu.

6. **Starting the Display:**
   - `start_display()` starts the display loop, allowing user interaction and rendering of the 3D model.

In summary, the code loads a STEP file, displays the 3D model in a graphical window, and provides a menu option to animate the camera's viewpoint, giving a dynamic view of the model.

## core_matplotlib_box.py

This Python code provides an example of how to use the `Tesselator` interface from the `pythonOCC` library to draw a 3D shape using `matplotlib`. Here is a detailed breakdown of its purpose and functionality:

1. **Imports:**
   - The script imports necessary modules from `OCC.Core` for tessellating and creating shapes.
   - It attempts to import `matplotlib` and its 3D toolkit. If `matplotlib` is not available, the script prints an error message and exits.

2. **Function Definition (`draw_shape_mpl`):**
   - The function `draw_shape_mpl(shape)` takes a `TopoDS_Shape` object as input and visualizes it using `matplotlib`.
   - It initializes a `ShapeTesselator` object with the given shape and computes the tessellation.
   - It retrieves the tessellated triangles and edges from the shape:
     - Triangles are extracted using `tess.GetTriangleIndex` and `tess.GetVertex`.
     - Edges are extracted using `tess.GetEdgeVertex`.
   - The function then creates a 3D plot using `matplotlib`:
     - Triangles are added to the plot with a semi-transparent appearance.
     - Edges are added to the plot with white color.
   - The plot is displayed using `plt.show()`.

3. **Main Execution:**
   - A box shape is created using `BRepPrimAPI_MakeBox(1, 1, 1).Shape()`, which defines a box with dimensions 1x1x1.
   - The `draw_shape_mpl` function is called with the created box shape to visualize it.

**Summary:**
The script demonstrates how to tessellate a 3D shape and visualize it using `matplotlib`'s 3D plotting capabilities. It specifically creates a 1x1x1 box and uses the `ShapeTesselator` from the `pythonOCC` library to convert the shape into a format suitable for plotting. The resulting plot shows the tessellated triangles and edges of the box.

## core_webgl_threejs_bigfile.py

This Python script is designed to read and render a 3D model from a STEP file using the pythonOCC library, which is a set of Python bindings for the Open Cascade Technology (OCCT) 3D modeling library. Here’s a breakdown of its functionality:

1. **Shebang Line**: `#!/usr/bin/env python`
   - Specifies the script should be run using the Python interpreter.

2. **License Information**: 
   - The script includes a block of comments specifying the copyright information and licensing under the GNU Lesser General Public License.

3. **Imports**:
   - `os`: Standard library module for interacting with the operating system.
   - `read_step_file` from `OCC.Extend.DataExchange`: Function to read a STEP file and convert it into a shape.
   - `threejs_renderer` from `OCC.Display.WebGl`: Module for rendering 3D shapes using Three.js via WebGL.

4. **Read STEP File**:
   - `big_shp = read_step_file(os.path.join("..", "assets", "models", "RC_Buggy_2_front_suspension.stp"))`
     - Constructs the file path to the STEP file `RC_Buggy_2_front_suspension.stp` located in the `../assets/models/` directory.
     - Reads the STEP file and stores the resulting shape in the variable `big_shp`.

5. **Render the Shape**:
   - `my_renderer = threejs_renderer.ThreejsRenderer()`
     - Creates an instance of the `ThreejsRenderer` class.
   - `my_renderer.DisplayShape(big_shp)`
     - Displays the shape stored in `big_shp` using the renderer.
   - `my_renderer.render()`
     - Renders the displayed shape.

**Summary**:
The script reads a 3D model from a specified STEP file and renders it using a WebGL-based renderer provided by the pythonOCC library. This allows visualization of the 3D model in a web browser using Three.js.

## core_display_activate_manipulator.py

The provided Python code is a graphical application using PyQt5 and pythonOCC (a set of Python bindings for the OpenCASCADE CAD kernel). Here's a clear and concise description of its purpose and functionality:

### Purpose:
The code creates a graphical user interface (GUI) application that allows users to interact with 3D shapes (a box and a sphere) using a manipulator tool. The application is built using PyQt5 for the GUI components and pythonOCC for the 3D CAD operations.

### Functionality:
1. **GUI Setup**:
   - The `App` class inherits from `QDialog` and initializes the main window with a title, size, and layout.
   - It creates a horizontal group box which contains buttons and a 3D viewer canvas.

2. **3D Viewer and Shapes**:
   - The `createGeometry` method initializes the 3D viewer and adds a box and a sphere to the display.
   - These shapes are managed by a `Layer` object, which allows for easy manipulation and visibility toggling.

3. **Buttons and Interactivity**:
   - Two buttons are provided: "Activate Manipulator" and "Show Layer".
   - "Activate Manipulator" allows the user to select a shape and manipulate it (translate, rotate, etc.).
   - "Show Layer" toggles the visibility of the layer containing the shapes.

4. **Manipulator Functionality**:
   - When the "Activate Manipulator" button is pressed, the selected shape can be manipulated using the `AIS_Manipulator`.
   - Transformations applied to the shape via the manipulator are retrieved and applied to the shape in the layer when the manipulator is deactivated.

5. **Application Execution**:
   - The `if __name__ == "__main__":` block initializes the `QApplication` and runs the `App` class, starting the GUI event loop.

### Key Components:
- **PyQt5**: Used for creating the GUI elements (buttons, layouts, main window).
- **pythonOCC**: Used for creating and manipulating 3D shapes (box and sphere) and handling the 3D viewer.
- **AIS_Manipulator**: Provides interactive manipulation tools for the 3D shapes within the viewer.

### Summary:
This application provides a simple interface for displaying and interacting with 3D shapes using a manipulator in a PyQt5 window. It demonstrates the integration of PyQt5 for the GUI and pythonOCC for the 3D CAD functionalities.

## core_display_pbr.py

This Python code is part of the `pythonOCC` library, which is used for 3D CAD modeling and visualization. The script's primary purpose is to create a simple 3D scene that includes a bottle, a table, and a glass, and to display them using different lighting and shading models. Here's a detailed breakdown of its functionality:

1. **Import Statements**:
   - The script imports various modules from the `pythonOCC` library, including tools for creating and manipulating 3D shapes, setting up the display, and configuring lighting and materials.

2. **Geometry Creation**:
   - It creates a table using a box shape.
   - It creates a glass by making a cone and then performing a Boolean cut operation to hollow it out.
   - It translates the glass to a specific position.

3. **Display Initialization**:
   - Initializes the display using the `init_display` function, which provides functions to start the display, add menus, and add functions to menus.

4. **Lighting Setup**:
   - Adds ambient light, directional light, and a spotlight to the scene for better visualization.

5. **Material and Shading Setup**:
   - Configures a metallic roughness material for the bottle.
   - Configures a plastic material with glass properties for the glass object.

6. **Display Shapes**:
   - Displays the bottle, table, and glass in the initialized display, applying the respective materials and colors.

7. **Shading Model Functions**:
   - Defines functions to switch between different shading models: PBR (Physically Based Rendering), PBR Facet, and Phong shading.

8. **Menu and Event Handling**:
   - Adds a menu named "PBR" to the display menu.
   - Adds the shading model functions to the "PBR" menu.
   - Defines an `exit` function to terminate the program.

9. **Main Execution**:
   - If the script is run as the main module, it sets up the menu and starts the display loop.

### Summary
The script is essentially a demonstration of how to create and visualize 3D objects using the `pythonOCC` library. It sets up a scene with a bottle, table, and glass, applies different materials and lighting, and provides a menu to switch between various shading models. The code is well-structured to showcase basic functionalities of 3D modeling, lighting, and rendering using `pythonOCC`.

## core_topology_boolean.py

The provided Python code is a script that utilizes the `pythonOCC` library to perform and visualize various boolean operations on 3D shapes. The script sets up a graphical user interface (GUI) using `pyqt5` to display the results of these operations. Here’s a concise breakdown of its purpose and functionality:

### Purpose:
The script demonstrates how to perform and visualize boolean operations such as fuse, common, section, and cut on 3D shapes using the `pythonOCC` library.

### Functionality:

1. **Imports and Initialization**:
   - Imports necessary modules from `pythonOCC` for creating and manipulating 3D shapes.
   - Initializes a GUI display using `init_display` from `OCC.Display.SimpleGui`.

2. **Helper Function**:
   - `translate_topods_from_vector`: Translates a given shape by a specified vector. This function can optionally create a copy of the shape before translating it.

3. **Boolean Operation Functions**:
   - `fuse`: Creates two boxes, translates one of them, fuses them together, and displays the resulting shape.
   - `common`: Creates a box and a wedge, computes their common volume, and displays the resulting shape with transparency.
   - `slicer`: Slices a sphere (or a selected shape) into multiple sections along the Z-axis and displays the sections.
   - `section`: Creates a torus and computes its intersection with multiple spheres, displaying the resulting sections.
   - `cut`: Creates a box and a sphere, cuts the sphere by the box, and displays the resulting shape with transparency.

4. **Exit Function**:
   - `exit`: Exits the script.

5. **Main Execution**:
   - Adds a menu titled "topology boolean operations" to the GUI.
   - Adds the boolean operation functions and the exit function to the menu.
   - Starts the GUI display.

### Usage:
When executed, the script launches a GUI with a menu that allows users to select and visualize different boolean operations on predefined 3D shapes. Each menu item corresponds to one of the boolean operation functions, enabling interactive exploration of the results.

This script is useful for learning and demonstrating the capabilities of the `pythonOCC` library in handling complex 3D geometric operations.

## core_geometry_make_pipe_shell.py

This Python code is used to create and display a 3D geometric shape by sweeping a circular profile along a Bezier curve spline using the `pythonOCC` library, which is a set of Python wrappers for the OpenCASCADE geometric modeling kernel.

### Detailed Breakdown:

1. **Imports:**
   - The code imports various classes and functions from the `pythonOCC` library, which are needed for creating geometric shapes, performing operations on them, and displaying them.

2. **Display Initialization:**
   - `init_display` is used to initialize the display window where the 3D shapes will be rendered. It returns several functions for manipulating the display.

3. **Function `thicken_spline(event=None)`:**
   - **Creation of Points:**
     - An array of points is created using `TColgp_Array1OfPnt`. These points define the control points of a Bezier curve.
   - **Bezier Curve:**
     - A Bezier curve is created using `Geom_BezierCurve` with the defined points. This curve acts as the spine along which the profile will be swept.
     - The curve is then converted into an edge and subsequently into a wire using `BRepBuilderAPI_MakeEdge` and `BRepBuilderAPI_MakeWire`.
     - The Bezier curve wire is displayed using `display.DisplayShape`.
   - **Profile Creation:**
     - A circular profile is created using `gp_Circ` with a radius of 1. The circle is positioned at the first point of the Bezier curve.
     - The circle is then converted into an edge and subsequently into a wire.
   - **Sweeping Operation:**
     - A pipe shell is created using `BRepOffsetAPI_MakePipeShell`, which will sweep the circular profile along the Bezier curve wire.
     - A linear law (`Law_Linear`) is defined to control the scaling of the profile along the spine. The law is set to scale the profile from 0.5 to 1 along the length of the spine.
     - The law is applied to the pipe shell using `SetLaw`.
   - **Return Shape:**
     - The resulting shape from the sweeping operation is returned.

4. **Main Execution:**
   - If the script is executed directly, `thicken_spline` is called to create the shape, which is then displayed using `display.DisplayShape`.
   - The display loop is started with `start_display` to render the shape and allow user interaction.

### Purpose:
The purpose of this script is to demonstrate the creation of a 3D shape by sweeping a circular profile along a Bezier curve spline using the `pythonOCC` library. The script sets up the necessary geometric entities, performs the sweeping operation, and displays the resulting shape in a graphical window.

## core_topology_edge.py

This Python script is designed to create and display various types of geometric edges using the `pythonOCC` library, which is a set of Python bindings for the Open CASCADE Technology (OCCT) library, a software development platform for 3D CAD, CAM, CAE, etc. Here's a breakdown of its purpose and functionality:

1. **Imports**:
   - Imports necessary modules and classes from the `OCC.Core` package for geometric operations and display functionalities.
   - Imports the `init_display` function from `OCC.Display.SimpleGui` to initialize the display window.

2. **Display Initialization**:
   - Calls `init_display()` to set up the display environment, obtaining handles to various display functions like `display`, `start_display`, `add_menu`, and `add_function_to_menu`.

3. **Edge Creation Function (`edge`)**:
   - This function is responsible for creating different types of edges and vertices, and displaying them in the initialized display window.
   - **Blue Edge**: Created between two points `gp_Pnt(-80, -50, -20)` and `gp_Pnt(-30, -60, -60)`.
   - **Yellow Edge**: Created between two vertices `gp_Pnt(-20, 10, -30)` and `gp_Pnt(10, 7, -25)`.
   - **White Edge**: Created along a line defined by an axis (`gp_Ax1`) from point `gp_Pnt(10, 10, 10)` in the direction `(1, 0, 0)`.
   - **Red Edge**: Created along an elliptical arc defined by `gp_Elips` with semi-major and semi-minor axes (60, 30) and spanning from 0 to π/2 radians.
   - **Green Edge**: Created as a Bezier curve passing through a series of points defined in an array `TColgp_Array1OfPnt`.

4. **Displaying Edges and Vertices**:
   - Uses `display.DisplayColoredShape` to display the edges with specified colors (Blue, White, Yellow, Red, Green).
   - Uses `display.DisplayShape` to display the vertices associated with the edges.

5. **Main Execution**:
   - If the script is run as the main program, it calls the `edge()` function to create and display the edges, and then calls `start_display()` to start the display loop, allowing the user to interact with the 3D view.

In summary, this script demonstrates how to create and visualize various geometric edges and vertices using the `pythonOCC` library, showcasing different geometric constructs such as lines, ellipses, and Bezier curves in a 3D display window.

## core_geometry_minimal_distance.py

This Python script uses the `pythonOCC` library to perform 3D geometric computations and visualizations. Specifically, it calculates and visualizes the minimal distances between two cubes and two circles. Here is a detailed breakdown of its functionality:

1. **Imports and Setup:**
   - The script imports necessary modules from `pythonOCC` for creating shapes, computing distances, and displaying results.
   - It initializes a display environment using `init_display()`.

2. **`compute_minimal_distance_between_cubes` Function:**
   - This function creates two 3D cubes at specified positions.
   - It computes the minimal distance between these two cubes using `BRepExtrema_DistShapeShape`.
   - The minimal distance is printed to the console.
   - A line representing the shortest distance between the two cubes is created and displayed in cyan.

3. **`compute_minimal_distance_between_circles` Function:**
   - This function creates two circles in 3D space with specified centers and radii.
   - It adjusts the display context for precise rendering.
   - It computes the minimal distance between these two circles, which, in this case, corresponds to their intersection points.
   - The intersection parameters on both circles are printed to the console.
   - The intersection points are marked and displayed.

4. **Main Execution:**
   - The script calls the functions to compute and display the minimal distances between the cubes and the circles.
   - It fits all displayed shapes into the view and starts the display loop.

The script is designed to visually demonstrate geometric computations and their results using the `pythonOCC` library.

## core_topology_glue.py

The provided Python code is a script that utilizes the PythonOCC library (a set of Python bindings for the OpenCASCADE Technology CAD kernel) to create, manipulate, and visualize 3D shapes, specifically focusing on the operation of "gluing" two solid shapes together.

### Key Functionalities:

1. **Initialization and Display Setup:**
   - The script initializes the display environment using `init_display()` from the `OCC.Display.SimpleGui` module. This sets up the viewer for 3D visualization.

2. **Helper Functions:**
   - `get_faces(_shape)`: Extracts and returns all faces from a given shape.
   - `tag_faces(_shape, _color, shape_name)`: Tags and colors the faces of a given shape for easier identification in the viewer.
   - `tag_edge(_edge, msg, _color=(1, 0, 0))`: Tags an edge with a message and color for visualization.

3. **Gluing Solids:**
   - `glue_solids(event=None)`: Demonstrates gluing two boxes (`S1` and `S2`) together by selecting specific faces (`F1` from `S1` and `F2` from `S2`), performing the gluing operation, and displaying the result.
   - `glue_solids_edges(event=None)`: Similar to `glue_solids`, but focuses on gluing two boxes (`S3` and `S4`) that share common edges. It tags and binds these edges as part of the gluing process.

4. **Main Execution:**
   - The script adds a menu named "glue topology" with options to run the `glue_solids` and `glue_solids_edges` functions. The `start_display()` function is called to start the viewer and display the GUI.

### Purpose:
The primary purpose of this script is to demonstrate the process of gluing two solid shapes together using the PythonOCC library. It provides visual feedback by coloring and tagging the faces and edges involved in the gluing operation, making it easier to understand and inspect the results.

### Usage:
- Run the script to open a graphical user interface (GUI) with a menu.
- Use the menu to trigger the gluing operations (`glue_solids` or `glue_solids_edges`).
- Observe the displayed shapes, tagged faces, and edges to understand how the shapes are glued together.

This script is useful for CAD developers and engineers who need to perform and visualize complex shape operations using the OpenCASCADE Technology through Python.

## core_geometry_parabola.py

This Python script is designed to create and display a 2D parabola using the pythonOCC library, which is a set of Python bindings for the Open CASCADE Technology (OCCT) 3D modeling kernel. Below is a detailed explanation of its purpose and functionality:

### Purpose:
The script's primary purpose is to construct a 2D parabola and display it using a graphical user interface (GUI) provided by the pythonOCC library. It allows users to visualize geometric shapes, specifically a parabola in this case.

### Functionality:
1. **Imports and Initialization:**
   - The script imports necessary modules from the pythonOCC library, which include classes and functions for creating geometric shapes (`gp_Pnt2d`, `gp_Dir2d`, `gp_Ax22d`, `gp_Parab2d`), making parabolas (`GCE2d_MakeParabola`), and trimming curves (`Geom2d_TrimmedCurve`).
   - It also imports functions for initializing the display (`init_display`) and sets up the display environment.

2. **Parabola Creation Function (`parabola`):**
   - This function is responsible for constructing the parabola and displaying it.
   - **Vertex and Axis of Symmetry:** It defines a vertex point (`a_pnt`) and a direction (`a_dir`) to create an axis (`an_ax`) for the parabola.
   - **Parabola Definition:** It constructs a 2D parabola (`para`) using the axis and a specified focal length (6 units).
   - **Display Vertex:** The vertex point is displayed on the GUI, and a message "P" is shown at this point.
   - **Parabola Construction:** It creates the parabola using `GCE2d_MakeParabola` and retrieves the geometric parabola (`gParabola`).
   - **Trimming Curve:** The parabola is trimmed to a specified range (-100 to 100) using `Geom2d_TrimmedCurve`.
   - **Display Parabola:** The trimmed curve is displayed in the GUI.

3. **Main Execution:**
   - When the script is run as the main module, it calls the `parabola` function to create and display the parabola.
   - The `start_display` function is called to start the GUI event loop, allowing the user to interact with the display.

### Summary:
In summary, this script leverages the pythonOCC library to create a 2D parabola based on a specified vertex, direction, and focal length, and displays it using a simple GUI. It showcases how to construct and visualize geometric shapes using high-level abstractions provided by pythonOCC.

## core_webgl_x3dom_random_boxes.py

The provided Python code is designed to generate and render 3D boxes with random dimensions, positions, orientations, colors, and transparency levels using the `pythonOCC` library and the `x3dom_renderer` for WebGL visualization. Below is a detailed breakdown of its functionality:

1. **Imports:**
   - `random`: Standard library module for generating random numbers.
   - `x3dom_renderer` from `OCC.Display.WebGl`: Module for rendering 3D objects using WebGL.
   - `BRepPrimAPI_MakeBox` from `OCC.Core.BRepPrimAPI`: Function to create a box shape.
   - `gp_Vec` from `OCC.Core.gp`: Class for representing 3D vectors.
   - `translate_shp` and `rotate_shp_3_axis` from `OCC.Extend.ShapeFactory`: Functions for translating and rotating shapes.

2. **Renderer Initialization:**
   - `my_ren = x3dom_renderer.X3DomRenderer()`: Initializes the WebGL renderer.

3. **Main Loop (for i in range(100)):**
   - **Box Creation:**
     - `box_shp = BRepPrimAPI_MakeBox(random.random() * 20, random.random() * 20, random.random() * 20).Shape()`: Creates a box with random dimensions (width, height, depth) between 0 and 20 units.
   
   - **Random Orientation:**
     - `angle_x`, `angle_y`, `angle_z`: Generate random angles (0 to 360 degrees) for rotation around the x, y, and z axes.
     - `rotated_box = rotate_shp_3_axis(box_shp, angle_x, angle_y, angle_z, "deg")`: Rotates the box by the random angles.

   - **Random Position:**
     - `tr_x`, `tr_y`, `tr_z`: Generate random translation values between -20 and 20 units along the x, y, and z axes.
     - `trans_box = translate_shp(rotated_box, gp_Vec(tr_x, tr_y, tr_z))`: Translates the rotated box to the new random position.
   
   - **Random Color and Transparency:**
     - `rnd_color = (random.random(), random.random(), random.random())`: Generates a random RGB color.
     - `my_ren.DisplayShape(trans_box, export_edges=True, color=rnd_color, transparency=random.random())`: Displays the box with the random color and transparency level.

4. **Rendering:**
   - `my_ren.render()`: Renders all the generated and transformed boxes in the WebGL viewer.

In summary, this script generates 100 boxes with random dimensions, positions, orientations, colors, and transparency levels, and then renders them using the WebGL-based `x3dom_renderer` for visualization in a web browser.

## core_geometry_face_recognition_from_stepfile.py

This Python script is designed to load a STEP file, identify the geometrical nature of each face (such as whether the face is planar or cylindrical), and display the properties of these faces. The script provides two modes of operation: interactive mode and batch mode. Below is a detailed breakdown of its functionality:

1. **Imports and Dependencies**:
   - The script imports various modules from the `OCC` (Open CASCADE Technology) library, which is used for 3D CAD, CAM, CAE, etc.
   - It also imports standard Python modules like `os` and `sys`.

2. **Reading the STEP File**:
   - The `read_step_file(filename)` function reads a STEP file and returns its shape. It uses the `STEPControl_Reader` class to read the file and transfer its contents.

3. **Face Recognition**:
   - The `recognize_face(a_face)` function takes a face from the shape and identifies whether it is a plane or a cylinder. It prints the properties of the face:
     - For a plane: It prints the location and normal vector.
     - For a cylinder: It prints the location and axis vector.

4. **Interactive Mode**:
   - The `recognize_clicked(shp, *kwargs)` function is called whenever a face is clicked in the 3D view. It identifies and prints the properties of the clicked face using the `recognize_face` function.

5. **Batch Mode**:
   - The `recognize_batch(event=None)` function processes all faces of the shape and identifies their properties. It iterates over all faces using `TopologyExplorer` and calls `recognize_face` for each one.

6. **Initialization and Display**:
   - The script initializes the 3D display using `init_display()` from `OCC.Display.SimpleGui`.
   - It registers the `recognize_clicked` function as a callback for face selection.
   - It loads and displays the STEP file specified in the script.
   - It sets the selection mode to face selection.
   - It adds a menu item to trigger the batch mode recognition (`recognize_batch`).

7. **Execution**:
   - The script starts the display loop, allowing for interactive selection and recognition of faces.

**Overall Purpose**:
The primary purpose of this script is to load a STEP file, identify the type of each face (planar or cylindrical), and display the properties of these faces. It provides both an interactive mode for clicking and identifying individual faces and a batch mode for processing all faces at once. This can be useful in CAD applications where understanding the geometrical properties of a model is necessary.

## core_webgl_threejs_bigfile_oneshape.py

This Python script is designed to read and render a 3D model from a STEP file using the `pythonOCC` library, which is a set of Python wrappers for the Open CASCADE Technology (OCCT) CAD kernel.

Here's a breakdown of its functionality:

1. **Metadata and Licensing Information**:
   - The script starts with a shebang (`#!/usr/bin/env python`) to indicate that it should be executed using the Python interpreter.
   - It includes a copyright notice and licensing information, specifying that the code is part of `pythonOCC` and is distributed under the GNU Lesser General Public License (LGPL).

2. **Imports**:
   - The `os` module is imported for handling file paths.
   - Specific functions and classes from the `pythonOCC` library are imported:
     - `read_step_file` from `OCC.Extend.DataExchange` to read STEP files.
     - `threejs_renderer` from `OCC.Display.WebGl` to render the model using Three.js, a JavaScript 3D library.

3. **Reading the STEP File**:
   - The script constructs the file path to a STEP file named `RC_Buggy_2_front_suspension.stp` located in the `../assets/models` directory relative to the script's location.
   - It uses the `read_step_file` function to read the STEP file and store the resulting shape in the variable `big_shp`.

4. **Rendering the 3D Model**:
   - An instance of `ThreejsRenderer` is created and stored in `my_renderer`.
   - The `DisplayShape` method of `my_renderer` is called with `big_shp` as an argument to prepare the shape for rendering.
   - Finally, the `render` method of `my_renderer` is called to render the 3D model.

In summary, this script reads a 3D model from a specific STEP file and renders it using a Three.js-based renderer provided by the `pythonOCC` library.

## core_tesselation_vertices_list.py

This Python code is a script that uses the `pythonOCC` library to create a 3D box shape, perform tessellation on it, and then process the tessellated vertices and normals. Here's a step-by-step breakdown of its purpose and functionality:

1. **Library Imports**:
   - The script imports `ShapeTesselator` from `OCC.Core.Tesselator` for tessellation.
   - It imports `BRepPrimAPI_MakeBox` from `OCC.Core.BRepPrimAPI` to create a 3D box shape.
   - It attempts to import `numpy` to handle numerical operations, setting a flag (`HAVE_NUMPY`) based on the success of the import.

2. **Shape Creation**:
   - It creates a 3D box shape with dimensions 10x20x30 using `BRepPrimAPI_MakeBox(10, 20, 30).Shape()` and stores the shape in `box_s`.

3. **Tessellation**:
   - A `ShapeTesselator` object is created with the box shape (`box_s`).
   - The tessellation is computed using `tess.Compute()`.

4. **Vertex and Triangle Data Extraction**:
   - The vertices of the tessellated shape are obtained as a tuple using `tess.GetVerticesPositionAsTuple()`.
   - The number of triangles in the tessellated shape is retrieved using `tess.ObjGetTriangleCount()`.
   - The number of vertices is determined by the length of the `vertices_position` tuple.

5. **Validation**:
   - The script checks if the number of vertices is a multiple of 3. If not, it raises an `AssertionError`.
   - It verifies that the number of vertices corresponds to the expected number based on the number of triangles (each triangle should have 9 vertices since each vertex has 3 coordinates). If the counts don't match, it raises an `AssertionError`.

6. **Normals Extraction and Validation**:
   - The normals of the tessellated shape are obtained as a tuple using `tess.GetNormalsAsTuple()`.
   - It checks if the number of normals matches the number of vertices. If not, it raises an `AssertionError`.

7. **Numpy Array Conversion (if available)**:
   - If `numpy` is available (`HAVE_NUMPY` is `True`), the script reshapes the vertices and normals tuples into 2D numpy arrays with each row representing a vertex or normal vector in 3D space. This is done using `np.array()` and `reshape()`.

In summary, this script creates a 3D box, tessellates it, extracts and validates the vertices and normals, and optionally converts these data into numpy arrays for further numerical processing if `numpy` is available.

## core_webgl_STEP_to_X3D.py

This Python code is designed to read a STEP file containing 3D CAD data, extract the shapes, labels, and colors from it, and then render the shapes using the x3dom renderer for web-based visualization. Here's a step-by-step breakdown of its functionality:

1. **Importing Required Modules:**
   - `read_step_file_with_names_colors` from `OCC.Extend.DataExchange`: This function reads a STEP file and extracts shapes along with their associated labels and colors.
   - `x3dom_renderer` from `OCC.Display.WebGl`: This module provides functionality to render 3D shapes using the x3dom renderer.

2. **File Path Specification:**
   - The variable `filename` is assigned the path to the STEP file (`"../assets/models/as1-oc-214.stp"`).

3. **Reading the STEP File:**
   - `shapes_labels_colors` is assigned the result of `read_step_file_with_names_colors(filename)`, which reads the STEP file and returns a dictionary where keys are shapes and values are tuples containing labels and colors.

4. **Creating the Renderer:**
   - An instance of `X3DomRenderer` is created and assigned to `my_renderer`.

5. **Rendering the Shapes:**
   - The code iterates over the `shapes_labels_colors` dictionary. For each shape (`shp`):
     - Retrieves the associated label and color (`label, c`).
     - Calls `my_renderer.DisplayShape` to render the shape with its color. The color is specified using the `Red()`, `Green()`, and `Blue()` methods of the color object `c`.
     - The `export_edges` parameter is set to `False`, meaning edges are not exported in the rendering process.

6. **Final Rendering:**
   - `my_renderer.render()` is called to finalize and display the rendered shapes.

### Summary
The script reads a STEP file containing 3D CAD data, extracts the shapes along with their labels and colors, and renders these shapes using the x3dom renderer for web-based visualization.

## core_helloworld.py

The provided Python code is an introductory example for the `pythonOCC` library, which is a set of Python bindings for the Open CASCADE Technology (OCCT) framework, used for 3D CAD, CAM, CAE, etc. The script demonstrates the following key functionalities:

1. **Checking Installation**: Ensures that `pythonOCC` is correctly installed and its modules can be imported without errors.
2. **GUI Manager**: Verifies that a GUI manager (either wxPython or PyQt/PySide) is installed, which is necessary for displaying a 3D window.
3. **Rendering Setup**: Tests that the rendering window can be initialized and set up correctly, confirming that the graphics driver and OpenGL are working properly.

### Breakdown of the Code:

1. **Imports**:
   - `init_display` from `OCC.Display.SimpleGui`: Initializes the display window.
   - `BRepPrimAPI_MakeBox` from `OCC.Core.BRepPrimAPI`: Allows creation of a 3D box shape.

2. **Initialization**:
   - `display, start_display, add_menu, add_function_to_menu = init_display()`: Initializes the display window and sets up the necessary functions for starting the display, adding menus, and adding functions to menus.

3. **3D Shape Creation**:
   - `my_box = BRepPrimAPI_MakeBox(10.0, 20.0, 30.0).Shape()`: Creates a 3D box with dimensions 10x20x30 units.

4. **Display Shape**:
   - `display.DisplayShape(my_box, update=True)`: Displays the created box shape in the initialized display window.

5. **Start Display**:
   - `start_display()`: Launches the display window, allowing the user to interact with the 3D scene.

### Purpose:

The script serves as a basic test to ensure that the `pythonOCC` library is properly installed and configured on the user's machine. It provides a simple way to verify that a 3D shape can be created and rendered in a GUI window, indicating that the environment is correctly set up for further exploration and use of the `pythonOCC` library.

## core_topology_evolved_shape.py

The provided Python code is a script that uses the `pythonOCC` library, which is a set of Python bindings for the Open CASCADE Technology (OCCT) library. This script is designed to create and display a 3D evolved shape using geometric modeling techniques. Here's a detailed breakdown of its purpose and functionality:

1. **Imports**:
    - `gp_Pnt` from `OCC.Core.gp`: Used to define 3D points.
    - `BRepBuilderAPI_MakePolygon` from `OCC.Core.BRepBuilderAPI`: Used to create polygonal wires.
    - `GeomAbs_Arc` from `OCC.Core.GeomAbs`: Represents the type of geometry for the evolution.
    - `BRepOffsetAPI_MakeEvolved` from `OCC.Core.BRepOffsetAPI`: Used to create evolved shapes (swept shapes).
    - `init_display` from `OCC.Display.SimpleGui`: Used to initialize the display window for visualization.

2. **Display Initialization**:
    - `init_display()` initializes the display window and returns functions for managing the display (`display`, `start_display`, `add_menu`, `add_function_to_menu`).

3. **Function `evolved_shape`**:
    - Creates a polygon `P` with vertices at specified 3D points to form a closed wire.
    - Creates another polygon `wprof` to serve as the profile wire for the evolution.
    - Uses `BRepOffsetAPI_MakeEvolved` to create an evolved shape by sweeping the profile wire `wprof` along the path defined by the wire `P`. The `GeomAbs_Arc` parameter specifies the type of evolution.
    - `S.Build()` constructs the evolved shape.
    - `display.DisplayShape(S.Shape(), update=True)` displays the created shape in the visualization window.

4. **Main Execution Block**:
    - Calls the `evolved_shape` function to create and display the shape.
    - Calls `start_display()` to start the GUI event loop, which keeps the display window open and responsive.

### Summary
The script creates a 3D evolved shape by sweeping a profile wire along a defined path wire. It then displays the resulting shape using a graphical user interface provided by the `pythonOCC` library. The shape is constructed by defining a base polygon and a profile polygon, and then using the `BRepOffsetAPI_MakeEvolved` function to perform the evolution. The display is initialized and managed using functions from `OCC.Display.SimpleGui`.

## core_geometry_nurbs_converter.py

This Python code is designed to create a 3D torus shape, convert it into a NURBS (Non-Uniform Rational B-Splines) representation, and then analyze its surface properties. Here is a step-by-step breakdown of its functionality:

1. **Library Imports**:
   - It imports various modules from the `OCC` (Open CASCADE Technology) library, which is used for 3D CAD, CAM, CAE development.
   - Specifically, it imports functions for creating a torus (`BRepPrimAPI_MakeTorus`), converting shapes to NURBS (`BRepBuilderAPI_NurbsConvert`), adapting surfaces (`BRepAdaptor_Surface`), and exploring topological elements (`TopologyExplorer`).

2. **Create a Torus**:
   - `base_shape = BRepPrimAPI_MakeTorus(30, 10).Shape()`: This line creates a torus with a major radius of 30 units and a minor radius of 10 units.

3. **Convert to NURBS**:
   - `nurbs_converter = BRepBuilderAPI_NurbsConvert(base_shape, True)`: This initializes a NURBS converter for the torus shape.
   - `converted_shape = nurbs_converter.Shape()`: This converts the torus shape into its NURBS representation.

4. **Topology Exploration**:
   - `expl = TopologyExplorer(converted_shape)`: This initializes a topology explorer to traverse the converted shape.

5. **Analyze Faces**:
   - The code loops over each face of the NURBS-converted shape:
     ```python
     for face in expl.faces():
     ```
   - For each face, it checks if the surface type is a BSpline surface:
     ```python
     if not surf_type == GeomAbs_BSplineSurface:
         raise AssertionError("the face was not converted to a GeomAbs_BSplineSurface")
     ```
   - It retrieves and prints various properties of the BSpline surface:
     - **Degrees**: UDegree and VDegree of the surface.
     - **Knots**: Arrays of UKnots and VKnots.
     - **Weights**: A 2D array of weights (if available).
     - **Control Points**: A 2D array of control points (also known as poles).

6. **Output**:
   - The code prints detailed information about each face's NURBS representation, including degrees, knots, weights, and control points.

### Summary
The purpose of this code is to:
1. Create a 3D torus shape.
2. Convert the torus into its NURBS representation.
3. Verify and analyze the NURBS properties of the torus's faces, ensuring they are correctly converted to BSpline surfaces.
4. Print detailed information about the NURBS representation, including degrees, knots, weights, and control points.

## core_classic_occ_bottle.py

The provided Python code is a script that uses the `pythonOCC` library to create a 3D model of a bottle with a threaded neck. Here's a breakdown of its purpose and functionality:

### Purpose:
The script generates a 3D bottle model, including its body, neck, and threading on the neck. It then displays the bottle using a graphical user interface (GUI) provided by `pythonOCC`.

### Functionality:
1. **Imports and Setup**:
    - The script begins by importing necessary modules from `pythonOCC` for 3D geometric operations, transformations, and modeling.
    - It defines two helper functions: `face_is_plane` to check if a face is planar, and `geom_plane_from_face` to extract the geometric plane from a face.

2. **Bottle Body Creation**:
    - The script defines the dimensions of the bottle (height, width, thickness).
    - It creates five points to define the profile of the bottle's body.
    - Using these points, it constructs edges (line segments and an arc) and combines them into a wire.
    - The wire is mirrored along the X-axis to create a symmetrical profile.
    - The mirrored wire and the original wire are combined into a single wire profile.
    - This wire profile is then used to create a face, which is extruded (swept) along the Z-axis to form the bottle's body.

3. **Adding Fillets**:
    - Fillets (rounded edges) are added to all edges of the bottle's body using an edge explorer to iterate over the edges.

4. **Creating the Neck**:
    - A cylindrical neck is created at the top of the bottle using the defined neck radius and height.
    - The neck is fused with the body of the bottle.

5. **Making the Bottle Hollow**:
    - The script identifies the highest Z face (the top face) to remove it and create a hollow bottle.
    - It then thickens the bottle walls by creating a thick solid with a specified thickness.

6. **Adding Threading to the Neck**:
    - Cylindrical surfaces are defined for threading.
    - 2D curves (ellipses and segments) are created to define the shape of the threads.
    - These 2D curves are converted into 3D edges and wires.
    - The wires are used to create the threading surface using the `BRepOffsetAPI_ThruSections` tool.

7. **Combining Components**:
    - The body of the bottle (with fillets and neck) and the threading are combined into a single compound shape.

8. **Displaying the Bottle**:
    - If the script is run as the main module, it initializes a display window using `OCC.Display.SimpleGui`.
    - The bottle is displayed in the GUI.

### Summary:
The script leverages `pythonOCC` to create a detailed 3D model of a bottle with a hollow body, a neck, and threading on the neck. It demonstrates various CAD operations such as creating vertices, edges, wires, faces, extrusions, filleting, fusing shapes, and creating threaded surfaces. Finally, it visualizes the resulting 3D model using a GUI.

## core_topology_boolean_general_fuse_algorithm.py

This Python code is part of the `pythonOCC` library, which is a set of Python wrappers for the OpenCASCADE 3D modeling library. The code's primary purpose is to create and display a 3D shape resulting from the fusion of two boxes using the General Fuse Algorithm.

Here's a step-by-step breakdown of the code:

1. **Imports**:
   - `init_display` from `OCC.Display.SimpleGui`: Initializes the display window for rendering 3D shapes.
   - `BRepPrimAPI_MakeBox` from `OCC.Core.BRepPrimAPI`: Used to create box shapes.
   - `BOPAlgo_Builder` from `OCC.Core.BOPAlgo`: Provides algorithms for Boolean operations on shapes.

2. **Display Initialization**:
   - `init_display()` initializes the display and returns four functions: `display`, `start_display`, `add_menu`, and `add_function_to_menu`.

3. **Box Creation**:
   - `my_box1` and `my_box2` are created using `BRepPrimAPI_MakeBox`, with dimensions (10.0, 20.0, 30.0) and (20.0, 1.0, 30.0) respectively.

4. **Boolean Operation (Fusion)**:
   - An instance of `BOPAlgo_Builder` is created.
   - The two boxes are added as arguments to the builder using `AddArgument`.
   - The builder is set to run in parallel mode with `SetRunParallel(True)`.
   - The fusion operation is performed using `Perform()`.

5. **Error Handling**:
   - If there are any errors during the fusion operation, an `AssertionError` is raised with a message containing the error details.

6. **Result Display**:
   - The resulting fused shape is obtained using `builder.Shape()`.
   - The result is displayed in the initialized display window using `display.DisplayShape(result, update=True)`.
   - `start_display()` is called to start the display loop, allowing the user to view the fused shape interactively.

In summary, this code creates two box shapes, fuses them together using a Boolean operation, and displays the resulting shape in a graphical window.

## core_display_textured_shape.py

This Python script is designed to create and display a 3D cylinder with a texture applied to it using the `pythonOCC` library, which is a set of Python bindings for the Open CASCADE Technology (OCCT) 3D modeling library.

Here's a breakdown of its purpose and functionality:

1. **Imports and Initialization:**
   - The script imports necessary modules: `os` for file operations, `BRepPrimAPI_MakeCylinder` from `OCC.Core.BRepPrimAPI` for creating the cylinder, and `init_display` from `OCC.Display.SimpleGui` for initializing the display environment.
   - It initializes the display environment using `init_display`, which returns functions for managing the display.

2. **Texture Class:**
   - A `Texture` class is defined to encapsulate texture properties such as filename, scaling, repeating, and origin coordinates.
   - The constructor `__init__` checks if the texture file exists and initializes default properties.
   - Methods `TextureScale`, `TextureRepeat`, and `TextureOrigin` are provided to set the respective properties.
   - `GetProperties` method returns a tuple of all the texture properties.

3. **Creating and Applying Texture:**
   - An instance of the `Texture` class is created using a specified texture file (`ground.bmp`).
   - A cylinder is created with a radius of 60 and height of 200 using `BRepPrimAPI_MakeCylinder`.

4. **Displaying the Cylinder:**
   - The cylinder shape is displayed with the specified texture applied using `display.DisplayShape`.
   - The `start_display` function is called to start the display loop, rendering the cylinder on the screen.

### Summary
The script creates a textured 3D cylinder and displays it. It defines a `Texture` class to manage texture properties and uses the `pythonOCC` library to handle 3D modeling and rendering. The texture is applied to the cylinder, and the display environment is initialized and started to visualize the result.

## ifc_clip_plane.py

This Python script is designed to visualize and manipulate an IFC (Industry Foundation Classes) file using the `ifcopenshell` and `pythonOCC` libraries. Here's a detailed breakdown of its purpose and functionality:

1. **Library Imports**:
   - The script imports necessary modules from `OCC.Core` for geometric and graphical operations.
   - It also imports `ifcopenshell` and `ifcopenshell.geom` for handling IFC files.
   - `init_display` from `OCC.Display.SimpleGui` is used to initialize the graphical display.

2. **Initialization**:
   - The script initializes the display using `init_display` which returns functions to control the display (`display`, `start_display`, `add_menu`, and `add_function_to_menu`).
   - It sets up `ifcopenshell` to use `pythonocc` for geometry processing.

3. **IFC File Loading**:
   - The script attempts to load an IFC file named `IFC Schependomlaan.ifc` from a specified directory.
   - It ensures the file exists using an assertion and then opens it with `ifcopenshell`.

4. **Clip Plane Setup**:
   - A clipping plane (`clip_plane_1`) is created using `Graphic3d_ClipPlane`.
   - The clipping plane is configured with capping and hatch settings and is initially turned off.
   - The material and color of the clipping plane are set for visualization purposes.

5. **Processing IFC Products**:
   - The script iterates over all `IfcProduct` entities in the IFC file.
   - For each product with a 3D representation, it:
     - Creates a shape using `ifcopenshell.geom.create_shape`.
     - Extracts the color of the shape.
     - Displays the shape in the viewer using `display.DisplayShape`.
     - Adds the clipping plane to the displayed shape.
     - Updates the viewer every 50 shapes to improve performance.

6. **Clip Plane Animation**:
   - A function `animate_translate_clip_plane` is defined to animate the translation of the clipping plane.
   - This function moves the clipping plane along the Z-axis in small increments and updates the viewer accordingly.

7. **Main Execution**:
   - If the script is run as the main module, it adds a menu item for the clipping plane animation.
   - It fits all shapes in the viewer and starts the display loop.

In summary, the script loads an IFC file, visualizes its 3D components using `pythonOCC`, and sets up a clipping plane that can be animated to translate through the model. This functionality is useful for inspecting and analyzing the interior structures of complex 3D models in IFC format.

## core_boolean_sewed_shapes.py

This Python script leverages the `pythonOCC` library to perform various 3D shape operations and visualize the results. Here’s a concise breakdown of its purpose and functionality:

### Purpose:
The script demonstrates the creation and manipulation of 3D geometric shapes using the `pythonOCC` library. It specifically focuses on constructing an L-shaped object, performing Boolean operations (cut, fuse, and common) on boxes and L-shaped objects, and visualizing the results using a graphical display.

### Functionality:

1. **Imports and Initialization:**
   - Imports necessary classes and functions from `pythonOCC` for geometric operations and display.
   - Initializes the display environment using `init_display()`.

2. **Helper Functions:**
   - `MakeSolidFromShell(shell)`: Converts a shell into a solid.
   - `make_face_from_4_points(pnt1, pnt2, pnt3, pnt4)`: Creates a face from four points by first constructing a polygon wire and then making a face from it.
   - `get_faceted_L_shape(x, y, z)`: Constructs an L-shaped object using a series of points and faces, and returns the sewed shape.

3. **Main Operations:**
   - Creates and performs Boolean operations (cut, fuse, and common) on boxes and L-shaped objects:
     - **Cut Operation:** Subtracts one box from another and an L-shaped object from a box.
     - **Common Operation:** Finds the intersection between an L-shaped object and a box.
     - **Fuse Operation:** Merges an L-shaped object with a box.

4. **Visualization:**
   - Displays the results of the Boolean operations using different colors for each operation:
     - Red for the first cut operation.
     - Blue for the second cut operation.
     - White for the intersection operation.
     - Green for the solid cut operation.
     - Yellow for the fuse operation.
     - Cyan for the common operation.
   - Fits all shapes into the view and starts the display.

### Summary:
The script is a comprehensive example of using `pythonOCC` to create complex 3D shapes, perform Boolean operations, and visualize the results. It demonstrates the capabilities of `pythonOCC` for 3D geometric modeling and provides a clear structure for creating and manipulating 3D objects programmatically.

## core_display_customize_prs3d.py

This Python script is designed to demonstrate how to adjust the display quality of 3D shapes using the `pythonOCC` library, which is a set of Python wrappers for the OpenCASCADE Technology (OCCT) library. Here's a detailed breakdown of its purpose and functionality:

### Purpose:
The script shows how to set display quality for 3D shapes, specifically a cylinder, in a graphical window. It highlights how to manipulate various display settings such as line width and hidden line rendering.

### Functionality:

1. **Imports:**
   - `BRepPrimAPI_MakeCylinder` from `OCC.Core.BRepPrimAPI`: Used to create a cylinder shape.
   - `init_display` from `OCC.Display.SimpleGui`: Initializes the display window and provides functions to control it.

2. **Display Initialization:**
   - `init_display()` is called to initialize the display window and retrieve control functions (`display`, `start_display`, `add_menu`, `add_function_to_menu`).
   - `display.SetModeHLR()`: Sets the display mode to Hidden Line Removal (HLR), which improves the visibility of the shape's edges.

3. **Context and Drawer Setup:**
   - `ais_context = display.GetContext()`: Retrieves the interactive context from the display.
   - `drawer = ais_context.DefaultDrawer()`: Gets the default drawer (a set of display attributes) from the context.
   - `drawer.SetIsoOnPlane(True)`: Sets the drawer to display isometric planes.
   - `la = drawer.LineAspect()`: Retrieves the line aspect settings from the drawer.
   - `la.SetWidth(4)`: Increases the line width to 4 units.
   - `line_aspect = drawer.SeenLineAspect()`: Retrieves the aspect settings for seen lines.
   - `drawer.EnableDrawHiddenLine()`: Enables drawing of hidden lines.
   - `line_aspect.SetWidth(4)`: Sets the width of seen lines to 4 units.
   - `drawer.SetWireAspect(line_aspect)`: Applies the line aspect settings to wireframe aspects.

4. **Shape Creation and Display:**
   - `s = BRepPrimAPI_MakeCylinder(50.0, 50.0).Shape()`: Creates a cylinder with a radius and height of 50 units.
   - `display.DisplayShape(s)`: Displays the created cylinder shape in the window.

5. **Display Settings and Loop:**
   - `display.View_Iso()`: Sets the view to an isometric perspective.
   - `display.FitAll()`: Adjusts the view to fit all displayed shapes within the window.
   - `start_display()`: Starts the display loop, allowing the window to remain open and interactive.

### Summary:
The script demonstrates how to create a cylinder and adjust its display properties, such as line width and hidden line visibility, using the `pythonOCC` library. It sets up the display, modifies the visual attributes, creates the cylinder, and then starts an interactive display loop. This example is useful for understanding how to control the quality and appearance of 3D shapes in a `pythonOCC` application.

## core_geometry_axis.py

This Python script is designed to work with the `pythonOCC` library, which is a set of Python bindings for the Open CASCADE Technology (OCCT) CAD kernel. The script demonstrates how to create and manipulate 3D geometric entities and display them using a simple graphical user interface.

Here is a breakdown of the script's functionality:

1. **Imports and Initialization**:
    - The script imports necessary modules, including `sys` and specific classes from `OCC.Core.gp` for geometric operations (`gp_Pnt`, `gp_Dir`, `gp_Ax3`).
    - It also imports the `init_display` function from `OCC.Display.SimpleGui` to initialize the display window and related functions.

2. **Display Initialization**:
    - `init_display()` is called to set up the display environment. This function returns several objects (`display`, `start_display`, `add_menu`, `add_function_to_menu`) for managing the display window and adding functionalities.

3. **`axis` Function**:
    - The `axis` function creates two 3D points (`gp_Pnt`) and a direction vector (`gp_Dir`).
    - It uses these points and direction to create two 3D coordinate systems (`gp_Ax3`).
    - The function then checks and prints whether these coordinate systems are "direct" (right-handed) or not.
    - It displays the points in the graphical window and adds labels "P1" and "P2" to them.

4. **`exit` Function**:
    - A simple function to exit the program using `sys.exit()`.

5. **Main Execution**:
    - If the script is executed as the main program, it calls the `axis` function to perform the geometric operations and display them.
    - `start_display()` is called to start the graphical user interface and render the display window.

In summary, the script demonstrates the creation and manipulation of 3D geometric entities and displays them using the `pythonOCC` library's graphical interface. It provides a basic example of how to work with 3D points, directions, and coordinate systems, and how to visualize them in a simple GUI.

## core_display_clip_planes.py

This Python script is designed to work with the `pythonOCC` library, which is a set of Python bindings for the Open CASCADE Technology (OCCT) 3D modeling library. The script performs the following functions:

1. **Imports Required Libraries and Modules:**
   - It imports various modules from `OCC.Core` for geometric operations, graphical display, color management, and BREP (Boundary Representation) tools.
   - It also imports the `init_display` function from `OCC.Display.SimpleGui` to set up the graphical display.

2. **Initializes the Display:**
   - The `init_display` function is called to initialize the display window and related functions (`display`, `start_display`, `add_menu`, and `add_function_to_menu`).

3. **Loads a 3D Model:**
   - A `TopoDS_Shape` object named `cylinder_head` is created.
   - A `BRep_Builder` object is used to read a BREP file (`cylinder_head.brep`) and store the shape in `cylinder_head`.
   - The shape is then displayed using `display.DisplayShape`.

4. **Sets Up a Clipping Plane:**
   - A `Graphic3d_ClipPlane` object named `clip_plane_1` is created.
   - The clipping plane is configured to enable capping and capping hatch.
   - The clipping plane is initially set to be off.
   - The clipping plane's material color is set to a specific RGB color (0.5, 0.6, 0.7).
   - The clipping plane is added to the displayed shape (`ais_shp`).

5. **Defines Functions for User Interaction:**
   - `enable_clip_plane`: Enables the clipping plane and updates the viewer.
   - `disable_clip_plane`: Disables the clipping plane and updates the viewer.
   - `animate_translate_clip_plane`: Animates the translation of the clipping plane along the Z-axis.
   - `exit`: Exits the application.

6. **Sets Up the User Interface:**
   - A menu named "clip plane" is added to the display.
   - Functions for enabling, disabling, and animating the clipping plane are added to the menu.
   - The display is fitted to show all objects, and the display loop is started.

**Purpose and Functionality:**
The script's primary purpose is to demonstrate the use of a clipping plane in a 3D model visualization using the `pythonOCC` library. It allows the user to interactively enable, disable, and animate a clipping plane on a loaded 3D model (in this case, a cylinder head). The clipping plane can be used to view cross-sections of the model for better inspection and analysis.

## core_mesh_data_source_numpy_stl.py

This Python code is designed to load and visualize a 3D model from an STL (Stereolithography) file using the `numpy-stl` library and the `pythonOCC` library, which is a set of Python bindings for the Open CASCADE Technology (OCCT), a software development platform for 3D CAD, CAM, CAE.

Here is a step-by-step breakdown of its functionality:

1. **Imports**:
   - Standard library `os` for file path manipulation.
   - `MeshDS_DataSource` and `MeshVS` from `OCC.Core` for handling mesh data.
   - `init_display` from `OCC.Display.SimpleGui` for initializing the display.
   - `numpy` for numerical operations.
   - `stl` from `numpy-stl` for reading STL files.

2. **Load STL File**:
   - The STL file named "fan.stl" is located in a relative path (`../assets/models/fan.stl`).
   - The `numpy-stl` library is used to load the STL file into a mesh object (`stl_mesh`).
   - The vertices of the mesh are extracted and reshaped into a 2D array where each row represents a vertex.

3. **Generate Faces**:
   - Faces of the mesh are created by grouping vertices into sets of three (triangles). This is done using a list comprehension and `numpy` array operations.

4. **Create Mesh Data Source**:
   - A `MeshDS_DataSource` object is created using the vertices and faces arrays.
   - A `MeshVS_Mesh` object (`a_mesh_prs`) is created to represent the mesh.
   - A `MeshVS_MeshPrsBuilder` object (`a_builder`) is created and associated with the mesh to build its presentation.

5. **Display Initialization and Visualization**:
   - The display is initialized using `init_display()`.
   - The mesh presentation (`a_mesh_prs`) is displayed in the context.
   - The display is fitted to show the entire mesh.
   - The `start_display()` function is called to start the interactive display loop.

In summary, this code loads a 3D model from an STL file, constructs a mesh data structure from the vertices and faces, and then visualizes the mesh using the `pythonOCC` library's display capabilities.

## core_layer_mgmt.py

This Python code uses the `pythonOCC` library, which is a set of Python bindings for the Open CASCADE Technology (OCCT), a software development platform for 3D CAD, CAM, CAE, etc. The code creates and manipulates several 3D box shapes, organizes them into layers, and displays them in a graphical window. Here is a breakdown of its functionality:

1. **Initialization:**
   - The script starts by importing necessary modules from the `pythonOCC` library.
   - It initializes the display window and related functions using `init_display()`.

2. **Creating Box Shapes:**
   - Six box shapes (`box1` to `box6`) are created using `BRepPrimAPI_MakeBox` with different dimensions and positions:
     - `box1`: Positioned at `(0, 0, 10)` with dimensions `10x10x100`.
     - `box2`: Positioned at the origin `(0, 0, 0)` with dimensions `100x10x10`.
     - `box3`: Positioned at the origin with dimensions `10x100x10`.
     - `box4`: Positioned at `(100, 100, 0)` with dimensions `10x10x100`.
     - `box5`: Positioned at `(0, 100, 0)` with dimensions `100x10x10`.
     - `box6`: Positioned at `(100, 0, 0)` with dimensions `10x100x10`.

3. **Transformation:**
   - A translation transformation `trns` is defined to move objects along the Z-axis by `110` units using `gp_Trsf` and `gp_Vec`.

4. **Layer Management:**
   - Three layers (`layer1`, `layer2`, and `layer3`) are created to organize the shapes.
     - `layer1`: Contains `box1` and is assigned a color `123`.
     - `layer2`: Contains `box4` and `box5`, assigned color `86` and transparency `0.6`.
     - `layer3`: Contains `box2`, `box3`, and `box6`, assigned color `76`.
   - `layer3` is merged with `layer1`, including the shapes from `layer1`.

5. **Displaying Layers:**
   - `layer2` and `layer3` are explicitly shown.
   - Shapes from `layer3` are retrieved and translated using the defined transformation `trns`, then added to a new `layer4` with color `32`.
   - `layer4` is shown.

6. **Final Display:**
   - The display is adjusted to fit all shapes using `display.FitAll()`.
   - The graphical display is started with `start_display()`.

In summary, this code demonstrates the creation and manipulation of 3D box shapes, the use of layers to organize these shapes, and the application of transformations to visualize the final arrangement in a 3D graphical window using the `pythonOCC` library.

