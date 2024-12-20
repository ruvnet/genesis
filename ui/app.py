import gradio as gr
from typing import Dict, Any
import time

from .components import (
    create_config_panel,
    create_output_panel,
    create_control_panel,
    create_object_panel,
    create_visualization_panel
)
from .simulation.simulation_manager import SimulationManager
from .utils.console_logger import console

class GenesisUI:
    def __init__(self):
        self.simulation = SimulationManager()
        self.demo = None
        self.inputs = {}
        self.outputs = {}
        self.controls = {}
    
    def start_simulation(self, *args) -> tuple:
        """Start simulation with the given parameters."""
        # Convert args to config dict
        config = {
            "physics_solver": args[0],
            "compute_backend": args[1],
            "fps_target": args[2],
            "gravity_x": args[3],
            "gravity_y": args[4],
            "gravity_z": args[5],
            "dt": args[6],
            "verbose": args[7]
        }
        
        return self.simulation.start(config)
    
    def stop_simulation(self) -> tuple:
        """Stop the simulation."""
        return self.simulation.stop()
    
    def create_ui(self) -> gr.Blocks:
        """Create the Gradio interface."""
        with gr.Blocks(title="Genesis Physics Simulation") as self.demo:
            gr.Markdown("# Genesis Physics Simulation")
            
            with gr.Tabs() as tabs:
                # Introduction Tab
                with gr.TabItem("Introduction"):
                    gr.Markdown("""
                    # Welcome to Genesis Physics Simulation
                    
                    Genesis is a versatile physics simulation framework that supports:
                    - Multiple physics solvers (Rigid Body, MPM, SPH, PBD, FEM)
                    - Real-time visualization and rendering
                    - Various object types and materials
                    - Data collection and analysis
                    
                    Use the tabs above to configure and control your simulation.
                    """)
                
                # Current Capabilities Tab
                with gr.TabItem("Current Capabilities"):
                    gr.Markdown("""
                    # Current Features
                    
                    ## Physics
                    - Rigid body simulation
                    - Gravity and force fields
                    - Collision detection
                    
                    ## Objects
                    - Sphere primitives
                    - Ground plane
                    
                    ## Analysis
                    - Position tracking
                    - Velocity monitoring
                    - Energy calculations
                    - Data export to CSV
                    """)
                
                # Physics Configuration Tab
                with gr.TabItem("Physics Configuration"):
                    # Create UI components
                    self.inputs, config_panel = create_config_panel()
                    self.controls, control_panel = create_control_panel()
                    self.outputs, output_panel = create_output_panel()
                
                # Placeholder tabs
                with gr.TabItem("Visualization"):
                    # Create visualization panel
                    vis_inputs, vis_outputs, vis_panel = create_visualization_panel()
                    self.inputs.update(vis_inputs)
                    self.outputs.update(vis_outputs)
                    
                    # Connect apply button to simulation manager
                    def update_visualization(*args):
                        if self.simulation is None or self.simulation.scene is None:
                            return "Error: No active simulation. Start simulation first."
                        
                        # Convert args to config dict
                        config = {
                            "renderer_type": args[0],
                            "max_fps": args[1],
                            "tracing_depth": args[2],
                            "rr_depth": args[3],
                            "rr_threshold": args[4],
                            "env_radius": args[5],
                            "resolution_w": args[6],
                            "resolution_h": args[7],
                            "camera_fov": args[8],
                            "camera_pos_x": args[9],
                            "camera_pos_y": args[10],
                            "camera_pos_z": args[11],
                            "lookat_x": args[12],
                            "lookat_y": args[13],
                            "lookat_z": args[14],
                            "show_world_frame": args[15],
                            "world_frame_size": args[16],
                            "show_link_frame": args[17],
                            "show_cameras": args[18],
                            "plane_reflection": args[19],
                            "ambient_r": args[20],
                            "ambient_g": args[21],
                            "ambient_b": args[22],
                            "recording_enabled": args[23],
                            "output_dir": args[24],
                            "filename": args[25],
                            "record_fps": args[26],
                            "record_rgb": args[27],
                            "record_depth": args[28],
                            "record_segmentation": args[29],
                            "record_normal": args[30]
                        }
                        
                        return self.simulation.update_visualization(config)
                    
                    # Connect apply button
                    vis_inputs["apply_btn"].click(
                        fn=update_visualization,
                        inputs=[
                            vis_inputs["renderer_type"],
                            vis_inputs["max_fps"],
                            vis_inputs["tracing_depth"],
                            vis_inputs["rr_depth"],
                            vis_inputs["rr_threshold"],
                            vis_inputs["env_radius"],
                            vis_inputs["resolution_w"],
                            vis_inputs["resolution_h"],
                            vis_inputs["camera_fov"],
                            vis_inputs["camera_pos_x"],
                            vis_inputs["camera_pos_y"],
                            vis_inputs["camera_pos_z"],
                            vis_inputs["lookat_x"],
                            vis_inputs["lookat_y"],
                            vis_inputs["lookat_z"],
                            vis_inputs["show_world_frame"],
                            vis_inputs["world_frame_size"],
                            vis_inputs["show_link_frame"],
                            vis_inputs["show_cameras"],
                            vis_inputs["plane_reflection"],
                            vis_inputs["ambient_r"],
                            vis_inputs["ambient_g"],
                            vis_inputs["ambient_b"],
                            vis_inputs["recording_enabled"],
                            vis_inputs["output_dir"],
                            vis_inputs["filename"],
                            vis_inputs["record_fps"],
                            vis_inputs["record_rgb"],
                            vis_inputs["record_depth"],
                            vis_inputs["record_segmentation"],
                            vis_inputs["record_normal"]
                        ],
                        outputs=[vis_outputs["status"]]
                    )
                
                with gr.TabItem("Object Creation"):
                    # Create object creation panel
                    object_inputs, object_outputs, object_panel = create_object_panel()
                    self.inputs.update(object_inputs)
                    self.outputs.update(object_outputs)
                    
                    # Connect create button to simulation manager
                    def create_object(*args):
                        if self.simulation is None or self.simulation.scene is None:
                            return "Error: No active simulation. Start simulation first."
                        
                        # Convert args to config dict
                        config = {
                            "object_type": args[0],
                            "pos_x": args[1], "pos_y": args[2], "pos_z": args[3],
                            "rot_x": args[4], "rot_y": args[5], "rot_z": args[6],
                            "density": args[7],
                            "sphere_radius": args[8],
                            "box_width": args[9], "box_depth": args[10], "box_height": args[11],
                            "capsule_radius": args[12], "capsule_length": args[13],
                            "plane_height": args[14],
                            "plane_normal_x": args[15], "plane_normal_y": args[16], "plane_normal_z": args[17],
                            "mesh_file": args[18], "mesh_scale": args[19],
                            "use_convex": args[20], "max_convex": args[21],
                            "collision_enabled": args[22],
                            "collision_margin": args[23],
                            "collision_group": args[24]
                        }
                        
                        return self.simulation.create_object(config)
                    
                    # Connect create button
                    object_inputs["create_btn"].click(
                        fn=create_object,
                        inputs=[
                            object_inputs["object_type"],
                            object_inputs["pos_x"], object_inputs["pos_y"], object_inputs["pos_z"],
                            object_inputs["rot_x"], object_inputs["rot_y"], object_inputs["rot_z"],
                            object_inputs["density"],
                            object_inputs["sphere_radius"],
                            object_inputs["box_width"], object_inputs["box_depth"], object_inputs["box_height"],
                            object_inputs["capsule_radius"], object_inputs["capsule_length"],
                            object_inputs["plane_height"],
                            object_inputs["plane_normal_x"], object_inputs["plane_normal_y"], object_inputs["plane_normal_z"],
                            object_inputs["mesh_file"], object_inputs["mesh_scale"],
                            object_inputs["use_convex"], object_inputs["max_convex"],
                            object_inputs["collision_enabled"],
                            object_inputs["collision_margin"],
                            object_inputs["collision_group"]
                        ],
                        outputs=[object_outputs["create_status"]]
                    )
                
                with gr.TabItem("Analysis"):
                    gr.Markdown("Analysis tools coming soon...")
            
            # Connect components
            self.controls["start_btn"].click(
                fn=self.start_simulation,
                inputs=[
                    self.inputs["physics_solver"],
                    self.inputs["compute_backend"],
                    self.inputs["fps_target"],
                    self.inputs["gravity_x"],
                    self.inputs["gravity_y"],
                    self.inputs["gravity_z"],
                    self.inputs["dt"],
                    self.inputs["verbose"]
                ],
                outputs=[
                    self.outputs["init_output"],
                    self.outputs["stats_output"],
                    self.outputs["console_output"]
                ]
            )
            
            self.controls["stop_btn"].click(
                fn=self.stop_simulation,
                inputs=[],
                outputs=[
                    self.outputs["stats_output"],
                    self.outputs["console_output"]
                ]
            )
            
            # Set up periodic console refresh using the every parameter
            def refresh_console():
                return console.get_messages()
            
            self.outputs["console_output"].value = refresh_console
            self.outputs["console_output"].every = 1
        
        return self.demo

def create_app() -> gr.Blocks:
    """Create and return the Gradio application."""
    app = GenesisUI()
    return app.create_ui()

if __name__ == "__main__":
    demo = create_app()
    demo.queue().launch(share=True, server_port=8080)
