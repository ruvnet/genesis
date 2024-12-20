import gradio as gr
from ui import create_app

if __name__ == "__main__":
    # Create and launch the Gradio interface
    demo = create_app()
    
    # Launch with queue for handling concurrent requests
    demo.queue().launch(
        server_name="0.0.0.0",  # Allow external connections
        server_port=8080,
        share=True,  # Create public URL
        show_error=True  # Show detailed error messages
    )
