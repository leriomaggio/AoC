""" -- Advent of Code 2021 --
Day 05, https://adventofcode.com/2021/day/5

Notes on Solutions:
- Part 1: Most of the interesting part about this solution lies in the loading
          function: first coordinates are swapped to use them in the code
          in a way that is semantically correct. That is `y` refers to
          _rows_ whereas `x` refers to cols - so coordinates are stored
          into a _row-major_ compliant format.
          Then `Points` are sorted (using Python tuple sorting)
          so that `source` and `destination` will always correspond to `left`
          and `right` of each `Vent`.
          All that said, I guess the new entry for this challenge is the
          [`chain`](https://docs.python.org/3/library/itertools.html#itertools.chain) and [`chain.from_iterable`](https://docs.python.org/3/library/itertools.html#itertools.chain.from_iterable) 
          functions which are used in turn to easily iterate over the whole
          matrix, and lazy iterable generated for coordinates.
          The `line_segment` function uses `product` to simply generate the
          right set of coordinates, without checking which is the repeated
          index.
- Part 2: In part2 90% of the implementation is borrowed//re-used from _part 1_
          apart from the `diagonal_segment` function which this times generates
          coordinates for **only** elements on the main diagonal.
          Therefore, this time is even easier as we don't need to generate the 
          all cartesian product of coordinates (to get a sub-matrix, btw)
          but just `zip` would suffice.
"""

__day__ = "05"
__title__ = "Hydrothermal Venture"
__author__ = "leriomaggio"


from pathlib import Path
from collections import namedtuple
from itertools import chain, product
from typing import Iterable

Point = namedtuple("Point", ["x", "y"])


def load(lines: list[str]) -> list[tuple[Point, Point]]:
    vents = list()
    for line in lines:
        left, right = line.split("->")
        vents.append(
            tuple(
                sorted(
                    [
                        Point(*map(int, left.strip().split(",")[::-1])),
                        Point(*map(int, right.strip().split(",")[::-1])),
                    ]
                )
            )
        )
    return vents


# =========== Part 1 ============

is_line = lambda pots: (pots[0].x == pots[1].x) or (pots[0].y == pots[1].y)


def line_segment(left: Point, right: Point) -> Iterable[Point]:
    rows, cols = range(left.x, right.x + 1), range(left.y, right.y + 1)
    return product(rows, cols)


def shape(vents: list[tuple[Point, Point]]) -> tuple[int, int]:
    all_points = list(
        chain.from_iterable((map(lambda p: p[0], vents), map(lambda p: p[1], vents)))
    )
    return (
        max(all_points, key=lambda p: p.x).x + 1,
        max(all_points, key=lambda p: p.y).y + 1,
    )


def part1(vents: list[tuple[Point, Point]]) -> int:
    nrows, ncols = shape(vents)
    board = [[0 for _ in range(ncols)] for _ in range(nrows)]
    coordinates = chain.from_iterable(
        map(lambda points: line_segment(*points), filter(is_line, vents))
    )
    for row, col in coordinates:
        board[row][col] += 1
    return len(list(filter(lambda v: v >= 2, chain(board))))


# =========== Part 2 ============


def diagonal_segment(left: Point, right: Point) -> Iterable[Point]:
    if is_line((left, right)):
        return line_segment(left, right)
    stepy = 1 if left.y <= right.y else -1
    stepx = 1 if left.x <= right.x else -1
    return zip(
        range(left.x, right.x + stepx, stepx), range(left.y, right.y + stepy, stepy)
    )


def part2(vents: list[tuple[Point, Point]]) -> int:
    nrows, ncols = shape(vents)
    board = [[0 for _ in range(ncols)] for _ in range(nrows)]
    coordinates = chain.from_iterable(
        map(lambda points: diagonal_segment(*points), vents)
    )
    for row, col in coordinates:
        board[row][col] += 1
    return len(list(filter(lambda v: v >= 2, chain(board))))


if __name__ == "__main__":
    print("=*=*=*=*=*=*=*=*=*= Advent of Code 2021 =*=*=*=*=*=*=*=*=*=")
    print(f"Day {__day__}: {__title__}")
    print("-" * 59)
    filepath = Path(__file__).with_name(f"input.{__day__}")
    data = load(lines=open(filepath).read().strip().splitlines())
    # solve part 1
    print(part1(data))
    # solve part 2
    print(part2(data))
