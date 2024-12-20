import threading
import time
import numpy as np
import genesis as gs
import os
import torch
from typing import Optional, Tuple, List, Dict, Any
from ..utils.console_logger import console

class SimulationManager:
    def __init__(self):
        self.simulation_running = False
        self.simulation_thread: Optional[threading.Thread] = None
        self.scene: Optional[gs.Scene] = None
        self.sphere: Optional[Any] = None
        self.trajectory_data: List[List[float]] = []
        self.data_lock = threading.Lock()
    
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
            # Initialize backend
            backend = self.detect_backend(config["compute_backend"])
            gs.init(backend=backend)
            
            # Create scene with minimal visualization
            self.scene = gs.Scene(
                show_viewer=False,
                sim_options=gs.options.SimOptions(
                    dt=config["dt"],
                    substeps=2,
                    gravity=(config["gravity_x"], config["gravity_y"], config["gravity_z"]),
                    requires_grad=False
                ),
                renderer_options=gs.options.RendererOptions(
                    headless=True,
                    use_offscreen=True,
                    enable_shadow=False,
                    enable_ao=False
                )
            )
            
            # Add ground plane
            self.scene.add_entity(gs.morphs.Plane())
            
            # Add sphere
            self.sphere = self.scene.add_entity(
                gs.morphs.Sphere(
                    pos=(0, 0, 1),
                    radius=0.2
                )
            )
            
            # Build scene
            self.scene.build()
            
            return "Simulation initialized successfully"
        except Exception as e:
            return f"Error initializing simulation: {str(e)}"

    def simulate_frames(self) -> None:
        """Background thread function to run the simulation and collect data."""
        frame_count = 0
        start_time = time.time()
        last_status_time = start_time
        
        while self.simulation_running and self.scene is not None and self.sphere is not None:
            try:
                # Physics step
                self.scene.step()
                frame_count += 1
                
                # Collect data
                pos = self.sphere.get_pos()
                vel = self.sphere.get_vel()
                with self.data_lock:
                    self.trajectory_data.append([
                        len(self.trajectory_data),
                        float(pos[0]),
                        float(pos[1]),
                        float(pos[2])
                    ])
                
                # Update status every 1 second
                current_time = time.time()
                if current_time - last_status_time >= 1.0:
                    elapsed = current_time - start_time
                    fps = frame_count / elapsed
                    
                    # Get physics state
                    ke = 0.5 * self.sphere.get_mass() * np.sum(np.array(vel) ** 2)
                    pe = self.sphere.get_mass() * 9.81 * pos[2]
                    
                    status = (
                        f"Frame: {frame_count} | "
                        f"FPS: {fps:.1f} | "
                        f"Position: ({pos[0]:.2f}, {pos[1]:.2f}, {pos[2]:.2f}) | "
                        f"Velocity: ({vel[0]:.2f}, {vel[1]:.2f}, {vel[2]:.2f}) | "
                        f"KE: {ke:.2f}J | PE: {pe:.2f}J"
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
        
        # Clean up scene
        if self.scene is not None:
            try:
                self.scene.destroy()
                self.scene = None
                console.add_message("Scene resources cleaned up", "system")
            except Exception as e:
                console.add_message(f"Warning: Scene cleanup error: {str(e)}", "warning")
        
        # Save trajectory data
        if len(self.trajectory_data) > 0:
            try:
                os.makedirs("data", exist_ok=True)
                csv_file = os.path.join("data", "sphere_trajectory.csv")
                
                with self.data_lock:
                    trajectory = np.array(self.trajectory_data)
                    np.savetxt(
                        csv_file,
                        trajectory,
                        header="step,x,y,z",
                        delimiter=',',
                        fmt=['%3d', '%9.6f', '%9.6f', '%9.6f'],
                        comments=''
                    )
                
                # Calculate statistics
                initial_height = trajectory[0, 3]
                final_height = trajectory[-1, 3]
                distance_fallen = initial_height - final_height
                sim_time = trajectory[-1, 0] * 0.01
                avg_velocity = distance_fallen / sim_time if sim_time > 0 else 0
                
                stats = f"""
Simulation Statistics:
Initial height: {initial_height:.3f} m
Final height: {final_height:.3f} m
Total distance fallen: {distance_fallen:.3f} m
Simulation time: {sim_time:.2f} seconds
Average velocity: {avg_velocity:.3f} m/s
Data points collected: {len(trajectory)}
Data saved to: {csv_file}
"""
                console.add_message("Simulation completed successfully", "success")
                console.add_message(f"Saved {len(trajectory)} data points to {csv_file}", "system")
                return stats, console.get_messages()
                
            except Exception as e:
                error_msg = f"Error saving data: {str(e)}"
                console.add_message(error_msg, "error")
                return error_msg, console.get_messages()
        
        msg = "Simulation stopped (no data collected)"
        console.add_message(msg, "warning")
        return msg, console.get_messages()
