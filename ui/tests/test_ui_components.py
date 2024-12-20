import unittest
from unittest.mock import Mock, patch, MagicMock
import gradio as gr
from ui.components import (
    create_config_panel,
    create_output_panel,
    create_control_panel,
    create_object_panel
)

@patch('gradio.File')
@patch('gradio.Dropdown')
@patch('gradio.Slider')
@patch('gradio.Checkbox')
@patch('gradio.Textbox')
@patch('gradio.Button')
@patch('gradio.Column')
@patch('gradio.Row')
class TestUIComponents(unittest.TestCase):
    def setUp(self):
        self.blocks_ctx = MagicMock()
        self.blocks_patcher = patch('gradio.Blocks')
        self.mock_blocks = self.blocks_patcher.start()
        self.mock_blocks.return_value.__enter__.return_value = self.blocks_ctx
    
    def tearDown(self):
        self.blocks_patcher.stop()
    
    def test_config_panel_creation(self, mock_row, mock_col, mock_btn, mock_textbox, 
                                 mock_checkbox, mock_slider, mock_dropdown, mock_file):
        """Test configuration panel creation."""
        inputs, panel = create_config_panel()
        
        # Verify all expected inputs exist
        expected_inputs = {
            "physics_solver",
            "compute_backend",
            "fps_target",
            "gravity_x",
            "gravity_y",
            "gravity_z",
            "dt",
            "verbose"
        }
        self.assertEqual(set(inputs.keys()), expected_inputs)
        
        # Verify input types and default values
        mock_dropdown.assert_has_calls([
            unittest.mock.call(choices=["rigid_body"], label="Physics Solver", value="rigid_body"),
            unittest.mock.call(choices=["CPU", "GPU"], label="Compute Backend", value="CPU")
        ], any_order=True)
        
        mock_slider.assert_has_calls([
            unittest.mock.call(minimum=30, maximum=120, value=60, step=1, label="Target FPS"),
            unittest.mock.call(minimum=-20, maximum=20, value=-9.81, step=0.1, label="Gravity Z")
        ], any_order=True)
    
    def test_output_panel_creation(self, mock_row, mock_col, mock_btn, mock_textbox, 
                                 mock_checkbox, mock_slider, mock_dropdown, mock_file):
        """Test output panel creation."""
        outputs, panel = create_output_panel()
        
        # Verify all expected outputs exist
        expected_outputs = {
            "init_output",
            "stats_output",
            "console_output"
        }
        self.assertEqual(set(outputs.keys()), expected_outputs)
        
        # Verify output properties
        mock_textbox.assert_has_calls([
            unittest.mock.call(label="Initialization Status", interactive=False, show_label=True),
            unittest.mock.call(label="Simulation Statistics", max_lines=15, interactive=False, show_label=True),
            unittest.mock.call(label="Console Output", max_lines=20, interactive=False, autoscroll=True, show_label=True, container=True)
        ], any_order=True)
    
    def test_control_panel_creation(self, mock_row, mock_col, mock_btn, mock_textbox, 
                                  mock_checkbox, mock_slider, mock_dropdown, mock_file):
        """Test control panel creation."""
        controls, panel = create_control_panel()
        
        # Verify all expected controls exist
        expected_controls = {
            "start_btn",
            "stop_btn"
        }
        self.assertEqual(set(controls.keys()), expected_controls)
        
        # Verify button properties
        mock_btn.assert_has_calls([
            unittest.mock.call(value="Start Simulation", variant="primary", size="lg", interactive=True),
            unittest.mock.call(value="Stop Simulation", variant="secondary", size="lg", interactive=True)
        ], any_order=True)

    def test_object_panel_creation(self, mock_row, mock_col, mock_btn, mock_textbox,
                                 mock_checkbox, mock_slider, mock_dropdown, mock_file):
        """Test object creation panel."""
        inputs, panel = create_object_panel()
        
        # Verify basic transform inputs exist
        transform_inputs = {
            "pos_x", "pos_y", "pos_z",
            "rot_x", "rot_y", "rot_z",
            "density"
        }
        self.assertTrue(transform_inputs.issubset(inputs.keys()))
        
        # Verify object type selection
        mock_dropdown.assert_any_call(
            choices=["Sphere", "Box", "Capsule", "Plane", "Mesh"],
            value="Sphere",
            label="Object Type"
        )
        
        # Verify collision properties
        collision_inputs = {
            "collision_enabled",
            "collision_margin",
            "collision_group"
        }
        self.assertTrue(collision_inputs.issubset(inputs.keys()))
        
        # Verify create button
        mock_btn.assert_any_call("Create Object", variant="primary")

if __name__ == '__main__':
    unittest.main()
