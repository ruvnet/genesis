import gradio as gr
from typing import Dict, Any
import time

from .components import (
    create_config_panel,
    create_output_panel,
    create_control_panel
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
            
            # Create UI components
            self.inputs, config_panel = create_config_panel()
            self.controls, control_panel = create_control_panel()
            self.outputs, output_panel = create_output_panel()
            
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
