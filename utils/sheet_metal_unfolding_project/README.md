
To run
python src/main.py '/home/dhanuzch/meher-web-view/models/WP-13.step' -t 2

### **Project Directory Structure:**

```
/sheet_metal_unfolding_project
│
├── /src                        # Main source code folder
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # Main application entry point
│   ├── file_loader.py           # STEP file loading and geometry extraction
│   ├── sheet_tree.py            # Tree structure and node management
│   ├── face_operations.py       # Face extraction, transformation logic (rotation/translation)
│   ├── bend_analysis.py         # Bend detection and unfolding logic
│   ├── export_handler.py        # Unfolded face exporting (STEP/DXF)
│   └── utils.py                 # Utility functions (e.g., logging, helper functions)
│
├── /tests                      # Folder for unit tests
│   ├── test_file_loader.py      # Tests for STEP file loading and face extraction
│   ├── test_sheet_tree.py       # Tests for tree structure and node creation
│   ├── test_face_operations.py  # Tests for face transformations (rotation/translation)
│   ├── test_bend_analysis.py    # Tests for bend detection and unfolding logic
│   ├── test_export_handler.py   # Tests for exporting unfolded parts
│
├── /data                       # Sample STEP/DXF files for testing
│   ├── example_1.step           # Example STEP file for testing unfolding
│   ├── example_2.step           # Another test file for complex shapes
│
├── /scripts                    # Folder for helper scripts
│   ├── run_tests.sh             # Script to run all tests
│   ├── run_unfold_example.py    # Script to run a sample unfolding operation
│
├── README.md                   # Project documentation
├── requirements.txt            # Dependencies (PythonOCC, pytest, etc.)
└── .gitignore                  # Git ignore file for version control
```

### **Explanation of Each Folder:**

1. **/src (Source Code)**:
   - **main.py**: The main script to run the unfolding workflow. You can start by developing functions incrementally and call them here.
   - **file_loader.py**: Responsible for loading the STEP file and extracting geometric information (e.g., faces, edges).
   - **sheet_tree.py**: Manages the tree structure (`SheetTree` class) and node operations. This will handle the recursive traversal and face processing.
   - **face_operations.py**: Contains functions to perform face transformations (rotations, translations) and geometric calculations.
   - **bend_analysis.py**: Contains the logic for detecting bends, calculating bend angles, and applying unfolding transformations.
   - **export_handler.py**: Responsible for exporting the final unfolded shapes into different formats (STEP, DXF).
   - **utils.py**: A helper module that can contain logging functions, utility classes, or common functionality used across the project.

2. **/tests (Unit Tests)**:
   - Each module in `/src` should have corresponding unit tests. For example, `test_file_loader.py` tests the functionality of the STEP file loading, `test_sheet_tree.py` verifies that the tree structure is built correctly, etc.
   - This ensures that each part is working independently before being integrated into the larger system.

3. **/data (Test Files)**:
   - Store sample CAD files (e.g., `.step`, `.iges`) that will be used for testing your unfolding functions.
   - Start with simple files and add more complex ones as your project progresses.

4. **/scripts (Helper Scripts)**:
   - **run_tests.sh**: A script to execute all the tests using `pytest` or another testing framework. You can use this to quickly verify that everything is working.
   - **run_unfold_example.py**: This script could run a specific example using the source code to test the overall functionality (loading, unfolding, exporting).

5. **README.md**:
   - Document the project, explaining the purpose, how to run the code, and any setup instructions.
   - Include details for testing and contributing to the project.

6. **requirements.txt**:
   - List all the dependencies (e.g., PythonOCC, pytest, numpy, etc.) required to run the project.

7. **.gitignore**:
   - If you're using Git, this file will ensure that irrelevant files (e.g., temporary files, build artifacts) are not committed to version control.

---

### **Development and Integration Plan:**

1. **Initial Development:**
   - Start by building the **file_loader.py** module to load and extract faces from the STEP files.
   - Develop basic tests in `/tests/test_file_loader.py` to verify that the faces are extracted correctly.
   
2. **Tree Structure and Face Operations:**
   - Implement **sheet_tree.py** to manage the tree structure of faces and handle unfolding logic.
   - Develop tests for building the tree and verifying the correctness of the structure.

