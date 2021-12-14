#!/usr/bin/env python3
#
#  Advent of Code 2019 - Day 12
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
        start-A
        start-b
        A-c
        A-b
        b-d
        A-end
        b-end
        """,
        10
    ),
    (
        """
        dc-end
        HN-start
        start-kj
        dc-start
        dc-HN
        LN-dc
        HN-end
        kj-sa
        kj-HN
        kj-dc
        """,
        19
    ),
    (
        """
        fs-end
        he-DX
        fs-he
        start-DX
        pj-DX
        end-zg
        zg-sl
        zg-pj
        pj-he
        RW-he
        fs-DX
        pj-RW
        zg-RW
        start-pj
        he-WI
        zg-he
        pj-fs
        start-RW
        """,
        226
    ),
]


SAMPLE_CASES2 = [
    (
        """
        start-A
        start-b
        A-c
        A-b
        b-d
        A-end
        b-end
        """,
        36
    ),
    (
        """
        dc-end
        HN-start
        start-kj
        dc-start
        dc-HN
        LN-dc
        HN-end
        kj-sa
        kj-HN
        kj-dc
        """,
        103
    ),
    (
        """
        fs-end
        he-DX
        fs-he
        start-DX
        pj-DX
        end-zg
        zg-sl
        zg-pj
        pj-he
        RW-he
        fs-DX
        pj-RW
        zg-RW
        start-pj
        he-WI
        zg-he
        pj-fs
        start-RW
        """,
        3509
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

Graph = dict[str, list[str]]

def parse_input(lines: Lines) -> Graph:
    graph = defaultdict(list)
    for line in lines:
        a, b = line.split("-")
        graph[a].append(b)
        graph[b].append(a)
    return graph

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    graph = parse_input(lines)
    paths = []
    queue = [("start", [], False)]
    while queue:
        node, hist, revisited = queue.pop(0)
        if node == "end":
            paths.append(hist + ["end"])
            continue
        for nayb in graph[node]:
            if  nayb.isupper():
                queue.append((nayb, hist + [node], revisited))
                continue
            if nayb == "start" or (revisited and nayb in hist):
                continue
            queue.append((nayb, hist + [node], revisited or nayb in hist))
    # for i, path in enumerate(sorted(paths)):
    #     print(f"{i:4d}: {path}")

    return len(paths)

def solve(lines: Lines) -> int:
    """Solve the problem."""
    graph = parse_input(lines)
    paths = []
    queue = [("start", [])]
    while queue:
        node, hist = queue.pop(0)
        if node == "end":
            paths.append(hist + ["end"])
            continue
        for nayb in graph[node]:
            if not nayb.isupper() and nayb in hist:
                continue
            queue.append((nayb, hist + [node]))
    return len(paths)


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
    assert result == 4573
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
    assert result == 117509
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
