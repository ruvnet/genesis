import unittest
from unittest.mock import Mock, patch, MagicMock
import gradio as gr
from ui.app import GenesisUI
from ui.utils.console_logger import console

@patch('gradio.Dropdown')
@patch('gradio.Slider')
@patch('gradio.Checkbox')
@patch('gradio.Textbox')
@patch('gradio.Button')
@patch('gradio.Column')
@patch('gradio.Row')
@patch('gradio.Markdown')
class TestGenesisUI(unittest.TestCase):
    def setUp(self):
        self.blocks_ctx = MagicMock()
        self.blocks_patcher = patch('gradio.Blocks')
        self.mock_blocks = self.blocks_patcher.start()
        self.mock_blocks.return_value.__enter__.return_value = self.blocks_ctx
        
        # Mock simulation manager
        self.sim_patcher = patch('ui.app.SimulationManager')
        self.mock_sim = self.sim_patcher.start()
        
        # Mock console logger
        self.console_patcher = patch('ui.app.console')
        self.mock_console = self.console_patcher.start()
        self.mock_console.get_messages.return_value = "Test console output"
        
        self.app = GenesisUI()
    
    def tearDown(self):
        self.blocks_patcher.stop()
        self.sim_patcher.stop()
        self.console_patcher.stop()
    
    def test_ui_creation(self, mock_md, mock_row, mock_col, mock_btn, 
                        mock_textbox, mock_checkbox, mock_slider, mock_dropdown):
        """Test UI creation and component setup."""
        demo = self.app.create_ui()
        
        # Verify components were created
        self.assertIsNotNone(self.app.inputs)
        self.assertIsNotNone(self.app.outputs)
        self.assertIsNotNone(self.app.controls)
        
        # Verify required inputs exist
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
        self.assertEqual(set(self.app.inputs.keys()), expected_inputs)
        
        # Verify required outputs exist
        expected_outputs = {
            "init_output",
            "stats_output",
            "console_output"
        }
        self.assertEqual(set(self.app.outputs.keys()), expected_outputs)
        
        # Verify control buttons exist
        expected_controls = {
            "start_btn",
            "stop_btn"
        }
        self.assertEqual(set(self.app.controls.keys()), expected_controls)
    
    def test_simulation_control(self, mock_md, mock_row, mock_col, mock_btn, 
                              mock_textbox, mock_checkbox, mock_slider, mock_dropdown):
        """Test simulation start/stop functionality."""
        # Configure mock simulation manager
        mock_sim_instance = self.mock_sim.return_value
        mock_sim_instance.start.return_value = ("Init OK", "Started", "Console output")
        mock_sim_instance.stop.return_value = ("Stopped", "Console output")
        
        # Create UI with mocked components
        demo = self.app.create_ui()
        
        # Test simulation start
        test_params = [
            "rigid_body",  # physics_solver
            "CPU",        # compute_backend
            60,          # fps_target
            0.0,         # gravity_x
            0.0,         # gravity_y
            -9.81,       # gravity_z
            0.01,        # dt
            False        # verbose
        ]
        
        init_msg, status_msg, console_msg = self.app.start_simulation(*test_params)
        self.assertEqual(init_msg, "Init OK")
        self.assertEqual(status_msg, "Started")
        
        # Verify simulation manager was called with correct config
        mock_sim_instance.start.assert_called_once()
        config = mock_sim_instance.start.call_args[0][0]
        self.assertEqual(config["physics_solver"], "rigid_body")
        self.assertEqual(config["compute_backend"], "CPU")
        self.assertEqual(config["gravity_z"], -9.81)
        
        # Test simulation stop
        stats_msg, console_msg = self.app.stop_simulation()
        self.assertEqual(stats_msg, "Stopped")
        mock_sim_instance.stop.assert_called_once()

    def test_console_refresh(self, mock_md, mock_row, mock_col, mock_btn, 
                           mock_textbox, mock_checkbox, mock_slider, mock_dropdown):
        """Test console refresh mechanism."""
        # Create UI
        demo = self.app.create_ui()
        
        # Get the console output component
        console_output = self.app.outputs["console_output"]
        
        # Verify refresh function is set
        self.assertIsNotNone(console_output.value)
        self.assertTrue(callable(console_output.value))
        
        # Verify refresh interval is set
        self.assertEqual(console_output.every, 1)
        
        # Test refresh function
        refresh_fn = console_output.value
        result = refresh_fn()
        self.assertEqual(result, "Test console output")
        self.mock_console.get_messages.assert_called_once()

if __name__ == '__main__':
    unittest.main()
