#!/usr/bin/env python3
#
#  Advent of Code 2019 - Day 17
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
        target area: x=20..30, y=-10..-5        
        """,
        45
    ),
]

SAMPLE_CASES2 = [
    (
        """
        target area: x=20..30, y=-10..-5        
        """,
        112
    ),
]

TARGET_AREA_RE = re.compile(r"target area: x=(-?\d+)[.][.](-?\d+), y=(-?\d+)[.][.](-?\d+)") 

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

def parse_input(text: str) ->  tuple[int, int, int, int]:
    m = TARGET_AREA_RE.match(text)
    xmin, xmax, ymin,  ymax = map(int, m.groups())
    return xmin, xmax, ymin, ymax

def invsum(ntot: int) -> float:
    assert ntot > 0
    return (math.sqrt(1 + 8 * ntot) - 1) / 2

def seqsum(n: int) -> int:
    assert n > 0
    return (n * (n + 1)) // 2

def x_at_t(vx: int, t: int) -> int:
    assert vx > 0 and t >= 0
    if t >= vx:
        return int(vx * (vx + 1) / 2)
    return int((vx * t) - (t * (t - 1) / 2))

def y_at_t(vy: int, t: int) -> int:
    assert t >= 0
    return int((vy * t) - (t * (t - 1) / 2))

def vx_for_xt_at_t(xt: int, t: int) -> float:
    assert xt > 0 and t >= 0
    return (xt + (t * (t - 1) / 2)) / t

def vy_for_yt_at_t(yt: int, t: int) -> float:
    assert t >= 0
    return (yt + (t * (t - 1) / 2)) / t

def t_for_xt_and_vx(xt: int, vx: int) -> float:
    assert 0 <= xt <= max_xt(vx)
    return vx + 0.5 - math.sqrt((vx * vx) + vx - (2 * xt) + 0.25)

def t_for_yt_and_vy(yt: int, vy: int) -> float:
    assert yt <= y_highest(vy)
    term1 = vy + 0.5
    term2 = math.sqrt(vy * vy + vy - 2 * yt + 0.25)
    if term2 > term1:
        return  term1 + term2
    return  term1 - term2

def max_xt(vx: int) -> int:
    assert vx > 0
    return vx * (vx + 1) // 2

def min_vx(xf: int) -> float:
    assert xf > 0
    return (math.sqrt(1 + 8 * xf) - 1) / 2

def y_highest(vy: int) -> int:
    if vy > 0:
        return vy * (vy + 1) / 2
    return 0

def hits_target(vx, vy, target) -> tuple[bool, int]:
    xmin, xmax, ymin, ymax = target
    assert max_xt(vx) >= xmin
    height = y_highest(vy)
    t_start = math.floor(t_for_yt_and_vy(ymax, vy))
    t_end = math.ceil(t_for_yt_and_vy(ymin, vy))
    for t in range(t_start, t_end+2):
        xt = x_at_t(vx, t)
        yt = y_at_t(vy, t)
        on_target = ymin <= yt <= ymax and xmin <= xt <= xmax
        if on_target:
            return True, height
    return False, None

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    target = parse_input(lines[0])
    xmin, xmax, ymin, ymax = target
    # print(f"target: {xmin} <= x <= {xmax} and {ymin} <= y <= {ymax}")

    vx_min, vx_max = math.ceil(min_vx(xmin)), abs(xmax)
    # print(f"vx range: {vx_min} : {vx_max}")

    count = 0
    for vx in range(vx_min, vx_max+1):
        t_at_xmin = t_for_xt_and_vx(xmin, vx)
        vy_min = math.ceil(vy_for_yt_at_t(ymin, t_at_xmin))
        vy_max = abs(ymin)
        for vy in range(vy_min, vy_max+1):
            hit, height = hits_target(vx, vy, target)
            # print(f"(vx, vy) = ({vx}, {vy})  ->  {hit},  {height}") 
            if hit:
                count += 1
    return count

def solve(lines: Lines) -> int:
    """Solve the problem."""
    target = parse_input(lines[0])
    xmin, xmax, ymin, ymax = target
    # print(f"target: {xmin} <= x <= {xmax} and {ymin} <= y <= {ymax}")

    vx_min, vx_max = math.ceil(min_vx(xmin)), math.floor(min_vx(xmax))

    max_height = 0
    for vx in range(vx_min, vx_max+1):
        t_at_xmin = t_for_xt_and_vx(xmin, vx)
        vy_min = math.ceil(vy_for_yt_at_t(ymin, t_at_xmin))
        vy_max = math.ceil(3 * abs(ymax - ymin))
        for vy in range(vy_min, vy_max+1):
            hit, height = hits_target(vx, vy, target)
            # print(f"(vx, vy) = ({vx}, {vy})  ->  {hit},  {height}") 
            if hit and height > max_height:
                max_height = height
    return max_height


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
    assert result == 5886
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
    assert result == 1806
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
