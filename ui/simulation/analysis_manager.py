import numpy as np
import pandas as pd
import os
from typing import Dict, List, Optional
import matplotlib.pyplot as plt

class AnalysisManager:
    def __init__(self):
        self.position_history = []
        self.velocity_history = []
        self.energy_history = []
        self.timestamps = []
        
        # Analysis settings
        self.track_position = True
        self.track_velocity = True
        self.track_energy = True
        
        # Initialize plots
        self.setup_plots()
    
    def setup_plots(self):
        """Initialize matplotlib plots for visualization."""
        plt.style.use('dark_background')
    
    def update_tracking(self, scene, timestamp: float):
        """Update tracking data from the current scene state."""
        if scene is None:
            return
        
        self.timestamps.append(timestamp)
        
        if self.track_position:
            positions = []
            for obj in scene.objects:
                if hasattr(obj, 'position'):
                    positions.append(obj.position)
            self.position_history.append(positions)
        
        if self.track_velocity:
            velocities = []
            for obj in scene.objects:
                if hasattr(obj, 'velocity'):
                    velocities.append(obj.velocity)
            self.velocity_history.append(velocities)
        
        if self.track_energy:
            ke = self.calculate_kinetic_energy(scene)
            pe = self.calculate_potential_energy(scene)
            self.energy_history.append({
                'kinetic': ke,
                'potential': pe,
                'total': ke + pe
            })
    
    def calculate_kinetic_energy(self, scene) -> float:
        """Calculate total kinetic energy of the system."""
        ke = 0.0
        for obj in scene.objects:
            if hasattr(obj, 'mass') and hasattr(obj, 'velocity'):
                velocity = np.array(obj.velocity)
                ke += 0.5 * obj.mass * np.dot(velocity, velocity)
        return ke
    
    def calculate_potential_energy(self, scene) -> float:
        """Calculate total gravitational potential energy of the system."""
        pe = 0.0
        gravity = np.array([scene.gravity_x, scene.gravity_y, scene.gravity_z])
        for obj in scene.objects:
            if hasattr(obj, 'mass') and hasattr(obj, 'position'):
                position = np.array(obj.position)
                pe += -obj.mass * np.dot(gravity, position)
        return pe
    
    def get_position_plot(self):
        """Generate position plot."""
        if not self.position_history:
            return None
            
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111)
        
        # Plot x, y, z positions for each object
        for i in range(len(self.position_history[0])):
            positions = np.array([[pos[i][j] for pos in self.position_history] for j in range(3)])
            ax.plot(self.timestamps, positions[0], label=f'Object {i+1} X')
            ax.plot(self.timestamps, positions[1], label=f'Object {i+1} Y')
            ax.plot(self.timestamps, positions[2], label=f'Object {i+1} Z')
        
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Position (m)')
        ax.legend()
        ax.grid(True)
        
        return fig
    
    def get_velocity_plot(self):
        """Generate velocity plot."""
        if not self.velocity_history:
            return None
            
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111)
        
        # Plot velocity magnitude for each object
        for i in range(len(self.velocity_history[0])):
            velocities = np.array([np.linalg.norm(vel[i]) for vel in self.velocity_history])
            ax.plot(self.timestamps, velocities, label=f'Object {i+1}')
        
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Velocity (m/s)')
        ax.legend()
        ax.grid(True)
        
        return fig
    
    def get_energy_plot(self):
        """Generate energy plot."""
        if not self.energy_history:
            return None
            
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111)
        
        ke = [e['kinetic'] for e in self.energy_history]
        pe = [e['potential'] for e in self.energy_history]
        total = [e['total'] for e in self.energy_history]
        
        ax.plot(self.timestamps, ke, label='Kinetic')
        ax.plot(self.timestamps, pe, label='Potential')
        ax.plot(self.timestamps, total, label='Total')
        
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Energy (J)')
        ax.legend()
        ax.grid(True)
        
        return fig
    
    def get_current_energy(self) -> Dict[str, float]:
        """Get current energy values."""
        if not self.energy_history:
            return {'kinetic': 0.0, 'potential': 0.0, 'total': 0.0}
        return self.energy_history[-1]
    
    def export_data(self, path: str, prefix: str, 
                   export_position: bool = True,
                   export_velocity: bool = True,
                   export_energy: bool = True) -> str:
        """Export tracked data to CSV files."""
        try:
            os.makedirs(path, exist_ok=True)
            
            if export_position and self.position_history:
                positions_df = pd.DataFrame(columns=['time'])
                positions_df['time'] = self.timestamps
                
                for i in range(len(self.position_history[0])):
                    for j, coord in enumerate(['x', 'y', 'z']):
                        col_name = f'object_{i+1}_{coord}'
                        positions_df[col_name] = [pos[i][j] for pos in self.position_history]
                
                positions_df.to_csv(os.path.join(path, f'{prefix}_positions.csv'), index=False)
            
            if export_velocity and self.velocity_history:
                velocities_df = pd.DataFrame(columns=['time'])
                velocities_df['time'] = self.timestamps
                
                for i in range(len(self.velocity_history[0])):
                    for j, coord in enumerate(['x', 'y', 'z']):
                        col_name = f'object_{i+1}_{coord}'
                        velocities_df[col_name] = [vel[i][j] for vel in self.velocity_history]
                
                velocities_df.to_csv(os.path.join(path, f'{prefix}_velocities.csv'), index=False)
            
            if export_energy and self.energy_history:
                energy_df = pd.DataFrame(columns=['time'])
                energy_df['time'] = self.timestamps
                energy_df['kinetic'] = [e['kinetic'] for e in self.energy_history]
                energy_df['potential'] = [e['potential'] for e in self.energy_history]
                energy_df['total'] = [e['total'] for e in self.energy_history]
                
                energy_df.to_csv(os.path.join(path, f'{prefix}_energy.csv'), index=False)
            
            return "Data exported successfully"
        except Exception as e:
            return f"Error exporting data: {str(e)}"
    
    def reset(self):
        """Reset all tracking data."""
        self.position_history.clear()
        self.velocity_history.clear()
        self.energy_history.clear()
        self.timestamps.clear()
