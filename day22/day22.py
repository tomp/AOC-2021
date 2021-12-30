#!/usr/bin/env python3
#
#  Advent of Code 2019 - Day 22
#
import pdb
from typing import Sequence
from pathlib import Path
from dataclasses import dataclass
import re

INPUTFILE = "input.txt"

SAMPLE_CASES = [
    (
        """
        on x=10..12,y=10..12,z=10..12
        on x=11..13,y=11..13,z=11..13
        off x=9..11,y=9..11,z=9..11
        on x=10..10,y=10..10,z=10..10
        """,
        39
    ),
    (
        """
        on x=-20..26,y=-36..17,z=-47..7
        on x=-20..33,y=-21..23,z=-26..28
        on x=-22..28,y=-29..23,z=-38..16
        on x=-46..7,y=-6..46,z=-50..-1
        on x=-49..1,y=-3..46,z=-24..28
        on x=2..47,y=-22..22,z=-23..27
        on x=-27..23,y=-28..26,z=-21..29
        on x=-39..5,y=-6..47,z=-3..44
        on x=-30..21,y=-8..43,z=-13..34
        on x=-22..26,y=-27..20,z=-29..19
        off x=-48..-32,y=26..41,z=-47..-37
        on x=-12..35,y=6..50,z=-50..-2
        off x=-48..-32,y=-32..-16,z=-15..-5
        on x=-18..26,y=-33..15,z=-7..46
        off x=-40..-22,y=-38..-28,z=23..41
        on x=-16..35,y=-41..10,z=-47..6
        off x=-32..-23,y=11..30,z=-14..3
        on x=-49..-5,y=-3..45,z=-29..18
        off x=18..30,y=-20..-8,z=-3..13
        on x=-41..9,y=-7..43,z=-33..15
        on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
        on x=967..23432,y=45373..81175,z=27513..53682
        """,
        590784
    ),
]

