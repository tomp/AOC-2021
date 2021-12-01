#!/usr/bin/env python3
#
#  Advent of Code 2021 - Day 1
#
from typing import Sequence, Any
from pathlib import Path

INPUTFILE = "input.txt"

SAMPLE_INPUT = """
199
200
208
210
200
207
240
269
260
263
"""

Lines = Sequence[str]

# Utility functions

def load_input(infile: str) -> Lines:
    return filter_blank_lines(Path(infile).open())

def filter_blank_lines(lines: Lines) -> Lines:
    return [line.strip() for line in lines if line.strip()]


# Solution

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    increases = 0
    last_depth = None
    depths = [int(line) for line in lines]
    for start in range(len(depths) - 2):
        depth = sum(depths[start:start+3])
        if last_depth is not None and depth > last_depth:
            increases += 1
        last_depth = depth
    return increases

def solve(lines: Lines) -> int:
    """Solve the problem."""
    increases = 0
    last_depth = None
    for depth in [int(line) for line in lines]:
        if last_depth is not None and depth > last_depth:
            increases += 1
        last_depth = depth
    return increases

# PART 1

#!! DELETE THE example1 FUNCTION YOU'RE NOT GOING TO USE

def example1() -> None:
    """Run example for problem with input lines."""
    print("EXAMPLE 1:")
    lines = filter_blank_lines(SAMPLE_INPUT.split("\n"))
    result = solve(lines)
    expected = 7
    print(f"'sample-input' -> {result} (expected {expected})")
    assert result == expected
    print("= " * 32)

def part1(lines: Lines) -> None:
    print("PART 1:")
    result = solve(lines)
    print(f"result is {result}")
    assert result == 1342
    print("= " * 32)

# PART 2

def example2() -> None:
    """Run example for problem with input lines."""
    print("EXAMPLE 2:")
    lines = filter_blank_lines(SAMPLE_INPUT.split("\n"))
    result = solve2(lines)
    expected = 5
    print(f"'sample-input' -> {result} (expected {expected})")
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
    example2()
    part2(input_lines)
