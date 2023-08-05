from .geometry import Geometry as Geometry
from _typeshed import Incomplete

class Rotation(Geometry):
    geometry: Incomplete
    R: Incomplete
    R_inv: Incomplete
    def __init__(self, geometry, angle) -> None: ...
    def dist(self, x): ...
    def boundary_step(self, x): ...
