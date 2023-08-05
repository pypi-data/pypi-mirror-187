from ..helpers import multi_newton as multi_newton
from .geometry import Geometry as Geometry
from _typeshed import Incomplete

class Ellipse(Geometry):
    x0: Incomplete
    a: Incomplete
    b: Incomplete
    def __init__(self, x0, a, b) -> None: ...
    def dist(self, x): ...
    def boundary_step(self, x): ...
