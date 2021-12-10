#!/usr/bin/env python3
#
#  Advent of Code 2019 - Day 10
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
        [({(<(())[]>[[{[]{<()<>>
        [(()[<>])]({[<{<<[]>>(
        {([(<{}[<>[]}>{[]{[(<()>
        (((({<>}<{<{<>}{[]{[]{}
        [[<[([]))<([[{}[[()]]]
        [{[{({}]{}}([{[{{{}}([]
        {<[[]]>}<{[{[{[]{()[[[]
        [<(<(<(<{}))><([]([]()
        <{([([[(<>()){}]>(<<{{
        <{([{{}}[<[[[<>{}]]]>[]]
        """,
        26397
    ),
]

SAMPLE_CASES2 = [
    (
        """
        [({(<(())[]>[[{[]{<()<>>
        [(()[<>])]({[<{<<[]>>(
        {([(<{}[<>[]}>{[]{[(<()>
        (((({<>}<{<{<>}{[]{[]{}
        [[<[([]))<([[{}[[()]]]
        [{[{({}]{}}([{[{{{}}([]
        {<[[]]>}<{[{[{[]{()[[[]
        [<(<(<(<{}))><([]([]()
        <{([([[(<>()){}]>(<<{{
        <{([{{}}[<[[[<>{}]]]>[]]
        """,
        288957
    ),
]

Lines = Sequence[str]

CLOSE = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}

PENALTY = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

VALUE = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}


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

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    scores = []
    for line in lines:
        stack = []
        corrupt = False
        for ch in line:
            if ch in CLOSE:
                stack.append(CLOSE[ch])
            elif ch == stack[-1]:
                stack.pop()
            else:
                corrupt = True
        if not corrupt and stack:
            score = 0
            for ch in reversed(stack):
                score = score* 5 + VALUE[ch]
            scores.append(score)

    i = len(scores) // 2
    scores.sort()

    return scores[i]

def solve(lines: Lines) -> int:
    """Solve the problem."""
    score = 0
    for lineno, line in enumerate(lines):
        stack = []
        for ch in line:
            if ch in CLOSE:
                stack.append(CLOSE[ch])
            elif ch == stack[-1]:
                stack.pop()
            else:
                score += PENALTY[ch]
                break
                print(f"unexpected character: '{ch}'")
    return score


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
    assert result == 266301
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
    assert result == 3404870164
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
