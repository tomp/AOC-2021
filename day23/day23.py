#!/usr/bin/env python3
#
#  Advent of Code 2019 - Day 23
#
from typing import Sequence, Union, Optional, Any
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass
from heapq import heapify, heappush, heappop
import math
import re

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    (
        """
        #############
        #...........#
        ###B#C#B#D###
        ###A#D#C#A###
        #############
        """,
        12521,
    ),
]

SAMPLE_CASES2 = [
    (
        """
        #############
        #...........#
        ###B#C#B#D###
        ###A#D#C#A###
        #############
        """,
        44169,
    ),
]

Lines = Sequence[str]
Sections = Sequence[Lines]

Location = tuple[int, int]

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

HALL, VEST, ROOM_A, ROOM_B, ROOM_C, ROOM_D = range(6)

EMPTY, AMPHI_A, AMPHI_B, AMPHI_C, AMPHI_D = " ", "A", "B", "C", "D"

HALL_DESTS = [(0, 0), (0, 1), (0, 3), (0, 5), (0, 7), (0, 9), (0, 10)]

DESTS = {
    AMPHI_A: [(1, 2), (2, 2)],
    AMPHI_B: [(1, 4), (2, 4)],
    AMPHI_C: [(1, 6), (2, 6)],
    AMPHI_D: [(1, 8), (2, 8)],
}

DESTS2 = {
    AMPHI_A: [(1, 2), (2, 2), (3, 2), (4, 2)],
    AMPHI_B: [(1, 4), (2, 4), (3, 4), (4, 4)],
    AMPHI_C: [(1, 6), (2, 6), (3, 6), (4, 6)],
    AMPHI_D: [(1, 8), (2, 8), (3, 8), (4, 8)],
}

AMPHI_COL = {obj: locs[0][1] for obj, locs in DESTS.items() if locs[0][0] == 1}

COST = {
    AMPHI_A: 1,
    AMPHI_B: 10,
    AMPHI_C: 100,
    AMPHI_D: 1000,
}


def available_moves(
    pods: list[tuple[Location, str]]
) -> tuple[Location, Location, str, int]:
    # print(f"available_moves:\n{pods}")
    moves = []
    pod_locs = set([loc for loc, _ in pods])
    obj_at = dict(pods)
    for loc, obj in pods:
        row, col = loc
        unit_cost = COST[obj]
        dest_col = AMPHI_COL[obj]
        if row == 0:
            # amphipod is in the hallway...
            dest1, dest2 = DESTS[obj]
            if dest1 not in pod_locs:
                if dest2 not in pod_locs:
                    cost = open_route(loc, dest2, pod_locs)
                    if cost:
                        moves.append((loc, dest2, obj, cost * unit_cost))
                elif obj_at[dest2] == obj:
                    cost = open_route(loc, dest1, pod_locs)
                    if cost:
                        moves.append((loc, dest1, obj, cost * unit_cost))

        if row == 2 and col != dest_col:
            if (1, col) in pod_locs:
                continue
            for dest in HALL_DESTS:
                cost = open_route(loc, dest, pod_locs)
                if cost:
                    moves.append((loc, dest, obj, cost * unit_cost))

            # dest1, dest2 = DESTS[obj]
            # if dest2 not in pod_locs:
            #     cost = open_route((0, col), dest2, pod_locs)
            #     if cost:
            #         moves.append((loc, dest2, obj, (cost + 2)*unit_cost))
            # elif dest1 not in pod_locs:
            #     cost = open_route((0, col), dest1, pod_locs)
            #     if cost:
            #         moves.append((loc, dest1, obj, (cost + 2)*unit_cost))

        if row == 1:
            for dest in HALL_DESTS:
                cost = open_route(loc, dest, pod_locs)
                if cost:
                    moves.append((loc, dest, obj, cost * unit_cost))

            # dest1, dest2 = DESTS[obj]
            # if dest2 not in pod_locs:
            #     cost = open_route((0, col), dest2, pod_locs)
            #     if cost:
            #         moves.append((loc, dest2, obj, (cost + 1)*unit_cost))
            # elif dest1 not in pod_locs:
            #     cost = open_route((0, col), dest1, pod_locs)
            #     if cost:
            #         moves.append((loc, dest1, obj, (cost + 1)*unit_cost))

    return moves


