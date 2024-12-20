# Physics Solvers

Genesis provides multiple physics solvers for different types of simulations. Each solver is optimized for specific types of physics phenomena.

## Available Solvers

### Rigid Body Solver

```python
# Basic rigid body simulation
scene = gs.Scene(
    sim_options=gs.options.SimOptions(
        dt=0.01,
        gravity=(0, 0, -9.81)
    )
)
```

Best for:
- Solid objects with no deformation
- Articulated bodies (robots, mechanisms)
- Fast and stable simulations
- Real-time applications

### Material Point Method (MPM)

```python
# MPM simulation for deformable materials
scene = gs.Scene(
    sim_options=gs.options.SimOptions(
        dt=0.001,  # Smaller timestep for stability
        substeps=10
    )
)
```

Best for:
- Deformable solids
- Granular materials
- Snow simulation
- Material fracture

### Smoothed Particle Hydrodynamics (SPH)

```python
# SPH simulation for fluids
scene = gs.Scene(
    sim_options=gs.options.SimOptions(
        dt=0.001,
        substeps=5,
        requires_grad=True  # For differentiable simulation
    )
)
```

Best for:
- Liquid simulation
- Free surface flows
- Fluid-solid interaction
- Splashing effects

### Position Based Dynamics (PBD)

```python
# PBD simulation for cloth and soft bodies
scene = gs.Scene(
    sim_options=gs.options.SimOptions(
        dt=0.016,  # 60 FPS
        substeps=10
    )
)
```

Best for:
- Cloth simulation
- Rope and cable dynamics
- Real-time soft bodies
- Interactive applications

### Finite Element Method (FEM)

```python
# FEM simulation for accurate deformation
scene = gs.Scene(
    sim_options=gs.options.SimOptions(
        dt=0.001,
        substeps=20,
        requires_grad=True
    )
)
```

Best for:
- Accurate deformation
- Stress analysis
- Material engineering
- Medical simulation

## Simulation Options

Common parameters for configuring solvers:

```python
gs.options.SimOptions(
    dt: float = 0.01,          # Timestep size
    substeps: int = 1,         # Physics substeps per frame
    gravity: tuple = (0,0,-9.81), # Gravity vector
    floor_height: float = 0.0,  # Height of ground plane
    requires_grad: bool = False # Enable gradients for differentiable physics
)
```

## Multi-Physics Coupling

Genesis supports coupling between different solvers:

```python
# Coupling rigid bodies with MPM
scene = gs.Scene(
    sim_options=gs.options.SimOptions(dt=0.001),
    coupler_options=gs.options.CouplerOptions(
        rigid_mpm=True,  # Enable rigid-MPM coupling
        rigid_sph=False,
        rigid_pbd=False
    )
)
```

Available couplings:
- Rigid-MPM
- Rigid-SPH
- Rigid-PBD
- SPH-MPM
- MPM-PBD

## Best Practices

1. Solver Selection:
   - Choose based on material behavior
   - Consider performance requirements
   - Account for coupling needs

2. Timestep Selection:
   - Smaller dt for stability
   - More substeps for accuracy
   - Balance with performance

3. Performance Optimization:
   - Use appropriate solver for material
   - Adjust substeps based on needs
   - Enable gradients only when needed

4. Stability Considerations:
   - Start with conservative timesteps
   - Increase substeps for complex interactions
   - Monitor energy conservation

## Example Configurations

### Real-time Gaming Physics
```python
sim_options = gs.options.SimOptions(
    dt=0.016,  # 60 FPS
    substeps=2,
    gravity=(0, 0, -9.81)
)
```

### Scientific Simulation
```python
sim_options = gs.options.SimOptions(
    dt=0.001,
    substeps=20,
    requires_grad=True,
    gravity=(0, 0, -9.81)
)
```

### Interactive Demo
```python
sim_options = gs.options.SimOptions(
    dt=0.01,
    substeps=5,
    gravity=(0, 0, -9.81)
)
```

## Common Issues and Solutions

### Instability
- Reduce timestep
- Increase substeps
- Check for interpenetration
- Verify material parameters

### Performance
- Use appropriate solver
- Balance accuracy vs speed
- Consider GPU acceleration
- Profile and optimize hotspots

### Coupling Issues
- Verify coupling compatibility
- Adjust contact parameters
- Use consistent timesteps
- Handle boundary conditions
