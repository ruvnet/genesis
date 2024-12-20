import gradio as gr
from typing import Dict, Any, Tuple
import os

def create_visualization_panel() -> Tuple[Dict[str, Any], Dict[str, Any], gr.Column]:
    """Create the visualization panel interface.
    
    Returns:
        Tuple containing:
        - Dictionary of input components
        - Dictionary of output components
        - The panel component
    """
    inputs = {}
    outputs = {}
    
    with gr.Column() as panel:
        gr.Markdown("## Visualization Settings")
        
        # Renderer Selection
        with gr.Column() as renderer_settings:
            gr.Markdown("### Renderer")
            inputs["renderer_type"] = gr.Radio(
                choices=["Rasterizer", "RayTracer"],
                value="Rasterizer",
                label="Renderer Type"
            )
            
            # Rasterizer settings (always visible)
            inputs["max_fps"] = gr.Slider(
                minimum=30,
                maximum=120,
                value=60,
                step=1,
                label="Max FPS"
            )
            
            # RayTracer settings (initially hidden)
            with gr.Column(visible=False) as raytracer_settings:
                inputs["tracing_depth"] = gr.Slider(
                    minimum=1,
                    maximum=64,
                    value=32,
                    step=1,
                    label="Ray Tracing Depth"
                )
                inputs["rr_depth"] = gr.Slider(
                    minimum=0,
                    maximum=32,
                    value=0,
                    step=1,
                    label="Russian Roulette Depth"
                )
                inputs["rr_threshold"] = gr.Slider(
                    minimum=0.0,
                    maximum=1.0,
                    value=0.95,
                    step=0.01,
                    label="Russian Roulette Threshold"
                )
                inputs["env_radius"] = gr.Number(
                    value=1000.0,
                    label="Environment Radius"
                )
        
        # Camera Settings
        with gr.Column() as camera_settings:
            gr.Markdown("### Camera")
            with gr.Row():
                inputs["resolution_w"] = gr.Number(value=1280, label="Width", precision=0)
                inputs["resolution_h"] = gr.Number(value=720, label="Height", precision=0)
            
            with gr.Row():
                inputs["camera_fov"] = gr.Slider(
                    minimum=10,
                    maximum=120,
                    value=40,
                    label="Field of View (degrees)"
                )
            
            gr.Markdown("#### Camera Position")
            with gr.Row():
                inputs["camera_pos_x"] = gr.Number(value=3.5, label="X")
                inputs["camera_pos_y"] = gr.Number(value=0.0, label="Y")
                inputs["camera_pos_z"] = gr.Number(value=2.5, label="Z")
            
            gr.Markdown("#### Look At Point")
            with gr.Row():
                inputs["lookat_x"] = gr.Number(value=0.0, label="X")
                inputs["lookat_y"] = gr.Number(value=0.0, label="Y")
                inputs["lookat_z"] = gr.Number(value=0.5, label="Z")
        
        # Visual Options
        with gr.Column() as visual_settings:
            gr.Markdown("### Visual Options")
            inputs["show_world_frame"] = gr.Checkbox(
                value=True,
                label="Show World Frame"
            )
            inputs["world_frame_size"] = gr.Slider(
                minimum=0.1,
                maximum=5.0,
                value=1.0,
                label="World Frame Size"
            )
            inputs["show_link_frame"] = gr.Checkbox(
                value=False,
                label="Show Link Frames"
            )
            inputs["show_cameras"] = gr.Checkbox(
                value=False,
                label="Show Camera Frustums"
            )
            inputs["plane_reflection"] = gr.Checkbox(
                value=True,
                label="Enable Ground Plane Reflection"
            )
            
            gr.Markdown("#### Ambient Light")
            with gr.Row():
                inputs["ambient_r"] = gr.Slider(
                    minimum=0.0,
                    maximum=1.0,
                    value=0.5,
                    label="Red"
                )
                inputs["ambient_g"] = gr.Slider(
                    minimum=0.0,
                    maximum=1.0,
                    value=0.5,
                    label="Green"
                )
                inputs["ambient_b"] = gr.Slider(
                    minimum=0.0,
                    maximum=1.0,
                    value=0.5,
                    label="Blue"
                )
        
        # Recording Controls
        with gr.Column() as recording_controls:
            gr.Markdown("### Recording")
            inputs["recording_enabled"] = gr.Checkbox(
                value=False,
                label="Enable Recording"
            )
            
            with gr.Column(visible=False) as recording_settings:
                inputs["output_dir"] = gr.Textbox(
                    value="data/recordings",
                    label="Output Directory"
                )
                inputs["filename"] = gr.Textbox(
                    value="simulation",
                    label="Base Filename"
                )
                inputs["record_fps"] = gr.Number(
                    value=60,
                    label="Recording FPS"
                )
                inputs["record_rgb"] = gr.Checkbox(
                    value=True,
                    label="Record RGB"
                )
                inputs["record_depth"] = gr.Checkbox(
                    value=False,
                    label="Record Depth"
                )
                inputs["record_segmentation"] = gr.Checkbox(
                    value=False,
                    label="Record Segmentation"
                )
                inputs["record_normal"] = gr.Checkbox(
                    value=False,
                    label="Record Normal"
                )
        
        # Apply button
        inputs["apply_btn"] = gr.Button("Apply Visualization Settings", variant="primary")
        
        # Status output
        outputs["status"] = gr.Textbox(
            label="Status",
            interactive=False,
            show_label=True
        )
        
        # Show/hide raytracer settings based on renderer selection
        def update_raytracer_visibility(renderer):
            return gr.update(visible=(renderer == "RayTracer"))
        
        inputs["renderer_type"].change(
            fn=update_raytracer_visibility,
            inputs=[inputs["renderer_type"]],
            outputs=[raytracer_settings]
        )
        
        # Show/hide recording settings based on recording enabled
        def update_recording_visibility(enabled):
            return gr.update(visible=enabled)
        
        inputs["recording_enabled"].change(
            fn=update_recording_visibility,
            inputs=[inputs["recording_enabled"]],
            outputs=[recording_settings]
        )
    
    return inputs, outputs, panel
