#src/sheet_tree.py
from OCC.Core.TopoDS import topods
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.GProp import GProp_GProps
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_VERTEX
from OCC.Core.gp import gp_Trsf
from face_operations import extract_faces  
from bend_analysis import calculate_bend_angle, BendNode  
from math import radians
from OCC.Core.BRepExtrema import BRepExtrema_DistShapeShape
from math import isclose, acos, degrees
from math import acos, degrees, radians

class SheetTreeNode(BendNode):  # Extend from BendNode to ensure consistency
    def __init__(self, face):
        super().__init__(face)  # Initialize the BendNode with the face
        self.type = None # Bend or plane node
        self.children = []
        self.parent = None
        self.bend_angle = None  # Angle betw    een this face and its parent (if applicable)
        self.bend_type = None # UP or DOWN
        self.transformed_face = None  # Store the transformed face
        self.tangent_vectors = []  # Store tangent vectors for transformation

    def unfold(self):
        """
        Unfold the node by applying transformations (rotation/translation).
        """
        self.apply_transformation()
        # Recursively unfold child nodes
        for child in self.children:
            child.unfold()
    
    def apply_transformation(self):
        """
        Applies the unfolding transformation to the node.
        The transformation includes rotation and translation based on the bend angle.
        """
        if self.bend_angle and self.tangent_vectors:
            axis_point = self.bend_center
            rotation_axis = self.axis
            angle_deg = self.bend_angle

            # Perform the rotation using the bend angle
            transformation = gp_Trsf()
            transformation.SetRotation(rotation_axis, radians(angle_deg))
            rotated_face = self.face.copy()
            rotated_face.Rotate(axis_point, transformation)

            # Perform the translation using the tangent vectors
            translation_vec = self.tangent_vectors[0]  # Example using first tangent vector
            rotated_face.Translate(translation_vec)

            # Update the node with transformed face
            self.update_transformed_face(rotated_face)

    def update_transformed_face(self, transformed_face):
        """
        Updates the node with the newly transformed face and recalculates vertex positions.
        """
        self.transformed_face = transformed_face
        self.track_vertices()

    def track_vertices(self):
        """
        Tracks the original and unfolded positions of vertices.
        """
        self.vertexDict = {}
        original_vertices = self._get_vertices(self.face)
        unfolded_vertices = self._get_vertices(self.transformed_face)

        for i, original_vertex in enumerate(original_vertices):
            unfolded_vertex = unfolded_vertices[i]
            self.vertexDict[i] = (original_vertex, unfolded_vertex)

    def _get_vertices(self, face):
        """
        Utility function to extract vertices from a face.
        """
        explorer = TopExp_Explorer(face, TopAbs_VERTEX)
        vertices = []
        while explorer.More():
            vertex = topods.Vertex(explorer.Current())
            vertices.append(vertex)
            explorer.Next()
        return vertices



class SheetTree:
    def __init__(self, shape):
        self.shape = shape
        self.root = None
        self.faces = []
        self.thickness = 2.0 #mm
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
            self.faces.append(node)

        if self.faces:
            self.root = self.faces[0]  # Set the first face as root for now
            
        # Detect bends and establish parent child relation
        self.detect_bends(tolerance=1e-6)  # Detect bends between all faces


    def unfold(self):
        """
        Unfold the sheet metal part by invoking the unfold method on each node.
        """
        if self.root:
            self.root.unfold()
            
    def get_face_info(self, face):
        """
        Get basic info (area) of the face for printing purposes.
        """
        props = GProp_GProps()
        brepgprop.SurfaceProperties(face, props)
        area = props.Mass()
        return f"Area: {area:.2f}"
    
    def detect_bends(self,tolerance=1e-6):
        """
        Detects bends between faces by checking proximity and thickness.

        Args:
            faces: List of BendNode faces from the tree.
            thickness: Expected thickness of the sheet metal.
            tolerance: Tolerance for thickness comparison.

        Returns:
            list: List of tuples representing the bend relationships between nodes.
        """
        plane_bent_pairs = []
        for face in self.faces:
            face.analyze_surface_type()
            face.analyze_edges_and_vertices()  # Analyze both edges and vertices
            face.calculate_normal()  
            # If the node represents a cylindrical surface, calculate the bend center
            if face.surface_type == "Cylindrical":
                face.calculate_bend_center()  # Call to calculate the bend center
                face.calculate_bend_direction()
                face.calculate_tangent_vectors()  # Calculate tangent vectors for unfolding

        # Now, check for adjacent face pairs that form a bend
        for i, face in enumerate(self.faces):
            if face.processed:
                continue
            for j, other_face in enumerate(self.faces):
                if i == j or other_face.processed:
                    continue
                # Check if one face is flat and the other is cylindrical
                if face.surface_type == "Flat" and other_face.surface_type == "Cylindrical":
                    dist = BRepExtrema_DistShapeShape(face.face, other_face.face).Value()
                    if isclose(dist, self.thickness, rel_tol=tolerance):
                        bend_angle, bend_type = calculate_bend_angle(face,other_face,self.thickness)
                        face.add_child(other_face, bend_angle, bend_type)
                        face.type = "flat"
                        other_face.type = "bent"
                        other_face.processed = True
                        plane_bent_pairs.append((face, other_face))
                        print(f"Bend detected between face {i+1} and face {j+1} with bend angle {bend_angle} - {bend_type}")
                        break
            if not plane_bent_pairs:
                print("No bends detected.")

