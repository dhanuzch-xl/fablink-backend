TODO:
flaten the goemetry - Note that step files vertical axis could be Y or Z axis.
inverse stud.
painting operation.
factory report update.
welding and folding specifications.
If the file is already an STL file, it’s directly returned without hole extraction. Have to change it.
Need to check for non circular holes.
Keep in mind that corrdinates of both the edges are necessary for operations to work.
scaling factor variable used to map holes and rendering should be global setting.

Add Loading Indicators:
    On the frontend, add visual cues like spinners or progress bars while files are uploading or being processed.



### main.js 

primarily a 3D scene rendering and interaction system built using **Three.js** with functionalities to manipulate and edit 3D models:

### 1. **Three.js Scene Initialization and Setup**
   - **Scene Creation**: A Three.js scene is created where the CAD model (plate with holes and edges) is rendered.
   - **Renderer**: A WebGL renderer is initialized and attached to a container element with dimensions that match the HTML container.
   - **Camera**: A perspective camera is set up to view the 3D scene, with default positioning and aspect ratio adjusted to fit the container.
   - **Lighting**: Both directional and ambient lights are added to the scene for proper lighting of 3D objects.
   - **Axes Helper**: A visual helper (axes) is added for debugging purposes.

### 2. **User Controls**
   - **OrbitControls**: Users can interact with the 3D model using mouse movements and zoom using Three.js OrbitControls, allowing rotation, zoom, and panning.

### 3. **Raycasting for User Interaction**
   - **Mouse Hover & Click Detection**: Raycasting is used to detect when the user's mouse hovers over or clicks on specific objects in the 3D scene (such as holes and edges). This enables highlighting and selecting specific elements.
   - **Raycasting Visualization**: There is a helper function (`visualizeRaycasting()`) to display the ray direction for debugging purposes.

### 4. **3D Model Loading and File Uploads**
   - **File Input Handling**: The code handles file inputs for uploading CAD models (STEP/STL files). The uploaded file is sent to a Flask backend via an API (`/api/upload_file`), which returns the STL URL and hole/edge data for rendering.
   - **STL Loading**: After uploading, the STL model is loaded and rendered in the scene using Three.js STLLoader.
   - **Stud Placement**: Users can upload a STEP file for a stud. The backend converts it to an STL file, which is then placed in a preselected hole in the model.
   - **Model Reloading**: When the model is updated (e.g., hole diameter change), the modified STL is loaded into the scene, replacing the previous version.

### 5. **Hole Detection and Editing**
   - **Hole Detection**: The system detects holes in the model using raycasting and provides information about the closest hole, such as its position and diameter. This data is shown in a tooltip or dropdown menu.
   - **Hole Diameter Editing**: Users can edit the diameter of selected holes. Upon editing, the change is sent to the backend via an API (`/api/change_hole_size`) to update the 3D model in real-time. The new model is reloaded and rendered.
   - **Highlighting Holes**: A hole is visually highlighted when hovered or clicked. Highlighting is applied using a small sphere drawn around the hole in the 3D model.

### 6. **Edge Detection and Manipulation**
   - **Edge Highlighting**: Similar to holes, edges are detected using raycasting. When an edge is hovered, it is highlighted with a different color and visual offset.
   - **Edge Selection and Locking**: Edges can be selected and locked when clicked (with support for multi-select using Ctrl key). Two edges can be selected simultaneously for weld or fold operations.
   - **Edge Visualization**: Edges extracted from the backend are rendered in the scene as lines, with a corresponding Three.js LineSegments object.

### 7. **Job Management for Undo Operations**
   - **Job Tracking**: Every action (such as placing a stud, editing a hole diameter, or manipulating edges) is tracked as a "job" in the `jobs` array. Each job includes its type (`stud`, `weld`, `Edithole`), the data involved, and an optional description.
   - **Undo Functionality**: Each job added to the list has an "Undo" button, allowing users to revert actions. For example:
     - For stud placement, `removeStudFromHole()` is called to remove the placed stud.
     - Placeholder functions exist for edge and hole edit undo operations.
   - **Job UI**: Jobs are displayed in a list (HTML `jobs-list`), and each job has a button to trigger undo operations, with corresponding DOM manipulation to remove the job entry.

### 8. **Tooltip and Hole Info Display**
   - **Tooltip**: A dynamic tooltip shows hole information (diameter, position) when hovering over a hole.
   - **Hole Info**: Detailed hole data is shown in a separate section (`hole-data`) and dynamically updates based on the current selection.

### 9. **Weld and Fold Operations**
   - **Edge Operations**: When two edges are selected, the user can perform weld or fold operations, which are tracked in the job system. Currently, these operations are placeholders with logged outputs, but they can be expanded to include specific edge manipulation logic.

### 10. **Window Resizing Support**
   - **Responsive Rendering**: The camera and renderer are updated on window resize to ensure that the scene always fits the current browser window dimensions.

### 11. **Additional Features**
   - **Dropdown Menu for Holes**: Holes are categorized by diameter, and dropdown menus allow users to navigate through holes.
   - **Edge Highlight Toggle**: Selected edges can be highlighted and toggled (deselected) with visual feedback to the user.
   - **Plate Scaling**: The plate (main object in the scene) can be scaled, and the scaling factor is considered when positioning objects like holes and studs.

### Summary of Features:
- **3D Scene Rendering**: Full 3D rendering with object manipulation, highlighting, and interaction.
- **Model Loading**: Ability to load STL files, display holes and edges, and modify them.
- **Hole Editing**: Users can change hole diameters and view hole data in real-time.
- **Stud Placement**: Upload a stud file and place it within a selected hole.
- **Undo Feature**: A job-based undo system for reversing stud placement, hole edits, and edge operations.
- **User Controls**: OrbitControls for smooth camera navigation and raycasting for user interaction with the model.
- **Edge Operations**: Select, highlight, and manage edges with options for future weld and fold operations.



