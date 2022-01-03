#!/usr/bin/env python3
#
#  Advent of Code 2019 - Day 25
#
from typing import Sequence, Union, Optional, Any
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass
import math
import re

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    (
        """
        v...>>.vv>
        .vv>>.vv..
        >>.>v>...v
        >>v>>.>.v.
        v>v.vv.v..
        >.>>..v...
        .vv..>.>v.
        v.v..>>v.v
        ....v..v.>
        """,
        58
    ),
]

Lines = Sequence[str]

# Utility functions

def load_input(infile: str) -> Lines:
    return load_text(Path(infile).read_text())

def sample_case(idx: int = 0) -> tuple[Lines, int]:
    text, expected = SAMPLE_CASES[idx]
    lines = load_text(text)
    return lines, expected

def load_text(text: str) -> Lines:
    return filter_blank_lines(text.split("\n"))

def filter_blank_lines(lines: Lines) -> Lines:
    return [line.strip() for line in lines if line.strip()]

# Solution

Grid = list[list[str]]

EAST, SOUTH, EMPTY = ">", "v", "."

def parse_input(lines: Lines) -> Grid:
    return [list(line) for line in lines]

def propagate(grid: Grid) -> tuple[int, Grid]:
    nrow, ncol = len(grid), len(grid[0])

    # which east-facing cucumbers can move?
    east_movers = []
    for r in range(nrow):
        row = grid[r]
        for c in range(ncol):
            if row[c] == EAST and row[(c + 1) % ncol] == EMPTY:
                east_movers.append((r, c))
    for r, c in east_movers:
        grid[r][c] = EMPTY
        grid[r][(c + 1) % ncol] = EAST

    # which south-facing cucumbers can move?
    south_movers = []
    for r in range(nrow):
        row = grid[r]
        below = grid[(r + 1) % nrow]
        for c in range(ncol):
            if row[c] == SOUTH and below[c] == EMPTY:
                south_movers.append((r, c))
    for r, c in south_movers:
        grid[r][c] = EMPTY
        grid[(r + 1) % nrow][c] = SOUTH

    return len(east_movers) + len(south_movers), grid


def solve2(lines: Lines) -> int:
    """Solve the problem."""
    return 0

def solve(lines: Lines) -> int:
    """Solve the problem."""
    grid = parse_input(lines)

    moved, grid = propagate(grid)
    step = 1
    while moved:
        print(f"step {step}:  {moved} sea cucumbers moved")
        moved, grid = propagate(grid)
        step += 1
    print(f"No sea cucumbers moved on step {step}")
    return step


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
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    # example2()
    # part2(input_lines)
