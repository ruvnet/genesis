# Renderers

Genesis provides two main rendering backends: Rasterizer and RayTracer. Each has its own advantages and use cases.

## Rasterizer

The default renderer using OpenGL for fast real-time rendering.

```python
gs.renderers.Rasterizer()
```

### Features
- Fast real-time rendering
- Hardware acceleration
- Basic lighting and shadows
- Suitable for interactive visualization

### Limitations
- Requires OpenGL support
- Limited visual quality compared to ray tracing
- May have issues in headless environments

### Usage Example

```python
scene = gs.Scene(
    show_viewer=True,
    renderer=gs.renderers.Rasterizer(),
    vis_options=gs.options.VisOptions(
        show_world_frame=True,
        ambient_light=(0.5, 0.5, 0.5)
    )
)
```

## RayTracer

Advanced renderer using LuisaRender for high-quality offline rendering.

```python
gs.renderers.RayTracer(
    tracing_depth: int = 32,
    rr_depth: int = 0,
    rr_threshold: float = 0.95,
    env_radius: float = 1000.0
)
```

### Parameters
- `tracing_depth`: Maximum ray bounces
- `rr_depth`: Russian roulette depth for path termination
- `rr_threshold`: Russian roulette threshold
- `env_radius`: Environment map radius

### Features
- High-quality rendering
- Global illumination
- Physically based materials
- Better reflections and shadows

### Limitations
- Slower than rasterization
- Requires LuisaRender installation
- Higher memory usage

### Usage Example

```python
scene = gs.Scene(
    show_viewer=False,  # Typically used for offline rendering
    renderer=gs.renderers.RayTracer(
        tracing_depth=2,
        rr_depth=2,
        rr_threshold=0.8,
        env_radius=10.0
    )
)
```

## Headless Rendering

For environments without display access:

1. Use `show_viewer=False` in Scene constructor
2. Render to images/video instead of display:

```python
# Add camera
camera = scene.add_camera(
    res=(640, 480),
    pos=(3.5, 0.0, 2.5),
    lookat=(0.0, 0.0, 0.5)
)

# Option 1: Save individual frames
rgb = camera.render(rgb=True)
import imageio
imageio.imwrite("frame.png", rgb)

# Option 2: Record video
camera.start_recording()
for i in range(120):
    scene.step()
    camera.render()
camera.stop_recording(save_to_filename="video.mp4", fps=60)
```

## Environment Setup

### OpenGL (Rasterizer)
- Requires working OpenGL installation
- May need X server or virtual framebuffer (xvfb) in headless environments
- Consider using EGL/OSMesa for headless rendering

### LuisaRender (RayTracer)
- Requires LuisaRender installation
- CUDA GPU recommended for performance
- Can work in headless environments

## Best Practices

1. Choose renderer based on needs:
   - Rasterizer for real-time visualization
   - RayTracer for high-quality offline rendering

2. For headless environments:
   - Always use `show_viewer=False`
   - Save to files instead of displaying
   - Consider using RayTracer if OpenGL is problematic

3. Memory management:
   - Lower resolution for real-time preview
   - Higher resolution for final renders
   - Clear recorded frames when not needed

4. Error handling:
   - Catch rendering exceptions
   - Provide fallback options
   - Log rendering issues for debugging
