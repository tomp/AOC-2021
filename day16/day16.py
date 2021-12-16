#!/usr/bin/env python3
#
#  Advent of Code 2019 - Day 16
#
from typing import Sequence, Union
from pathlib import Path
from dataclasses import dataclass
import math

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    ("8A004A801A8002F478", 16),
    ("620080001611562C8802118E34", 12),
    ("C0015000016115A2E0802F182340", 23),
    ("A0016C880162017C3686B18A3D4780", 31)
]

SAMPLE_CASES2 = [
    ("C200B40A82", 3),
    ("04005AC33890", 54),
    ("880086C3E88112", 7),
    ("CE00C43D881120", 9),
    ("D8005AC2A8F0", 1),
    ("F600BC2D8F", 0),
    ("9C005AC2F8F0", 0),
    ("9C0141080250320F1802104A08", 1),
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

ONE, ZERO = 1, 0

@dataclass(frozen=True)
class Packet:
    ver: int
    typ: int
    val: Union[int, list["Packet"]]

    def version_sum(self) -> int:
        if self.typ == 4:
            return self.ver
        return self.ver + sum([p.version_sum() for p in self.val])

    def value(self) -> int:
        if self.typ == 0:
            return sum([p.value() for p in self.val])
        if self.typ == 1:
            return math.prod([p.value() for p in self.val])
        if self.typ == 2:
            return min([p.value() for p in self.val])
        if self.typ == 3:
            return max([p.value() for p in self.val])
        if self.typ == 4:
            return self.val

        p1, p2 = self.val
        if self.typ == 5:
            return int(p1.value() > p2.value())
        if self.typ == 6:
            return int(p1.value() < p2.value())
        if self.typ == 7:
            return int(p1.value() == p2.value())


PACKET_EXAMPLES = [
    (
        "110100101111111000101000", Packet(6, 4, 2021)
    ),
    (
        "00111000000000000110111101000101001010010001001000000000",
        Packet(1, 6, [Packet(6, 4, 10), Packet(2, 4, 20)])
    ),
    (
        "11101110000000001101010000001100100000100011000001100000",
        Packet(7, 3, [Packet(2, 4, 1), Packet(4, 4, 2), Packet(1, 4, 3)])
    ),
]


def parse_input(text: str) -> str:
    """Return a string of '1's and '0''s representing the input hex string."""
    return "".join([f"{int(text[i:i+2], 16):08b}" for i in range(0, len(text), 2)])

def consume(bits: str, cur: int, size: int) -> tuple[int, int]:
    instr, incur = bits[cur:cur+size], cur
    val, cur = int(bits[cur:cur+size], 2), cur+size
    # print(f"[consume @{incur} {instr} -> {val}, {cur}]")
    return val, cur

def parse_packet(bits: str, cur: int = 0) -> tuple[Packet, int]:
    ver, cur = consume(bits, cur, 3)
    typ, cur = consume(bits, cur, 3)
    if typ == 4:
        val, more = 0, True
        while more:
            more, cur = consume(bits, cur, 1)
            chunk, cur = consume(bits, cur, 4)
            val = (val * 16) + chunk
        p = Packet(ver, typ, val)
        return p, cur

    ltyp, cur = consume(bits, cur, 1)
    if ltyp == ZERO:
        sub_size, cur = consume(bits, cur, 15)
        sub_packets = []
        start = cur
        while cur - start < sub_size:
            p, cur = parse_packet(bits, cur)
            sub_packets.append(p)
        return Packet(ver, typ, sub_packets), cur
    else:
        sub_len, cur = consume(bits, cur, 11)
        sub_packets = []
        start = cur
        for _ in range(sub_len):
            p, cur = parse_packet(bits, cur)
            sub_packets.append(p)
        return Packet(ver, typ, sub_packets), cur


def solve2(lines: Lines) -> int:
    """Solve the problem."""
    bits = parse_input(lines[0])
    packet, _ = parse_packet(bits)
    return packet.value()

def solve(lines: Lines) -> int:
    """Solve the problem."""
    bits = parse_input(lines[0])
    packet, _ = parse_packet(bits)
    return packet.version_sum()


# PART 1
902198718880
def example1() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 1:")
    for text, expected in PACKET_EXAMPLES:
        p, _ = parse_packet(text)
        print(f"'{text}' -> {p} (expected {expected})")
        assert p == expected
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
    assert result == 951
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
    assert result == 902198718880
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
