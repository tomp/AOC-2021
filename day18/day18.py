#!/usr/bin/env python3
#
#  Advent of Code 2019 - Day 18
#
from typing import Sequence, Union, Any, Optional
from pathlib import Path
from collections import defaultdict
from itertools import permutations
from dataclasses import dataclass, field
import math
import re

INPUTFILE = "input.txt"

EXPLODE_CASES = [
    (
        "[[[[[9,8],1],2],3],4]",
        "[[[[0,9],2],3],4]"
    ),
    (   
        "[7,[6,[5,[4,[3,2]]]]]",
        "[7,[6,[5,[7,0]]]]"
    ),
    (   
        "[[6,[5,[4,[3,2]]]],1]",
        "[[6,[5,[7,0]]],3]"
    ),
    (   
        "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]",
        "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"
    ),
    (  
        "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]",
        "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"
    ),
]

SPLIT_CASES = [
    (
        "[[[[0,7],4],[[7,8],[0,13]]],[1,1]]",
        "[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]"
    ),
]

REDUCE_CASES = [
    (
        "[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]",
        "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"
    ),
]

ADDITION_CASES = [
    (
        """
        [1,1]
        [2,2]
        [3,3]
        [4,4]
        """,
        "[[[[1,1],[2,2]],[3,3]],[4,4]]"
    ),
    (
        """
        [1,1]
        [2,2]
        [3,3]
        [4,4]
        [5,5]
        """,
        "[[[[3,0],[5,3]],[4,4]],[5,5]]"
    ),
    (
        """
        [1,1]
        [2,2]
        [3,3]
        [4,4]
        [5,5]
        [6,6]
        """,
        "[[[[5,0],[7,4]],[5,5]],[6,6]]"
    ),
    (
        """
        [[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
        [7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
        [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
        [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
        [7,[5,[[3,8],[1,4]]]]
        [[2,[2,2]],[8,[8,1]]]
        [2,9]
        [1,[[[9,3],9],[[9,0],[0,7]]]]
        [[[5,[7,4]],7],1]
        [[[[4,2],2],6],[8,7]]
        """,
        "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"
    ),
    (
        """
        [1,1]
        [2,2]
        [3,3]
        [4,4]
        """,
        "[[[[1,1],[2,2]],[3,3]],[4,4]]"
    ),
]

SAMPLE_CASES = [
    (
        """
        [[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
        [[[5,[2,8]],4],[5,[[9,9],0]]]
        [6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
        [[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
        [[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
        [[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
        [[[[5,4],[7,7]],8],[[8,3],8]]
        [[9,3],[[9,9],[6,[4,9]]]]
        [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
        [[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
        """,
        4140
    ),
]

