#!/usr/bin/env python3
#
#  Advent of Code 2019 - Day 7
#
from typing import Sequence, Any
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass
import math
import re

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    (
        """
        16,1,2,0,4,2,7,1,2,14
        """,
        37
    ),
]

SAMPLE_CASES2 = [
    (
        """
        16,1,2,0,4,2,7,1,2,14
        """,
        168
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

def parse_input(line: str) -> list[int]:
    return list(map(int, line.split(",")))

def linsum(n: int) -> int:
    """Return the sum of the integers from 1 to n."""
    return n * ( n + 1) // 2

def cost2(pos: list[int], target: int) -> int:
    return sum([linsum(abs(v - target)) for v in pos])

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    crabs = parse_input(lines[0])
    best_cost = cost2(crabs, crabs[0])
    for move_to in range(min(crabs), max(crabs) + 1):
        move_cost = cost2(crabs, move_to)
        if move_cost < best_cost:
            best = move_to
            best_cost = move_cost
    return best_cost

def cost(pos: list[int], target: int) -> int:
    return sum([abs(v - target) for v in pos])

def solve(lines: Lines) -> int:
    """Solve the problem."""
    crabs = parse_input(lines[0])
    best_cost = cost(crabs, crabs[0])
    for move_to in range(min(crabs), max(crabs) + 1):
        move_cost = cost(crabs, move_to)
        if move_cost < best_cost:
            best = move_to
            best_cost = move_cost
    return best_cost


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
    assert result == 336040
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
    assert result == 94813675
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
