#!/usr/bin/env python3
#
#  Advent of Code 2019 - Day 14
#
from typing import Sequence, Any
from pathlib import Path
from collections import Counter, defaultdict

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    (
        """
        NNCB

        CH -> B
        HH -> N
        CB -> H
        NH -> C
        HB -> C
        HC -> B
        HN -> C
        NN -> C
        BH -> H
        NC -> B
        NB -> B
        BN -> B
        BB -> N
        BC -> B
        CC -> N
        CN -> C
        """,
        1588
    ),
]

SAMPLE_CASES2 = [
    (
        """
        NNCB

        CH -> B
        HH -> N
        CB -> H
        NH -> C
        HB -> C
        HC -> B
        HN -> C
        NN -> C
        BH -> H
        NC -> B
        NB -> B
        BN -> B
        BB -> N
        BC -> B
        CC -> N
        CN -> C
        """,
        2188189693529
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

def parse_input(lines) -> tuple[str, dict[str, str]]:
    sect1, sect2 = parse_sections(lines)
    template = sect1[0]
    rules = {}
    for line in sect2:
        pair, insert = line.split(" -> ")
        rules[pair] = insert
    return template, rules

def apply_rules2(pairs: str, rules: dict[str, str]) -> str:
    result = defaultdict(int)
    for pair, count in pairs.items():
        insert = rules.get(pair, "")
        if insert:
            ac = pair[0] + insert
            cb = insert + pair[1]
            result[ac] += count
            result[cb] += count
        else:
            result[pair] += count
    return result

def apply_rules(polymer: str, rules: dict[str, str]) -> str:
    result = []
    for i in range(len(polymer)-1):
        result.append(polymer[i])
        insert = rules.get(polymer[i:i+2], "")
        if insert:
            result.append(insert)
    result.append(polymer[i+1])
    return "".join(result)

def solve2(lines: Lines, steps=40) -> int:
    """Solve the problem."""
    polymer, rules = parse_input(lines)
    element0, elementN = polymer[0], polymer[-1]

    pairs = defaultdict(int)
    for i in range(len(polymer)-1):
        pairs[polymer[i:i+2]] += 1

    for step in range(steps):
        pairs = apply_rules2(pairs, rules)
        # print(f"After step {step+1}: {sum(pairs.values()) + 1}")
    element = defaultdict(int)
    element[elementN] += 1
    for pair, count in pairs.items():
        element[pair[0]] += count

    counts = list(element.items())
    counts.sort(key=lambda count: count[1], reverse=True)

    max_element, max_count = counts[0]
    min_element, min_count = counts[-1]
    return max_count - min_count

def solve(lines: Lines, steps=10) -> int:
    """Solve the problem."""
    polymer, rules = parse_input(lines)
    # print(f"Template:     {polymer}")
    for step in range(steps):
        polymer = apply_rules(polymer, rules)
        # print(f"After step {step+1}: {polymer}")
    counts = list(Counter(polymer).most_common())
    max_element, max_count = counts[0]
    min_element, min_count = counts[-1]
    return max_count - min_count


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
    assert result == 4517
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
    assert result == 4704817645083
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
