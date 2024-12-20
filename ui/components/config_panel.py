import gradio as gr
from typing import Dict, Any, Tuple

def create_config_panel() -> Tuple[Dict[str, Any], gr.Column]:
    """Create the configuration panel components."""
    with gr.Column() as config_panel:
        with gr.Row():
            with gr.Column():
                # Basic configuration
                solver = gr.Dropdown(
                    choices=["rigid_body"],
                    label="Physics Solver",
                    value="rigid_body"
                )
                
                backend = gr.Dropdown(
                    choices=["CPU", "GPU"],
                    label="Compute Backend",
                    value="CPU"
                )
                
                fps = gr.Slider(
                    minimum=30,
                    maximum=120,
                    value=60,
                    step=1,
                    label="Target FPS"
                )

            with gr.Column():
                # Physics configuration
                gr.Markdown("## Physics Configuration")
                gravity_x = gr.Slider(
                    minimum=-20,
                    maximum=20,
                    value=0.0,
                    step=0.1,
                    label="Gravity X"
                )
                gravity_y = gr.Slider(
                    minimum=-20,
                    maximum=20,
                    value=0.0,
                    step=0.1,
                    label="Gravity Y"
                )
                gravity_z = gr.Slider(
                    minimum=-20,
                    maximum=20,
                    value=-9.81,
                    step=0.1,
                    label="Gravity Z"
                )
                dt_val = gr.Slider(
                    minimum=1e-4,
                    maximum=1e-1,
                    value=1e-2,
                    step=1e-4,
                    label="Time-step (dt)"
                )
                verbose = gr.Checkbox(
                    label="Verbose Output",
                    value=False
                )

    # Create dictionary of input components
    inputs = {
        "physics_solver": solver,
        "compute_backend": backend,
        "fps_target": fps,
        "gravity_x": gravity_x,
        "gravity_y": gravity_y,
        "gravity_z": gravity_z,
        "dt": dt_val,
        "verbose": verbose
    }
    
    return inputs, config_panel