### server.py:

This code implements a Flask-based server with various routes to handle file uploads, 3D model manipulations, and hole recognition. It also includes utilities for working with STEP and STL files, manipulating holes in 3D models, and serving modified files. Below is a breakdown of the features:

### 1. **Basic Flask Setup**:
   - **Flask Application**: The code uses Flask to build a server, with routes to handle file uploads and serve files (HTML, JS, and 3D model files).
   - **Static File Handling**: 
     - `send_from_directory()` serves static files like HTML, JS, and CSS from the `static` directory.
     - Routes like `/static/<path:path>` and `/output/<path:filename>` allow serving files from the `static` and `output` directories.

### 2. **File Handling and Uploads**:
   - **File Upload Handling**: 
     - `upload_file()` route allows users to upload files, checks the file type, and stores the file in the `output` directory.
     - The function accepts STEP (`.step`, `.stp`) and STL (`.stl`) files.
     - Uploaded files are securely saved with a unique filename generated using `uuid`.
   
### 3. **STEP to STL Conversion**:
   - **Automatic Conversion**: 
     - If a STEP file is uploaded, it is converted to an STL file using `write_stl_file()`. The file is saved and served as output via the `/output` route.
   - **STEP to STL API**: 
     - A separate API endpoint `/convert_step_to_stl/<filename>` also allows converting a specific STEP file to STL by its filename.
   
### 4. **Recognizing Holes in 3D Models**:
   - **Hole Recognition**:
     - `recognize_hole_faces(step_file)` reads a STEP file and extracts faces, checking if they represent holes using the `recognize_face()` function.
     - Holes are identified by checking for cylindrical surfaces and calculating their positions, diameters, depths, and axes.
     - The hole data is returned as JSON.
   
### 5. **Handling Stud Uploads and Placement**:
   - **Stud File Handling**:
     - The `/api/upload_stud` route allows uploading a file for a stud, converts it from STEP to STL, and saves it in the `output` directory.
   - **Stud Placement**:
     - The API processes the uploaded STEP file, converts it to an STL, and returns the URL to the STL file for further use.

### 6. **Edge Recognition**:
   - **Edge Data Extraction**:
     - When a STEP file is uploaded, edges are extracted using the `get_edges()` function (presumably implemented in `utils.find_edges`), and each edge is converted to a dictionary format using `edge_to_dict()`.
     - Both edge and hole data are returned as part of the file processing response.

### 7. **Hole Modification**:
   - **Changing Hole Size**:
     - The `/api/change_hole_size` route modifies the size of a hole in a STEP file.
     - It dynamically reads a STEP file, performs a boolean cut with a new cylinder (representing the new hole size), and saves the modified STEP file.
     - The modified STEP file is converted to STL, and both files are returned as downloadable links.
   
### 8. **3D Geometry Manipulation**:
   - **Cylinder Creation**: 
     - The code uses `gp_Ax2`, `gp_Pnt`, and `gp_Dir` from the Open CASCADE library to define axis and direction for 3D geometric manipulations.
   - **Boolean Cut Operations**: 
     - `BRepAlgoAPI_Cut` is used to perform boolean operations, specifically cutting a new cylinder (hole) from a shape.
   - **Bounding Box Calculations**: 
     - `Bnd_Box` is used to compute bounding boxes to help determine the depth of cylindrical holes.

### 9. **STEP and STL Utilities**:
   - **File Operations**:
     - The Open CASCADE utilities (`read_step_file()`, `write_stl_file()`, `write_step_file()`) are used for reading and writing 3D STEP and STL files.
     - `read_step_file_with_names_colors()` extracts both geometry and metadata (names, colors, and shapes) from a STEP file.

### 10. **Error Handling**:
   - **File Type Validation**: 
     - `allowed_file()` checks the file extension before processing the uploaded files to ensure they are STEP or STL files.
   - **Error Responses**: 
     - If a file is missing, invalid, or unsupported, the server returns appropriate JSON error messages (e.g., `{"error": "No file part"}` or `{"error": "File type not allowed"}`).

### 11. **Application Startup**:
   - **Directory Creation**:
     - The application ensures that the necessary directories (`models` and `output`) are created when the server starts if they don't already exist.
   - **Flask Debug Mode**:
     - The server is set to run in debug mode on host `0.0.0.0` and port `5000`, making it accessible on the local network.

### Key Libraries Used:
- **Flask**: Web framework for handling HTTP requests, serving static files, and JSON responses.
- **Open CASCADE (OCC)**: Core library for 3D modeling operations, including STEP file reading, shape manipulation, and geometry extraction.
- **Werkzeug**: Utility library for secure file handling.
- **UUID**: Used to generate unique filenames for uploaded files.

### Summary of Features:
1. **File Uploads and Handling** for STEP and STL files.
2. **STEP to STL Conversion**.
3. **3D Model Manipulation** including extracting holes and edges from STEP files.
4. **Stud Upload and Placement** with STEP to STL conversion.
5. **Hole Modification** by changing the size of holes in a STEP model and saving the modified file.
6. **Boolean Operations** for cutting and modifying 3D shapes.
7. **Edge and Hole Extraction** for detecting geometric features in STEP files.
8. **Serving Static Files and 3D Models** via Flask endpoints.
9. **Error Handling** and validation for uploads and model manipulation.
