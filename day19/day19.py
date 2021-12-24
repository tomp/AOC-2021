#!/usr/bin/env python3
#
#  Advent of Code 2019 - Day 19
#
from typing import Sequence, Union, Optional, Any
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass, field
import math
import re
from point3d import Point3D, Delta3D, Rot3D, ROTS

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    (
        """--- scanner 0 ---
        404,-588,-901
        528,-643,409
        -838,591,734
        390,-675,-793
        -537,-823,-458
        -485,-357,347
        -345,-311,381
        -661,-816,-575
        -876,649,763
        -618,-824,-621
        553,345,-567
        474,580,667
        -447,-329,318
        -584,868,-557
        544,-627,-890
        564,392,-477
        455,729,728
        -892,524,684
        -689,845,-530
        423,-701,434
        7,-33,-71
        630,319,-379
        443,580,662
        -789,900,-551
        459,-707,401

        --- scanner 1 ---
        686,422,578
        605,423,415
        515,917,-361
        -336,658,858
        95,138,22
        -476,619,847
        -340,-569,-846
        567,-361,727
        -460,603,-452
        669,-402,600
        729,430,532
        -500,-761,534
        -322,571,750
        -466,-666,-811
        -429,-592,574
        -355,545,-477
        703,-491,-529
        -328,-685,520
        413,935,-424
        -391,539,-444
        586,-435,557
        -364,-763,-893
        807,-499,-711
        755,-354,-619
        553,889,-390

        --- scanner 2 ---
        649,640,665
        682,-795,504
        -784,533,-524
        -644,584,-595
        -588,-843,648
        -30,6,44
        -674,560,763
        500,723,-460
        609,671,-379
        -555,-800,653
        -675,-892,-343
        697,-426,-610
        578,704,681
        493,664,-388
        -671,-858,530
        -667,343,800
        571,-461,-707
        -138,-166,112
        -889,563,-600
        646,-828,498
        640,759,510
        -630,509,768
        -681,-892,-333
        673,-379,-804
        -742,-814,-386
        577,-820,562

        --- scanner 3 ---
        -589,542,597
        605,-692,669
        -500,565,-823
        -660,373,557
        -458,-679,-417
        -488,449,543
        -626,468,-788
        338,-750,-386
        528,-832,-391
        562,-778,733
        -938,-730,414
        543,643,-506
        -524,371,-870
        407,773,750
        -104,29,83
        378,-903,-323
        -778,-728,485
        426,699,580
        -438,-605,-362
        -469,-447,-387
        509,732,623
        647,635,-688
        -868,-804,481
        614,-800,639
        595,780,-596

        --- scanner 4 ---
        727,592,562
        -293,-554,779
        441,611,-461
        -714,465,-776
        -743,427,-804
        -660,-479,-426
        832,-632,460
        927,-485,-438
        408,393,-506
        466,436,-512
        110,16,151
        -258,-428,682
        -393,719,612
        -211,-452,876
        808,-476,-593
        -575,615,604
        -485,667,467
        -680,325,-822
        -627,-443,-432
        872,-547,-609
        833,512,582
        807,604,487
        839,-516,451
        891,-625,532
        -652,-548,-490
        30,-46,-14
        """,
        79
    ),
]

SAMPLE_CASES2 = [
    (SAMPLE_CASES[0][0], 3621),
]