SAMPLE_CASES2 = [
    (
        """
        [[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
        [[[5,[2,8]],4],[5,[[9,9],0]]]
        [6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
        [[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
        [[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
        [[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
        [[[[5,4],[7,7]],8],[[8,3],8]]
        [[9,3],[[9,9],[6,[4,9]]]]
        [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
        [[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
        """,
        3993
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

## Use these if blank lines should be discarded.

def load_text(text: str) -> Lines:
    return filter_blank_lines(text.split("\n"))

def filter_blank_lines(lines: Lines) -> Lines:
    return [line.strip() for line in lines if line.strip()]

# Solution

OPEN_BRACE, CLOSE_BRACE, COMMA = "[", "]", ","
INT_RE = re.compile(r"\d+")

Pair = list[Union[str, int]]

class Pair:
    def __init__(self, pair: list[Union[str, int]]) -> None:
        self.pair = pair

    def __str__(self) -> str:
        return "".join(map(str, self.pair))

    def __repr__(self) -> str:
        return str(self)

    def __add__(self, other: "Pair") -> "Pair":
        pair = Pair([OPEN_BRACE] + self.pair + [COMMA] + other.pair + [CLOSE_BRACE])
        pair.reduce()
        return pair

    @classmethod
    def from_text(cls, text: str) -> "Pair":
        text = text.strip().replace(" ", "")
        pair, _ = parse_pair(text)
        return cls(pair)

    def __abs__(self) -> int:
        outq = []
        cur = 0
        while cur < len(self.pair):
            if self.pair[cur] == CLOSE_BRACE:
                y = outq.pop()
                x = outq.pop()
                outq.append(3*x + 2*y)
            elif is_int(self.pair[cur]):
                outq.append(self.pair[cur])
            cur += 1
        assert len(outq) == 1
        return outq.pop()

    def reduce(self) -> bool:
        reduced = False
        # print(f"reduce: {str(self)}")
        while True:
            exploded, split_value = False, False
            while self.explode():
                # print(f"After explode: {str(self)}")
                exploded = True
            if self.split():
                # print(f"After split:   {str(self)}")
                split_value = True
            if not (exploded or split_value):
                break
            reduced = True
        return reduced
        

    def explode(self) -> bool:
        """Find and explode the next eligble sub-pair.
        Returns True if a sub-pair was exploded, else False.
        """
        # print(f"explode: {str(self)}")
        cur = 0
        depth = 0
        x_target = 0
        shrapnel = -1 
        exploded = False
        while True:
            # print(f"[{depth}] cur: {cur} {''.join(map(str, self.pair[:cur]))}"
            #       f"*{''.join(map(str, self.pair[cur:]))}")

            if self.pair[cur] == OPEN_BRACE:
                depth += 1
                if depth > 4 and shrapnel == -1:
                    if is_int(self.pair[cur+1]) and is_int(self.pair[cur+3]):
                        # explode this pair
                        if x_target:
                            self.pair[x_target] += self.pair[cur+1]
                        shrapnel = self.pair[cur+3]
                        # print(f"{''.join(map(str, self.pair[cur:cur+5]))} "
                        #       f"-> {self.pair[cur+1]}, 0, {shrapnel}")
                        self.pair[cur:cur+5] = [0]
                        exploded = True
                        depth -= 1
                        cur += 1
                        continue
                cur += 1

            elif self.pair[cur] == CLOSE_BRACE:
                depth -= 1
                cur += 1
                if cur >= len(self.pair):
                     break

            elif self.pair[cur] == COMMA:
                cur += 1

            elif is_int(self.pair[cur]):
                if shrapnel > -1:
                    self.pair[cur] += shrapnel
                    break
                if not exploded:
                    x_target = cur
                cur += 1

        return exploded


    def split(self) -> bool:
        """Find and split the next eligble regular number.
        Returns True if a regular number was split, else False.
        """
        # print(f"split: {str(self)}")
        cur = 0
        split_value = False
        while cur < len(self.pair):
            if self.pair[cur] in (OPEN_BRACE, CLOSE_BRACE, COMMA):
                cur += 1
            elif is_int(self.pair[cur]):
                if self.pair[cur] > 9:
                    val = self.pair[cur]
                    left, right = val // 2, val - (val // 2)
                    self.pair[cur:cur+1] = ["[", left, ",", right, "]"]
                    split_value = True
                    break
                cur += 1

        return split_value


def is_int(val: Any) -> bool:
    return isinstance(val, int)

def parse_pair(text: str, cur: int = 0) -> tuple[Pair, int]:
    """Parse the string repreentation of the given pair into list form.
    The list representation of the pair is returned.
    """
    result = []
    if text[cur] == OPEN_BRACE:
        result.append(text[cur])
        cur += 1

        pair, cur = parse_pair(text, cur)
        result.extend(pair)

        assert text[cur] == COMMA
        result.append(text[cur])
        cur += 1

        pair, cur = parse_pair(text, cur)
        result.extend(pair)

        assert text[cur] == CLOSE_BRACE
        result.append(text[cur])
        cur += 1

        return result, cur

    m = INT_RE.match(text, cur)
    if not m:
        raise ValueError(f"no pair found in '{text[cur:]}'")
    result.append(int(m.group()))
    cur += len(m.group())

    return result, cur


def solve2(lines: Lines) -> int:
    """Solve the problem."""
    pairs = [Pair.from_text(line) for line in lines]
    max_abs = 0
    for p1, p2 in permutations(pairs, 2):
        p = p1 + p2
        p.reduce()
        if abs(p) > max_abs:
            max_abs = abs(p)
    return max_abs

def solve(lines: Lines) -> int:
    """Solve the problem."""
    pairs = [Pair.from_text(line) for line in lines]
    pair = pairs.pop(0)
    for p in pairs:
        pair += p
    pair.reduce()
    return abs(pair)


# PART 1

def example1() -> None:
    """Run example for problem with input arguments."""
    print("UNIT TESTS 1:")
    for text, expected in EXPLODE_CASES:
        pair = Pair.from_text(text)
        pair.explode()
        result = str(pair)
        print(f"'{text}' -> {result} (expected {expected})")
        assert result == expected

    for text, expected in SPLIT_CASES:
        pair = Pair.from_text(text)
        pair.split()
        result = str(pair)
        print(f"'{text}' -> {result} (expected {expected})")
        assert result == expected

    for text, expected in REDUCE_CASES:
        pair = Pair.from_text(text)
        pair.reduce()
        result = str(pair)
        print(f"'{text}' -> {result} (expected {expected})")
        assert result == expected

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
    assert result == 4137
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
    assert result == 4573
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