def available_moves2(
    pods: list[tuple[Location, str]],
    dests: dict[Location, str]
) -> tuple[Location, Location, str, int]:
    # print(f"available_moves:\n{pods}")
    moves = []
    pod_locs = set([loc for loc, _ in pods])
    obj_at = dict(pods)
    for loc, obj in pods:
        row, col = loc
        unit_cost = COST[obj]
        dest_col = AMPHI_COL[obj]
        if row == 0:
            # amphipod is in the hallway...
            if all([obj_at.get(dest, obj) == obj for dest in dests[obj]]):
                for dest in reversed(dests[obj]):
                    if dest not in pod_locs:
                        cost = open_route2(loc, dest, pod_locs)
                        if cost:
                            moves.append((loc, dest, obj, cost * unit_cost))
                        break

        else:
            if col == dest_col:
                if all([obj_at.get(dest, obj) == obj for dest in dests[obj]]):
                    continue
            for dest in HALL_DESTS:
                cost = open_route2(loc, dest, pod_locs)
                if cost:
                    moves.append((loc, dest, obj, cost * unit_cost))

    return moves


def open_route(start: Location, dest: Location, pod_locs: list[Location]) -> int:
    r0, c0 = start
    r1, c1 = dest
    # print(f"open_route: {start} -> {dest}")
    assert r0 != r1

    if dest in pod_locs:
        return 0

    if r0 == 0:
        if r1 == 2:
            if (1, c1) in pod_locs:
                return 0
        if c0 < c1:
            for c in range(c0 + 1, c1):
                if (0, c) in pod_locs:
                    return 0
        else:
            for c in range(c1, c0):
                if (0, c) in pod_locs:
                    return 0
        return abs(c1 - c0) + r1

    if r0 == 2:
        if (1, c0) in pod_locs:
            return 0
    if c0 < c1:
        for c in range(c0 + 1, c1 + 1):
            if (0, c) in pod_locs:
                return 0
    else:
        for c in range(c1 + 1, c0):
            if (0, c) in pod_locs:
                return 0
    return abs(c1 - c0) + r0


def open_route2(start: Location, dest: Location, pod_locs: list[Location]) -> int:
    r0, c0 = start
    r1, c1 = dest
    # print(f"open_route: {start} -> {dest}")
    assert r0 == 0 or r1 == 0 or c0 != c1

    if dest in pod_locs:
        return 0

    if r0 == 0:
        if r1 > 1:
            if any([(r, c1) in pod_locs for r in range(1, r1)]):
                return 0
        if c0 < c1:
            for c in range(c0 + 1, c1):
                if (0, c) in pod_locs:
                    return 0
        else:
            for c in range(c1, c0):
                if (0, c) in pod_locs:
                    return 0
        return abs(c1 - c0) + r1

    if r0 > 1:
        if any([(r, c0) in pod_locs for r in range(1, r0)]):
            return 0
    if c0 < c1:
        for c in range(c0 + 1, c1):
            if (0, c) in pod_locs:
                return 0
    else:
        for c in range(c1 + 1, c0):
            if (0, c) in pod_locs:
                return 0
    return abs(c1 - c0) + r0 + r1


def heuristic(pods: list[tuple[Location, str]]) -> int:
    best_cost = 0
    for loc, obj in pods:
        row, col = loc
        dest_col = AMPHI_COL[obj]
        unit_cost = COST[obj]
        if row == 0:
            best_cost += unit_cost * (abs(col - dest_col) + 1)
        elif col != dest_col:
            best_cost += unit_cost * (abs(col - dest_col) + row + 1)
    return best_cost


def done(pods) -> bool:
    for loc, obj in pods:
        row, col = loc
        if row == 0:
            return False
        dest_col = AMPHI_COL[obj]
        if col != dest_col:
            return False
    return True


def parse_input(lines: Lines) -> list[tuple[Location, str]]:
    pods = []
    row = 0
    for i, line in enumerate(lines):
        print(f"line {i}: {line}")
        if line[:3] == "###" and line[3] != "#":
            row += 1
            for col in (2, 4, 6, 8):
                pods.append(((row, col), line[col + 1]))
    return pods


