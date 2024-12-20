import unittest
from unittest.mock import Mock, patch, MagicMock
import gradio as gr
from ui.components.object_panel import create_object_panel

class TestObjectPanel(unittest.TestCase):
    def setUp(self):
        self.blocks_ctx = MagicMock()
        self.blocks_patcher = patch('gradio.Blocks')
        self.mock_blocks = self.blocks_patcher.start()
        self.mock_blocks.return_value.__enter__.return_value = self.blocks_ctx
    
    def tearDown(self):
        self.blocks_patcher.stop()
    
    @patch('gradio.Column')
    @patch('gradio.Row')
    @patch('gradio.Markdown')
    @patch('gradio.Dropdown')
    @patch('gradio.Number')
    @patch('gradio.Slider')
    @patch('gradio.Checkbox')
    @patch('gradio.File')
    @patch('gradio.Button')
    @patch('gradio.Textbox')
    def test_panel_creation(self, mock_textbox, mock_btn, mock_file, mock_checkbox, 
                           mock_slider, mock_number, mock_dropdown, mock_md, 
                           mock_row, mock_col):
        """Test object panel creation and component initialization."""
        inputs, outputs, panel = create_object_panel()
        
        # Verify all required inputs exist
        expected_basic_inputs = {
            "object_type",
            "pos_x", "pos_y", "pos_z",
            "rot_x", "rot_y", "rot_z",
            "density"
        }
        self.assertTrue(expected_basic_inputs.issubset(inputs.keys()))
        
        # Verify shape-specific inputs
        expected_shape_inputs = {
            # Sphere
            "sphere_radius",
            # Box
            "box_width", "box_depth", "box_height",
            # Capsule
            "capsule_radius", "capsule_length",
            # Plane
            "plane_height", "plane_normal_x", "plane_normal_y", "plane_normal_z",
            # Mesh
            "mesh_file", "mesh_scale", "use_convex", "max_convex"
        }
        self.assertTrue(expected_shape_inputs.issubset(inputs.keys()))
        
        # Verify collision inputs
        expected_collision_inputs = {
            "collision_enabled",
            "collision_margin",
            "collision_group"
        }
        self.assertTrue(expected_collision_inputs.issubset(inputs.keys()))
        
        # Verify create button and status output exist
        self.assertIn("create_btn", inputs)
        self.assertIn("create_status", outputs)
        
        # Verify button and status properties
        mock_btn.assert_any_call("Create Object", variant="primary")
        mock_textbox.assert_any_call(
            label="Creation Status",
            interactive=False,
            show_label=True
        )
    
    def test_property_visibility_update(self):
        """Test property visibility updates based on object type selection."""
        inputs, outputs, panel = create_object_panel()
        
        # Test sphere properties
        result = inputs["object_type"].change.fn("Sphere")
        self.assertTrue(result[0])  # sphere_props visible
        self.assertFalse(result[1]) # box_props hidden
        self.assertFalse(result[2]) # capsule_props hidden
        self.assertFalse(result[3]) # plane_props hidden
        self.assertFalse(result[4]) # mesh_props hidden
        
        # Test box properties
        result = inputs["object_type"].change.fn("Box")
        self.assertFalse(result[0]) # sphere_props hidden
        self.assertTrue(result[1])  # box_props visible
        self.assertFalse(result[2]) # capsule_props hidden
        self.assertFalse(result[3]) # plane_props hidden
        self.assertFalse(result[4]) # mesh_props hidden
    
    def test_convex_options_visibility(self):
        """Test convex decomposition options visibility toggle."""
        inputs, outputs, panel = create_object_panel()
        
        # Test when convex decomposition is enabled
        result = inputs["use_convex"].change.fn(True)
        self.assertTrue(result["visible"])
        
        # Test when convex decomposition is disabled
        result = inputs["use_convex"].change.fn(False)
        self.assertFalse(result["visible"])

if __name__ == '__main__':
    unittest.main()
