""" -- Advent of Code 2021 --
Day 11, https://adventofcode.com/2021/day/11

Notes on Solutions:
- Part 1: Solution to this part is a combination of Solution to Day 06 "Lanterfish", 
          combined with Day 09 "Smoke Basin" for neighbourhood inspection.
          The latter expands on the neighbourhood calculation by also including diagonals.
          This is pretty easily achieved by using this time `itertools.product` in combination
          with the same strategy for checking boundaries.
          Similarly to the Lanterfish case, flashing are counted and simulated, rather than explicitly
          enumerated.
- Part 2: Part 2 is identical to Part 1, with the only difference that we need to return the step when all 
          Octopus are off. This is achieved by using `all` on `area.values()` in combination with the 
          `operator.not_` function, which implements the logical not operator.
          This works due to how Python treats `bool` and `int` types: `not(3)==False` whereas `not(0) == True`.
          So when all values are zeros (i.e. `all(not, values)`), the execution breaks, and function returns.
"""

__day__ = "11"
__title__ = "Dumbo Octopus"
__author__ = "leriomaggio"

from typing import Union
from pathlib import Path
from itertools import starmap
from operator import le, lt, and_
from itertools import repeat, product

# -- part 2
from operator import not_


def load(filepath: Union[str, Path]):
    return [list(map(int, l)) for l in open(filepath).read().strip().splitlines()]


# =========== Part 1 ============


def neighbourhood(coord, borders):
    nw, n, ne, w, _, e, sw, s, se = tuple(product((-1, 0, 1), repeat=2))
    return filter(
        lambda l: and_(*starmap(le, zip((0, 0), l)))
        and and_(*starmap(lt, zip(l, borders))),
        map(lambda n: tuple(map(sum, zip(coord, n))), (n, s, w, e, nw, ne, sw, se)),
    )


def shape(area: dict[tuple[int], int]) -> tuple[int]:
    return (max(l + 1 for l, _ in area), max(r + 1 for _, r in area))


def part1(board: list[list[int]]) -> int:
    flashes = 0
    area = {(r, c): v for r, row in enumerate(board) for c, v in enumerate(row)}
    shape_ = shape(area)

    for _ in range(100):
        area.update(zip(area.keys(), map(lambda v: v + 1, area.values())))
        flashing = list(filter(lambda c: area[c] > 9, area))
        marked = set()
        while flashing:
            flashes += len(flashing)
            marked |= set(flashing)
            area.update(zip(flashing, repeat(0, len(flashing))))
            for fc in flashing:
                for neigh in filter(
                    lambda n: n not in marked, neighbourhood(fc, shape_)
                ):
                    area[neigh] += 1
            flashing = list(filter(lambda c: area[c] > 9 and not c in marked, area))
    return flashes


# =========== Part 2 ============


def part2(board: list[list[int]]) -> int:
    area = {(r, c): v for r, row in enumerate(board) for c, v in enumerate(row)}
    shape_ = shape(area)
    step = 0
    while True:
        step += 1
        area.update(zip(area.keys(), map(lambda v: v + 1, area.values())))
        flashing = list(filter(lambda c: area[c] > 9, area))
        marked = set()
        while flashing:
            marked |= set(flashing)
            area.update(zip(flashing, repeat(0, len(flashing))))
            for fc in flashing:
                for neigh in filter(
                    lambda n: n not in marked, neighbourhood(fc, shape_)
                ):
                    area[neigh] += 1
            flashing = list(filter(lambda c: area[c] > 9 and not c in marked, area))

        if all(map(not_, area.values())):
            return step


if __name__ == "__main__":
    print("=*=*=*=*=*=*=*=*=*= Advent of Code 2021 =*=*=*=*=*=*=*=*=*=")
    print(f"Day {__day__}: {__title__}")
    print("-" * 59)
    filepath = Path(__file__).with_name(f"input.{__day__}")
    data = load(filepath=filepath)
    # solve part 1
    print(part1(data))
    # solve part 2
    print(part2(data))
