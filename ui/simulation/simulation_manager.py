import threading
import time
import numpy as np
import genesis as gs
import os
import torch
from typing import Optional, Tuple, List, Dict, Any
from ..utils.console_logger import console
from .analysis_manager import AnalysisManager

class SimulationManager:
    def __init__(self):
        self.simulation_running = False
        self.simulation_thread: Optional[threading.Thread] = None
        self.scene: Optional[gs.Scene] = None
        self.sphere: Optional[Any] = None
        self.trajectory_data: List[List[float]] = []
        self.data_lock = threading.Lock()
        self.entities: Dict[str, Any] = {}
        self.entity_count = 0
        self.camera: Optional[Any] = None
        self.recording: bool = False
        self.analysis = AnalysisManager()
    
    def detect_backend(self, compute_backend: str) -> Any:
        """Configure appropriate backend based on selection."""
        if compute_backend == "GPU" and torch.cuda.is_available():
            console.add_message("CUDA GPU detected - using GPU backend", "system")
            return gs.cuda
        else:
            console.add_message("Using CPU backend", "system")
            return gs.cpu
    
    def initialize_simulation(self, config: Dict[str, Any]) -> str:
        """Initialize Genesis simulation with given parameters"""
        try:
            # Try to reset Genesis state if already running
            try:
                if hasattr(gs, 'clear'):
                    gs.clear()
                    console.add_message("Reset Genesis state", "system")
                elif hasattr(gs, 'reset'):
                    gs.reset()
                    console.add_message("Reset Genesis state", "system")
            except:
                pass  # Ignore any reset errors
            
            # Initialize Genesis with new backend
            backend = self.detect_backend(config["compute_backend"])
            gs.init(backend=backend)
            console.add_message("Genesis initialized successfully", "success")
            
            # Create simulation options
            console.add_message("Creating simulation options...", "system")
            sim_opts = gs.options.SimOptions(
                dt=config["dt"],
                substeps=2,
                gravity=(config["gravity_x"], config["gravity_y"], config["gravity_z"]),
                floor_height=0.0,
                requires_grad=False
            )
            console.add_message("Simulation options created successfully", "success")
            
            # Create scene with physics only (no rendering)
            console.add_message("Creating physics scene...", "system")
            try:
                # Create scene with options
                self.scene = gs.Scene(
                    sim_options=sim_opts,
                    show_viewer=False
                )
                console.add_message("Scene created successfully", "success")
            except Exception as scene_error:
                console.add_message(f"Scene creation failed: {str(scene_error)}", "error")
                console.add_message(f"Scene error type: {type(scene_error)}", "error")
                raise
            
            try:
                # Add ground plane
                console.add_message("Adding ground plane...", "system")
                self.scene.add_entity(gs.morphs.Plane())
                console.add_message("Ground plane added successfully", "success")
                
                # Add sphere
                console.add_message("Adding sphere...", "system")
                self.sphere = self.scene.add_entity(
                    gs.morphs.Sphere(
                        pos=(0, 0, 1),
                        radius=0.2
                    )
                )
                console.add_message("Sphere added successfully", "success")
            except Exception as entity_error:
                console.add_message(f"Error adding entities: {str(entity_error)}", "error")
                console.add_message(f"Entity error type: {type(entity_error)}", "error")
                raise
            
            # Build scene
            self.scene.build()
            
            return "Simulation initialized successfully"
        except Exception as e:
            return f"Error initializing simulation: {str(e)}"
    
    def create_object(self, obj_config: Dict[str, Any]) -> str:
        """Create a new object in the scene."""
        if self.scene is None:
            return "Error: No active simulation scene"
        
        try:
            obj_type = obj_config["object_type"]
            pos = (obj_config["pos_x"], obj_config["pos_y"], obj_config["pos_z"])
            rot = (obj_config["rot_x"], obj_config["rot_y"], obj_config["rot_z"])
            
            console.add_message(f"Creating {obj_type} object...", "system")
            
            if obj_type == "Sphere":
                entity = self.scene.add_entity(
                    gs.morphs.Sphere(
                        pos=pos,
                        radius=obj_config["sphere_radius"],
                        density=obj_config["density"]
                    )
                )
                console.add_message(f"Created sphere with radius {obj_config['sphere_radius']}", "success")
            
            elif obj_type == "Box":
                entity = self.scene.add_entity(
                    gs.morphs.Box(
                        pos=pos,
                        size=(obj_config["box_width"], obj_config["box_depth"], obj_config["box_height"]),
                        density=obj_config["density"]
                    )
                )
                console.add_message(f"Created box with dimensions {obj_config['box_width']}x{obj_config['box_depth']}x{obj_config['box_height']}", "success")
            
            elif obj_type == "Capsule":
                entity = self.scene.add_entity(
                    gs.morphs.Capsule(
                        pos=pos,
                        radius=obj_config["capsule_radius"],
                        length=obj_config["capsule_length"],
                        density=obj_config["density"]
                    )
                )
                console.add_message(f"Created capsule with radius {obj_config['capsule_radius']} and length {obj_config['capsule_length']}", "success")
            
            elif obj_type == "Plane":
                entity = self.scene.add_entity(
                    gs.morphs.Plane(
                        height=obj_config["plane_height"],
                        normal=(obj_config["plane_normal_x"], obj_config["plane_normal_y"], obj_config["plane_normal_z"])
                    )
                )
                console.add_message(f"Created plane at height {obj_config['plane_height']}", "success")
            
            elif obj_type == "Mesh":
                if not obj_config.get("mesh_file"):
                    return "Error: No mesh file provided"
                
                entity = self.scene.add_entity(
                    gs.morphs.Mesh(
                        file=obj_config["mesh_file"],
                        scale=obj_config["mesh_scale"],
                        pos=pos,
                        convex=obj_config["use_convex"],
                        max_convex_pieces=obj_config["max_convex"] if obj_config["use_convex"] else None
                    )
                )
                console.add_message(f"Created mesh from {obj_config['mesh_file']}", "success")
            
            else:
                return f"Error: Unknown object type {obj_type}"
            
            # Set collision properties
            if not obj_config["collision_enabled"]:
                entity.disable_collision()
            else:
                entity.set_collision_margin(obj_config["collision_margin"])
                entity.set_collision_group(obj_config["collision_group"])
            
            # Store entity
            self.entity_count += 1
            entity_id = f"{obj_type.lower()}_{self.entity_count}"
            self.entities[entity_id] = entity
            
            console.add_message(f"Object created successfully with ID: {entity_id}", "success")
            return f"Created {obj_type} (ID: {entity_id})"
            
        except Exception as e:
            error_msg = f"Error creating object: {str(e)}"
            console.add_message(error_msg, "error")
            return error_msg
    
    def update_visualization(self, vis_config: Dict[str, Any]) -> str:
        """Update visualization settings."""
        if self.scene is None:
            return "Error: No active simulation scene"
        
        try:
            # Create renderer
            if vis_config["renderer_type"] == "RayTracer":
                renderer = gs.renderers.RayTracer(
                    tracing_depth=vis_config["tracing_depth"],
                    rr_depth=vis_config["rr_depth"],
                    rr_threshold=vis_config["rr_threshold"],
                    env_radius=vis_config["env_radius"]
                )
            else:  # Rasterizer
                renderer = gs.renderers.Rasterizer()
            
            # Create visualization options
            vis_opts = gs.options.VisOptions(
                show_world_frame=vis_config["show_world_frame"],
                world_frame_size=vis_config["world_frame_size"],
                show_link_frame=vis_config["show_link_frame"],
                show_cameras=vis_config["show_cameras"],
                plane_reflection=vis_config["plane_reflection"],
                ambient_light=(
                    vis_config["ambient_r"],
                    vis_config["ambient_g"],
                    vis_config["ambient_b"]
                )
            )
            
            # Update scene options
            self.scene.set_renderer(renderer)
            self.scene.set_vis_options(vis_opts)
            
            # Update or create camera
            if self.camera is None:
                self.camera = self.scene.add_camera(
                    res=(vis_config["resolution_w"], vis_config["resolution_h"]),
                    pos=(vis_config["camera_pos_x"], vis_config["camera_pos_y"], vis_config["camera_pos_z"]),
                    lookat=(vis_config["lookat_x"], vis_config["lookat_y"], vis_config["lookat_z"]),
                    fov=vis_config["camera_fov"]
                )
            else:
                self.camera.set_resolution(vis_config["resolution_w"], vis_config["resolution_h"])
                self.camera.set_pose(
                    pos=(vis_config["camera_pos_x"], vis_config["camera_pos_y"], vis_config["camera_pos_z"]),
                    lookat=(vis_config["lookat_x"], vis_config["lookat_y"], vis_config["lookat_z"])
                )
                self.camera.set_fov(vis_config["camera_fov"])
            
            # Handle recording settings
            if vis_config["recording_enabled"]:
                if not self.recording:
                    os.makedirs(vis_config["output_dir"], exist_ok=True)
                    self.camera.start_recording()
                    self.recording = True
                    console.add_message("Started recording", "success")
            elif self.recording:
                self.stop_recording(
                    vis_config["output_dir"],
                    vis_config["filename"],
                    vis_config["record_fps"]
                )
            
            console.add_message("Visualization settings updated successfully", "success")
            return "Visualization settings updated successfully"
            
        except Exception as e:
            error_msg = f"Error updating visualization: {str(e)}"
            console.add_message(error_msg, "error")
            return error_msg
    
    def stop_recording(self, output_dir: str, filename: str, fps: int) -> None:
        """Stop recording and save video."""
        if self.recording and self.camera is not None:
            try:
                video_path = os.path.join(output_dir, f"{filename}.mp4")
                self.camera.stop_recording(save_to_filename=video_path, fps=fps)
                self.recording = False
                console.add_message(f"Recording saved to {video_path}", "success")
            except Exception as e:
                console.add_message(f"Error saving recording: {str(e)}", "error")
    
    def simulate_frames(self) -> None:
        """Background thread function to run the simulation and collect data."""
        frame_count = 0
        start_time = time.time()
        last_status_time = start_time
        
        while self.simulation_running and self.scene is not None:
            try:
                # Physics step
                self.scene.step()
                frame_count += 1
                
                # Update analysis tracking
                current_time = time.time() - start_time
                self.analysis.update_tracking(self.scene, current_time)
                
                # Update status every 1 second
                current_time = time.time()
                if current_time - last_status_time >= 1.0:
                    elapsed = current_time - start_time
                    fps = frame_count / elapsed
                    
                    # Get current energy values
                    energy = self.analysis.get_current_energy()
                    
                    status = (
                        f"Frame: {frame_count} | "
                        f"FPS: {fps:.1f} | "
                        f"KE: {energy['kinetic']:.2f}J | "
                        f"PE: {energy['potential']:.2f}J | "
                        f"Total E: {energy['total']:.2f}J"
                    )
                    console.add_message(status, "status")
                    last_status_time = current_time
                
                # Control simulation speed
                time.sleep(0.01)  # 100 Hz update rate
                
            except Exception as e:
                console.add_message(f"Simulation error: {str(e)}", "error")
                break
    
    def start(self, config: Dict[str, Any]) -> Tuple[str, Optional[str], str]:
        """Start the simulation with given parameters."""
        # Reset data
        with self.data_lock:
            self.trajectory_data = []
        console.clear()
        
        # Log simulation parameters
        console.add_message("Starting simulation with parameters:", "system")
        for key, value in config.items():
            console.add_message(f"{key}: {value}", "config")
        
        # Initialize simulation
        msg = self.initialize_simulation(config)
        
        if "Error" in msg:
            console.add_message(msg, "error")
            return msg, None, console.add_message("Initialization failed", "error")
        
        # Start simulation thread
        self.simulation_running = True
        self.simulation_thread = threading.Thread(target=self.simulate_frames, daemon=True)
        self.simulation_thread.start()
        
        status_msg = "Simulation started successfully"
        console.add_message(status_msg, "success")
        return msg, status_msg, console.get_messages()
    
    def stop(self) -> Tuple[str, str]:
        """Stop the running simulation."""
        console.add_message("Stopping simulation...", "system")
        self.simulation_running = False
        if self.simulation_thread is not None:
            self.simulation_thread.join()
        
        # Clean up resources
        if self.scene is not None:
            # Set scene to None first to ensure simulation loop stops
            scene = self.scene
            self.scene = None
            
            try:
                # Try different cleanup methods
                if hasattr(scene, 'clear'):
                    scene.clear()
                elif hasattr(scene, 'reset'):
                    scene.reset()
                elif hasattr(gs, 'clear'):
                    gs.clear()
                elif hasattr(gs, 'reset'):
                    gs.reset()
                
                console.add_message("Scene resources cleaned up", "success")
            except Exception as e:
                console.add_message(f"Warning: Scene cleanup error: {str(e)}", "warning")
            
            # Clear other resources
            self.sphere = None
            self.entities.clear()
            self.entity_count = 0
            self.camera = None
            self.recording = False
        
        msg = "Simulation stopped"
        console.add_message(msg, "success")
        return msg, console.get_messages()
    
    def get_analysis_plots(self) -> Tuple[Optional[Any], Optional[Any], Optional[Any]]:
        """Get current analysis plots."""
        return (
            self.analysis.get_position_plot(),
            self.analysis.get_velocity_plot(),
            self.analysis.get_energy_plot()
        )
    
    def get_current_energy(self) -> Dict[str, float]:
        """Get current energy values."""
        return self.analysis.get_current_energy()
    
    def export_analysis_data(self, path: str, prefix: str,
                           export_position: bool = True,
                           export_velocity: bool = True,
                           export_energy: bool = True) -> str:
        """Export analysis data to CSV files."""
        return self.analysis.export_data(
            path, prefix,
            export_position,
            export_velocity,
            export_energy
        )
    
    def update_analysis_settings(self, track_position: bool,
                               track_velocity: bool,
                               track_energy: bool) -> None:
        """Update analysis tracking settings."""
        self.analysis.track_position = track_position
        self.analysis.track_velocity = track_velocity
        self.analysis.track_energy = track_energy
