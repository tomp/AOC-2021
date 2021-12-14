#!/usr/bin/env python3
#
from typing import Sequence, Optional, Union, Any
from dataclasses import dataclass
from collections import defaultdict

X_AXIS = "x"
Y_AXIS = "y"

@dataclass(frozen=True)
class Location:
    """A Location instance represents a location on a grid.
    Internally, it's represented using (row, column) coordinates
    """
    r: int
    c: int

    def __str__(self) -> str:
        return f"({self.r}, {self.c})"

    def right(self) -> "Location":
        return Location(self.r, self.c + 1)

    def left(self) -> "Location":
        return Location(self.r, self.c - 1)

    def up(self) -> "Location":
        return Location(self.r - 1, self.c)

    def down(self) -> "Location":
        return Location(self.r + 1, self.c)

    def __add__(self, delta: "Delta") -> "Location":
        return Location(self.r + delta.dr, self.c + delta.dc)

    def __sub__(self, other: "Location") -> "Delta":
        return Delta(self.r - other.r, self.c - other.c)

    def reflect(self, axis: str, value: int) -> "Location":
        if axis == X_AXIS:
            return Location(self.r, 2*value - self.c)
        if axis == Y_AXIS:
            return Location(2*value - self.r, self.c)
        raise ValueError(f"unrecognized axis '{axis}'")


@dataclass(frozen=True)
class Delta:
    """A Delta instance represents the difference between two locations
    on a grid.  Internally, it's represented using (row, column) offsets.
    """
    dr: int
    dc: int

    def __str__(self) -> str:
        return f"delta({self.dr}, {self.dc})"

    def __add__(self, other: "Delta") -> "Delta":
        return Delta(self.dr + other.dr, self.dc + other.dc)

    def __sub__(self, other: "Delta") -> "Delta":
        return Delta(self.dr - other.dr, self.dc - other.dc)

