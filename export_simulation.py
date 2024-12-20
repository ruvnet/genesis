import genesis as gs
import numpy as np
import torch
import os
import imageio

def main():
    # Create output directory for frames
    os.makedirs("frames", exist_ok=True)
    
    # Initialize Genesis with CPU backend
    gs.init(backend=gs.cpu, seed=0, precision="32", logging_level="debug")
    
    # Configure OpenGL for headless rendering
    os.environ['PYOPENGL_PLATFORM'] = 'osmesa'
    os.environ['LIBGL_ALWAYS_INDIRECT'] = '0'
    
    # Create scene with ray tracer renderer instead of rasterizer
    scene = gs.Scene(
        show_viewer=False,
        sim_options=gs.options.SimOptions(
            dt=1/60,
            substeps=1,
            gravity=(0, 0, -9.81)
        ),
        renderer=gs.renderers.RayTracer(
            samples_per_pixel=1,  # Low samples for faster rendering
            max_bounces=2
        )
    )

    # Add camera with good viewing angle
    camera = scene.add_camera(
        res=(1280, 720),  # HD resolution
        pos=(3.5, 0.0, 2.5),
        lookat=(0.0, 0.0, 0.5)
    )

    # Add a ground plane
    plane = scene.add_entity(
        gs.morphs.Plane(),
        material=gs.materials.Diffuse(color=(0.8, 0.8, 0.8))  # Light gray color
    )

    # Add a sphere to simulate
    sphere = scene.add_entity(
        gs.morphs.Sphere(
            pos=(0, 0, 2),
            radius=0.1
        ),
        material=gs.materials.Diffuse(color=(0.2, 0.5, 1.0))  # Blue color
    )

    # Add lighting
    scene.add_light(
        gs.lights.Point(
            pos=(5, 5, 5),
            color=(1, 1, 1),
            intensity=100
        )
    )

    # Build scene
    scene.build()

    frames = []
    print("Starting simulation and frame capture...")

    # Run simulation for 5 seconds (300 frames at 60 FPS)
    for i in range(300):
        scene.step()
        
        # Render and save frame
        frame = camera.render(rgb=True)
        frames.append(frame)
        
        if i % 60 == 0:  # Progress update every second
            print(f"Processed {i}/300 frames")

    print("Saving video...")
    # Save frames as video using imageio
    with imageio.get_writer("simulation_output.mp4", fps=60) as writer:
        for frame in frames:
            writer.append_data(frame)

    print("Simulation recording completed. Output saved as 'simulation_output.mp4'")

if __name__ == "__main__":
    main()
