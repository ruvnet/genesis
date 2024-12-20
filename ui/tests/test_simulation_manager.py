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
    def test_create_object(self, mock_gs):
        """Test object creation functionality."""
        # Setup mock scene and entity
        mock_scene = MagicMock()
        mock_entity = MagicMock()
        mock_scene.add_entity.return_value = mock_entity
        mock_gs.Scene.return_value = mock_scene
        
        # Initialize simulation
        self.manager.initialize_simulation(self.test_config)
        
        # Test creating a sphere
        sphere_config = {
            "object_type": "Sphere",
            "pos_x": 0.0, "pos_y": 0.0, "pos_z": 1.0,
            "rot_x": 0.0, "rot_y": 0.0, "rot_z": 0.0,
            "density": 1000.0,
            "sphere_radius": 0.2,
            "collision_enabled": True,
            "collision_margin": 0.01,
            "collision_group": 0
        }
        result = self.manager.create_object(sphere_config)
        self.assertIn("Created Sphere", result)
        mock_gs.morphs.Sphere.assert_called_once_with(
            pos=(0.0, 0.0, 1.0),
            radius=0.2,
            density=1000.0
        )
        
        # Test creating a box
        box_config = {
            "object_type": "Box",
            "pos_x": 0.0, "pos_y": 0.0, "pos_z": 1.0,
            "rot_x": 0.0, "rot_y": 0.0, "rot_z": 0.0,
            "density": 1000.0,
            "box_width": 1.0, "box_depth": 0.5, "box_height": 0.2,
            "collision_enabled": True,
            "collision_margin": 0.01,
            "collision_group": 0
        }
        result = self.manager.create_object(box_config)
        self.assertIn("Created Box", result)
        mock_gs.morphs.Box.assert_called_once_with(
            pos=(0.0, 0.0, 1.0),
            size=(1.0, 0.5, 0.2),
            density=1000.0
        )
        
        # Test error when no scene exists
        self.manager.scene = None
        result = self.manager.create_object(sphere_config)
        self.assertIn("Error", result)
        self.assertIn("No active simulation", result)
    
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
    @patch('ui.simulation.simulation_manager.gs')
    def test_visualization_update(self, mock_gs):
        """Test visualization settings update."""
        # Setup mock scene and camera
        mock_scene = MagicMock()
        mock_camera = MagicMock()
        mock_scene.add_camera.return_value = mock_camera
        mock_gs.Scene.return_value = mock_scene
        
        # Initialize simulation
        self.manager.initialize_simulation(self.test_config)
        
        # Test visualization update with Rasterizer
        vis_config = {
            "renderer_type": "Rasterizer",
            "max_fps": 60,
            "tracing_depth": 32,
            "rr_depth": 0,
            "rr_threshold": 0.95,
            "env_radius": 1000.0,
            "resolution_w": 1280,
            "resolution_h": 720,
            "camera_fov": 40,
            "camera_pos_x": 3.5,
            "camera_pos_y": 0.0,
            "camera_pos_z": 2.5,
            "lookat_x": 0.0,
            "lookat_y": 0.0,
            "lookat_z": 0.5,
            "show_world_frame": True,
            "world_frame_size": 1.0,
            "show_link_frame": False,
            "show_cameras": False,
            "plane_reflection": True,
            "ambient_r": 0.5,
            "ambient_g": 0.5,
            "ambient_b": 0.5,
            "recording_enabled": False,
            "output_dir": "data/recordings",
            "filename": "simulation",
            "record_fps": 60,
            "record_rgb": True,
            "record_depth": False,
            "record_segmentation": False,
            "record_normal": False
        }
        
        result = self.manager.update_visualization(vis_config)
        self.assertIn("updated successfully", result)
        
        # Verify renderer was created and set
        mock_gs.renderers.Rasterizer.assert_called_once()
        mock_scene.set_renderer.assert_called_once()
        
        # Verify camera was created with correct parameters
        mock_scene.add_camera.assert_called_once_with(
            res=(1280, 720),
            pos=(3.5, 0.0, 2.5),
            lookat=(0.0, 0.0, 0.5),
            fov=40
        )
        
        # Test visualization update with RayTracer
        vis_config["renderer_type"] = "RayTracer"
        self.manager.update_visualization(vis_config)
        
        # Verify RayTracer was created with correct parameters
        mock_gs.renderers.RayTracer.assert_called_once_with(
            tracing_depth=32,
            rr_depth=0,
            rr_threshold=0.95,
            env_radius=1000.0
        )
    
    @patch('ui.simulation.simulation_manager.gs')
    def test_recording(self, mock_gs):
        """Test recording functionality."""
        # Setup mock scene and camera
        mock_scene = MagicMock()
        mock_camera = MagicMock()
        mock_scene.add_camera.return_value = mock_camera
        mock_gs.Scene.return_value = mock_scene
        
        # Initialize simulation
        self.manager.initialize_simulation(self.test_config)
        
        # Test starting recording
        vis_config = {
            "renderer_type": "Rasterizer",
            "recording_enabled": True,
            "output_dir": "data/recordings",
            "filename": "test_recording",
            "record_fps": 60,
            "record_rgb": True,
            "record_depth": False,
            "record_segmentation": False,
            "record_normal": False
        }
        
        self.manager.update_visualization(vis_config)
        mock_camera.start_recording.assert_called_once()
        self.assertTrue(self.manager.recording)
        
        # Test stopping recording
        vis_config["recording_enabled"] = False
        self.manager.update_visualization(vis_config)
        mock_camera.stop_recording.assert_called_once_with(
            save_to_filename="data/recordings/test_recording.mp4",
            fps=60
        )
        self.assertFalse(self.manager.recording)
    
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

if __name__ == '__main__':
    unittest.main()