SAMPLE_CASES2 = [
    (
        """
        on x=10..12,y=10..12,z=10..12
        on x=11..13,y=11..13,z=11..13
        off x=9..11,y=9..11,z=9..11
        on x=10..10,y=10..10,z=10..10
        """,
        39
    ),
    (
        """
        on x=-20..26,y=-36..17,z=-47..7
        on x=-20..33,y=-21..23,z=-26..28
        on x=-22..28,y=-29..23,z=-38..16
        on x=-46..7,y=-6..46,z=-50..-1
        on x=-49..1,y=-3..46,z=-24..28
        on x=2..47,y=-22..22,z=-23..27
        on x=-27..23,y=-28..26,z=-21..29
        on x=-39..5,y=-6..47,z=-3..44
        on x=-30..21,y=-8..43,z=-13..34
        on x=-22..26,y=-27..20,z=-29..19
        off x=-48..-32,y=26..41,z=-47..-37
        on x=-12..35,y=6..50,z=-50..-2
        off x=-48..-32,y=-32..-16,z=-15..-5
        on x=-18..26,y=-33..15,z=-7..46
        off x=-40..-22,y=-38..-28,z=23..41
        on x=-16..35,y=-41..10,z=-47..6
        off x=-32..-23,y=11..30,z=-14..3
        on x=-49..-5,y=-3..45,z=-29..18
        off x=18..30,y=-20..-8,z=-3..13
        on x=-41..9,y=-7..43,z=-33..15
        """,
        590784
    ),
    (
        """
        on x=-5..47,y=-31..22,z=-19..33
        on x=-44..5,y=-27..21,z=-14..35
        on x=-49..-1,y=-11..42,z=-10..38
        on x=-20..34,y=-40..6,z=-44..1
        off x=26..39,y=40..50,z=-2..11
        on x=-41..5,y=-41..6,z=-36..8
        off x=-43..-33,y=-45..-28,z=7..25
        on x=-33..15,y=-32..19,z=-34..11
        off x=35..47,y=-46..-34,z=-11..5
        on x=-14..36,y=-6..44,z=-16..29
        on x=-57795..-6158,y=29564..72030,z=20435..90618
        on x=36731..105352,y=-21140..28532,z=16094..90401
        on x=30999..107136,y=-53464..15513,z=8553..71215
        on x=13528..83982,y=-99403..-27377,z=-24141..23996
        on x=-72682..-12347,y=18159..111354,z=7391..80950
        on x=-1060..80757,y=-65301..-20884,z=-103788..-16709
        on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856
        on x=-52752..22273,y=-49450..9096,z=54442..119054
        on x=-29982..40483,y=-108474..-28371,z=-24328..38471
        on x=-4958..62750,y=40422..118853,z=-7672..65583
        on x=55694..108686,y=-43367..46958,z=-26781..48729
        on x=-98497..-18186,y=-63569..3412,z=1232..88485
        on x=-726..56291,y=-62629..13224,z=18033..85226
        on x=-110886..-34664,y=-81338..-8658,z=8914..63723
        on x=-55829..24974,y=-16897..54165,z=-121762..-28058
        on x=-65152..-11147,y=22489..91432,z=-58782..1780
        on x=-120100..-32970,y=-46592..27473,z=-11695..61039
        on x=-18631..37533,y=-124565..-50804,z=-35667..28308
        on x=-57817..18248,y=49321..117703,z=5745..55881
        on x=14781..98692,y=-1341..70827,z=15753..70151
        on x=-34419..55919,y=-19626..40991,z=39015..114138
        on x=-60785..11593,y=-56135..2999,z=-95368..-26915
        on x=-32178..58085,y=17647..101866,z=-91405..-8878
        on x=-53655..12091,y=50097..105568,z=-75335..-4862
        on x=-111166..-40997,y=-71714..2688,z=5609..50954
        on x=-16602..70118,y=-98693..-44401,z=5197..76897
        on x=16383..101554,y=4615..83635,z=-44907..18747
        off x=-95822..-15171,y=-19987..48940,z=10804..104439
        on x=-89813..-14614,y=16069..88491,z=-3297..45228
        on x=41075..99376,y=-20427..49978,z=-52012..13762
        on x=-21330..50085,y=-17944..62733,z=-112280..-30197
        on x=-16478..35915,y=36008..118594,z=-7885..47086
        off x=-98156..-27851,y=-49952..43171,z=-99005..-8456
        off x=2032..69770,y=-71013..4824,z=7471..94418
        on x=43670..120875,y=-42068..12382,z=-24787..38892
        off x=37514..111226,y=-45862..25743,z=-16714..54663
        off x=25699..97951,y=-30668..59918,z=-15349..69697
        off x=-44271..17935,y=-9516..60759,z=49131..112598
        on x=-61695..-5813,y=40978..94975,z=8655..80240
        off x=-101086..-9439,y=-7088..67543,z=33935..83858
        off x=18020..114017,y=-48931..32606,z=21474..89843
        off x=-77139..10506,y=-89994..-18797,z=-80..59318
        off x=8476..79288,y=-75520..11602,z=-96624..-24783
        on x=-47488..-1262,y=24338..100707,z=16292..72967
        off x=-84341..13987,y=2429..92914,z=-90671..-1318
        off x=-37810..49457,y=-71013..-7894,z=-105357..-13188
        off x=-27365..46395,y=31009..98017,z=15428..76570
        off x=-70369..-16548,y=22648..78696,z=-1892..86821
        on x=-53470..21291,y=-120233..-33476,z=-44150..38147
        off x=-93533..-4276,y=-16170..68771,z=-104985..-24507
        """,
        2758514936282235
    ),
]

Lines = Sequence[str]

CUBOID_RE = re.compile(r"(on|off) x=(-?\d+)[.][.](-?\d+),y=(-?\d+)[.][.](-?\d+),z=(-?\d+)[.][.](-?\d+)")


# Utility functions

def load_input(infile: str) -> Lines:
    return load_text(Path(infile).read_text())

def load_text(text: str) -> Lines:
    return filter_blank_lines(text.split("\n"))

def filter_blank_lines(lines: Lines) -> Lines:
    return [line.strip() for line in lines if line.strip()]

# Solution

XYZ = tuple[int, int, int]

MIN_XYZ = -50
MAX_XYZ = 50