3. **Bend Analysis and Transformation:**
   - Implement **bend_analysis.py** to detect bends, calculate bending angles, and apply transformations.
   - Write tests to verify that the bends are correctly identified and unfolded.

4. **Exporting Unfolded Geometry:**
   - Implement **export_handler.py** to export the unfolded geometry in formats like STEP or DXF.
   - Develop tests for export functionality.

5. **Full Integration:**
   - In the **main.py** file, call the functions from the other modules to create a full workflow:
     - Load a STEP file.
     - Build the face tree.
     - Perform bend analysis and transformations.
     - Export the unfolded part.
   - Run integration tests using **/scripts/run_unfold_example.py** to test the end-to-end process.



Refactoring plan

### **Refactoring and Test Planning:**

Given the current code structure and your project goals, we can refactor and integrate the functionality across all modules efficiently while preparing for comprehensive tests. Here's an analysis and a step-by-step integration plan based on the files you have provided:

---

### **1. Refactor `sheet_tree.py` to integrate with `bend_analysis.py` and `face_operations.py`:**

**Current Code**:
- The `sheet_tree.py` is responsible for building the tree structure of faces and managing the relationships between connected faces.
- `face_operations.py` provides methods for transforming and extracting faces.
- `bend_analysis.py` detects bends and calculates bend angles.

**Changes**:
- Use the `BendNode` from `face_operations.py` across the project for consistent node representation.
- Call the `detect_bends()` function from `bend_analysis.py` after the tree is constructed to ensure bend detection is uniform across the project.
- Calculate bend angles for the tree's connected nodes using `calculate_bend_angle()`.

**Refactor Plan**:
1. **Import necessary modules**:
    - From `bend_analysis.py`: `detect_bends()` and `calculate_bend_angle()`.
    - From `face_operations.py`: `extract_faces()` and other utility functions.

2. **Build tree and perform bend analysis**:
    - After constructing the face hierarchy in `sheet_tree.py`, call `detect_bends()` to identify all bends.
    - For every identified bend, calculate the bend angle and attach it to the respective nodes.

---

### **2. Refactor `bend_analysis.py` to work with `sheet_tree.py`:**

**Current Code**:
- The `BendNode` is defined here, but we need to centralize it in one place (perhaps in `face_operations.py`).
- The core logic of detecting bends is correct but needs to be integrated with the tree structure.

**Refactor Plan**:
1. **Centralize `BendNode`**: Move `BendNode` to `face_operations.py` to avoid code duplication.
2. **Enhance `detect_bends()`**:
    - When `detect_bends()` is called in `sheet_tree.py`, pass the tree’s faces and detect all bends between connected faces.

---

### **3. Refactor `face_operations.py`**:

**Current Code**:
- The core functionality for extracting faces, performing transformations, and analyzing surfaces is well defined.

**Refactor Plan**:
1. **Move `BendNode` here**: As mentioned earlier, centralize the `BendNode` class here.
2. **Enhance modularity**:
    - Ensure that functions like `extract_faces()` are used in `sheet_tree.py` and are also independently testable.

---

### **4. Ensure `file_loader.py` loads STEP files properly**:

**Current Code**:
- The `load_step_file()` function reads a STEP file and returns a `TopoDS_Shape`. This is used in the workflow's entry point (`main.py`).

**Refactor Plan**:
1. **No major changes needed**: This file is performing its task well. Just ensure that the tests in `test_file_loader.py` validate its functionality effectively.

---

### **5. Full Workflow in `main.py`**:

**Current Code**:
- The `process_unfold()` function is the workflow’s main entry point, where STEP files are processed, unfolded, and exported.

**Refactor Plan**:
1. **Unfolding workflow**:
    - Ensure the `sheet_tree.py` builds the tree, performs the bend analysis, and manages relationships between the faces.
    - Use the results from the bend analysis to generate the unfolded shape and export it.

---

### **6. Write Comprehensive Tests**:

Now that the core functionality has been refactored, write unit and integration tests across all modules:

#### **Unit Tests**:
1. **Test `file_loader.py`**:
    - Verify that `load_step_file()` correctly loads STEP files.

2. **Test `face_operations.py`**:
    - Test face extraction, transformations (rotation and translation), and thickness filtering independently.

3. **Test `bend_analysis.py`**:
    - Test `detect_bends()` and `calculate_bend_angle()` using mock faces.

