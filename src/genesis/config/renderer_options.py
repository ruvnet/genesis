from typing import Optional, List, Dict
from pydantic import BaseModel

class RendererOptions(BaseModel):
    cuda_device: int = 0  # CUDA device ID
    logging_level: str = "warning"  # Logging level
    state_limit: int = 2**25  # State memory limit
    tracing_depth: int = 32  # Tracing depth for rendering
    rr_depth: int = 0  # Ray tracing depth
    rr_threshold: float = 0.95  # Russian Roulette threshold
    env_surface: Optional[str] = None  # Environment surface type
    env_radius: float = 1000.0  # Environment radius
    env_pos: tuple = (0.0, 0.0, 0.0)  # Environment position
    env_euler: tuple = (0.0, 0.0, 0.0)  # Environment orientation (Euler angles)
    env_quat: Optional[tuple] = None  # Environment orientation (Quaternion)
    lights: List[Dict] = [
        {
            "pos": (0.0, 0.0, 10.0),
            "color": (1.0, 1.0, 1.0),
            "intensity": 10.0,
            "radius": 4.0
        }
    ]  # List of light sources
    normal_diff_clamp: float = 180  # Normal and diffuse clamp angle
