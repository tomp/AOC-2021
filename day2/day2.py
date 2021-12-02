#!/usr/bin/env python3
#
#  Advent of Code 2021 - Day 2
#
from typing import Sequence, Any
from pathlib import Path

INPUTFILE = "input.txt"

SAMPLE_INPUT = """
forward 5
down 5
forward 8
up 3
down 8
forward 2
"""

Lines = Sequence[str]

# Utility functions

## Use these if blank lines should be discarded.
def sample_input() -> Lines:
    return filter_blank_lines(SAMPLE_INPUT.split("\n"))

def load_input(infile: str) -> Lines:
    return filter_blank_lines(Path(infile).open())

def filter_blank_lines(lines: Lines) -> Lines:
    return [line.strip() for line in lines if line.strip()]


# Solution

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    x, aim, depth = 0, 0, 0
    for line in lines:
        cmd, arg = line.split()
        if cmd == "forward":
            x += int(arg)
            depth += aim * int(arg)
        elif cmd == "down":
            aim += int(arg)
        elif cmd == "up":
            aim -= int(arg)
    return x * depth

def solve(lines: Lines) -> int:
    """Solve the problem."""
    x, depth = 0, 0
    for line in lines:
        cmd, arg = line.split()
        if cmd == "forward":
            x += int(arg)
        elif cmd == "down":
            depth += int(arg)
        elif cmd == "up":
            depth -= int(arg)
    return x * depth


# PART 1

def example1() -> None:
    """Run example for problem with input lines."""
    print("EXAMPLE 1:")
    lines = sample_input()
    result = solve(lines)
    expected = 150
    print(f"'sample-input' -> {result} (expected {expected})")
    assert result == expected
    print("= " * 32)

def part1(lines: Lines) -> None:
    print("PART 1:")
    result = solve(lines)
    print(f"result is {result}")
    assert result == 1648020
    print("= " * 32)


# PART 2

def example2() -> None:
    """Run example for problem with input lines."""
    print("EXAMPLE 2:")
    lines = sample_input()
    result = solve2(lines)
    expected = 900
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
