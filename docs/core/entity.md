# Entity

An Entity represents a physical object in the Genesis simulation. It combines geometry (morph), material properties, and dynamic behavior.

## Creation

Entities are created through the Scene's add_entity method:

```python
# Basic entity creation
entity = scene.add_entity(
    gs.morphs.Sphere(
        pos=(0, 0, 1),
        radius=0.2
    )
)

# Entity with specific material
entity = scene.add_entity(
    gs.morphs.Box(
        pos=(0, 0, 1),
        size=(1, 1, 1)
    ),
    material=gs.materials.Rigid(
        density=1000.0,
        friction=0.5
    )
)
```

## Properties

### Transform
```python
# Get position
pos = entity.get_pos()

# Set position
entity.set_pos((1, 0, 0))

# Get orientation (quaternion)
quat = entity.get_quat()

# Set orientation (Euler angles)
entity.set_euler((0, 0, 90))

# Get/set velocity
vel = entity.get_vel()
entity.set_vel((1, 0, 0))

# Get/set angular velocity
ang_vel = entity.get_ang_vel()
entity.set_ang_vel((0, 0, 1))
```

### State
```python
# Mass properties
mass = entity.get_mass()
inertia = entity.get_inertia()

# Momentum
linear_momentum = entity.get_linear_momentum()
angular_momentum = entity.get_angular_momentum()

# Energy
kinetic_energy = entity.get_kinetic_energy()
potential_energy = entity.get_potential_energy()
```

### Forces
```python
# Apply force
entity.apply_force(
    force=(10, 0, 0),
    pos=(0, 0, 0)  # Application point
)

# Apply impulse
entity.apply_impulse(
    impulse=(0, 5, 0),
    pos=(0, 0, 0)
)

# Apply torque
entity.apply_torque((0, 0, 1))
```

## Entity Types

### Rigid Body
```python
rigid = scene.add_entity(
    gs.morphs.Box(size=(1, 1, 1)),
    material=gs.materials.Rigid(
        density=1000.0,
        friction=0.5,
        restitution=0.5
    )
)
```

### Deformable Body
```python
soft = scene.add_entity(
    gs.morphs.Mesh(file="model.obj"),
    material=gs.materials.Deformable(
        density=1000.0,
        youngs_modulus=1e5,
        poissons_ratio=0.3
    )
)
```

### Articulated Body
```python
robot = scene.add_entity(
    gs.morphs.URDF(
        file="robot.urdf",
        fixed=True
    )
)

# Access joints
joint = robot.joints[0]
joint.set_target_position(1.57)
joint.set_target_velocity(1.0)
```

## Interactions

### Collision Groups
```python
# Set collision group
entity.set_collision_group(1)

# Filter collisions
entity.set_collision_mask(0b0011)  # Collide with groups 0 and 1
```

### Constraints
```python
# Fixed constraint
scene.add_constraint(
    gs.constraints.Fixed(
        entity1=obj1,
        entity2=obj2
    )
)

# Distance constraint
scene.add_constraint(
    gs.constraints.Distance(
        entity1=obj1,
        entity2=obj2,
        distance=1.0
    )
)
```

## Entity Management

### Lifecycle
```python
# Remove entity
scene.remove_entity(entity)

# Enable/disable
entity.set_enabled(False)
entity.set_enabled(True)

# Check state
is_active = entity.is_enabled()
```

### Queries
```python
# Check collision
is_colliding = entity.is_colliding()

# Get contacts
contacts = entity.get_contacts()

# Get nearby entities
nearby = entity.get_nearby_entities(radius=1.0)
```

## Best Practices

1. Entity Creation:
   - Use appropriate morph for geometry
   - Set realistic material properties
   - Consider collision performance

2. State Management:
   - Update transforms carefully
   - Handle velocity changes smoothly
   - Monitor energy conservation

3. Performance:
   - Minimize dynamic entities
   - Use efficient collision shapes
   - Batch state updates

4. Stability:
   - Apply forces gradually
   - Use appropriate constraints
   - Monitor numerical errors

## Example Configurations

### Game Character
```python
character = scene.add_entity(
    gs.morphs.Capsule(
        radius=0.5,
        height=2.0
    ),
    material=gs.materials.Rigid(
        density=1000.0,
        friction=0.5
    )
)
character.set_collision_group(1)
```

### Robot Joint
```python
joint = robot.joints[0]
joint.set_control_mode("position")
joint.set_gains(kp=100.0, kd=10.0)
joint.set_limits(
    position=(-3.14, 3.14),
    velocity=(-10.0, 10.0)
)
```

### Soft Object
```python
cloth = scene.add_entity(
    gs.morphs.Mesh(file="cloth.obj"),
    material=gs.materials.PBD(
        density=100.0,
        stiffness=1.0
    )
)
cloth.set_damping(0.1)
```

## Common Issues and Solutions

### Physics Issues
- Check mass properties
- Verify collision shapes
- Adjust material properties
- Monitor energy levels

### Performance
- Optimize collision geometry
- Use appropriate entity types
- Manage active entities
- Profile state updates

### Stability
- Control force magnitudes
- Use stable constraints
- Monitor numerical drift
- Handle edge cases
