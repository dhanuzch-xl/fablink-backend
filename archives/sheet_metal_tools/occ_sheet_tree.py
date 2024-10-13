from OCC.Core.BRep import BRep_Tool_Surface
from OCC.Core.TopoDS import topods_Face
from OCC.Core.gp import gp_Trsf, gp_Ax1, gp_Pnt, gp_Dir
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse

import math

class SheetTree:
    def __init__(self, shape, face_idx, k_factor_lookup):
        self.shape = shape
        self.face_idx = face_idx
        self.k_factor_lookup = k_factor_lookup
        self.faces = []
        self.build_face_list()
        self.root = None

    def build_face_list(self):
        """Extracts faces from the shape and stores them."""
        explorer = TopExp_Explorer(self.shape, TopAbs_FACE)
        while explorer.More():
            face = topods_Face(explorer.Current())
            self.faces.append(face)
            explorer.Next()

    def unfold_tree(self, node):
        """Recursively unfold faces, applying the necessary transformations."""
        unfolded_faces = []
        for child in node.child_list:
            unfolded_faces.extend(self.unfold_tree(child))
        
        if node.node_type == "Bend":
            self.apply_bend_transformation(node, unfolded_faces)
        else:
            unfolded_faces.append(self.build_new_face(node.idx))

        return unfolded_faces

    def apply_bend_transformation(self, node, unfolded_faces):
        """Rotate and translate faces based on the bend angle and direction."""
        axis = node.axis  # Axis of rotation
        trans_vec = node.tan_vec * node.trans_length  # Translation vector

        # Apply transformation to all unfolded faces
        for face in unfolded_faces:
            trsf = gp_Trsf()
            trsf.SetRotation(gp_Ax1(node.bend_center, axis), node.bend_angle)
            transformer = BRepBuilderAPI_Transform(face, trsf)
            rotated_face = transformer.Shape()

            # Translate the face
            trsf.SetTranslation(trans_vec)
            transformer = BRepBuilderAPI_Transform(rotated_face, trsf)
            translated_face = transformer.Shape()

            unfolded_faces.append(translated_face)

    def build_new_face(self, idx):
        """Rebuilds the face based on any adjustments, if necessary."""
        return self.faces[idx]

class SimpleNode:
    def __init__(self, idx, parent=None, edge=None, k_factor_lookup=None):
        self.idx = idx
        self.parent = parent
        self.edge = edge
        self.node_type = None  # "Flat" or "Bend"
        self.k_factor_lookup = k_factor_lookup
        self.child_list = []
        self.tan_vec = None  # Tangent vector for translation
        self.bend_center = None
        self.axis = None
        self.bend_angle = 0
        self.trans_length = 0
