""" -- Advent of Code 2022 --
Day 14 , https://adventofcode.com/2022/day/14

Notes on Solutions:
They key (and also, the trick I learnt with this exercise is to use Python complex
numbers to represent 2D coordinates! In this way, we could easily check specific
axis (i.e. accessing `.real` and `.imag` for `x` and `y`, respectively), as well
as generating neighbourhood with simple arithmetic on the real and/or imaginary part.
Just amazing!
More details about this trick could be found here:ttps://erikw.me/blog/tech/advent-of-code-tricks/#grids

The solutions to this puzzle are actually connected, and the code for the two parts
is indeed the very same, but one parameter.
- Part 1: We are interested in counting how many grains of salt fall down (according rocks found
along the way, and the sliding strategy reported in the puzzle text).
In P1 the pit is believed to be bottomless, therefore as soon as we exceed the known fringe in space
(from input data) we can return - as we don't have notion of sands falling in the pit.

- Part 2: In P2 we are adding some flooring to the pit, therefore we re-apply the same code for
sand simulation of P1, and we return as soon as we have filled up the space.
"""

__day__ = "14"
__title__ = "Regolith Reservoir"
__author__ = "leriomaggio"

from typing import Union
from pathlib import Path


def load(filepath: Union[str, Path]):
    return parse_input(open(filepath).read().split("\n"))


def parse_input(data: list[str]) -> list[tuple[tuple[int, int]]]:
    return [
        tuple(
            tuple(map(int, trace.strip().split(",")))
            for trace in line.strip().split(" -> ")
        )
        for line in data
    ]


def trace(scans: list[tuple[tuple[int, int]]]):
    rocks, pit = set(), -1
    for paths in scans:
        for (x1, y1), (x2, y2) in zip(paths, paths[1:]):
            (x1, x2), (y1, y2) = sorted((x1, x2)), sorted((y1, y2))
            for x in range(x1, x2 + 1):
                for y in range(y1, y2 + 1):
                    rocks.add(x + y * 1j)
                    pit = max(pit, y + 1)
    return rocks, pit


def fill(data, bottomless: bool = True, source: complex = 500) -> int:
    blocks, pit = trace(data)
    units = 0
    while (
        source not in blocks
    ):  # fill up until the bottleneck (source) has been reached
        sand = source  # (500, 0)
        while True:
            if sand.imag >= pit:
                if bottomless:
                    return units  # stop counting
                break
            for step in (1j, 1j - 1, 1j + 1):
                if sand + step not in blocks:
                    sand += step
                    break  # keep falling
            else:
                break
        blocks.add(sand)
        units += 1
    return units


# =========== Part 1 ============


def part1(data: list[tuple[int, int]]) -> int:
    return fill(data, bottomless=True)  # bottomless pit!


# =========== Part 2 ============


def part2(data: list[int]) -> int:
    return fill(data, bottomless=False)


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
