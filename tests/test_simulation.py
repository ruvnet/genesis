import unittest
from genesis import Simulation
from genesis.config.sim_options import SimOptions
from genesis.config.coupler_options import CouplerOptions
from genesis.config.renderer_options import RendererOptions

class TestSimulationInitialization(unittest.TestCase):
    def test_simulation_initialization(self):
        sim_options = SimOptions(
            dt=1e-3,
            substeps=2,
            gravity=(0.0, -9.81, 0.0),
            floor_height=0.5,
            requires_grad=True
        )

        coupler_options = CouplerOptions(
            rigid_mpm=False,
            rigid_sph=True,
            rigid_pbd=True
        )

        renderer_options = RendererOptions(
            cuda_device=1,
            logging_level="info",
            state_limit=2**20,
            tracing_depth=16,
            rr_depth=5,
            rr_threshold=0.9,
            env_surface="metal",
            env_radius=500.0,
            env_pos=(1.0, 2.0, 3.0),
            lights=[{
                "pos": (10.0, 10.0, 10.0),
                "color": (1.0, 0.8, 0.6),
                "intensity": 15.0,
                "radius": 5.0
            }]
        )

        simulation = Simulation(
            sim_options=sim_options,
            coupler_options=coupler_options,
            renderer_options=renderer_options
        )

        self.assertIsNotNone(simulation)
        self.assertEqual(simulation.sim_options.dt, 1e-3)
        self.assertFalse(simulation.coupler_options.rigid_mpm)
        self.assertEqual(simulation.renderer_options.cuda_device, 1)

if __name__ == '__main__':
    unittest.main()
