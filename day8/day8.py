#!/usr/bin/env python3
#
#  Advent of Code 2019 - Day 8
#
from typing import Sequence, Any
from pathlib import Path
from collections import defaultdict

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    (
"""
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
""",
        26
    ),
]


SAMPLE_CASES2 = [
    (
"""
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
""",
        61229
    ),
]

SEGMENTS = {
    0: ('a', 'b', 'c',      'e', 'f', 'g'),
    1: (          'c',           'f'     ),
    2: ('a',      'c', 'd', 'e',      'g'),
    3: ('a',      'c', 'd',      'f', 'g'),
    4: (     'b', 'c', 'd',      'f'     ),
    5: ('a', 'b',      'd',      'f', 'g'),
    6: ('a', 'b',      'd', 'e', 'f', 'g'),
    7: ('a',      'c',           'f'     ),
    8: ('a', 'b', 'c', 'd', 'e', 'f', 'g'),
    9: ('a', 'b', 'c', 'd',      'f', 'g'),
}

PATTERNS = { digit: "".join(segments) for digit, segments in SEGMENTS.items() }

DIGITS = {pattern: digit for digit, pattern in PATTERNS.items()}

UNIQUE_LENGTH = (2, 3, 4, 7)


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

def parse_input(lines: Lines):
    result = []
    for line in lines:
        part1, part2 = line.split(" | ")
        patterns = part1.split()
        digits = part2.split()
        result.append((patterns, digits))
    return result

def normalize_pattern(patt):
    return "".join(sorted(patt))

def decode_value(patterns, digits) -> int:

    # print(f"{'-' * 64}\ndecode_value")
    # print(f"patterns: {patterns}")
    # print(f"digits: {digits}")

    patterns = [normalize_pattern(patt) for patt in patterns]
    digits = [normalize_pattern(patt) for patt in digits]

    digit_code = {}  # map digit to pattern
    segment_code = {} # map found segment to actual segment label
    has_segments = defaultdict(set) # map digit to found segments
    has_digits = defaultdict(set) # map found segment to digits

    for patt in patterns:
        if len(patt) == 2:
            digit = 1
        elif len(patt) == 3:
            digit = 7
        elif len(patt) == 4:
            digit = 4
        elif len(patt) == 7:
            digit = 8
        else:
            continue
        digit_code[digit] = patt
        for segment in patt:
            has_digits[digit].add(segment)

    # print(f"digit_code: {digit_code}")

    for segment in digit_code[7]:
        if segment not in digit_code[1]:
            segment_code[segment] = "a"
            break

    digit_count = defaultdict(int) # map found segment to number of digits it is in
    for segment in "abcdefg":
        for patt in patterns:
            if segment in patt:
                digit_count[segment] += 1

    # print(f"digit_count: {digit_count}")

    for segment, count in digit_count.items():
        if count == 9:
            segment_code[segment] = "f"
        elif count == 6:
            segment_code[segment] = "b"
        elif count == 4:
            segment_code[segment] = "e"
        elif count == 7:
            if segment in digit_code[4]:
                segment_code[segment] = "d"
            else:
                segment_code[segment] = "g"
        elif count == 8:
            if segment not in segment_code:
                segment_code[segment] = "c"

    # print(f"segment_code: {segment_code}")
                
    for patt in patterns:
        real_patt = "".join(sorted([segment_code[v] for v in patt]))
        digit = DIGITS[real_patt]
        digit_code[digit] = patt

    # print(f"digit_code: {digit_code}")

    pattern_digit = {patt: str(digit) for digit, patt in digit_code.items()}

    # print(f"pattern_digit: {pattern_digit}")
    
    value = int("".join([pattern_digit[patt] for patt in digits]))

    # print(f"value: {digits} -> {value}")

    return value


def solve2(lines: Lines) -> int:
    """Solve the problem."""
    notes = parse_input(lines)
    result = 0
    for patterns, digits in notes:
        value = decode_value(patterns, digits)
        result += value
    return result

def solve(lines: Lines) -> int:
    """Solve the problem."""
    notes = parse_input(lines)
    result = 0
    for patterns, digits in notes:
        for digit in digits:
            if len(digit) in UNIQUE_LENGTH:
                result += 1
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
    assert result == 504
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
    assert result == 1073431
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
