#!/usr/bin/env python3
#
#  Advent of Code 2021 - Day N
#
from typing import Sequence
from pathlib import Path

INPUTFILE = "input.txt"

SAMPLE_INPUT = """
"""

SAMPLE_CASES = [
    (arg1, expected1),
    (arg2, expected2),
]

Lines = Sequence[str]
Sections = Sequence[Lines]

# Utility functions

## Use these if blank lines should be discarded.
def sample_input() -> Lines:
    return filter_blank_lines(SAMPLE_INPUT.split("\n"))

def load_input(infile: str) -> Lines:
    return filter_blank_lines(Path(infile).open())

def filter_blank_lines(lines: Lines) -> Lines:
    return [line.strip() for line in lines if line.strip()]


## Use these if blank lines in input are meaningful.
def sample_input() -> Lines:
    return SAMPLE_INPUT.strip("\n").split("\n")

def load_input(infile: str) -> Lines:
    return [line.strip() for line in Path(infile).open()]

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

def solve(lines: Lines) -> Any:
    """Solve the problem."""
    pass


# PART 1

#!! DELETE THE example1 FUNCTION YOU'RE NOT GOING TO USE

def example1() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 1:")
    for arg, expected in SAMPLE_CASES:
        result = solve(arg)
        print(f"'{arg}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)

def example1() -> None:
    """Run example for problem with input lines."""
    print("EXAMPLE 1:")
    lines = filter_blank_lines(SAMPLE_INPUT.split("\n"))
    result = solve(lines)
    expected = 0
    print(f"'sample-input' -> {result} (expected {expected})")
    assert result == expected
    print("= " * 32)

def part1(lines: Lines) -> None:
    print("PART 1:")
    result = solve(lines)
    print(f"result is {result}")
    print("= " * 32)


# PART 2


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    # example2()
    # part2(input_lines)
