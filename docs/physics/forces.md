# Forces and Force Fields

Genesis provides various ways to apply forces and create force fields that influence the behavior of simulated objects.

## Basic Forces

### Gravity
```python
# Global gravity
scene = gs.Scene(
    sim_options=gs.options.SimOptions(
        gravity=(0, 0, -9.81)  # X, Y, Z components
    )
)
```

### Applied Force
```python
# Direct force application
entity.apply_force(
    force=(10.0, 0.0, 0.0),  # Force vector
    pos=(0, 0, 0)  # Application point (world coordinates)
)
```

### Impulse
```python
# Instantaneous force
entity.apply_impulse(
    impulse=(0.0, 5.0, 0.0),  # Impulse vector
    pos=(0, 0, 0)  # Application point
)
```

## Force Fields

### Uniform Field
```python
# Constant force throughout space
field = gs.force_fields.Uniform(
    force=(0, 0, -9.81),  # Force vector
    affected_groups=[0, 1]  # Entity groups affected
)
scene.add_force_field(field)
```

### Radial Field
```python
# Force varying with distance
field = gs.force_fields.Radial(
    center=(0, 0, 0),
    strength=10.0,
    falloff=1.0,  # 1/r falloff
    radius=5.0    # Maximum effect radius
)
scene.add_force_field(field)
```

### Vortex Field
```python
# Spinning force field
field = gs.force_fields.Vortex(
    center=(0, 0, 0),
    axis=(0, 0, 1),
    strength=5.0,
    radius=2.0
)
scene.add_force_field(field)
```

## Special Forces

### Spring Force
```python
# Spring between entities
spring = gs.forces.Spring(
    entity1=obj1,
    entity2=obj2,
    stiffness=100.0,
    damping=1.0,
    rest_length=1.0
)
scene.add_force(spring)
```

### Drag Force
```python
# Air/fluid resistance
drag = gs.forces.Drag(
    coefficient=0.5,
    affected_groups=[0]
)
scene.add_force(drag)
```

### Motor Force
```python
# Rotational motor
motor = gs.forces.Motor(
    joint=robot.joints[0],
    target_velocity=1.0,
    max_torque=10.0
)
scene.add_force(motor)
```

## Time-Varying Forces

### Periodic Force
```python
# Oscillating force
def force_function(t):
    return (np.sin(t * 2 * np.pi), 0, 0)

scene.add_force(
    gs.forces.TimeVarying(
        force_func=force_function,
        affected_groups=[0]
    )
)
```

### Triggered Force
```python
# Force activated by condition
def trigger_condition(t, state):
    return state.height < 1.0

scene.add_force(
    gs.forces.Conditional(
        force=(0, 0, 10.0),
        condition=trigger_condition
    )
)
```

## Force Application Methods

### Global Forces
```python
# Affect all entities
scene.add_force_field(
    gs.force_fields.Uniform(
        force=(0, -1, 0)
    )
)
```

### Group-Specific Forces
```python
# Affect specific groups
field = gs.force_fields.Radial(
    center=(0, 0, 0),
    strength=10.0,
    affected_groups=[1, 2]
)
scene.add_force_field(field)
```

### Entity-Specific Forces
```python
# Force on single entity
entity.add_force(
    gs.forces.Constant(
        force=(1, 0, 0)
    )
)
```

## Best Practices

1. Force Magnitude:
   - Use physically realistic values
   - Consider mass scaling
   - Avoid extreme forces

2. Force Application:
   - Apply forces at appropriate points
   - Consider torque effects
   - Use impulses for instantaneous changes

3. Performance:
   - Limit force field complexity
   - Use efficient force calculations
   - Consider update frequency

4. Stability:
   - Balance opposing forces
   - Add appropriate damping
   - Consider timestep requirements

## Example Configurations

### Game Physics
```python
# Simple game forces
scene.add_force_field(
    gs.force_fields.Uniform(
        force=(0, 0, -10),  # Simplified gravity
        drag=0.1  # Basic air resistance
    )
)
```

### Scientific Simulation
```python
# Accurate physical forces
scene.add_force_field(
    gs.force_fields.Composite([
        gs.force_fields.Uniform(force=(0, 0, -9.81)),
        gs.force_fields.Drag(coefficient=1.225)  # Air density
    ])
)
```

### Interactive Demo
```python
# User-controlled force
def user_force(t):
    return get_user_input() * 10.0

scene.add_force(
    gs.forces.TimeVarying(
        force_func=user_force,
        max_force=100.0
    )
)
```

## Common Issues and Solutions

### Instability
- Reduce force magnitudes
- Add damping
- Decrease timestep
- Check force application points

### Performance
- Optimize force field calculations
- Limit affected entities
- Use simpler force models
- Consider force update frequency

### Behavior Issues
- Verify force directions
- Check group assignments
- Test edge cases
- Monitor energy conservation
