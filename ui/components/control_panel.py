import gradio as gr
from typing import Dict, Any, Tuple

def create_control_panel() -> Tuple[Dict[str, Any], gr.Row]:
    """Create the control panel components."""
    with gr.Row() as control_panel:
        # Create control buttons with specific styling
        start_btn = gr.Button(
            value="Start Simulation",
            variant="primary",
            size="lg",
            interactive=True
        )
        stop_btn = gr.Button(
            value="Stop Simulation",
            variant="secondary",
            size="lg",
            interactive=True
        )

    # Create dictionary of control components
    controls = {
        "start_btn": start_btn,
        "stop_btn": stop_btn
    }
    
    return controls, control_panel
