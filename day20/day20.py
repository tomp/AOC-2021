#!/usr/bin/env python3
#
#  Advent of Code 2019 - Day 20
#
from typing import Sequence, Union, Optional, Any
from pathlib import Path
from collections import defaultdict
from itertools import chain
from dataclasses import dataclass
import math
import re

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    (
        """
        ..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

        #..#.
        #....
        ##..#
        ..#..
        ..###
        """,
        35
    ),
]

SAMPLE_CASES2 = [
    (
        """
        ..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

        #..#.
        #....
        ##..#
        ..#..
        ..###
        """,
        3351
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

def load_text(text: str) -> Lines:
    return [line.strip() for line in text.strip("\n").split("\n")]

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

def parse_input(lines: Lines) -> tuple[str, Lines]:
    part1, part2 = parse_sections(lines)
    algo = part1[0].strip().replace(".", "0").replace("#", "1")
    image = [row.replace(".", "0").replace("#", "1") for row in part2]
    return algo, image

def expand(image: Lines, back: str = "0") -> Lines:
    cols = len(image[0])
    empty = [back * cols]
    return [ (back * 3) + row + (back * 3) for row in chain(empty, empty, empty, image, empty, empty, empty)]

def enhance(image: Lines, algo: str, back: str = "0") -> Lines:
    work = []
    image = expand(image, back)
    rows, cols = len(image), len(image[0])
    # print(f"==== enhance {rows} x {cols} image  (background '{back}')")
    for r in range(0, rows-2):
        row = []
        for c in range(1, cols-1):
            code = int(image[r][c-1:c+2] + image[r+1][c-1:c+2] + image[r+2][c-1:c+2], 2)
            row.append(algo[code])
        work.append("".join(row))
    back = work[0][0]
    result = [row[1:-1] for row in work[1:-1]]
    return result, back

def display(image: Lines) -> None:
    print("-" * len(image[0]))
    print("\n".join(["".join(["#" if v == "1" else "." for v in row]) for row in image]))

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    algo, image = parse_input(lines)
    print(f"algorithm has length {len(algo)}")
    print(f"image size: w:{len(image[0])}  h:{len(image)}")

    back = "0"
    display(image)

    for _ in range(50):
        image, back = enhance(image, algo, back)
    result = sum([row.count("1") for row in image])
    return result

def solve(lines: Lines) -> int:
    """Solve the problem."""
    algo, image = parse_input(lines)
    print(f"algorithm has length {len(algo)}")
    print(f"image size: w:{len(image[0])}  h:{len(image)}")

    back = "0"
    display(image)

    for _ in range(2):
        image, back = enhance(image, algo, back)
        display(image)

    result = sum([row.count("1") for row in image])
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
    assert result == 5437
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
    assert result == 19340
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
