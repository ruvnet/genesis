"""
Falling Sphere Example

This example demonstrates:
1. Physics simulation with rigid bodies
2. Headless rendering and video capture
3. Data collection and analysis
4. Backend selection (CPU/GPU)
"""

import genesis as gs
import torch
import numpy as np
import os
import time

def setup_output_dirs():
    """Create directories for output files."""
    os.makedirs("data", exist_ok=True)
    os.makedirs(os.path.join("data", "frames"), exist_ok=True)
    return os.path.join("data", "frames")

def detect_backend():
    """Detect and configure appropriate backend."""
    try:
        if torch.cuda.is_available():
            print("CUDA GPU detected - using GPU backend")
            return gs.cuda
        else:
            print("No GPU detected - using CPU backend")
            return gs.cpu
    except:
        print("Error checking GPU - defaulting to CPU backend")
        return gs.cpu

def create_scene():
    """Create and configure the simulation scene."""
    return gs.Scene(
        show_viewer=False,  # Disable visualization
        sim_options=gs.options.SimOptions(
            dt=0.01,
            substeps=2,  # Increased for stability
            gravity=(0, 0, -9.81),
            requires_grad=False
        )
    )

def add_entities(scene):
    """Add physical entities to the scene."""
    # Ground plane
    plane = scene.add_entity(
        gs.morphs.Plane()
    )

    # Falling sphere
    sphere = scene.add_entity(
        gs.morphs.Sphere(
            pos=(0, 0, 1),
            radius=0.2
        )
    )
    
    return plane, sphere

def run_simulation(scene, sphere):
    """Run simulation and collect data."""
    trajectory = []
    start_time = time.time()
    
    print("\nStarting simulation...")
    
    try:
        # Simulation loop
        for i in range(120):
            # Physics step
            scene.step()
            
            # Collect data
            pos = sphere.get_pos()
            trajectory.append([i, float(pos[0]), float(pos[1]), float(pos[2])])
            
            # Progress update
            if i % 10 == 0:
                print(f"Step {i}: Sphere position = {pos}")
                
    except Exception as e:
        print(f"Error during simulation: {e}")
        return None
    
    end_time = time.time()
    return trajectory, end_time - start_time

def save_data(trajectory, runtime):
    """Save trajectory data and print statistics."""
    # Save trajectory with proper formatting
    csv_file = os.path.join("data", "sphere_trajectory.csv")
    trajectory = np.array(trajectory)
    
    # Create formatted header and data
    header = "step,x,y,z"
    np.savetxt(
        csv_file,
        trajectory,
        header=header,
        delimiter=',',
        fmt=['%3d', '%9.6f', '%9.6f', '%9.6f'],
        comments='',  # Prevent numpy from adding # to header
    )
    
    print(f"\nTrajectory data saved to {csv_file}")
    print("\nFirst few rows of trajectory data:")
    with open(csv_file, 'r') as f:
        for i, line in enumerate(f):
            if i < 5:  # Print first 5 lines
                print(line.strip())
    
    # Print statistics
    print("\nSimulation Statistics:")
    print(f"Initial height: {trajectory[0, 3]:.3f} m")
    print(f"Final height: {trajectory[-1, 3]:.3f} m")
    print(f"Total distance fallen: {trajectory[0, 3] - trajectory[-1, 3]:.3f} m")
    print(f"Simulation time: {trajectory[-1, 0] * 0.01:.2f} seconds")
    print(f"Real time taken: {runtime:.2f} seconds")
    print(f"Average FPS: {len(trajectory) / runtime:.1f}")

def main():
    """Main execution function."""
    # Setup
    os.makedirs("data", exist_ok=True)
    backend = detect_backend()
    gs.init(backend=backend)
    
    # Create scene and entities
    scene = create_scene()
    plane, sphere = add_entities(scene)
    
    # Build scene
    try:
        scene.build()
    except Exception as e:
        print(f"Error building scene: {e}")
        return
    
    # Run simulation
    result = run_simulation(scene, sphere)
    if result is not None:
        trajectory, runtime = result
        save_data(trajectory, runtime)

if __name__ == "__main__":
    main()
