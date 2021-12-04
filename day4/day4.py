#!/usr/bin/env python3
#
#  Advent of Code 2021 - Day 4
#
from typing import Sequence, Any
from collections import defaultdict
from itertools import chain
from dataclasses import dataclass
from pathlib import Path

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    (
        """
        7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

        22 13 17 11  0
         8  2 23  4 24
        21  9 14 16  7
         6 10  3 18  5
         1 12 20 15 19

         3 15  0  2 22
         9 18 13 17  5
        19  8  7 25 23
        20 11 10 24  4
        14 21 16 12  6

        14 21 17 24  4
        10 16 15  9 19
        18  8 23 26 20
        22 11 13  6  5
         2  0 12  3  7
        """, 
        4512
    ),
]

SAMPLE_CASES2 = [
    (
        """
        7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

        22 13 17 11  0
         8  2 23  4 24
        21  9 14 16  7
         6 10  3 18  5
         1 12 20 15 19

         3 15  0  2 22
         9 18 13 17  5
        19  8  7 25 23
        20 11 10 24  4
        14 21 16 12  6

        14 21 17 24  4
        10 16 15  9 19
        18  8 23 26 20
        22 11 13  6  5
         2  0 12  3  7
        """, 
        1924
    ),
]

Lines = Sequence[str]
Sections = Sequence[Lines]

# Utility functions

def sample_input(text) -> Lines:
    return text.strip("\n").split("\n")

def load_text(text: str) -> Lines:
    return [line.strip() for line in text.split("\n")]

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

def parse_input(lines):
    sects = parse_sections(lines)
    numbers = [int(v) for v in sects[0][0].split(",")]
    boards = []
    for lines in sects[1:]:
        board = [[int(v) for v in line.split()] for line in lines]
        boards.append(board)
    return numbers, boards

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    numbers, boards = parse_input(lines)
    # print(f"numbers: {numbers}")
    # for board in boards:
    #     print()
    #     print("\n".join([" ".join([f"{v:2d}" for v in row]) for row in board]))

    nboard = len(boards)

    board_values = []
    for board in boards:
        values = set(chain(*board))
        board_values.append(values)

    row_values = []
    for idx, board in enumerate(boards):
        for row in board:
            row_values.append((set(row), idx))
        for c in range(5):
            row_values.append((set([row[c] for row in board]), idx))

    bingo = set()
    for i in range(len(numbers)):
        called = set(numbers[:i+1])
        for values, idx in row_values:
            if len(values - called) == 0 and idx not in bingo:
                bingo.add(idx)
                board_num = idx
                last_call = numbers[i]
        if len(bingo) == nboard:
            break

    # print(f"{len(bingo)} bingos after {i} calls")
    # print(bingo)

    score = sum(list(board_values[board_num] - called))
    return score * last_call
    

def solve(lines: Lines) -> int:
    """Solve the problem."""
    numbers, boards = parse_input(lines)
    # print(f"numbers: {numbers}")
    # for board in boards:
    #     print()
    #     print("\n".join([" ".join([f"{v:2d}" for v in row]) for row in board]))

    board_values = []
    for board in boards:
        values = set(chain(*board))
        board_values.append(values)

    row_values = []
    for idx, board in enumerate(boards):
        for row in board:
            row_values.append((set(row), idx))
        for c in range(5):
            row_values.append((set([row[c] for row in board]), idx))

    # print(board_values[-1])
    # for values in row_values[-10:]:
    #     print(values)

    bingo = set()
    for i in range(len(numbers)):
        called = set(numbers[:i+1])
        for values, idx in row_values:
            if len(values - called) == 0:
                bingo.add(idx)
        if bingo:
            last_call = numbers[i]
            break

    board_num = bingo.pop()
    # print(f"{len(bingo)} bingos after {i} calls")
    # print(bingo)

    score = sum(list(board_values[board_num] - called))

    return score * last_call
    

# PART 1

def example1() -> None:
    """Run example for problem with input lines."""
    print("EXAMPLE 1:")
    text, expected = SAMPLE_CASES[0]
    lines = load_text(text)
    result = solve(lines)
    print(f"'sample-input' -> {result} (expected {expected})")
    assert result == expected
    print("= " * 32)

def part1(lines: Lines) -> None:
    print("PART 1:")
    result = solve(lines)
    print(f"result is {result}")
    assert result == 50008
    print("= " * 32)


# PART 2

def example2() -> None:
    """Run example for problem with input lines."""
    print("EXAMPLE 2:")
    text, expected = SAMPLE_CASES2[0]
    lines = load_text(text)
    result = solve2(lines)
    print(f"'sample-input' -> {result} (expected {expected})")
    assert result == expected
    print("= " * 32)

def part2(lines: Lines) -> None:
    print("PART 2:")
    result = solve2(lines)
    print(f"result is {result}")
    assert result == 17408
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
