from OCC.Core.TopoDS import topods
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.GProp import GProp_GProps
from face_operations import extract_faces, BendNode  # Import face extraction and BendNode
from bend_analysis import detect_bends, calculate_bend_angle  # Import bend detection

class SheetTreeNode(BendNode):  # Extend from BendNode to ensure consistency
    def __init__(self, face):
        super().__init__(face)  # Initialize the BendNode with the face
        self.children = []
        self.parent = None
        self.bend_angle = None  # Angle between this face and its parent (if applicable)
        self.bend_type = None   # Type of connection: flat, cylindrical, or other

    def add_child(self, child_node, bend_angle=None, bend_type=None):
        self.children.append(child_node)
        child_node.parent = self
        child_node.bend_angle = bend_angle
        child_node.bend_type = bend_type

class SheetTree:
    def __init__(self, shape):
        self.shape = shape
        self.root = None
        self.nodes = []

    def build_tree(self):
        """
        Build the tree structure from the loaded shape using extracted faces.
        """
        faces = extract_faces(self.shape)  # Use the face extraction from face_operations.py
        if not faces:
            print("No faces found.")
            return

        # Initialize tree nodes from faces
        for face in faces:
            node = SheetTreeNode(face)
            self.nodes.append(node)

        # Detect bends using bend_analysis.py
        bend_nodes = detect_bends(faces, thickness=2.0)  # Detect bends between all faces
        if not bend_nodes:
            print("No bends detected.")
            return

        # Establish parent-child relationships based on bends
        for node1, node2 in bend_nodes:
            bend_angle = calculate_bend_angle(node1.face, node2.face)
            node1.add_child(node2, bend_angle, "Bend")
            print(f"Bend detected between node {self.get_face_info(node1.face)} and node {self.get_face_info(node2.face)}")

        if self.nodes:
            self.root = self.nodes[0]  # Set the first face as root for now
            self._build_hierarchy(self.root)

    def _build_hierarchy(self, node):
        """
        Recursively build the hierarchy by analyzing faces, checking for bends,
        and determining child nodes.
        """
        for other_node in self.nodes:
            if node == other_node or other_node.parent is not None:
                continue
            # Since the bends are already detected, the child-parent relationship has been established

    def get_face_info(self, face):
        """
        Get basic info (area) of the face for printing purposes.
        """
        props = GProp_GProps()
        brepgprop.SurfaceProperties(face, props)
        area = props.Mass()
        return f"Area: {area:.2f}"
