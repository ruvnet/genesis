# Materials

Genesis provides various material types to define the physical properties of simulated objects. Each material type is designed to work with specific solvers and exhibit particular behaviors.

## Material Types

### Rigid Material

```python
# Basic rigid material
rigid_entity = scene.add_entity(
    gs.morphs.Sphere(
        pos=(0, 0, 1),
        material=gs.materials.Rigid(
            density=1000.0,
            friction=0.5,
            restitution=0.5
        )
    )
)
```

Properties:
- `density`: Mass per unit volume (kg/m³)
- `friction`: Friction coefficient (0-1)
- `restitution`: Bounciness (0-1)

Best for:
- Solid objects
- Non-deformable bodies
- Mechanical parts
- Robotic components

### Deformable Material

```python
# Soft deformable material
soft_entity = scene.add_entity(
    gs.morphs.Sphere(
        pos=(0, 0, 1),
        material=gs.materials.Deformable(
            density=1000.0,
            youngs_modulus=1e5,
            poissons_ratio=0.3
        )
    )
)
```

Properties:
- `density`: Mass per unit volume
- `youngs_modulus`: Stiffness
- `poissons_ratio`: Volume preservation (0-0.5)

Best for:
- Soft bodies
- Elastic objects
- Biological tissues
- Rubber-like materials

### Fluid Material

```python
# Liquid material
fluid_entity = scene.add_entity(
    gs.morphs.Sphere(
        pos=(0, 0, 1),
        material=gs.materials.Fluid(
            density=1000.0,
            viscosity=1e-3,
            surface_tension=0.072
        )
    )
)
```

Properties:
- `density`: Mass per unit volume
- `viscosity`: Flow resistance
- `surface_tension`: Surface cohesion

Best for:
- Liquids
- Gases
- Flow simulation
- Free surface flows

### Granular Material

```python
# Sand-like material
sand_entity = scene.add_entity(
    gs.morphs.Sphere(
        pos=(0, 0, 1),
        material=gs.materials.Granular(
            density=1500.0,
            friction_angle=30.0,
            cohesion=0.0
        )
    )
)
```

Properties:
- `density`: Mass per unit volume
- `friction_angle`: Internal friction
- `cohesion`: Particle adhesion

Best for:
- Sand
- Powders
- Grains
- Soil mechanics

## Material Combinations

### Multi-Material Objects

```python
# Object with different materials
composite = scene.add_entity(
    gs.morphs.Mesh(
        file="model.obj",
        materials=[
            gs.materials.Rigid(density=1000.0),
            gs.materials.Deformable(youngs_modulus=1e5)
        ],
        material_indices=[0, 0, 1, 1]  # Assign materials to parts
    )
)
```

### Material Interfaces

```python
# Coupling between different materials
scene = gs.Scene(
    coupler_options=gs.options.CouplerOptions(
        rigid_deformable=True,
        rigid_fluid=True
    )
)
```

## Common Material Properties

### Physical Properties
- `density`: Mass per unit volume
- `mass`: Total mass (computed from density × volume)
- `inertia`: Moment of inertia tensor

### Surface Properties
- `friction`: Surface friction coefficient
- `restitution`: Collision bounciness
- `adhesion`: Surface stickiness

### Thermal Properties
- `thermal_conductivity`: Heat transfer rate
- `specific_heat`: Heat capacity
- `melting_point`: Phase change temperature

## Best Practices

1. Material Selection:
   - Choose based on desired behavior
   - Consider solver compatibility
   - Account for performance impact

2. Parameter Tuning:
   - Start with physically realistic values
   - Adjust for numerical stability
   - Test extreme conditions

3. Performance Optimization:
   - Use simpler materials when possible
   - Limit material interfaces
   - Balance accuracy vs speed

4. Stability Considerations:
   - Avoid extreme property values
   - Consider timestep requirements
   - Test material combinations

## Example Configurations

### Game Physics Material
```python
game_material = gs.materials.Rigid(
    density=1000.0,
    friction=0.5,
    restitution=0.5
)
```

### Engineering Simulation
```python
engineering_material = gs.materials.Deformable(
    density=7800.0,  # Steel
    youngs_modulus=200e9,
    poissons_ratio=0.3
)
```

### Visual Effects
```python
vfx_material = gs.materials.Fluid(
    density=1000.0,
    viscosity=1e-3,
    surface_tension=0.072
)
```

## Common Issues and Solutions

### Instability
- Reduce extreme property values
- Check material compatibility
- Adjust solver parameters
- Consider numerical precision

### Performance
- Simplify material models
- Use appropriate solvers
- Optimize property ranges
- Limit material interactions

### Visual Artifacts
- Check material boundaries
- Adjust contact parameters
- Verify mesh quality
- Consider resolution effects
