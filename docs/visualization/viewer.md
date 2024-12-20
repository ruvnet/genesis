# Viewer and Visualization Options

Genesis provides extensive options for configuring the visualization of simulations through the ViewerOptions and VisOptions classes.

## ViewerOptions

Controls the viewer window and camera settings.

```python
gs.options.ViewerOptions(
    res: Tuple[int, int] = (1280, 960),
    camera_pos: Tuple[float, float, float] = (3.5, 0.0, 2.5),
    camera_lookat: Tuple[float, float, float] = (0.0, 0.0, 0.5),
    camera_fov: float = 40,
    max_FPS: int = 60
)
```

### Parameters

- `res`: Window resolution (width, height) in pixels
- `camera_pos`: Default camera position in world coordinates
- `camera_lookat`: Default camera target point
- `camera_fov`: Field of view in degrees
- `max_FPS`: Maximum frames per second for viewer

### Usage Example

```python
scene = gs.Scene(
    show_viewer=True,
    viewer_options=gs.options.ViewerOptions(
        res=(1280, 960),
        camera_pos=(3.5, 0.0, 2.5),
        camera_lookat=(0.0, 0.0, 0.5),
        camera_fov=40,
        max_FPS=60
    )
)
```

## VisOptions

Controls visual elements and rendering settings.

```python
gs.options.VisOptions(
    show_world_frame: bool = True,
    world_frame_size: float = 1.0,
    show_link_frame: bool = False,
    show_cameras: bool = False,
    plane_reflection: bool = True,
    ambient_light: Tuple[float, float, float] = (0.1, 0.1, 0.1)
)
```

### Parameters

- `show_world_frame`: Show coordinate axes
- `world_frame_size`: Size of coordinate axes
- `show_link_frame`: Show frames for articulated bodies
- `show_cameras`: Show camera frustums in scene
- `plane_reflection`: Enable reflections on ground plane
- `ambient_light`: Ambient light color (RGB, 0-1 range)

### Usage Example

```python
scene = gs.Scene(
    show_viewer=True,
    vis_options=gs.options.VisOptions(
        show_world_frame=True,
        world_frame_size=1.0,
        plane_reflection=True,
        ambient_light=(0.5, 0.5, 0.5)
    )
)
```

## Interactive Controls

When `show_viewer=True`, the following controls are available:

### Camera Controls
- Left Mouse: Rotate camera
- Right Mouse: Pan camera
- Mouse Wheel: Zoom in/out
- Middle Mouse: Reset camera

### Keyboard Shortcuts
- Space: Play/Pause simulation
- R: Reset simulation
- ESC: Exit viewer
- F: Focus on selected object
- C: Toggle camera controls

## Headless Mode

When running without a display (`show_viewer=False`):

```python
scene = gs.Scene(
    show_viewer=False,
    vis_options=gs.options.VisOptions(
        show_world_frame=True,
        ambient_light=(0.5, 0.5, 0.5)
    )
)

# Add camera for rendering
camera = scene.add_camera(
    res=(640, 480),
    pos=(3.5, 0.0, 2.5),
    lookat=(0.0, 0.0, 0.5)
)

# Render frames programmatically
rgb = camera.render(rgb=True)
```

## Best Practices

1. Resolution and Performance:
   - Lower resolution for development/preview
   - Higher resolution for final renders
   - Adjust max_FPS based on simulation complexity

2. Camera Settings:
   - Choose camera_pos to show relevant parts of scene
   - Adjust camera_fov for desired perspective
   - Use camera.set_pose() for dynamic views

3. Visual Clarity:
   - Use show_world_frame for spatial reference
   - Adjust ambient_light for proper visibility
   - Enable show_link_frame for debugging articulated bodies

4. Memory Management:
   - Disable unused visual features
   - Clear rendered frames when not needed
   - Consider headless mode for batch processing

## Common Configurations

### Development Setup
```python
vis_options = gs.options.VisOptions(
    show_world_frame=True,
    show_link_frame=True,
    show_cameras=True,
    ambient_light=(0.5, 0.5, 0.5)
)
```

### Production Rendering
```python
vis_options = gs.options.VisOptions(
    show_world_frame=False,
    plane_reflection=True,
    ambient_light=(0.1, 0.1, 0.1)
)
```

### Debug View
```python
vis_options = gs.options.VisOptions(
    show_world_frame=True,
    show_link_frame=True,
    show_cameras=True,
    plane_reflection=False,
    ambient_light=(1.0, 1.0, 1.0)
)
