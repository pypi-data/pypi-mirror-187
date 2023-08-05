from .geometry import Geometry as Geometry
from .polygon import LineSegmentPath as LineSegmentPath
from _typeshed import Incomplete

class Rectangle(Geometry):
    x0: Incomplete
    x1: Incomplete
    y0: Incomplete
    y1: Incomplete
    points: Incomplete
    paths: Incomplete
    def __init__(self, x0, x1, y0, y1) -> None: ...
    def dist(self, x): ...
    def boundary_step(self, x): ...
