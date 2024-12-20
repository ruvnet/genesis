# Options

Genesis uses various option classes to configure simulation components. These options provide fine-grained control over physics, visualization, and system behavior.

## Simulation Options

### SimOptions
Controls core simulation parameters.

```python
gs.options.SimOptions(
    dt: float = 0.01,          # Timestep size
    substeps: int = 1,         # Physics substeps per frame
    gravity: tuple = (0,0,-9.81), # Gravity vector
    floor_height: float = 0.0,  # Height of ground plane
    requires_grad: bool = False # Enable gradients for differentiable physics
)
```

Example usage:
```python
scene = gs.Scene(
    sim_options=gs.options.SimOptions(
        dt=0.01,
        substeps=2,
        gravity=(0, 0, -9.81)
    )
)
```

## Visualization Options

### ViewerOptions
Controls the viewer window and camera settings.

```python
gs.options.ViewerOptions(
    res: Tuple[int, int] = (1280, 960),  # Window resolution
    camera_pos: Tuple[float, float, float] = (3.5, 0.0, 2.5),
    camera_lookat: Tuple[float, float, float] = (0.0, 0.0, 0.5),
    camera_fov: float = 40,  # Field of view in degrees
    max_FPS: int = 60       # Maximum frames per second
)
```

Example usage:
```python
scene = gs.Scene(
    viewer_options=gs.options.ViewerOptions(
        res=(1280, 720),
        camera_pos=(3.5, 0.0, 2.5),
        camera_fov=40
    )
)
```

### VisOptions
Controls visual elements and rendering settings.

```python
gs.options.VisOptions(
    show_world_frame: bool = True,    # Show coordinate axes
    world_frame_size: float = 1.0,    # Size of coordinate axes
    show_link_frame: bool = False,    # Show frames for articulated bodies
    show_cameras: bool = False,       # Show camera frustums
    plane_reflection: bool = True,    # Enable reflections on ground plane
    ambient_light: Tuple[float, float, float] = (0.1, 0.1, 0.1)
)
```

Example usage:
```python
scene = gs.Scene(
    vis_options=gs.options.VisOptions(
        show_world_frame=True,
        ambient_light=(0.5, 0.5, 0.5)
    )
)
```

## Physics Options

### MaterialOptions
Configures material properties.

```python
gs.options.MaterialOptions(
    density: float = 1000.0,    # Mass per unit volume
    friction: float = 0.5,      # Friction coefficient
    restitution: float = 0.5,   # Bounciness
    youngs_modulus: float = 1e5, # Stiffness
    poissons_ratio: float = 0.3  # Volume preservation
)
```

### SolverOptions
Controls physics solver behavior.

```python
gs.options.SolverOptions(
    iterations: int = 10,       # Solver iterations
    tolerance: float = 1e-6,    # Convergence tolerance
    warm_start: bool = True,    # Use previous solution
    stabilization: bool = True  # Enable stabilization
)
```

## Coupling Options

### CouplerOptions
Controls interaction between different physics systems.

```python
gs.options.CouplerOptions(
    rigid_mpm: bool = False,    # Rigid-MPM coupling
    rigid_sph: bool = False,    # Rigid-SPH coupling
    rigid_pbd: bool = False,    # Rigid-PBD coupling
    sph_mpm: bool = False,      # SPH-MPM coupling
    mpm_pbd: bool = False       # MPM-PBD coupling
)
```

Example usage:
```python
scene = gs.Scene(
    coupler_options=gs.options.CouplerOptions(
        rigid_mpm=True,
        rigid_sph=True
    )
)
```

## Common Configurations

### Real-time Simulation
```python
scene = gs.Scene(
    sim_options=gs.options.SimOptions(
        dt=0.016,  # 60 FPS
        substeps=2
    ),
    viewer_options=gs.options.ViewerOptions(
        res=(1280, 720),
        max_FPS=60
    )
)
```

### Scientific Computing
```python
scene = gs.Scene(
    sim_options=gs.options.SimOptions(
        dt=0.001,
        substeps=10,
        requires_grad=True
    ),
    solver_options=gs.options.SolverOptions(
        iterations=20,
        tolerance=1e-8
    )
)
```

### Headless Rendering
```python
scene = gs.Scene(
    show_viewer=False,
    vis_options=gs.options.VisOptions(
        show_world_frame=False,
        ambient_light=(0.5, 0.5, 0.5)
    )
)
```

## Best Practices

1. Option Selection:
   - Choose appropriate defaults
   - Override only needed values
   - Consider dependencies

2. Performance Impact:
   - Balance quality vs speed
   - Monitor resource usage
   - Profile critical settings

3. Stability:
   - Start with conservative values
   - Test extreme settings
   - Validate combinations

4. Compatibility:
   - Check version requirements
   - Verify feature support
   - Test platform differences

## Common Issues and Solutions

### Performance
- Reduce visual quality
- Decrease physics accuracy
- Optimize update rates
- Balance resource usage

### Stability
- Adjust timestep
- Increase iterations
- Tune tolerances
- Add stabilization

### Visual Quality
- Increase resolution
- Adjust lighting
- Enable reflections
- Fine-tune materials

### Memory Usage
- Reduce state limits
- Optimize buffers
- Manage resources
- Clear unused data
