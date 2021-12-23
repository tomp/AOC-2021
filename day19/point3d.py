#!/usr/bin/env python3
#
from typing import Sequence, Optional, Union, Any
from dataclasses import dataclass
import math


@dataclass(frozen=True)
class Point3D:
    """A Point3D instance represents a location in 3D space.
    Internally, it's represented using (x, y, z) coordinates.
    """
    x: int
    y: int
    z: int

    def __str__(self) -> str:
        return f"({self.x:6.2f},{self.y:6.2f},{self.z:6.2f})"

    def distance(self, other: "Point3D") -> int:
        dx = other.x - self.x
        dy = other.y - self.y
        dz = other.z - self.z
        return math.sqrt(dx*dx + dy*dy + dz* dz)

    def __add__(self, delta: "Delta3D") -> "Point3D":
        return Point3D(self.x + delta.dx, self.y + delta.dy, self.z + delta.dz)

    def __sub__(self, other: "Point3D") -> "Delta3D":
        return Point3D(self.x - delta.dx, self.y - delta.dy, self.z - delta.dz)

    def __lt__(self, other: "Point3D") -> bool:
        if self.x != other.x:
            return self.x < other.x
        if self.y != other.y:
            return self.y < other.y
        return self.z < other.z


@dataclass(frozen=True)
class Delta3D:
    """A Delta3D instance represents the difference between two locations
    in 3D space.
    """
    dx: int
    dy: int
    dz: int

    def __str__(self) -> str:
        return f"delta({self.dx},{self.dy},{self.dz})"

    def __add__(self, other: "Delta3D") -> "Delta3D":
        return Delta3D(self.dx + other.dx, self.dy + other.dy, self.dz + other.dz)

    def __sub__(self, other: "Delta3D") -> "Delta3D":
        return Delta3D(self.dx - other.dx, self.dy - other.dy, self.dz - other.dz)
