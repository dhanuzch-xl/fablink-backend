# Project: Interactive 3D STL Viewer with Hole Detection

## Overview
This project allows you to view a 3D metal plate with holes and interactively display information such as hole diameter and depth when hovering over them. The project consists of two parts:
1. **Python Preprocessing**: This preprocesses the STEP file to recognize holes and calculates their properties (e.g., diameter, depth).
2. **Web Visualization**: The 3D model is rendered in a web browser using Three.js, and hole information is displayed when the user hovers over the holes.

## Project Structure
- `models/`: Contains the STEP file `Plate_1.step`.
- `output/`: Stores the JSON file `hole_data.json` containing the preprocessed hole information.
- `renderer/`: Contains the custom renderer script (if needed).
- `app/`: Contains the web viewer files (`index.html`, `main.js`, and `style.css`).
- `scripts/`: Contains the Python preprocessing script `preprocess.py`.

## Requirements

### Python Environment
- `pythonocc-core`
- `json`

-------------------------------------------------------------------------------------

### Recap:
1. **Frontend (index.html and style.css)**:
   - The **layout** displays the CAD viewer and the hole data side by side using a flexbox.
   - The hole data is dynamically populated with dropdowns based on diameter.
   - The **slider** and **file upload** elements are integrated to adjust hole sizes and load files.
   - A **tooltip** is displayed near the mouse for highlighting holes.
   
2. **Backend (server.py)**:
   - The Flask server processes file uploads (STEP/STL files).
   - It converts STEP files to STL and extracts hole data from the STEP file.
   - The system recognizes cylindrical holes, calculates their positions, diameters, and depths, and returns this data to the frontend.
   - There is also an endpoint to modify the hole size in the backend.

3. **Main.js**:
   - This handles interactions with the 3D viewer, raycasting to find intersections with holes, and displaying the hole data in the dropdown.
   - There's functionality for raycasting, visualizing the raycaster, and tooltips for hole information.
   - The hole data can be edited using the dropdown and updated in the backend via an API.

### Next Steps:
Now that we have a stable foundation, let's focus on adding more advanced features to improve the usability of the web-based CAD editor.

### Suggested Features to Add:
1. **Hole Selection and Highlighting**:
   - When the user hovers over a hole in the 3D model, highlight that hole in the model and in the hole data dropdown.
   - Allow clicking a hole in the 3D viewer to lock the selection.

2. **Editing Hole Properties**:
   - Add the ability to edit the diameter directly in the dropdown list or from the tooltip when hovering over a hole.
   - Update the CAD model in real-time when the hole's properties are changed.

3. **Zoom and Focus on Selected Hole**:
   - When a hole is selected (via click or hover), zoom in or pan the view to focus on the hole.

4. **Undo/Redo System**:
   - Implement a simple undo/redo system to allow users to revert changes to hole properties.

5. **Export Updated CAD**:
   - Add functionality to export the updated STEP/STL file with modified hole properties after the user edits the hole sizes.

### Proposed Approach:
#### Feature 1: Hole Selection and Highlighting
- **Frontend (main.js)**:
  - Use raycasting to detect which hole is hovered over.
  - Add functionality to highlight the hole in both the CAD viewer and the hole data dropdown when hovering.
  - When a hole is clicked, lock the selection until another hole is selected.

#### Feature 2: Editing Hole Properties
- **Frontend (main.js)**:
  - Add an input field next to each hole in the dropdown for editing the diameter.
  - Update the backend in real-time when the user changes the diameter, then refresh the 3D viewer to reflect the changes.

#### Feature 3: Zoom and Focus on Selected Hole
- **Frontend (main.js)**:
  - When a hole is clicked, adjust the camera position to zoom in or pan to the hole.
  - Use `camera.position` and `controls.target` to focus on the hole's position in the 3D space.

#### Feature 4: Undo/Redo System
- **Frontend**:
  - Maintain a history of hole property changes (diameter, position, etc.).
  - Add "Undo" and "Redo" buttons that allow navigating through the history stack to revert changes.

#### Feature 5: Export Updated CAD
- **Backend (server.py)**:
  - Implement an endpoint to export the modified STEP/STL file with updated hole properties.
  - Add a "Download" button in the frontend to allow the user to export the file after modifications.

Would you like to start by focusing on a specific feature from the list above, or would you prefer I go ahead and implement the features step-by-step? Let me know!