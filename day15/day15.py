#!/usr/bin/env python3
#
#  Advent of Code 2019 - Day 15
#
from typing import Sequence, Any
from pathlib import Path
from collections import defaultdict
from heapq import heappush, heappop
import time
from location import Location

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    (
        """
        1163751742
        1381373672
        2136511328
        3694931569
        7463417111
        1319128137
        1359912421
        3125421639
        1293138521
        2311944581
        """,
        40
    ),
]

SAMPLE_CASES2 = [
    (
        """
        1163751742
        1381373672
        2136511328
        3694931569
        7463417111
        1319128137
        1359912421
        3125421639
        1293138521
        2311944581
        """,
        315
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

def parse_input(lines: Lines) -> dict[Location, int]:
    grid = defaultdict(lambda: 10)
    for r, line in enumerate(lines):
        for c, risk in enumerate(line):
            grid[Location(r, c)] = int(risk)
    return grid

def dict_to_grid(risks):
    rows = max([loc.r for loc in risks.keys()]) + 1
    cols = max([loc.c for loc in risks.keys()]) + 1
    result = []
    for r in range(rows):
        result.append([risks[Location(r, c)] for c in range(cols)])
        # print("".join([str(risks[Location(r, c)]) for c in range(cols)]))
    return result

def grid_search(grid: list[list[int]]) -> int:
    start = time.time()
    rows = len(grid)
    cols = len(grid[0])
    print(f"{rows} rows, {cols} columns")
    assert rows == cols
    
    rmax = rows - 1
    cmax = cols - 1
    rcmax = rmax + cmax

    queue = []
    visited = set()

    r, c = 0, 0
    dist = rcmax - r - c
    heappush(queue, (dist, 0, (r, c)))
    while queue:
        best_risk, total_risk, (r, c) = heappop(queue)
        # if len(visited) % 10000 == 0:
        #     print(f"visited {len(visited)} states  best_risk: {best_risk}  {len(queue)} states queued")
        if r == rmax and c == cmax:
            break
        if (r, c) in visited:
            continue
        visited.add((r, c))
        for r1, c1 in ((r-1, c), (r, c-1), (r+1, c), (r, c+1)):
            if 0 <= r1 <= rmax and 0 <= c1 <= cmax:
                if (r1, c1) not in visited:
                    dist = rcmax - r1 - c1
                    new_total_risk = total_risk + grid[r1][c1]
                    heappush(queue, (dist + new_total_risk , new_total_risk, (r1, c1)))
    print(f"Examined {len(visited)} states")
    print(f"Found path to @({r}, {c}) with total risk {total_risk}")
    print(f"elapsed time: {time.time() - start} sec")
    return total_risk

def search(risks: dict[Location, int]) -> int:
    start = time.time()
    rmax = max([loc.r for loc in risks.keys()])
    cmax = max([loc.c for loc in risks.keys()])
    print(f"{rmax+1} rows, {cmax+1} columns")
    START_LOC = Location(0, 0)
    FINISH_LOC = Location(rmax, cmax)
    dist = START_LOC.distance(FINISH_LOC)

    queue = []
    visited = set()
    heappush(queue, (dist, 0, START_LOC))
    while queue:
        best_risk, total_risk, loc = heappop(queue)
        # if len(visited) % 10000 == 0:
        #     print(f"visited {len(visited)} states  best_risk: {best_risk}  {len(queue)} states queued")
        if loc in visited:
            continue
        visited.add(loc)
        if loc == FINISH_LOC:
            break
        for nayb in (loc.up(), loc.right(), loc.down(), loc.left()):
            if nayb not in visited and risks[nayb] < 10:
                dist = nayb.distance(FINISH_LOC)
                new_risk = total_risk + risks[nayb]
                heappush(queue, (new_risk + dist, new_risk, nayb))
    print(f"Examined {len(visited)} states")
    print(f"Found path to @({loc.r}, {loc.c}) with total risk {total_risk}")
    print(f"elapsed time: {time.time() - start} sec")
    return total_risk

def replicate_tile(tile: dict[Location, int], reps: int = 0) -> dict[Location, int]:
    rows = max([loc.r for loc in tile.keys()]) + 1
    cols = max([loc.c for loc in tile.keys()]) + 1
    grid = defaultdict(lambda: 10)
    for tr in range(reps):
        dr = rows * tr
        for tc in range(reps):
            dc = cols * tc
            for loc, risk in tile.items():
                grid[Location(loc.r + dr, loc.c + dc)] = 1 + (risk - 1 + tr + tc) % 9
    return grid

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    tile = parse_input(lines)
    risks = replicate_tile(tile, 5)
    # return search(risks)
    grid = dict_to_grid(risks)
    return grid_search(grid)

def solve(lines: Lines) -> int:
    """Solve the problem."""
    risks = parse_input(lines)
    # return search(risks)
    grid = dict_to_grid(risks)
    return grid_search(grid)


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
    assert result == 824
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
    assert result == 3063
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