4. **Test `sheet_tree.py`**:
    - Test tree creation and parent-child relationships between faces.
    - Verify that bends are detected and properly linked to nodes.

#### **Integration Tests**:
1. **Full Workflow**:
    - Simulate the full process: Load a STEP file, build the tree, detect bends, calculate angles, unfold, and export.

2. **Use Sample Files**:
    - Use the provided STEP files (e.g., `example_1.step`) to validate the entire workflow.

---

### **Conclusion**:

By integrating the existing functionality and properly refactoring the code across modules, we ensure that the development stays modular, maintainable, and testable. Now, you can move forward with writing the tests as outlined, ensuring that the entire sheet metal unfolding process is well-validated.


In the provided reference code, the following key steps are involved in the **bend analysis**:

1. **Bend Detection Logic:**
   - The reference code uses a node-based approach to handle faces and bends.
   - It uses `Simple_node` objects for representing each face and its bend characteristics.
   - The code relies on detecting "counter-faces" by comparing distances between faces and checking their relative positions and angles.
   - It calculates the **bend angle** and **k-factor** based on face geometry and material properties like thickness.

2. **Counter-Face Calculation:**
   - Faces are compared using their middle points (centroids) to find adjacent or counter faces.
   - If the distance between face centroids is within a certain tolerance (based on thickness), the faces are considered to be adjacent, forming a bend.
   - Counter-face detection is crucial to identifying which faces are part of the same bend.

3. **Bend Direction and K-Factor:**
   - The bend direction (up or down) is determined based on the surface curvature or face orientation.
   - The K-factor is calculated based on the bend angle and material thickness, which helps determine the correct unfolding transformation.
   - The K-factor also influences the translation length during the unfolding process.

4. **Unfolding Faces:**
   - Each bend node calculates its transformation (rotation, translation) relative to its parent node.
   - Unfolding transforms bend nodes into flat faces by applying these transformations recursively.

### Bend Analysis
Enhance the Bend Detection:

    Refine the detection logic to include surface type checks and not rely solely on proximity and thickness. Add functionality to handle edge properties, particularly for more complex bends like those involving cylindrical faces.
    Implement checks for sheet edges and manage nodes accordingly.

Integrate with the Node-Based Structure:

    Introduce a class-based structure, similar to Simple_node in the reference code, to track nodes (bends) and their relationships (children, parents, edges). This will allow you to process more complex unfolding scenarios, where multiple bends are involved.

Unfolding Transformation Enhancements:

    Improve the unfold_bend function to incorporate both rotations and translations, ensuring that the faces maintain correct relative positioning after unfolding.

Include Advanced Features:

    Implement features like k-factor adjustment, handling of edge cases (e.g., seams, welded edges), and edge splitting during unfolding, similar to the reference implementation.

Key Insights from Source Code:

    Error Handling and Validations:
        The source code has a comprehensive set of error codes and conditions, especially around thickness measurement, edge detection, and bend analysis. We need to ensure our system handles all potential issues (e.g., invalid shapes, incorrect thickness) before proceeding with bend detection and unfolding.

    Detailed Bend Node Structure:
        The source uses a Simple_node structure, which encapsulates various properties about the bend, such as axis, radius, vertex dictionary, tangent vector, and translation length. These are essential for accurate transformation and unfolding.
        Our current BendNode structure might need enhancements to capture all these properties. Specifically, we need to ensure we track the axis, bend center, tangent vectors, and translations as described in the source.

    Counter Faces and Thickness Validation:
        In the source, the thickness is validated by comparing faces that are opposite each other in the sheet metal. Our current approach doesn’t fully account for counter-face detection and validation, which is necessary to accurately determine if the bend analysis is valid.

    Vertex and Edge Tracking:
        The source code maintains a dictionary of vertices (vertexDict) and edges (edgeDict) for each node. These dictionaries are used for recalculating vertex positions during the unfolding process. This level of tracking is not currently present in our BendNode class and should be added to match the source functionality.

    Handling Non-planar Bends:
        The source code includes logic for handling both planar and non-planar bends (e.g., cylindrical). We need to ensure that our detect_bends function accommodates cylindrical and other complex bend types in addition to planar faces.

