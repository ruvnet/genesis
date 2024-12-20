# Genesis Physics Examples

This repository contains examples and experiments using the Genesis physics engine.

## Project Structure

- `examples/` - Example simulations and demonstrations
  - `falling_sphere.py` - Basic physics simulation of a sphere falling under gravity
- `data/` - Output directory for simulation data
- `src/` - Source code for Genesis configuration and extensions
- `tests/` - Test files

## Running Examples

To run the falling sphere example:

```bash
python examples/falling_sphere.py
```

The simulation will output trajectory data to the `data/` directory.

## Example Descriptions

### Falling Sphere (`examples/falling_sphere.py`)
A basic physics simulation demonstrating:
- Automatic CPU/GPU backend selection
- Rigid body physics with gravity
- Collision detection with a ground plane
- Data collection and analysis
- CSV output for trajectory visualization

Key simulation parameters:
- Time step (dt): 0.01s
- Gravity: -9.81 m/s²
- Sphere radius: 0.2m
- Initial height: ~1m

Output:
- Trajectory data saved to `data/sphere_trajectory.csv`
- Real-time position updates
- Final simulation statistics
