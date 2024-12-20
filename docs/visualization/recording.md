# Recording and Frame Capture

Genesis provides several ways to capture and save simulation output, from single frames to complete videos.

## Camera Recording

### Basic Video Recording

```python
# Add camera
camera = scene.add_camera(
    res=(640, 480),
    pos=(3.5, 0.0, 2.5),
    lookat=(0.0, 0.0, 0.5)
)

# Start recording
camera.start_recording()

# Run simulation
for i in range(120):
    scene.step()
    camera.render()

# Save video
camera.stop_recording(save_to_filename="output.mp4", fps=60)
```

### Recording with Moving Camera

```python
camera.start_recording()

for i in range(120):
    scene.step()
    
    # Update camera position to orbit scene
    camera.set_pose(
        pos=(3.0 * np.sin(i / 60), 3.0 * np.cos(i / 60), 2.5),
        lookat=(0, 0, 0.5)
    )
    
    camera.render()

camera.stop_recording(save_to_filename="orbit.mp4", fps=60)
```

## Frame Capture

### Single Frame Capture

```python
# Render single frame with different outputs
rgb = camera.render(rgb=True)
depth = camera.render(depth=True)
segmentation = camera.render(segmentation=True)
normal = camera.render(normal=True)

# Save frames
import imageio
imageio.imwrite("frame_rgb.png", rgb)
imageio.imwrite("frame_depth.png", depth)
imageio.imwrite("frame_segmentation.png", segmentation)
imageio.imwrite("frame_normal.png", normal)
```

### Frame Sequence Capture

```python
import os
import imageio

# Create output directory
os.makedirs("frames", exist_ok=True)

# Capture frame sequence
for i in range(120):
    scene.step()
    
    # Render and save frame
    rgb = camera.render(rgb=True)
    imageio.imwrite(f"frames/frame_{i:04d}.png", rgb)
```

### Combining Frames into Video

```python
import imageio

# Read frames
frames = []
for i in range(120):
    frame = imageio.imread(f"frames/frame_{i:04d}.png")
    frames.append(frame)

# Save video
with imageio.get_writer("output.mp4", fps=60) as writer:
    for frame in frames:
        writer.append_data(frame)
```

## Multi-Camera Recording

```python
# Add multiple cameras
camera1 = scene.add_camera(
    res=(640, 480),
    pos=(3.5, 0.0, 2.5),
    lookat=(0.0, 0.0, 0.5)
)

camera2 = scene.add_camera(
    res=(640, 480),
    pos=(0.0, 3.5, 2.5),
    lookat=(0.0, 0.0, 0.5)
)

# Start recording both cameras
camera1.start_recording()
camera2.start_recording()

# Run simulation
for i in range(120):
    scene.step()
    camera1.render()
    camera2.render()

# Save videos
camera1.stop_recording(save_to_filename="view1.mp4", fps=60)
camera2.stop_recording(save_to_filename="view2.mp4", fps=60)
```

## Best Practices

1. Memory Management:
   - Clear recorded frames when not needed
   - Use appropriate resolution for output
   - Consider frame sequence for large recordings

2. File Organization:
   - Create dedicated output directories
   - Use consistent naming conventions
   - Include timestamp or version in filenames

3. Quality Settings:
   - Adjust resolution based on needs
   - Set appropriate FPS for smooth playback
   - Consider compression settings

4. Error Handling:
   - Check disk space before recording
   - Verify output directories exist
   - Handle recording failures gracefully

## Common Issues and Solutions

### Memory Issues
```python
# Save frames directly instead of accumulating
for i in range(120):
    scene.step()
    rgb = camera.render(rgb=True)
    imageio.imwrite(f"frames/frame_{i:04d}.png", rgb)
```

### Quality Control
```python
# Higher quality recording
camera = scene.add_camera(
    res=(1920, 1080),  # Full HD
    pos=(3.5, 0.0, 2.5),
    lookat=(0.0, 0.0, 0.5)
)

camera.start_recording()
# ... simulation steps ...
camera.stop_recording(
    save_to_filename="high_quality.mp4",
    fps=60
)
```

### Headless Recording
```python
scene = gs.Scene(
    show_viewer=False,
    vis_options=gs.options.VisOptions(
        ambient_light=(0.5, 0.5, 0.5)
    )
)

camera = scene.add_camera(
    res=(640, 480),
    pos=(3.5, 0.0, 2.5),
    lookat=(0.0, 0.0, 0.5)
)

# Record frames in headless mode
camera.start_recording()
# ... simulation steps ...
camera.stop_recording(save_to_filename="headless_output.mp4", fps=60)