Proposed Changes to Bending Analysis:

    Enhance the BendNode Structure:
        Add properties such as axis, bend center, inner radius, tangent vector, and translation length.
        Ensure vertexDict and edgeDict are populated for each bend node.

    Counter Face Detection:
        Implement logic to detect and validate counter faces to ensure that thickness measurements are accurate and that the bend analysis is applied correctly.

    Accurate Bend Transformations:
        Use the bend angle, tangent vector, and translation length to correctly calculate the new positions of vertices and edges in the unfolded geometry.

    Handle Complex Bends:
        Ensure that detect_bends() correctly identifies cylindrical bends and that bend direction (up or down) is accounted for when calculating transformations.


The bend angle calculation in the provided source code involves several key steps and details that address how the bend angle and related attributes like the tangent vector, inner radius, and k-factor are calculated. Let's break down the logic behind the getBendAngle method:
1. Bend Angle Calculation:

    The code retrieves the angle range (angle_0 and angle_1) of the bend surface from the face's parameter range using theFace.ParameterRange. These parameters represent the start and end of the bend's angular span on the cylindrical surface.
    The starting angle is determined based on the position of the edge vector (edge_vec), which is calculated by finding the edge's first vertex (P_edge.Vertexes[0]).
    The bend angle is then computed as the difference between angle_start and angle_end. If the result is negative, it flips the sign to ensure a positive bend angle.

2. Tangent Vector Calculation:

    First Tangent Vector: The tangent vector is calculated by taking a radial vector from the edge position (edge_vec) to the bend center (s_Center), using the bend axis (s_Axis) to create the initial vector (first_vec).
    Second Tangent Vector: Another radial vector (sec_vec) is calculated from a point on the bend surface (tanPos), which is determined by evaluating the bend surface at a specific angle and position.
    Cross Product: The cross product of first_vec and sec_vec is calculated to determine the direction of the bend. If the triple product of the cross product and the bend axis (s_Axis) is negative, the axis is reversed to ensure proper direction.
    Final Tangent Vector: The final tangent vector (tan_vec) is stored in the node and is used for transformation during unfolding.

3. Bend Direction and Inner Radius:

    The bend direction (bend_dir) is used to determine whether the bend is "up" or "down". Based on the direction, the inner radius of the bend is calculated. If the bend is "up," the inner radius is the radius of the cylindrical surface (theFace.Surface.Radius). If the bend is "down," the inner radius is reduced by the sheet's thickness (self.__thickness).

4. K-Factor and Translation Length:

    The k-factor is a coefficient that accounts for the material stretching during bending. This factor, combined with the inner radius and sheet thickness, is used to calculate the translation length (newNode._trans_length), which is how far the material needs to unfold.
    The translation length formula is:

    makefile

    _trans_length = (innerRadius + k_Factor * thickness) * bend_angle

    This ensures that the correct amount of material is unfolded during the bending process.

5. Correcting the Bend Angle:

    The code compares the bend angle with the angle of the parent face (stored in cFaceAngle) to ensure the unfolding transformation is applied correctly.
    The difference between the calculated bend angle and the face angle (diffAngle) is used to adjust the transformation process during unfolding.

Summary of Key Concepts:

    Bend Angle: The angle between the start and end of the cylindrical surface on the sheet metal is calculated.
    Tangent Vectors: These vectors are crucial for the unfolding transformation and are calculated using the bend center and axis.
    Bend Direction: Determines whether the bend is "up" or "down," affecting the inner radius calculation.
    Inner Radius: The distance from the center of the bend to the inner surface of the material.
    Translation Length: The distance the material needs to be unfolded based on the bend angle, inner radius, and k-factor.

Why is Bend Detection Between a Flat and Cylindrical Surface?

This method calculates the bend angle when a flat face is adjacent to a cylindrical face because bends in sheet metal are typically defined as transitions from flat surfaces to curved (cylindrical) surfaces. The method considers both types of surfaces to ensure accurate unfolding and transformation.


Here’s how the bend center can be calculated based on that:

    Surface Identification: The bend center is located on cylindrical surfaces. Once the surface of the face is identified as cylindrical, the center of the cylinder can be extracted using Surface.Center.

    Distance from Edge to Cylinder Center: The edge vectors are used to determine the position of the bend with respect to the cylindrical center. This is accomplished by computing the distance between the edge vertices and the cylinder center, which represents the bending axis.




