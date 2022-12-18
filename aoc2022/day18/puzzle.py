""" -- Advent of Code 2022 --
Day 18, https://adventofcode.com/2022/day/18

Notes on Solutions:
- Part 1: This is a quite simple one-liner.
We simply generate all the cube faces for each input
surface, and we count off any of those already present
in the input collection (therefore, touching).

- Part 2: Following a similar idea from part one,
we consider the boundaries of all the surface reachable
by the droplet, as delimited by the minimum and maximum
set of coordinates wrt. the input sequences.

This is achieved quite easily with `min` and `max`
calculated on `zip`-ping over each axis.

We will then start exploring the neighbourhood of
all possible surfaces which are within the
considered boundaries (otherwise they wouldn't be
reachable at all). We will count any of those
actually corresponding to (input) cube faces, whilst
inductively exploring the neighbourhood of all the remaining ones.
"""

__day__ = "18"
__title__ = "Boiling Boulders"
__author__ = "leriomaggio"

from typing import Union
from pathlib import Path
from functools import partial

Coord = tuple[int, int, int]

OFFSET = [
    (0, 0, 1),
    (0, 1, 0),
    (1, 0, 0),
    (0, 0, -1),
    (0, -1, 0),
    (-1, 0, 0),
]


def face(a: Coord, b: Coord) -> Coord:
    return tuple(x + y for x, y in zip(a, b))


SURFACES = [partial(face, os) for os in OFFSET]


def load(filepath: Union[str, Path]):
    return parse_input(open(filepath).read().split("\n"))


def parse_input(data: list[str]) -> set[Coord]:
    return set(tuple(map(int, l.split(","))) for l in data)


# =========== Part 1 ============


def part1(data: list[int]) -> int:
    return (len(data) * 6) - sum(
        len(list(filter(lambda sf: sf(s) in data, SURFACES))) for s in data
    )


# =========== Part 2 ============


def within(face: Coord, lower_bound: Coord, upper_bound: Coord) -> bool:
    return all(lb <= c <= ub for lb, c, ub in zip(lower_bound, face, upper_bound))


def part2(data: list[int]) -> int:
    is_reachable = partial(
        within,
        lower_bound=(lower_bound := tuple(min(x) - 1 for x in zip(*data))),
        upper_bound=(upper_bound := tuple(max(x) + 1 for x in zip(*data))),
    )
    n_reachable = 0
    to_explore, explored = [lower_bound, upper_bound], set()
    while len(to_explore) > 0:
        surface = to_explore.pop()
        if surface in explored:
            continue
        explored.add(surface)
        reachable_surfaces = set(
            filter(
                lambda sf: is_reachable(face=sf), map(lambda sf: sf(surface), SURFACES)
            )
        )
        n_reachable += len(
            (cube_faces := set(filter(lambda sf: sf in data, reachable_surfaces)))
        )
        to_explore += list(reachable_surfaces - cube_faces)

    return n_reachable


if __name__ == "__main__":
    print("=*=*=*=*=*=*=*=*=*= Advent of Code 2022 =*=*=*=*=*=*=*=*=*=")
    print(f"Day {__day__}: {__title__}")
    print("-" * 59)
    filepath = Path(__file__).with_name(f"input.{__day__}")
    data = load(filepath=filepath)
    # solve part 1
    print(part1(data))
    # solve part 2
    print(part2(data))
