import gradio as gr
from typing import Dict, Any, Tuple

def create_object_panel() -> Tuple[Dict[str, Any], Dict[str, Any], gr.Column]:
    """Create the object creation panel interface.
    
    Returns:
        Tuple containing:
        - Dictionary of input components
        - Dictionary of output components
        - The panel component
    """
    inputs = {}
    outputs = {}
    
    with gr.Column() as panel:
        gr.Markdown("## Object Creation")
        
        with gr.Row():
            inputs["object_type"] = gr.Dropdown(
                choices=[
                    "Sphere",
                    "Box",
                    "Capsule",
                    "Plane",
                    "Mesh"
                ],
                value="Sphere",
                label="Object Type"
            )
        
        # Basic Properties
        with gr.Column() as basic_props:
            with gr.Row():
                inputs["pos_x"] = gr.Number(value=0.0, label="Position X")
                inputs["pos_y"] = gr.Number(value=0.0, label="Position Y")
                inputs["pos_z"] = gr.Number(value=1.0, label="Position Z")
            
            with gr.Row():
                inputs["rot_x"] = gr.Number(value=0.0, label="Rotation X")
                inputs["rot_y"] = gr.Number(value=0.0, label="Rotation Y")
                inputs["rot_z"] = gr.Number(value=0.0, label="Rotation Z")
            
            inputs["density"] = gr.Number(
                value=1000.0,
                label="Density (kg/m³)"
            )
        
        # Shape-specific Properties
        with gr.Column() as shape_props:
            # Sphere properties
            with gr.Column(visible=True) as sphere_props:
                inputs["sphere_radius"] = gr.Slider(
                    minimum=0.01,
                    maximum=10.0,
                    value=0.2,
                    label="Radius (m)"
                )
            
            # Box properties
            with gr.Column(visible=False) as box_props:
                with gr.Row():
                    inputs["box_width"] = gr.Number(value=1.0, label="Width")
                    inputs["box_depth"] = gr.Number(value=0.5, label="Depth")
                    inputs["box_height"] = gr.Number(value=0.2, label="Height")
            
            # Capsule properties
            with gr.Column(visible=False) as capsule_props:
                inputs["capsule_radius"] = gr.Slider(
                    minimum=0.01,
                    maximum=5.0,
                    value=0.1,
                    label="Radius (m)"
                )
                inputs["capsule_length"] = gr.Slider(
                    minimum=0.01,
                    maximum=10.0,
                    value=0.5,
                    label="Length (m)"
                )
            
            # Plane properties
            with gr.Column(visible=False) as plane_props:
                inputs["plane_height"] = gr.Number(
                    value=0.0,
                    label="Height Offset"
                )
                with gr.Row():
                    inputs["plane_normal_x"] = gr.Number(value=0.0, label="Normal X")
                    inputs["plane_normal_y"] = gr.Number(value=0.0, label="Normal Y")
                    inputs["plane_normal_z"] = gr.Number(value=1.0, label="Normal Z")
            
            # Mesh properties
            with gr.Column(visible=False) as mesh_props:
                inputs["mesh_file"] = gr.File(label="Mesh File (.obj)")
                inputs["mesh_scale"] = gr.Slider(
                    minimum=0.01,
                    maximum=10.0,
                    value=1.0,
                    label="Scale"
                )
                inputs["use_convex"] = gr.Checkbox(
                    value=False,
                    label="Use Convex Decomposition"
                )
                inputs["max_convex"] = gr.Slider(
                    minimum=1,
                    maximum=20,
                    value=10,
                    step=1,
                    label="Max Convex Pieces",
                    visible=False
                )
        
        # Collision Properties
        with gr.Column() as collision_props:
            gr.Markdown("### Collision Properties")
            inputs["collision_enabled"] = gr.Checkbox(
                value=True,
                label="Enable Collision"
            )
            inputs["collision_margin"] = gr.Slider(
                minimum=0.0,
                maximum=0.1,
                value=0.01,
                label="Collision Margin"
            )
            inputs["collision_group"] = gr.Number(
                value=0,
                label="Collision Group",
                step=1
            )
        
        # Status output
        outputs["create_status"] = gr.Textbox(
            label="Creation Status",
            interactive=False,
            show_label=True
        )
        
        # Create button
        inputs["create_btn"] = gr.Button("Create Object", variant="primary")
        
        # Show/hide appropriate property sections based on object type
        def update_property_visibility(obj_type):
            return {
                sphere_props: obj_type == "Sphere",
                box_props: obj_type == "Box",
                capsule_props: obj_type == "Capsule",
                plane_props: obj_type == "Plane",
                mesh_props: obj_type == "Mesh"
            }
        
        inputs["object_type"].change(
            fn=update_property_visibility,
            inputs=[inputs["object_type"]],
            outputs=[sphere_props, box_props, capsule_props, plane_props, mesh_props]
        )
        
        # Show/hide max convex pieces slider based on convex decomposition checkbox
        inputs["use_convex"].change(
            fn=lambda x: {"visible": x},
            inputs=[inputs["use_convex"]],
            outputs=[inputs["max_convex"]]
        )
    
    return inputs, outputs, panel
