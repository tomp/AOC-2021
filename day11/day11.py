#!/usr/bin/env python3
#
#  Advent of Code 2019 - Day 11
#
from typing import Sequence, Any
from pathlib import Path
from collections import defaultdict
from location import Location, Delta

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    (
        """
        5483143223
        2745854711
        5264556173
        6141336146
        6357385478
        4167524645
        2176841721
        6882881134
        4846848554
        5283751526
        """,
        1656
    ),
]

SAMPLE_CASES2 = [
    (
        """
        5483143223
        2745854711
        5264556173
        6141336146
        6357385478
        4167524645
        2176841721
        6882881134
        4846848554
        5283751526
        """,
        195
    ),
]

Lines = Sequence[str]
EnergyGrid = dict[Location, int]

# Utility functions

def load_input(infile: str) -> Lines:
    return load_text(Path(infile).read_text())

## Use these if blank lines should be discarded.

def load_text(text: str) -> Lines:
    return filter_blank_lines(text.split("\n"))

def filter_blank_lines(lines: Lines) -> Lines:
    return [line.strip() for line in lines if line.strip()]

# Solution

def parse_input(lines) -> tuple[EnergyGrid, int]:
    result = defaultdict(lambda: -10)
    for r, row in enumerate(lines):
        for c, value in enumerate(row):
            result[Location(r,c)] = int(value)
    return result

def neighbors(loc: Location) -> list[Location]:
    return [
        loc.up(),
        loc.up().right(),
        loc.right(),
        loc.right().down(),
        loc.down(),
        loc.down().left(),
        loc.left(),
        loc.left().up()
    ]

def grid_to_str(grid: EnergyGrid) -> str:
    rmin = min([loc.r for loc in grid])
    rmax = max([loc.r for loc in grid])
    cmin = min([loc.c for loc in grid])
    cmax = max([loc.c for loc in grid])
    rows = []
    for r in range(rmin, rmax+1):
        rows.append(
            "".join([str(grid[Location(r, c)]) for c in range(cmin, cmax+1)])
        )
    return "\n".join(rows)

def iterate(energies) -> tuple[EnergyGrid, int]:
    work = defaultdict(lambda: -10)
    for loc, energy in energies.items():
        work[loc] = energy + 1
    flash_locs = [loc for loc, energy in work.items() if energy > 9]
    flashed = set(flash_locs)
    queue = list(flash_locs)
    while queue:
        loc = queue.pop(0)
        for nayb in neighbors(loc):
            work[nayb] += 1
            if work[nayb] > 9 and nayb not in flashed:
                flashed.add(nayb)
                queue.append(nayb)
    final = defaultdict(lambda: -10)
    for loc, energy in work.items():
        if work[loc] > 9:
            final[loc] = 0
        elif energy > 0:
            final[loc] = energy
    return final, len(flashed)


def solve2(lines: Lines) -> int:
    """Solve the problem."""
    energies = parse_input(lines)
    nloc = len(energies)
    flashes = 0
    step = 0
    while flashes < nloc:
        step += 1
        energies, flashes = iterate(energies)
        # print(f"After step {step+1}:")
        # print(grid_to_str(energies))
    return step

def solve(lines: Lines, steps: int = 100) -> int:
    """Solve the problem."""
    energies = parse_input(lines)
    total_flashes = 0
    for step in range(steps):
        energies, flashes = iterate(energies)
        total_flashes += flashes
        # print(f"After step {step+1}:")
        # print(grid_to_str(energies))
    return total_flashes


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
    assert result == 1673
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
    assert result == 279
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
