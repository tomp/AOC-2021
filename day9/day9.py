#!/usr/bin/env python3
#
#  Advent of Code 2019 - Day 9
#
from typing import Sequence, Any
from pathlib import Path
from collections import defaultdict
import math
from location import Location, Delta

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    (
        """
        2199943210
        3987894921
        9856789892
        8767896789
        9899965678        
        """,
        15
    ),
]

SAMPLE_CASES2 = [
    (
        """
        2199943210
        3987894921
        9856789892
        8767896789
        9899965678        
        """,
        1134
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

## Use these if blank lines should be discarded.

def load_text(text: str) -> Lines:
    return filter_blank_lines(text.split("\n"))

def filter_blank_lines(lines: Lines) -> Lines:
    return [line.strip() for line in lines if line.strip()]

# Solution

def parse_input(lines):
    """Return the heightmap represeneted by the given input lines.
    The heightnap is a dict, mapping thr (row, col) coordinates to
    an integer height.
    """
    result = defaultdict(lambda: 10)
    for r, row in enumerate(lines):
        for c, height in enumerate(row):
            result[Location(r,c)] = int(height)
    return result

def low_points(heights) -> list[Location]:
    """Solve the problem."""
    result = []
    locs = list(heights.keys())
    for loc in locs:
        height = heights[loc]
        if heights[loc.up()] <= height:
            continue
        if heights[loc.down()] <= height:
            continue
        if heights[loc.right()] <= height:
            continue
        if heights[loc.left()] <= height:
            continue
        result.append(loc)
    return result

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    heights = parse_input(lines)
    minima = low_points(heights)
    sizes = []
    for basin_loc in minima:
        basin = set([basin_loc])
        queue = [basin_loc]
        while queue:
            loc = queue.pop(0)
            for nayb_loc in (loc.up(), loc.down(), loc.right(), loc.left()):
                if nayb_loc not in basin and heights[nayb_loc] < 9:
                    basin.add(nayb_loc)
                    queue.append(nayb_loc)
        sizes.append(len(basin))
    sizes.sort()
    return math.prod(sizes[-3:])

def solve(lines: Lines) -> int:
    """Solve the problem."""
    heights = parse_input(lines)
    result = sum([1 + heights[loc] for loc in low_points(heights)])
    return result


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
    assert result == 541
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
    assert result == 847504
    print("= " * 32)



if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