@dataclass
class Cuboid:
    on_off: str
    xmin: int
    xmax: int
    ymin: int
    ymax: int
    zmin: int
    zmax: int

    def __str__(self) -> str:
        return (
            f"{self.on_off} x={self.xmin}..{self.xmax},y={self.ymin}..{self.ymax},z={self.zmin}..{self.zmax}"
        )

    def __repr__(self) -> str:
        return (
            f"Cuboid({self.on_off} x={self.xmin}..{self.xmax},y={self.ymin}..{self.ymax},z={self.zmin}..{self.zmax})"
        )

    @property
    def on(self) -> bool:
        return self.on_off == "on"

    @property
    def off(self) -> bool:
        return self.on_off == "off"

    def __eq__(self, other: "Cuboid") -> bool:
        return (
             self.xmin == other.xmin and self.xmax == other.xmax and
             self.ymin == other.ymin and self.ymax == other.ymax and
             self.zmin == other.zmin and self.zmax == other.zmax and
             self.on_off == other.on_off
        )

    def __lt__(self, other: "Cuboid") -> bool:
        if self.xmin != other.xmin:
            return self.xmin < other.xmin 
        if self.ymin != other.ymin:
            return self.ymin < other.ymin 
        if self.zmin != other.zmin:
            return self.zmin < other.zmin 
        if self.xmax != other.xmax:
            return self.xmax < other.xmax 
        if self.ymax != other.ymax:
            return self.ymax < other.ymax 
        if self.zmax != other.zmax:
            return self.zmax < other.zmax 
        return self.on_off , other.on_off

    @property
    def volume(self) -> int:
        """Report the number of primitive cubes contained by this cuboid."""
        return (self.xmax - self.xmin + 1) * (self.ymax - self.ymin + 1) * (self.zmax - self.zmin + 1)

    def cubes(self) -> set[XYZ]:
        """Return the set of primitive cubes defined by this cuboid that are valid
        for initialization.
        """
        if self.xmax < MIN_XYZ or self.xmin > MAX_XYZ:
            return set()
        xmax = min(self.xmax, MAX_XYZ)
        xmin = max(self.xmin, MIN_XYZ)

        if self.ymax < MIN_XYZ or self.ymin > MAX_XYZ:
            return set()
        ymax = min(self.ymax, MAX_XYZ)
        ymin = max(self.ymin, MIN_XYZ)

        if self.zmax < MIN_XYZ or self.zmin > MAX_XYZ:
            return set()
        zmax = min(self.zmax, MAX_XYZ)
        zmin = max(self.zmin, MIN_XYZ)

        result = set()
        for x in range(xmin, xmax+1):
            for y in range(ymin, ymax+1):
                for z in range(zmin, zmax+1):
                    result.add((x, y, z))
        return result

    def union(self, other) -> list["Cuboid"]:
        return [self, other]

    def contains(self, XYZ) -> bool:
        return False

    def intersect(self, other) -> tuple["Cuboid", list["Cuboid"], list["Cuboid"]]:
        """Return a cuboid representing the region where this cuboid overlaps the other, and a list of non-overlapping
        cuboids that cover the remaining volume of this cuboid and the other.
        """
        # check whether we overlap at all, first.
        if self.xmax < other.xmin or self.xmin > other.xmax:
            return None, [self], [other]
        xlim = sorted([self.xmin, self.xmax, other.xmin, other.xmax])

        if self.ymax < other.ymin or self.ymin > other.ymax:
            return None, [self], [other]
        ylim = sorted([self.ymin, self.ymax, other.ymin, other.ymax])

        if self.zmax < other.zmin or self.zmin > other.zmax:
            return None, [self], [other]
        zlim = sorted([self.zmin, self.zmax, other.zmin, other.zmax])

        self_cubes = []
        other_cubes = []
        for i in range(3):
            # x = (xlim[i] + xlim[i+1] - 1) / 2
            x0 = xlim[i] if i < 2 else xlim[i] + 1
            x1 = xlim[i+1] if i > 0 else xlim[i+1] - 1
            x = (x0 + x1) / 2
            xself = self.xmin <= x <= self.xmax
            xother = other.xmin <= x <= other.xmax
            for j in range(3):
                # y = (ylim[j] + ylim[j+1] - 1) / 2
                y0 = ylim[j] if j < 2 else ylim[j] + 1
                y1 = ylim[j+1] if j > 0 else ylim[j+1] - 1
                y = (y0 + y1) / 2
                yself = self.ymin <= y <= self.ymax
                yother = other.ymin <= y <= other.ymax
                for k in range(3):
                    # z = (zlim[k] + zlim[k+1] - 1) / 2
                    z0 = zlim[k] if k < 2 else zlim[k] + 1
                    z1 = zlim[k+1] if k > 0 else zlim[k+1] - 1
                    z = (z0 + z1) / 2
                    zself = self.zmin <= z <= self.zmax
                    zother = other.zmin <= z <= other.zmax

                    # print(f"x,y,z: {x}, {y}, {z}   self? {xself},{yself},{zself}  other? {xother},{yother},{zother}")
                    if xself and yself and zself:
                        if xother and yother and zother:
                            common_cube = Cuboid(other.on_off, x0, x1, y0, y1, z0, z1)
                        else:
                            self_cubes.append(Cuboid(self.on_off, x0, x1, y0, y1, z0, z1))
                    elif xother and yother and zother:
                        other_cubes.append(Cuboid(other.on_off, x0, x1, y0, y1, z0, z1))
        return common_cube, self_cubes, other_cubes


