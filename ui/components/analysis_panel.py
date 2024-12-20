import gradio as gr
import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple

def create_analysis_panel() -> Tuple[Dict[str, Any], Dict[str, Any], gr.Column]:
    """Create the analysis panel with position, velocity, energy tracking and data export."""
    inputs = {}
    outputs = {}
    
    with gr.Column() as panel:
        with gr.Row():
            with gr.Column():
                gr.Markdown("## Position Tracking")
                inputs["track_position"] = gr.Checkbox(label="Enable Position Tracking", value=True)
                outputs["position_plot"] = gr.Plot(label="Object Positions")
                
            with gr.Column():
                gr.Markdown("## Velocity Monitoring")
                inputs["track_velocity"] = gr.Checkbox(label="Enable Velocity Tracking", value=True)
                outputs["velocity_plot"] = gr.Plot(label="Object Velocities")
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("## Energy Analysis")
                inputs["track_energy"] = gr.Checkbox(label="Enable Energy Tracking", value=True)
                outputs["energy_plot"] = gr.Plot(label="System Energy")
                with gr.Row():
                    outputs["kinetic_energy"] = gr.Number(label="Kinetic Energy", value=0.0)
                    outputs["potential_energy"] = gr.Number(label="Potential Energy", value=0.0)
                    outputs["total_energy"] = gr.Number(label="Total Energy", value=0.0)
            
            with gr.Column():
                gr.Markdown("## Data Export")
                inputs["export_path"] = gr.Textbox(
                    label="Export Directory",
                    value="data/analysis",
                    placeholder="Enter path to save data"
                )
                inputs["export_prefix"] = gr.Textbox(
                    label="File Prefix",
                    value="simulation",
                    placeholder="Enter prefix for exported files"
                )
                with gr.Row():
                    inputs["export_position"] = gr.Checkbox(label="Export Position Data", value=True)
                    inputs["export_velocity"] = gr.Checkbox(label="Export Velocity Data", value=True)
                    inputs["export_energy"] = gr.Checkbox(label="Export Energy Data", value=True)
                
                inputs["export_btn"] = gr.Button("Export Data")
                outputs["export_status"] = gr.Textbox(label="Export Status")

    return inputs, outputs, panel
