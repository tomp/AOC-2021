#!/usr/bin/env python3
#
#  Advent of Code 2019 - Day 21
#
from typing import Sequence, Union, Optional, Any, Generator
from pathlib import Path
from collections import defaultdict
from functools import cache
from dataclasses import dataclass, field
import math
import re

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    (
        """
        Player 1 starting position: 4
        Player 2 starting position: 8
        """,
        739785
    ),
]

SAMPLE_CASES2 = [
    (
        """
        Player 1 starting position: 4
        Player 2 starting position: 8
        """,
        444356092776315
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

INPUT_RE = re.compile(r"Player (\d+) starting position: (\d+)$")

def parse_input(lines: Lines) -> tuple[int, int]:
    result = {}
    for line in lines:
        m = INPUT_RE.match(line)
        player, pos = map(int, m.groups())
        result[player] = pos
    return result

@dataclass
class DeterministicDie:
    sides: int
    _state: int = field(default=0)
    rolls: int = field(default=0)

    def __post_init__(self):
        assert self.sides > 1

    def roll(self, rolls: int = 1) -> int:
        result = 0
        for _ in range(rolls):
            result += self._state + 1
            self._state = (self._state + 1) % self.sides
            self.rolls += 1
        return result

@cache
def rolls(sides: int = 3, nrolls: int = 3) -> dict[int, int]:
    """Perform 'nrolls' die rolls and return a dict mapping the sum of these
    rolls to the number of times this resulted, which is also the number of
    new universes created for that result.
    """
    init_dist: IntegerDist = defaultdict(int)
    init_dist[0] = 1
    for _ in range(nrolls):
        dist = defaultdict(int)
        for roll in range(1, sides+1):
            for val, count in init_dist.items():
                dist[val+roll] += count
        init_dist = dist
    return dist

def play(pos: dict[int, int]) -> tuple[dict[int, int], int]:
    """Return dict mapping player to their score, and the number of die rolls."""
    players = [1, 2]
    score = {p: 0 for p in players}
    MAX_SCORE = 1000
    die = DeterministicDie(100)
    while True:
        for player in players:
            roll = die.roll(3)
            pos[player] = (pos[player] + roll - 1) % POSITIONS + 1
            score[player] += pos[player]
            if score[player] >= MAX_SCORE:
                return score, die.rolls
        # print(pos, score)


StateDict = dict[tuple[int, int], int]  # map (position, score) to universe count
IntegerDist = dict[int, int]  # map value to frequency

DIRAC_SIDES = 3
POSITIONS = 10

class Game:
    """A two-player Dirac dice match.
    pos1, pos2 .. intial positions for players 1 and 2
    state ...... map (position1, score1, positions2, score2) tuple to number of universes in that state
    """
    def __init__(self, pos1: int, pos2: int, win: int = 21) -> None:
        self.winning_score: int = win
        self.state: StateDict = {(pos1, 0, pos2, 0): 1}
        self.wins1: int = 0
        self.wins2: int = 0
        self.turn: int = 0

    @property
    def universes(self) -> int:
        return sum(self.state.values())

    def step(self) -> "Player":
        """Roll the die three times and check for wins.
        """
        dirac_roll = rolls(3, 3)

        # Player 1 rolls...
        state: StateDict = defaultdict(int)
        for (pos1, score1, pos2, score2), count in self.state.items():
            for roll, nroll in dirac_roll.items():
                new_pos  = (pos1 + roll - 1) % POSITIONS + 1
                new_score = score1 + new_pos
                if new_score >= self.winning_score:
                    self.wins1 += count * nroll
                else:
                    state[(new_pos, new_score, pos2, score2)] += count * nroll
        self.state = state

        # Player 2 rolls...
        state: StateDict = defaultdict(int)
        for (pos1, score1, pos2, score2), count in self.state.items():
            for roll, nroll in dirac_roll.items():
                new_pos  = (pos2 + roll - 1) % POSITIONS + 1
                new_score = score2 + new_pos
                if new_score >= self.winning_score:
                    self.wins2 += count * nroll
                else:
                    state[(pos1, score1, new_pos, new_score)] += count * nroll
        self.state = state

        self.turn += 1
        return bool(self.state)


def solve2(lines: Lines) -> int:
    """Solve the problem."""
    pos = parse_input(lines)
    for player, start_pos in pos.items():
        print(f"Player {player} starts at position {start_pos + 1}")

    game = Game(pos[1], pos[2])
    print(f"turn {game.turn:2d}: player 1 wins {game.wins1}, "
          f"player 2 wins {game.wins2}  "
          f"({game.universes} universes)")
    while game.universes:
        game.step()
        print(f"turn {game.turn:2d}: player 1 wins {game.wins1}, "
              f"player 2 wins {game.wins2}  "
              f"({game.universes} universes)")
    return max(game.wins1, game.wins2)

def solve(lines: Lines) -> int:
    """Solve the problem."""
    pos = parse_input(lines)
    for player, start_pos in pos.items():
        print(f"Player {player} starts at position {start_pos}")

    score, rolls = play(pos)
    return rolls * min(score.values())


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
    assert result == 752247
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
    assert result == 221109915584112
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
