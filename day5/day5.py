#!/usr/bin/env python3
#
#  Advent of Code 2019 - Day 5
#
from typing import Sequence, Any
from collections import defaultdict
from dataclasses import dataclass
import math
import re
from pathlib import Path

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    (
        """
        0,9 -> 5,9
        8,0 -> 0,8
        9,4 -> 3,4
        2,2 -> 2,1
        7,0 -> 7,4
        6,4 -> 2,0
        0,9 -> 2,9
        3,4 -> 1,4
        0,0 -> 8,8
        5,5 -> 8,2
        """,
        5
    ),
]

SAMPLE_CASES2 = [
    (
        """
        0,9 -> 5,9
        8,0 -> 0,8
        9,4 -> 3,4
        2,2 -> 2,1
        7,0 -> 7,4
        6,4 -> 2,0
        0,9 -> 2,9
        3,4 -> 1,4
        0,0 -> 8,8
        5,5 -> 8,2
        """,
        12
    ),
]

Lines = Sequence[str]
Sections = Sequence[Lines]

# Utility functions

def load_input(infile: str) -> Lines:
    return load_text(Path(infile).read_text())

def sample_case(idx: int = 0) -> tuple[Lines, int]:
    text, expected = SAMPLE_CASES[idx]
    lines = load_text(text)
    return lines, expected

## Use these if blank lines should be discarded.

def load_text(text: str) -> Lines:
    return filter_blank_lines(text.split("\n"))

def filter_blank_lines(lines: Lines) -> Lines:
    return [line.strip() for line in lines if line.strip()]

# Solution

@dataclass(frozen=True)
class Location:
    r: int
    c: int

    def __str__(self) -> str:
        return f"({self.r}, {self.c})"

@dataclass(frozen=True)
class Vent:
    beg: Location
    end: Location

    def __str__(self) -> str:
        return f"{self.beg} -> {self.end}"

    def coords(self):
        return self.beg.r, self.beg.c, self.end.r, self.end.c

    def step(self):
        r0, c0, r1, c1 = self.coords()
        dr, dc = r1 - r0, c1 - c0
        if dr == 0:
            dc = 1 if dc > 0 else -1
        elif dc == 0:
            dr = 1 if dr > 0 else -1
        else:
            a = math.gcd(dr, dc)
            dr, dc = dr // a, dc // a
        return dr, dc

    def is_diagonal(self) -> bool:
        dr, dc = self.step()
        return not(dr == 0 or dc == 0)

    def points(self):
        r0, c0, r1, c1 = self.coords()
        dr, dc = self.step()
        n = max(abs(r1 - r0), abs(c1 - c0)) + 1
        return list([Location(r0 + j*dr, c0 + j*dc) for j in range(n)])


VENT_RE = re.compile(r"(-?\d+),(-?\d+) -> (-?\d+),(-?\d+)$")

def parse_input(lines) -> list[Vent]:
    result = []

    for line in lines:
        m = VENT_RE.match(line)
        r0, c0, r1, c1 = [int(v) for v in m.groups()]
        result.append(Vent(Location(r0, c0), Location(r1, c1)))
    return result

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    vents = parse_input(lines)
    points = defaultdict(int)
    for vent in vents:
        for p in vent.points():
            points[p] += 1
    return sum([1 for v in points.values() if v > 1])

def solve(lines: Lines) -> int:
    """Solve the problem."""
    vents = parse_input(lines)
    points = defaultdict(int)
    for vent in vents:
        if not vent.is_diagonal():
            for p in vent.points():
                points[p] += 1
    return sum([1 for v in points.values() if v > 1])


# PART 1

def example1() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 1:")
    for text, expected in SAMPLE_CASES:
        lines = load_text(text)
        result = solve(lines)
        print(f"'{text}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)

def part1(lines: Lines) -> None:
    print("PART 1:")
    result = solve(lines)
    print(f"result is {result}")
    assert result == 4826
    print("= " * 32)


# PART 2

def example2() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 2:")
    for text, expected in SAMPLE_CASES2:
        lines = load_text(text)
        result = solve2(lines)
        print(f"'{text}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)

def part2(lines: Lines) -> None:
    print("PART 2:")
    result = solve2(lines)
    print(f"result is {result}")
    assert result == 16793
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
