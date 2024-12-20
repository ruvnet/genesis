# Morphs

Morphs define the geometric shapes and properties of entities in Genesis simulations. They range from simple primitives to complex meshes and articulated bodies.

## Basic Primitives

### Plane
```python
# Infinite ground plane
plane = scene.add_entity(
    gs.morphs.Plane(
        height=0.0,  # Height offset
        normal=(0, 0, 1)  # Up direction
    )
)
```

### Sphere
```python
# Simple sphere
sphere = scene.add_entity(
    gs.morphs.Sphere(
        pos=(0, 0, 1),  # Position
        radius=0.2,     # Radius
        density=1000.0  # Optional material property
    )
)
```

### Box
```python
# Rectangular box
box = scene.add_entity(
    gs.morphs.Box(
        pos=(0, 0, 1),
        size=(1.0, 0.5, 0.2),  # Width, depth, height
        density=1000.0
    )
)
```

### Capsule
```python
# Capsule (cylinder with rounded ends)
capsule = scene.add_entity(
    gs.morphs.Capsule(
        pos=(0, 0, 1),
        radius=0.1,
        length=0.5,
        orientation=(1, 0, 0)  # Axis direction
    )
)
```

## Complex Geometries

### Mesh
```python
# Custom mesh from file
mesh = scene.add_entity(
    gs.morphs.Mesh(
        file="models/object.obj",
        scale=1.0,
        pos=(0, 0, 0),
        orientation=(0, 0, 0)
    )
)
```

### URDF Robot
```python
# Articulated robot from URDF
robot = scene.add_entity(
    gs.morphs.URDF(
        file="robots/panda.urdf",
        fixed=True,  # Fixed base
        pos=(0, 0, 0)
    )
)
```

### MJCF Model
```python
# MuJoCo model
model = scene.add_entity(
    gs.morphs.MJCF(
        file="models/humanoid.xml",
        pos=(0, 0, 0)
    )
)
```

## Compound Shapes

### Convex Decomposition
```python
# Automatic convex decomposition of mesh
convex = scene.add_entity(
    gs.morphs.Mesh(
        file="model.obj",
        convex=True,  # Enable convex decomposition
        max_convex_pieces=10
    )
)
```

### Multi-Body System
```python
# Connected bodies
system = scene.add_entity(
    gs.morphs.MultiBody(
        bodies=[
            gs.morphs.Sphere(radius=0.1),
            gs.morphs.Box(size=(0.2, 0.2, 0.2))
        ],
        joints=[
            gs.morphs.Joint(type="revolute", axis=(0, 0, 1))
        ]
    )
)
```

## Morph Properties

### Transform
- `pos`: Position in world coordinates
- `orientation`: Rotation (Euler angles or quaternion)
- `scale`: Size scaling factor

### Physics
- `density`: Material density
- `mass`: Override computed mass
- `inertia`: Custom inertia tensor

### Collision
- `collision`: Enable/disable collision
- `collision_margin`: Contact margin
- `collision_group`: Collision filtering

## Best Practices

1. Geometry Selection:
   - Use simplest shape possible
   - Consider collision performance
   - Balance accuracy vs speed

2. Mesh Optimization:
   - Clean up imported meshes
   - Use convex decomposition
   - Optimize vertex count

3. Scale Considerations:
   - Use consistent units
   - Consider numerical precision
   - Avoid extreme size differences

4. Performance Tips:
   - Prefer primitives over meshes
   - Use compound shapes carefully
   - Optimize collision geometry

## Example Configurations

### Simple Object
```python
# Basic physics object
ball = scene.add_entity(
    gs.morphs.Sphere(
        pos=(0, 0, 1),
        radius=0.2,
        density=1000.0
    )
)
```

### Robot Arm
```python
# Articulated robot
arm = scene.add_entity(
    gs.morphs.URDF(
        file="robots/arm.urdf",
        fixed=True,
        pos=(0, 0, 0),
        joint_damping=0.1
    )
)
```

### Game Physics
```python
# Optimized game object
game_obj = scene.add_entity(
    gs.morphs.Mesh(
        file="models/character.obj",
        convex=True,
        max_convex_pieces=8,
        collision_margin=0.01
    )
)
```

## Common Issues and Solutions

### Mesh Problems
- Clean mesh topology
- Fix non-manifold geometry
- Ensure proper scaling
- Check UV coordinates

### Collision Issues
- Adjust collision margins
- Verify collision groups
- Check mesh convexity
- Consider compound shapes

### Performance
- Simplify collision geometry
- Use appropriate primitives
- Optimize mesh complexity
- Balance detail levels

### Stability
- Check mass properties
- Verify joint limits
- Test extreme poses
- Consider numerical precision
