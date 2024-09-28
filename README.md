TODO:
Need undo facility. Create list of operations and when the tile of operation is closed that should undo the change in stl file.
have to clean imports in server.py
f the file is already an STL file, it’s directly returned without hole extraction. Have to change it.
Need to check for non circular holes.
Need to write code for welding line identification.
scaling factor variable used to map holes and rendering should be global setting.


Suggested Next Steps:

    Integrate Slider Functionality:
        Make sure the hole size slider sends values to the backend API and dynamically updates the 3D model in real time.

    Unify Hole Recognition Logic:
        Consider combining the preprocessing logic from preprocess.py with the API calls in server.py to avoid redundancy and make the system more robust.

    Improve Error Handling:
        Add more detailed error handling on both the frontend and backend to improve user experience and feedback during processing failures.

    Add Loading Indicators:
        On the frontend, add visual cues like spinners or progress bars while files are uploading or being processed.





### Key Features:

1. **3D Scene Rendering with Three.js**:
   - The code creates a 3D scene using the `THREE.Scene` object and renders it within a container element using `THREE.WebGLRenderer`.
   - A perspective camera (`THREE.PerspectiveCamera`) is used to view the scene.

2. **Orbit Controls for Camera Interaction**:
   - `THREE.OrbitControls` allows the user to interact with the camera, enabling smooth panning, zooming, and rotation of the scene.
   - Damping and constraints are applied to prevent excessive movement.

3. **Lighting Setup**:
   - The scene includes directional lighting (`THREE.DirectionalLight`) and ambient lighting (`THREE.AmbientLight`).
   - This ensures proper illumination of 3D objects.

4. **Axes Helper for Debugging**:
   - An axes helper (`THREE.AxesHelper`) is added to visualize the axes in the scene, helping to orient objects during development.

5. **File Upload and Parsing**:
   - The system includes a file input handler (`uploadAndLoadFile` function) that allows users to upload files (like 3D models).
   - The uploaded file is sent to the server, which processes and returns the STL model.

6. **STL Model Loading**:
   - STL files are loaded into the scene using `THREE.STLLoader`.
   - The loaded 3D models are rendered as `THREE.Mesh` objects with custom materials.

7. **Mouse Interactions and Raycasting**:
   - The system listens to mouse movements and uses a `THREE.Raycaster` to detect interactions between the mouse and 3D objects (such as the plate).
   - The raycaster detects intersections with objects for real-time feedback and interaction.

8. **Hole Data Management**:
   - The code manages holes in the model using an array `holes`, which stores information about the holes in the 3D model.
   - Holes are categorized by diameter and displayed dynamically in the UI.

9. **Hole Diameter Editing**:
   - A user can edit the diameter of a hole by selecting it and providing a new value via a prompt.
   - The updated hole diameter is reflected both locally and in the 3D model, with changes sent to the backend for further processing.

10. **Hole Highlighting**:
    - The code highlights holes in the 3D model using `highlightHoleInModel`, where a yellow sphere is used to indicate the selected hole.
    - Corresponding dropdown items in the UI are highlighted when a hole is selected.

11. **Raycast Visualization** (Optional):
    - There is a commented-out feature (`visualizeRaycasting`) to visualize the raycast direction, which could be used for debugging purposes.

12. **Dynamic Model Reloading**:
    - When a hole's size is modified, the STL model is reloaded with updated dimensions using `reloadModifiedModel`.

13. **Responsive Design**:
    - The renderer and camera adjust automatically to the size of the container element, making the 3D scene responsive to window resizing.

14. **Real-Time Stud Insertion**:
    - A user can upload a STEP file for a stud, which is processed and inserted into a selected hole.
    - The stud is scaled and aligned according to the hole's position and axis, providing accurate placement.

15. **Categorized Hole Data Display**:
    - Hole data is displayed in the UI, categorized by diameter, making it easy to view and interact with holes of different sizes.
   
These features combine to create an interactive, 3D model visualization and editing system, primarily focused on manipulating hole geometries within STL models and supporting dynamic model updates.