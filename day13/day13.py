#!/usr/bin/env python3
#
#  Advent of Code 2019 - Day 13
#
from typing import Sequence, Any
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass
import math
import re
from location import Location, X_AXIS, Y_AXIS

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    (
        """
        6,10
        0,14
        9,10
        0,3
        10,4
        4,11
        6,0
        6,12
        4,1
        0,13
        10,12
        3,4
        3,0
        8,4
        1,10
        2,14
        8,10
        9,0

        fold along y=7
        fold along x=5
        """,
        17
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

def load_text(text: str) -> Lines:
    return [line.strip() for line in text.strip("\n").split("\n")]

def parse_sections(lines: Lines) -> Sections:
    result = []
    sect = []
    for line in lines:
        line = line.strip()
        if not line:
            if sect:
                result.append(sect)
            sect = []
        else:
            sect.append(line)
    if sect:
        result.append(sect)
    return result


# Solution

Fold = tuple[str, int]

def parse_input(lines: Lines) -> tuple[list[Location], list[Fold]]:
    part1, part2 = parse_sections(lines)
    points = []
    for line in part1:
        x, y = line.split(",")
        points.append(Location(int(y), int(x)))
    folds = []
    for line in part2:
        if line.startswith("fold along "):
            axis, value = line[11:].split("=")
            folds.append((axis, int(value)))
    return points, folds

def fold_grid(points: list[Location], axis: str, value: int) -> list[Location]:
    """Solve the problem."""
    result = set()
    for loc in points:
        if axis == Y_AXIS and loc.r > value:
            result.add(loc.reflect(axis, value))
        elif axis == X_AXIS and loc.c > value:
            result.add(loc.reflect(axis, value))
        else:
            result.add(loc)
    return list(result)

def print_grid(points: list[Location]) -> None:
    rmin = min([loc.r for loc in points])
    rmax = max([loc.r for loc in points])
    cmin = min([loc.c for loc in points])
    cmax = max([loc.c for loc in points])
    grid = defaultdict(lambda: ".")
    for loc in points:
        grid[loc] = "#"
    for r in range(rmin, rmax+1):
        row = "".join([grid[Location(r, c)] for c in range(cmin, cmax+1)])
        print(row)

def solve2(lines: Lines) -> None:
    """Solve the problem."""
    points, folds = parse_input(lines)
    for axis, value in folds:
        points = fold_grid(points, axis, value)
    print_grid(points)

def solve(lines: Lines) -> int:
    """Solve the problem."""
    points, folds = parse_input(lines)
    axis, value = folds[0]
    points = fold_grid(points, axis, value)
    return len(points)


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
    print("= " * 32)


# PART 2

def part2(lines: Lines) -> None:
    print("PART 2:")
    result = solve2(lines)
    print(f"result is {result}")
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    part2(input_lines)
