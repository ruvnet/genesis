# Scene

The Scene class is the main container for a Genesis simulation. It manages entities, physics, and visualization.

## Constructor

```python
gs.Scene(
    show_viewer: bool = True,
    sim_options: SimOptions = None,
    vis_options: VisOptions = None,
    renderer: Renderer = None
)
```

### Parameters

- `show_viewer` (bool): Whether to show the real-time viewer window
- `sim_options` (SimOptions): Physics simulation settings
- `vis_options` (VisOptions): Visualization settings
- `renderer` (Renderer): Renderer to use (Rasterizer or RayTracer)

## Methods

### add_entity

```python
def add_entity(self, morph: Morph) -> Entity
```

Adds a physical entity to the scene.

Parameters:
- `morph`: The shape and properties of the entity (e.g., Plane, Sphere, URDF, MJCF)

Returns:
- `Entity`: The created entity object

### add_camera

```python
def add_camera(
    self,
    res: Tuple[int, int] = (1280, 720),
    pos: Tuple[float, float, float] = (0, 0, 0),
    lookat: Tuple[float, float, float] = (0, 0, 0),
    fov: float = 40,
    GUI: bool = False
) -> Camera
```

Adds a camera to the scene for visualization/recording.

Parameters:
- `res`: Resolution (width, height) in pixels
- `pos`: Camera position in world coordinates
- `lookat`: Point the camera looks at
- `fov`: Field of view in degrees
- `GUI`: Whether to show camera controls in GUI

Returns:
- `Camera`: The created camera object

### build

```python
def build(self)
```

Initializes the scene and prepares for simulation. Must be called after adding entities and before stepping the simulation.

### step

```python
def step(self)
```

Advances the simulation by one timestep.

## Example Usage

```python
import genesis as gs

# Initialize Genesis
gs.init(backend=gs.cpu)  # or gs.cuda if available

# Create a scene
scene = gs.Scene(
    show_viewer=True,
    sim_options=gs.options.SimOptions(
        dt=0.01,
        gravity=(0, 0, -9.81)
    ),
    vis_options=gs.options.VisOptions(
        show_world_frame=True,
        ambient_light=(0.5, 0.5, 0.5)
    )
)

# Add entities
plane = scene.add_entity(gs.morphs.Plane())
sphere = scene.add_entity(
    gs.morphs.Sphere(
        pos=(0, 0, 1),
        radius=0.2
    )
)

# Add camera
camera = scene.add_camera(
    res=(640, 480),
    pos=(3.5, 0.0, 2.5),
    lookat=(0.0, 0.0, 0.5)
)

# Build and run simulation
scene.build()

# Simulation loop
for i in range(120):
    scene.step()
```

## Common Options

### SimOptions

```python
gs.options.SimOptions(
    dt: float = 0.01,          # Timestep size
    substeps: int = 1,         # Physics substeps per frame
    gravity: tuple = (0,0,-9.81), # Gravity vector
    floor_height: float = 0.0,  # Height of ground plane
    requires_grad: bool = False # Enable gradients for differentiable physics
)
```

### VisOptions

```python
gs.options.VisOptions(
    show_world_frame: bool = True,    # Show coordinate axes
    world_frame_size: float = 1.0,    # Size of coordinate axes
    show_link_frame: bool = False,    # Show frames for articulated bodies
    show_cameras: bool = False,       # Show camera frustums
    plane_reflection: bool = True,    # Enable reflections on ground plane
    ambient_light: tuple = (0.1, 0.1, 0.1)  # Ambient light color
)
```

## Notes

- The Scene must be built with `build()` before running simulation steps
- Entities and cameras should be added before building the scene
- The simulation loop can be controlled with custom conditions or run indefinitely
- Camera positions can be updated during simulation with `camera.set_pose()`
- Scene state can be saved/loaded for checkpointing
