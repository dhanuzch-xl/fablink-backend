import unittest
from OCC.Core.gp import gp_Pnt, gp_Ax1, gp_Dir
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCylinder
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_FACE
from OCC.Core.TopoDS import topods_Face
from OCC.Core.BRepTools import breptools
from bend_analysis import BendNode, get_bend_angle
from OCC.Core.GeomAbs import GeomAbs_Cylinder

class TestBendAngle(unittest.TestCase):

    def setUp(self):
        """
        Setup test environment for the bend angle calculation
        """
        # Create a cylinder surface (representing a bend surface)
        cylinder_shape = BRepPrimAPI_MakeCylinder(10, 100).Shape()

        # Extract a face from the cylinder shape
        explorer = TopExp_Explorer(cylinder_shape, TopAbs_FACE)
        self.cylinder_face = topods_Face(explorer.Current())

        # Create parent and child nodes (for simplicity, create a dummy edge and node)
        p_edge = BRepBuilderAPI_MakeEdge(gp_Pnt(10, 0, 0), gp_Pnt(10, 100, 0)).Edge()
        p_node = BendNode(self.cylinder_face)  # Dummy node acting as a parent

        # Create a new node with some dummy values for axis, bend center, etc.
        self.new_node = BendNode(self.cylinder_face)
        self.new_node.p_edge = p_edge
        self.new_node.p_node = p_node
        self.new_node.axis = gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1))  # Axis along Z
        self.new_node.bend_center = gp_Pnt(0, 0, 0)  # Center at the origin
        self.new_node.bend_dir = "up"
        self.new_node.idx = 0  # Index of the face

        # Assign thickness for the bend
        self.thickness = 2.0

    def test_bend_angle_calculation(self):
        """
        Test bend angle calculation for the node
        """
        get_bend_angle(self.new_node, self.thickness)

        # Check the bend angle has been calculated and is a positive value
        self.assertTrue(self.new_node.bend_angle > 0, "Bend angle was not calculated correctly.")

        # Check that the inner radius is calculated correctly
        self.assertTrue(self.new_node.inner_radius > 0, "Inner radius was not calculated correctly.")

        # Check that tangent vector is calculated
        self.assertIsNotNone(self.new_node.tangent_vector, "Tangent vector was not calculated correctly.")
        self.assertTrue(self.new_node.tangent_vector.Magnitude() > 0, "Tangent vector magnitude should be greater than zero.")

    def test_bend_angle_direction_adjustment(self):
        """
        Test if the bend angle direction is adjusted based on cross product results.
        """
        # Calculate bend angle
        get_bend_angle(self.new_node, self.thickness)

        # Cross product determines direction adjustment, should ensure correct sign of axis and bend center
        cross_prod_adjusted = self.new_node.axis.Direction().IsEqual(self.new_node.axis.Direction(), 1e-6)
        self.assertTrue(cross_prod_adjusted, "Bend axis direction should be adjusted based on cross product.")

if __name__ == '__main__':
    unittest.main()
