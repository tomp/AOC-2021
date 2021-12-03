#!/usr/bin/env python3
#
#  Advent of Code 2021 - Day 3
#
from typing import Sequence, Any
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

INPUTFILE = "input.txt"

SAMPLE_INPUT = """
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
"""

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


# Solution

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    oxygen_values, co2_values = lines, lines
    nbits = len(lines[0])

    # oxygen
    for i in range(nbits):
        if len(oxygen_values) == 1:
            break
        ones = sum([1 for v in oxygen_values if v[i] == "1"])
        if ones >= len(oxygen_values) / 2:
            oxygen_values = [line for line in oxygen_values if line[i] == "1"]
        else:
            oxygen_values = [line for line in oxygen_values if line[i] == "0"]
    oxygen = int(oxygen_values[0], 2)

    # co2
    for i in range(nbits):
        if len(co2_values) == 1:
            break
        ones = sum([1 for v in co2_values if v[i] == "1"])
        if ones >= len(co2_values) / 2:
            co2_values = [line for line in co2_values if line[i] == "0"]
        else:
            co2_values = [line for line in co2_values if line[i] == "1"]
    co2 = int(co2_values[0], 2)

    return oxygen * co2


def solve(lines: Lines) -> int:
    """Solve the problem."""
    gamma_bits, epsilon_bits = [], []
    nlines = len(lines)
    nbits = len(lines[0])
    for i in range(nbits):
        ones = sum([1 for v in lines if v[i] == "1"])
        if ones > nlines / 2:
            gamma_bits.append('1')
            epsilon_bits.append('0')
        else:
            gamma_bits.append('0')
            epsilon_bits.append('1')
    gamma = int("".join(gamma_bits), 2)
    epsilon = int("".join(epsilon_bits), 2)
    return gamma * epsilon


# PART 1

def example1() -> None:
    """Run example for problem with input lines."""
    print("EXAMPLE 1:")
    lines = sample_input()
    result = solve(lines)
    expected = 198
    print(f"'sample-input' -> {result} (expected {expected})")
    assert result == expected
    print("= " * 32)

def part1(lines: Lines) -> None:
    print("PART 1:")
    result = solve(lines)
    print(f"result is {result}")
    assert result == 2250414
    print("= " * 32)


# PART 2

def example2() -> None:
    """Run example for problem with input lines."""
    print("EXAMPLE 2:")
    lines = sample_input()
    result = solve2(lines)
    expected = 230
    print(f"'sample-input' -> {result} (expected {expected})")
    assert result == expected
    print("= " * 32)

def part2(lines: Lines) -> None:
    print("PART 2:")
    result = solve2(lines)
    print(f"result is {result}")
    assert result == 6085575
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
