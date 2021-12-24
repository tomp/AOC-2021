#!/usr/bin/env python3
#
from typing import Sequence, Optional, Union, Any
from itertools import permutations, combinations
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

    def __repr__(self) -> str:
        return str(self)

    def distance(self, other: "Point3D") -> float:
        return abs(other - self)

    def __add__(self, delta: "Delta3D") -> "Point3D":
        return Point3D(self.x + delta.dx, self.y + delta.dy, self.z + delta.dz)

    def __sub__(self, other: "Point3D") -> "Delta3D":
        return Delta3D(self.x - other.x, self.y - other.y, self.z - other.z)

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

    def __repr__(self) -> str:
        return str(self)

    def __add__(self, other: "Delta3D") -> "Delta3D":
        return Delta3D(self.dx + other.dx, self.dy + other.dy, self.dz + other.dz)

    def __sub__(self, other: "Delta3D") -> "Delta3D":
        return Delta3D(self.dx - other.dx, self.dy - other.dy, self.dz - other.dz)

    def __abs__(self) -> float:
        return math.sqrt(self.dx*self.dx + self.dy*self.dy + self.dz* self.dz)

    def __lt__(self, other: "Delta3D") -> bool:
        if self.dx != other.dx:
            return self.dx < other.dx
        if self.dy != other.dy:
            return self.dy < other.dy
        return self.dz < other.dz

ZeroOne = int # -1, 0 or 1
Int3 = list[ZeroOne, ZeroOne, ZeroOne]

@dataclass(frozen=True)
class Rot3D:
    m: list[Int3, Int3, Int3]

    def __post_init__(self):
        assert len(self.m) == 3
        assert all([len(row) == 3 for row in self.m])

    def __str__(self) -> str:
        rows = []
        for row in self.m:
            rows.append(", ".join([f"{v:2d}" for v in row]))
        return "\n".join(rows)

    def __mul__(self, v: Union[Point3D, Delta3D]) -> Union[Point3D, Delta3D]:
        if isinstance(v, Point3D):
            x = self.m[0][0] * v.x + self.m[0][1] * v.y + self.m[0][2] * v.z
            y = self.m[1][0] * v.x + self.m[1][1] * v.y + self.m[1][2] * v.z
            z = self.m[2][0] * v.x + self.m[2][1] * v.y + self.m[2][2] * v.z
            return Point3D(int(x), int(y), int(z))
        dx = self.m[0][0] * v.dx + self.m[0][1] * v.dy + self.m[0][2] * v.dz
        dy = self.m[1][0] * v.dx + self.m[1][1] * v.dy + self.m[1][2] * v.dz
        dz = self.m[2][0] * v.dx + self.m[2][1] * v.dy + self.m[2][2] * v.dz
        return Delta3D(int(dx), int(dy), int(dz))

ROTS = []
for i, j, k in permutations((0, 1, 2)):
    for ones in range(8):
        ri, rj, rk = [1 - int(m)*2 for m in f"{ones:03b}"]
        matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        matrix[0][i] = ri
        matrix[1][j] = rj
        matrix[2][k] = rk
        # print(f"{len(ROTS):2d}: {str(matrix)}")
        ROTS.append(Rot3D(matrix))

