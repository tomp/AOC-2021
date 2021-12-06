#!/usr/bin/env python3
#
#  Advent of Code 2019 - Day 6
#
from typing import Sequence, Any
from pathlib import Path
from collections import defaultdict

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    (
        """
        3,4,3,1,2
        """,
        18, 26
    ),
    (
        """
        3,4,3,1,2
        """,
        80, 5934
    ),
]

SAMPLE_CASES2 = [
    (
        """
        3,4,3,1,2
        """,
        256, 26984457539
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

class School:
    """A school of fish, whose populations are tracked using their position
    in their reproductive cycle.
    """
    def __init__(self, ages: list[int]):
        self.steps = 0
        self.cohorts = defaultdict(int)
        for age in ages:
            self.cohorts[age % 9] += 1

    def step(self):
        new_cohorts = defaultdict(int)
        for age, count in self.cohorts.items():
            if age == 0:
                new_cohorts[6] += count
                new_cohorts[8] += count
            else:
                new_cohorts[age - 1] += count
        self.cohorts = new_cohorts
        self.steps += 1

    def population(self) -> int:
        return sum(self.cohorts.values())


def parse_input(line: str) -> School:
    ages = list(map(int, line.strip().split(",")))
    return School(ages)

def solve(lines: Lines, days: int = 0) -> int:
    """Solve the problem."""
    school = parse_input(lines[0])
    # print(f"Initially, there are {school.population()} lanternfish")
    for day in range(days):
        school.step()
        # print(f"after {day+1} day, there are {school.population()} lanternfish")
    return school.population()


# PART 1

def example1() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 1:")
    for text, days, expected in SAMPLE_CASES:
        lines = load_text(text)
        result = solve(lines, days)
        print(f"'{text}', {days} days -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)

def part1(lines: Lines) -> None:
    print("PART 1:")
    result = solve(lines, 80)
    print(f"result is {result}")
    assert result == 395627
    print("= " * 32)


# PART 2

def example2() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 2:")
    for text, days, expected in SAMPLE_CASES2:
        lines = load_text(text)
        result = solve(lines, days)
        print(f"'{text}', {days} days -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)

def part2(lines: Lines) -> None:
    print("PART 2:")
    result = solve(lines, 256)
    print(f"result is {result}")
    assert result == 1767323539209
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
