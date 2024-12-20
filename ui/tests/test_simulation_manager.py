import unittest
from unittest.mock import Mock, patch, MagicMock
import numpy as np
from ui.simulation.simulation_manager import SimulationManager

class TestSimulationManager(unittest.TestCase):
    def setUp(self):
        self.manager = SimulationManager()
        self.test_config = {
            "physics_solver": "rigid_body",
            "compute_backend": "CPU",
            "fps_target": 60,
            "gravity_x": 0.0,
            "gravity_y": 0.0,
            "gravity_z": -9.81,
            "dt": 0.01,
            "verbose": False
        }
    
    @patch('ui.simulation.simulation_manager.gs')
    def test_initialize_simulation(self, mock_gs):
        """Test simulation initialization."""
        # Setup mock scene
        mock_scene = MagicMock()
        mock_gs.Scene.return_value = mock_scene
        
        # Test initialization
        result = self.manager.initialize_simulation(self.test_config)
        
        # Verify genesis was initialized
        mock_gs.init.assert_called_once()
        
        # Verify scene was created with correct parameters
        mock_gs.Scene.assert_called_once()
        self.assertFalse(mock_gs.Scene.call_args[1]['show_viewer'])
        
        # Verify scene was built
        mock_scene.build.assert_called_once()
        
        # Check success message
        self.assertEqual(result, "Simulation initialized successfully")
    
    @patch('ui.simulation.simulation_manager.gs')
    def test_start_stop_simulation(self, mock_gs):
        """Test simulation start and stop."""
        # Setup mock scene
        mock_scene = MagicMock()
        mock_gs.Scene.return_value = mock_scene
        
        # Test start
        init_msg, status_msg, console_msg = self.manager.start(self.test_config)
        self.assertEqual(init_msg, "Simulation initialized successfully")
        self.assertTrue(self.manager.simulation_running)
        
        # Test stop
        stats_msg, console_msg = self.manager.stop()
        self.assertFalse(self.manager.simulation_running)
        self.assertIn("Simulation stopped", stats_msg)
        
        # Verify cleanup
        mock_scene.destroy.assert_called_once()
    
    @patch('ui.simulation.simulation_manager.gs')
    def test_data_collection(self, mock_gs):
        """Test trajectory data collection."""
        # Setup mock scene and sphere
        mock_scene = MagicMock()
        mock_sphere = MagicMock()
        
        # Configure sphere position and velocity mocks
        pos = np.array([0.0, 0.0, 1.0])
        vel = np.array([0.0, 0.0, -1.0])
        mock_sphere.get_pos.side_effect = [pos]  # Return pos once then stop simulation
        mock_sphere.get_vel.return_value = vel
        mock_sphere.get_mass.return_value = 1.0
        
        mock_scene.add_entity.return_value = mock_sphere
        mock_gs.Scene.return_value = mock_scene
        
        # Initialize and start simulation
        self.manager.initialize_simulation(self.test_config)
        self.manager.simulation_running = True
        
        # Mock time.sleep to avoid hanging
        with patch('time.sleep'):
            # Simulate one frame
            self.manager.simulate_frames()
            # Simulation should stop after one frame due to side_effect
        
        # Stop simulation and verify data
        stats_msg, _ = self.manager.stop()
        
        # Verify data collection
        self.assertTrue(len(self.manager.trajectory_data) > 0)
        self.assertIn("Data points collected:", stats_msg)
    
    @patch('ui.simulation.simulation_manager.gs')
    def test_error_handling(self, mock_gs):
        """Test error handling during simulation."""
        # Setup mock scene to raise an error
        mock_gs.Scene.side_effect = Exception("Test error")
        
        # Test initialization error
        init_msg, status_msg, console_msg = self.manager.start(self.test_config)
        self.assertIn("Error", init_msg)
        self.assertFalse(self.manager.simulation_running)
        
        # Test simulation error
        mock_gs.Scene.side_effect = None
        mock_scene = MagicMock()
        mock_scene.step.side_effect = Exception("Simulation error")
        mock_gs.Scene.return_value = mock_scene
        
        self.manager.initialize_simulation(self.test_config)
        self.manager.simulation_running = True
        
        # Mock time.sleep to avoid hanging
        with patch('time.sleep'):
            self.manager.simulate_frames()
        
        # Verify error handling
        self.assertFalse(self.manager.simulation_running)

if __name__ == '__main__':
    unittest.main()
