import unittest
from unittest.mock import Mock, patch, MagicMock
import gradio as gr
from ui.components.visualization_panel import create_visualization_panel

class TestVisualizationPanel(unittest.TestCase):
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
    @patch('gradio.Radio')
    @patch('gradio.Number')
    @patch('gradio.Slider')
    @patch('gradio.Checkbox')
    @patch('gradio.Textbox')
    @patch('gradio.Button')
    def test_panel_creation(self, mock_btn, mock_textbox, mock_checkbox, mock_slider,
                           mock_number, mock_radio, mock_md, mock_row, mock_col):
        """Test visualization panel creation and component initialization."""
        inputs, outputs, panel = create_visualization_panel()
        
        # Verify renderer inputs exist
        renderer_inputs = {
            "renderer_type",
            "max_fps",
            "tracing_depth",
            "rr_depth",
            "rr_threshold",
            "env_radius"
        }
        self.assertTrue(renderer_inputs.issubset(inputs.keys()))
        
        # Verify camera inputs exist
        camera_inputs = {
            "resolution_w",
            "resolution_h",
            "camera_fov",
            "camera_pos_x",
            "camera_pos_y",
            "camera_pos_z",
            "lookat_x",
            "lookat_y",
            "lookat_z"
        }
        self.assertTrue(camera_inputs.issubset(inputs.keys()))
        
        # Verify visual options exist
        visual_inputs = {
            "show_world_frame",
            "world_frame_size",
            "show_link_frame",
            "show_cameras",
            "plane_reflection",
            "ambient_r",
            "ambient_g",
            "ambient_b"
        }
        self.assertTrue(visual_inputs.issubset(inputs.keys()))
        
        # Verify recording inputs exist
        recording_inputs = {
            "recording_enabled",
            "output_dir",
            "filename",
            "record_fps",
            "record_rgb",
            "record_depth",
            "record_segmentation",
            "record_normal"
        }
        self.assertTrue(recording_inputs.issubset(inputs.keys()))
        
        # Verify apply button and status output exist
        self.assertIn("apply_btn", inputs)
        self.assertIn("status", outputs)
        
        # Verify button and status properties
        mock_btn.assert_any_call("Apply Visualization Settings", variant="primary")
        mock_textbox.assert_any_call(
            label="Status",
            interactive=False,
            show_label=True
        )
    
    def test_raytracer_visibility(self):
        """Test raytracer settings visibility toggle."""
        inputs, outputs, panel = create_visualization_panel()
        
        # Test when RayTracer is selected
        result = inputs["renderer_type"].change.fn("RayTracer")
        self.assertTrue(result["visible"])
        
        # Test when Rasterizer is selected
        result = inputs["renderer_type"].change.fn("Rasterizer")
        self.assertFalse(result["visible"])
    
    def test_recording_visibility(self):
        """Test recording settings visibility toggle."""
        inputs, outputs, panel = create_visualization_panel()
        
        # Test when recording is enabled
        result = inputs["recording_enabled"].change.fn(True)
        self.assertTrue(result["visible"])
        
        # Test when recording is disabled
        result = inputs["recording_enabled"].change.fn(False)
        self.assertFalse(result["visible"])

if __name__ == '__main__':
    unittest.main()
