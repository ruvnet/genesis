from pydantic import BaseModel

class CouplerOptions(BaseModel):
    rigid_mpm: bool = True  # Enable Rigid MPM coupling
    rigid_sph: bool = True  # Enable Rigid SPH coupling
    rigid_pbd: bool = True  # Enable Rigid PBD coupling