# sample beacons
"""
[
    [-892,524,684],
    [-876,649,763],
    [-838,591,734],
    [-789,900,-551],
    [-739,-1745,668],
    [-706,-3180,-659],
    [-697,-3072,-689],
    [-689,845,-530],
    [-687,-1600,576],
    [-661,-816,-575],
    [-654,-3158,-753],
    [-635,-1737,486],
    [-631,-672,1502],
    [-624,-1620,1868],
    [-620,-3212,371],
    [-618,-824,-621],
    [-612,-1695,1788],
    [-601,-1648,-643],
    [-584,868,-557],
    [-537,-823,-458],
    [-532,-1715,1894],
    [-518,-1681,-600],
    [-499,-1607,-770],
    [-485,-357,347],
    [-470,-3283,303],
    [-456,-621,1527],
    [-447,-329,318],
    [-430,-3130,366],
    [-413,-627,1469],
    [-345,-311,381],
    [-36,-1284,1171],
    [-27,-1108,-65],
    [7,-33,-71],
    [12,-2351,-103],
    [26,-1119,1091],
    [346,-2985,342],
    [366,-3059,397],
    [377,-2827,367],
    [390,-675,-793],
    [396,-1931,-563],
    [404,-588,-901],
    [408,-1815,803],
    [423,-701,434],
    [432,-2009,850],
    [443,580,662],
    [455,729,728],
    [456,-540,1869],
    [459,-707,401],
    [465,-695,1988],
    [474,580,667],
    [496,-1584,1900],
    [497,-1838,-617],
    [527,-524,1933],
    [528,-643,409],
    [534,-1912,768],
    [544,-627,-890],
    [553,345,-567],
    [564,392,-477],
    [568,-2007,-577],
    [605,-1665,1952],
    [612,-1593,1893],
    [630,319,-379],
    [686,-3108,-505],
    [776,-3184,-501],
    [846,-3110,-434],
    [1135,-1161,1235],
    [1243,-1093,1063],
    [1660,-552,429],
    [1693,-557,386],
    [1735,-437,1738],
    [1749,-1800,1813],
    [1772,-405,1572],
    [1776,-675,371],
    [1779,-442,1789],
    [1780,-1548,337],
    [1786,-1538,337],
    [1847,-1591,415],
    [1889,-1729,1762],
    [1994,-1805,1792],
]
"""

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

ClusterKey = tuple[int, int, int] # sorted integer distances
ClusterIds = tuple[int, int, int] # sorted beacon IDs
ClusterMap = dict[ClusterKey, ClusterIds]

ClusterCoords = tuple[Point3D, Point3D, Point3D] # unsorted beacon coordinates


@dataclass
class Scanner:
    name: str
    beacons: list[Point3D]
    location: Point3D = field(default=Point3D(0, 0, 0))
    _rotation: Rot3D = field(default=ROTS[0])
    _clusters: Optional[ClusterMap] = None
    aligned: bool = False

    def rotate(self, rot: Rot3D) -> None:
        self._rotation = rot
        self.beacons = [rot * p for p in self.beacons]

    def translate(self, delta: Delta3D) -> None:
        self.location += delta
        self.beacons = [p + delta for p in self.beacons]

    def locate(self, location: Point3D) -> None:
        self.translate(location - self.location)

    def distance(self, other: "Scanner") -> int:
        """Manhattan distance between this scanner and another."""
        delta = other.location - self.location
        return abs(delta.dx) + abs(delta.dy) + abs(delta.dz)

    def align(self, ref: "Scanner") -> bool:
        """Adjust the coordinates of this scanner's beacons to match those
        of a reference scanner.  Return True if successful, else False.
        """
        common = set(self.clusters.keys()) & set(ref.clusters.keys())
        # print(f"scanner {self.name} shares {len(common)} clusters with scanner {ref.name}")
        if common:
            last_rot = None
            for cluster in common:
                # print(f"#### cluster {cluster}")
                target_coords = []
                rot, delta = align_clusters(cluster, self, ref)
                assert rot and (last_rot == rot or last_rot == None) 
                last_rot = rot
            
            self.rotate(rot)
            self.translate(delta)
            self.aligned = True
        return self.aligned

    @property
    def clusters(self) -> ClusterMap:
        if not self._clusters:
            self._clusters = {}
            dists = self._distances(2)
            for i, inaybs in dists.items():
                if len(inaybs) < 2:
                    continue
                (dij, j), (dik, k) = inaybs
                assert len(dists[j]) == len(dists[k]) == 2
                djk = int(self.beacons[j].distance(self.beacons[k]))
                sig = tuple(sorted([dij, djk, dik]))
                ids = tuple(sorted([i, j, k]))
                # print(f"{sig} -> {ids}")
                self._clusters[sig] = ids
        return self._clusters

    def _distances(self, count=5):
        dists = defaultdict(list)
        n = len(self.beacons)
        for i in range(1, n):
            p1 = self.beacons[i]
            for j in range(i):
                p2 = self.beacons[j]
                d = int(p1.distance(p2))
                if d > 0:
                    dists[i].append((d, j))
                    dists[j].append((d, i))
        for i in sorted(dists, key=lambda k: self.beacons[k]):
            dists[i].sort()
            dists[i] = [(d, j) for d, j in dists[i][:count] if d < 500]
            # print(f"{i}, {self.beacons[i]}:   " + 
            #        ", ".join([f"{d} ({j})" for d, j in dists[i]]))
        return dists