EXTRA_PODS = [
    ((2, 2), "D"),
    ((2, 4), "C"),
    ((2, 6), "B"),
    ((2, 8), "A"),
    ((3, 2), "D"),
    ((3, 4), "B"),
    ((3, 6), "A"),
    ((3, 8), "C"),
]


def parse_input2(lines: Lines) -> list[tuple[Location, str]]:
    pods = list(EXTRA_PODS)
    row = 0
    for i, line in enumerate(lines):
        print(f"line {i}: {line}")
        if line[:3] == "###" and line[3] != "#":
            row = 1 if not row else 4
            for col in (2, 4, 6, 8):
                pods.append(((row, col), line[col + 1]))
    return pods


def podsig(pods: list[tuple[Location, str]]) -> str:
    return hex(hash(tuple(pods)) & 0xFFFFFFFF)[2:]


def podstr(pods: list[tuple[Location, str]], rows: int = 4) -> str:
    grid = [
        list("..........."),
        list("  . . . .  "),
        list("  . . . .  "),
        list("  . . . .  "),
        list("  . . . .  "),
    ]
    for (r, c), obj in pods:
        grid[r][c] = obj
    return "\n".join(["".join(row) for row in grid])


def solve2(lines: Lines) -> int:
    """Solve the problem."""
    init_pods = parse_input2(lines)
    print(init_pods)
    cost_to_finish = heuristic(init_pods)

    queue = []
    heappush(queue, (cost_to_finish, 0, init_pods, []))
    visited = set()
    while queue:
        est_score, score, pods, hist = heappop(queue)
        print(f"\n{est_score}_{podsig(pods)} [{score}]\n{podstr(pods)}")

        if done(pods):
            for i, step in enumerate(hist):
                print(f"{i:2d}: {step}")
            print(f"DONE!!")
            return score

        if tuple(pods) in visited:
            print("---- visited ----")
            continue
        visited.add(tuple(pods))

        for loc_from, loc_to, obj, cost in available_moves2(pods, DESTS2):
            new_hist = list(hist) + [(loc_from, loc_to, cost)]
            new_pods = [(k, v) for k, v in pods if k != loc_from]
            new_pods.append((loc_to, obj))
            new_pods.sort()
            if tuple(new_pods) in visited:
                continue
            cost_to_finish = heuristic(new_pods)
            new_score = score + cost
            new_est_score = new_score + cost_to_finish
            print(
                f"move {obj} {loc_from} -> {loc_to}  {new_est_score}_{podsig(new_pods)}"
            )
            assert new_est_score >= est_score
            heappush(queue, (new_est_score, new_score, new_pods, new_hist))

    return 0


def solve(lines: Lines) -> int:
    """Solve the problem."""
    init_pods = parse_input(lines)
    print(init_pods)
    cost_to_finish = heuristic(init_pods)

    queue = []
    heappush(queue, (cost_to_finish, 0, init_pods, []))
    visited = set()
    while queue:
        est_score, score, pods, hist = heappop(queue)
        print(f"\n[{est_score}] [{score}]\n{pods}")

        if done(pods):
            for i, step in enumerate(hist):
                print(f"{i:2d}: {step}")
            print(f"DONE!!")
            return score

        if tuple(pods) in visited:
            print("---- visited ----")
            continue
        visited.add(tuple(pods))

        for loc_from, loc_to, obj, cost in available_moves(pods):
            new_hist = list(hist) + [(loc_from, loc_to, cost)]
            new_pods = [(k, v) for k, v in pods if k != loc_from]
            new_pods.append((loc_to, obj))
            new_pods.sort()
            cost_to_finish = heuristic(new_pods)
            new_score = score + cost
            new_est_score = new_score + cost_to_finish
            print(f"move [{new_est_score}] {new_score} {loc_from} -> {loc_to}")
            assert new_est_score >= est_score
            heappush(queue, (new_est_score, new_score, new_pods, new_hist))

    return 0


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
    assert result == 15516
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
    assert result == 45272
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