SheetTreeNode (inherits from BendNode)
│
├── Unique Attributes:
│   ├── children             (redefined from BendNode)
│   ├── parent               (redefined from BendNode)
│   ├── bend_angle           (redefined from BendNode)
│   ├── transformed_face     (new, stores the transformed face after transformation)
│   ├── tangent_vectors      (redefined from BendNode, for transformation)
│
├── Methods:
│   ├── __init__(self, face)                      (overrides BendNode's constructor)
│   ├── unfold(self)                              (new, unfolds the node and its children recursively)
│   ├── apply_transformation(self)                (new, applies transformations such as rotation/translation)
│   ├── update_transformed_face(self, transformed_face) (new, updates the face after transformation)
│   ├── track_vertices(self)                      (overrides to track both original and unfolded vertex positions)
│   ├── _get_vertices(self, face)                 (new, helper method to extract vertices from a face)
│
└── Inherits from:
    BendNode
    │
    ├── Attributes:
    │   ├── face                (TopoDS_Face representing the surface)
    │   ├── edges               (list of edges associated with the face)
    │   ├── vertices            (list of vertices associated with the face)
    │   ├── surface_type        (e.g., "Planar", "Cylindrical")
    │   ├── children            (list of child BendNodes, representing relationships)
    │   ├── parent              (parent node in hierarchy)
    │   ├── processed           (flag indicating if node is processed)
    │   ├── bend_angle          (angle between this face and the parent face)
    │   ├── axis                (axis of the bend for cylindrical surfaces)
    │   ├── bend_center         (center point of the bend)
    │   ├── inner_radius        (radius for cylindrical bends)
    │   ├── tangent_vectors     (list of tangent vectors for unfolding)
    │   ├── vertexDict          (dictionary to track vertex positions before and after bending)
    │   ├── bend_dir            (direction of the bend: "up" or "down")
    │
    ├── Methods:
    │   ├── __init__(self, face)                  (initializes a BendNode)
    │   ├── analyze_surface_type(self)            (determines if the surface is planar or cylindrical)
    │   ├── add_child(self, child_node, bend_angle=None, bend_type=None) (adds a child node and stores bend info)
    │   ├── analyze_edges_and_vertices(self)      (analyzes edges and vertices of the face)
    │   ├── track_vertices(self, transformation=None) (tracks vertex positions before and after transformation)
    │   ├── calculate_tangent_vectors(self)       (calculates tangent vectors for unfolding at the bend)



           Simple_node
           ------------
           + idx
           + c_face_idx
           + node_type
           + p_node
           + p_edge
           + child_list
           + child_idx_lists
           + sheet_edges
           + axis
           + facePosi
           + bendCenter
           + distCenter
           + innerRadius
           + bend_dir
           + bend_angle
           + tan_vec
           + oppositePoint
           + vertexDict
           + edgeDict
           + _trans_length
           + analysis_ok
           + error_code
           + k_factor_lookup
           + nfIndexes
           + seam_edges
           + node_flattened_faces
           + unfoldTopList
           + unfoldCounterList
           + actual_angle
           + p_wire
           + c_wire
           + b_edges
           
           Methods:
           ---------
           + dump()
           + get_Face_idx()
           + get_surface()
           + getBendAngle()
           + make_new_face_node()
           + Bend_analysis()
           + handle_chamfer()

        ---------------------------
                |
                |
                V
           SheetTree
           ----------
           + root
           + cFaceTol
           + __Shape
           + error_code
           + failed_face_idx
           + k_factor_lookup
           + wire_replacements
           + f_list
           + index_list
           + index_unfold_list
           + max_f_idx
           + unfoldFaces

           Methods:
           ---------
           + dump()
           + get_node_faces()
           + is_sheet_edge_face()
           + same_edges()
           + isVertOpposite()
           + getDistanceToFace()
           + divideEdgeFace()
           + cutEdgeFace()
           + Bend_analysis()
           + handle_hole()


Modifications Required:
Transformation Propagation: You need to ensure that once the second plate of Bend 1 is transformed, all plates connected to it (such as Plate 3, etc.) receive the same transformation before we proceed to flattening Bend 2. This ensures that the recursive unfolding logic will work correctly.

Use of Transformed COM: After transforming the second plate (Plate 2) in Bend 1, the transformed COM of Plate 2 should be passed to the logic for Bend 2. This is critical because any transformations applied to Plate 2 will affect the subsequent plates (Plate 3, etc.).