class Reactor:
    """A Reactor instance records the active cubes in an AoC submarine reactor.
    _cubes .... The set of non-overlapping cuboids that spans the actives cubes of the reactor
    """

    def __init__(self, debug: bool = False):
        self._cubes = []
        self.debug = debug

    @property
    def active(self):
        return sum([cube.volume for cube in self._cubes])

    def log(self, text: str) -> None:
        if self.debug:
            print(text)
    
    def add_cubes(self, cuboids: list[Cuboid]) -> "Reactor":
        """Add the given cuboids to this reactor, in order.
        A reference to the reactor is returned, to allow chaining.
        """
        for cube in cuboids:
            self.add(cube)
        return self
    
    def add(self, add_cube: Cuboid) -> "Reactor":
        self.log(f"ADD: {add_cube} ({add_cube.volume} cubes)")
        adding = add_cube.on
        if not self._cubes:
            if adding:
                self._cubes.append(add_cube)
            return self

        # self._cubes represent all active cubes, as a list of non-overlapping cuboids.
        old_cubes = list(self._cubes)

        # new_cubes represent the portion of the self._cubes that remain after removing
        # any overlaps with the given cuboid, when it is "off".  If the add_cube is "on"
        # then new_cubes is not necessary.
        new_cubes = []

        # add_cubes represent the cuboid being added, as a list of non-overlapping
        # cuboids.  Portions of the input add_cube that overlap with self._cubes 
        # are progressively removed in this method.
        add_cubes = [add_cube]

        while old_cubes:
            cube = old_cubes.pop()
            self.log(f"==== old cube {cube}")
            ## pdb.set_trace()

            intersects = False
            fragments = []
            for add_cube in add_cubes:
                self.log(f"---- add cube {add_cube}")
                ab, a, b = cube.intersect(add_cube)
                if not ab:
                    fragments.append(add_cube)
                    continue
                intersects = True

                if adding:
                    fragments.extend(b)
                    self.log("fragments:\n" + "\n".join([f".... {frag}" for frag in b]))
                else:
                    new_cubes.extend(a)
                    self.log("new cubes:\n" + "\n".join([f"<<<< {frag}" for frag in a]))
                    break
            if adding:
                add_cubes = fragments
            elif not intersects:
                new_cubes.append(cube)
                self.log(f"<<<< {cube}")
            self.log(f"=============")

        if adding:
            self._cubes.extend(add_cubes)
        else:
            self._cubes = new_cubes
        self._cubes.sort()
        self.log("RESULT:\n" + "\n".join([f"<--- {frag}" for frag in self._cubes]))

        return self

        


def parse_input(lines: Lines) -> list[Cuboid]:
    result = []
    for line in lines:
        m = CUBOID_RE.match(line)
        on_off = m.group(1)
        result.append(Cuboid(on_off, *(map(int, m.groups()[1:]))))
    return result

def solve2(lines: Lines) -> int:
    """Solve the problem."""
    cuboids = parse_input(lines)
    reactor = Reactor()
    for cuboid in cuboids:
        reactor.add(cuboid)
    return reactor.active

def add_cuboids(cuboids: list[Cuboid]) -> set[XYZ]:
    """Run the given cuboids, in order, and return the set of
    primitive cubes that are activated, at the end.
    """
    reactor = set()
    for cuboid in cuboids:
        cubes = cuboid.cubes()
        if not cubes:
            continue
        if cuboid.on:
            reactor |= cubes
        else:
            reactor -= cubes
    return reactor

def solve(lines: Lines) -> int:
    """Solve the problem."""
    cuboids = parse_input(lines)
    reactor = add_cuboids(cuboids)
    return len(reactor)


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
    assert result == 606484
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
    assert result == 1162571910364852
    print("= " * 32)


if __name__ == "__main__":
    example1()
    input_lines = load_input(INPUTFILE)
    part1(input_lines)
    example2()
    part2(input_lines)