def align_clusters(cluster: ClusterKey, scan: Scanner, ref: Scanner) -> tuple[Rot3D, Delta3D]:
    """Find the rotation (if any) that needs to be applied to the scanner to
    get this cluster's coordinates to its coordinates in the reference scanner.
    Return the rotation, or None, if noe was found.
    """
    # print(f"#### align scanner {scan.name} to scanner {ref.name} using cluster {cluster}")

    t1, t2, t3 = [ref.beacons[k] for k in ref.clusters[cluster]]
    # print(f"t1: {t1}")
    # print(f"t2: {t2}")
    # print(f"t3: {t3}")

    t12 = t2 - t1
    t13 = t3 - t1
    t23 = t3 - t2
    # print(f"t12: {t12}")
    # print(f"t13: {t13}")
    # print(f"t23: {t23}")

    p1, p2, p3 = [scan.beacons[k] for k in scan.clusters[cluster]]
    # print(f"p1: {p1}")
    # print(f"p2: {p2}")
    # print(f"p3: {p3}")

    d12 = p2 - p1
    d13 = p3 - p1
    d23 = p3 - p2
    # print(f"d12: {d12}")
    # print(f"d13: {d13}")
    # print(f"d23: {d23}")

    if abs(d12) == abs(t12): 
        q3 = t3
        if abs(d23) == abs(t23):
            q1, q2 = t1, t2
        else:
            q1, q2 = t2, t1
    elif abs(d12) == abs(t23):
        q3 = t1
        if abs(d23) == abs(t12):
            q1, q2 = t3, t2
        else:
            q1, q2 = t2, t3
    else:
        q3 = t2
        if abs(d13) == abs(t12):
            q1, q2 = t1, t3
        else:
            q1, q2 = t3, t1
    # print(f"q1: {q1}")
    # print(f"q2: {q2}")
    # print(f"q3: {q3}")

    q12 = q2 - q1
    q13 = q3 - q1
    q23 = q3 - q2
    # print(f"q12: {q12}")
    # print(f"q13: {q13}")
    # print(f"q23: {q23}")

    for i, rot in enumerate(ROTS):
        r12 = rot * d12
        r13 = rot * d13
        r23 = rot * d23

        if r12 == q12 and r13 == q13 and r23 == q23:
            # print(f"\n{str(rot)}")
            # print(f"r12: {r12}")
            # print(f"r13: {r13}")
            # print(f"r23: {r23}")
            
            # print(f"rot*p1: {rot*p1}    q1: {q1}")
            # print(f"rot*p2: {rot*p2}    q2: {q2}")
            # print(f"rot*p3: {rot*p3}    q3: {q3}")
            delta = q1 - (rot * p1)
            # print(f"delta: {delta}")
            return rot, delta
    return None


def parse_input(lines: Lines) -> list[Scanner]:
    result = []
    sects = parse_sections(lines)
    for sect in sects:
        beacons = []
        name = " ".join(sect[0].split()[1:3])
        for line in sect[1:]:
            beacons.append(Point3D(*map(int, line.split(","))))
        result.append(Scanner(name, beacons))
    return result

def align_scanners(scans):
    aligned = [scans[0]]
    unaligned = list(scans[1:])
    while unaligned:
        scan = unaligned.pop(0)
        # print(f"======== {scan.name} ========")
        for ref in aligned:
            if scan.align(ref):
                # print(f">>> aligned {scan.name} to {ref.name}")
                aligned.append(scan)
                break
        if not scan.aligned:
            unaligned.append(scan)
    return scans

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    scans = parse_input(lines)
    scans = align_scanners(scans)
    max_dist = 0
    for i in range(len(scans)-1):
        for j in range(i+1, len(scans)):
            dist = scans[i].distance(scans[j])
            max_dist = max(dist, max_dist)
    return max_dist

def solve(lines: Lines) -> int:
    """Solve the problem."""
    scans = parse_input(lines)
    scans = align_scanners(scans)
    beacons = set()
    for scan in scans:
        beacons |= set(scan.beacons)
    return len(beacons)


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
    assert result == 408
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
    assert result == 13348
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
