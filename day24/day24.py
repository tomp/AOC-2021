#!/usr/bin/env python3
#
#  Advent of Code 2019 - Day 24
#
from typing import Sequence, Union, Optional, Any
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass, field
import math
import re

INPUTFILE = "input.txt"

ALU_CASES = [
    (
        """
        inp w
        add z w
        mod z 2
        div w 2
        add y w
        mod y 2
        div w 2
        add x w
        mod x 2
        div w 2
        mod w 2
        """,
        [12],
        [1, 1, 0, 0]
    ),
    (
        """
        inp z
        inp x
        mul z 3
        eql z x
        """,
        [2, 3],
        [0, 3, 0, 0]
    ),
    (
        """
        inp z
        inp x
        mul z 3
        eql z x
        """,
        [2, 6],
        [0, 6, 0, 1]
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

def load_text(text: str) -> Lines:
    return filter_blank_lines(text.split("\n"))

def filter_blank_lines(lines: Lines) -> Lines:
    return [line.strip() for line in lines if line.strip()]

# Solution

Operation = str
Variable = str

OPERATIONS = ["inp", "add", "mul", "div", "mod", "eql"]
VARIABLES = ["w", "x", "y", "z"]

@dataclass
class Instruction:
    op: Operation
    a: Variable
    b: Optional[Union[Variable, int]] = None
    
    def __post_init__(self):
        assert self.op in OPERATIONS
        assert self.a in VARIABLES
        if self.b is not None:
            if self.b not in VARIABLES:
                self.b = int(self.b)

    def __str__(self) -> str:
        return f"{self.op} {self.a}" if self.b is None else \
               f"{self.op} {self.a} {self.b}"

class ALU:
    def __init__(self, prog: list[Instruction]) -> None:
        self.prog = prog
        self.var = {"w": 0, "x": 0, "y": 0, "z": 0}
        self.ip = 0 # instruction pointer
        self.inp = [] # unread input data
        self.cycle = 0

    def reset(self)-> None:
        self.var = {"w": 0, "x": 0, "y": 0, "z": 0}
        self.inp = []
        self.cycle = 0

    def input(self, items: list[int]) -> None:
        self.inp.extend(items)

    def print_state(self):
        inp = self.cycle
        w = self.var["w"]
        x = self.var["x"]
        y = self.var["y"]
        z = self.var["z"]
        print(f"@{inp:-2d}  w:{w:-2d}  x:{x:-2d}  y:{y:-2d}  z:{z:-2d}")

    def run(self):
        self.ip = 0
        while self.ip < len(self.prog):
            self.step()
        self.print_state()
        return self.var["z"]

    def step(self) -> None:
        if self.ip < len(self.prog):
            ins = self.prog[self.ip]
            a = ins.a
            if isinstance(ins.b, str):
                b = self.var[ins.b]
            else:
                b = ins.b

            if ins.op == "inp":
                self.print_state()
                self.cycle += 1
                self.var[a] = self.inp.pop(0)
            elif ins.op == "add":
                self.var[a] += b
            elif ins.op == "mul":
                self.var[a] *= b
            elif ins.op == "div":
                self.var[a] //= b
            elif ins.op == "mod":
                self.var[a] = self.var[a] % b
            elif ins.op == "eql":
                self.var[a] = int(self.var[a] == b)
            else:
                raise RuntimeError(f"unrecognized instruction {ins}")
            # print(f"[{self.ip:02d}] {str(ins):10s}  "
            #       f"w:{self.var['w']} x:{self.var['x']} "
            #       f"y:{self.var['y']}  z:{self.var['z']} ")
            self.ip += 1


def parse_input(lines: Lines) -> list[Instruction]:
    result = []
    for line in lines:
        op, *vars = line.split()
        result.append(Instruction(op, *vars))
    return result

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    return 0

def solve(lines: Lines) -> int:
    """Solve the problem."""
    prog = parse_input(lines)
    alu = ALU(prog)
    model = 11527259839889
    last_model = 0
    while model > 11111111111111:
        alu.reset()
        digits = [int(v) for v in str(model)]
        if '0' not in digits:
            alu.input(digits)
            err = alu.run()
            if not err:
                print(model)
                last_model = model
        return model
        model -= 1
    return last_model


# PART 1

def example1() -> None:
    """Run example for problem with input arguments."""
    print("EXAMPLE 1:")
    for text, inp, expected in ALU_CASES:
        lines = load_text(text)
        prog = parse_input(lines)
        alu = ALU(prog)
        alu.input(inp)
        alu.run()
        result = [alu.var['w'], alu.var['x'], alu.var['y'], alu.var['z']] 
        print(f"'{text}' -> {result} (expected {expected})")
        assert result == expected
    print("= " * 32)

def part1(lines: Lines) -> None:
    print("PART 1:")
    result = solve(lines)
    print(f"result is {result}")
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
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    # example2()
    # part2(input_lines)
