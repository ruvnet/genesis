import gradio as gr
from typing import Dict, Any, Tuple

def create_output_panel() -> Tuple[Dict[str, Any], gr.Column]:
    """Create the output panel components."""
    with gr.Column() as output_panel:
        with gr.Row():
            with gr.Column():
                # Status outputs
                init_output = gr.Textbox(
                    label="Initialization Status",
                    interactive=False,
                    show_label=True
                )
                stats_output = gr.Textbox(
                    label="Simulation Statistics",
                    max_lines=15,
                    interactive=False,
                    show_label=True
                )
            
            # Live console output
            console_output = gr.Textbox(
                label="Console Output",
                max_lines=20,
                interactive=False,
                autoscroll=True,
                show_label=True,
                container=True
            )

    # Create dictionary of output components
    outputs = {
        "init_output": init_output,
        "stats_output": stats_output,
        "console_output": console_output
    }
    
    return outputs, output_panel
