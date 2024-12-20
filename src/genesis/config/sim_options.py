from typing import Optional
from pydantic import BaseModel

class SimOptions(BaseModel):
    dt: float = 1e-2  # Time-step size
    substeps: int = 1  # Number of sub-steps
    substeps_local: Optional[int] = None  # Local sub-steps
    gravity: tuple = (0.0, 0.0, -9.81)  # Gravity vector
    floor_height: float = 0.0  # Height of the simulation floor
    requires_grad: bool = False  # Enable gradient computation
