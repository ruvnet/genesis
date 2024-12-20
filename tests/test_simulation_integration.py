import unittest
from genesis import Simulation
from genesis.config.sim_options import SimOptions
from genesis.config.coupler_options import CouplerOptions
from genesis.config.renderer_options import RendererOptions

class TestSimulationIntegration(unittest.TestCase):
    def test_simulation_run(self):
        sim_options = SimOptions(
            dt=1e-2,
            substeps=1,
            gravity=(0.0, 0.0, -9.81),
            floor_height=0.0,
            requires_grad=False
        )

        coupler_options = CouplerOptions(
            rigid_mpm=True,
            rigid_sph=True,
            rigid_pbd=True
        )

        renderer_options = RendererOptions(
            cuda_device=0,
            logging_level="warning",
            state_limit=2**25,
            tracing_depth=32,
            rr_depth=0,
            rr_threshold=0.95,
            env_radius=1000.0,
            env_pos=(0.0, 0.0, 0.0),
            lights=[{
                "pos": (0.0, 0.0, 10.0),
                "color": (1.0, 1.0, 1.0),
                "intensity": 10.0,
                "radius": 4.0
            }]
        )

        simulation = Simulation(
            sim_options=sim_options,
            coupler_options=coupler_options,
            renderer_options=renderer_options
        )

        # Initialize simulation
        simulation.initialize()

        # Run simulation for a few steps
        for _ in range(10):
            simulation.step()

        # Render a frame
        frame = simulation.render_frame()

        self.assertIsNotNone(frame)
        self.assertEqual(frame.size, (800, 600))  # Assuming default frame size

if __name__ == '__main__':
    unittest.main()
