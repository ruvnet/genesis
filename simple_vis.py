import genesis as gs
import numpy as np
import os

# Configure OpenGL to use EGL for headless rendering
os.environ['PYOPENGL_PLATFORM'] = 'egl'

# Initialize Genesis
print("Initializing Genesis...")
gs.init(backend=gs.cpu)

# Create scene with minimal options
print("Creating scene...")
scene = gs.Scene(
    show_viewer=False,  # Disable viewer since we're in headless mode
    sim_options=gs.options.SimOptions(
        dt=1/60,
        substeps=1,
        gravity=(0, 0, -9.81)
    ),
    renderer=gs.renderers.Rasterizer()  # Use rasterizer for basic rendering
)

# Add a ground plane
print("Adding ground plane...")
plane = scene.add_entity(
    gs.morphs.Plane(),
    material=gs.materials.Diffuse(color=(0.8, 0.8, 0.8))  # Light gray
)

# Add a sphere
print("Adding sphere...")
sphere = scene.add_entity(
    gs.morphs.Sphere(
        pos=(0, 0, 2),
        radius=0.1
    ),
    material=gs.materials.Diffuse(color=(0.2, 0.5, 1.0))  # Blue
)

# Add camera
print("Adding camera...")
cam = scene.add_camera(
    res=(640, 480),
    pos=(3.5, 0.0, 2.5),
    lookat=(0, 0, 0.5),
    fov=30,
    GUI=False,
)

print("Building scene...")
scene.build()

print("Starting recording...")
cam.start_recording()

print("Running simulation...")
for i in range(60):  # 1 second at 60 FPS
    scene.step()
    pos = sphere.get_pos()
    print(f"\rFrame {i+1}/60: Sphere position = {pos}", end="", flush=True)
    cam.render()

print("\nSaving video...")
cam.stop_recording(save_to_filename='sphere_fall.mp4', fps=60)
print("Done! Video saved as sphere_fall.mp4")
