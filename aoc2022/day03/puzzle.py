""" -- Advent of Code 2022 --
Day 03, https://adventofcode.com/2022/day/3

Notes on Solutions:
OK both solutions are very convoluted one-liners (no reason, only love to functionally 
compose generator expressions)

- Part 1: In part1 the inner-loop is taking care or calculating priorities
gathered from intersection.

- Part 2:Whereas in part2 the same nested loops generator expression is performed but with an
additional step. Input are processed in triplets (three-lines a row, incrementally)
which are then mapped to sets to calculate intersection (1 ^ (2 ^ 3))
"""

__day__ = "03"
__title__ = "Rucksack Reorganization"
__author__ = "leriomaggio"

from typing import Union
from pathlib import Path
from string import ascii_letters


def load(filepath: Union[str, Path]) -> list[str]:
    return list(open(filepath).read().split("\n"))


PRIORITIES = {l: p for l, p in zip(ascii_letters, range(1, 58))}

# =========== Part 1 ============
def part1(data: list[str]) -> int:
    return sum(
        PRIORITIES[l]
        for items in data
        for l in set(items[: (len(items) // 2)]).intersection(
            set(items[(len(items) // 2) :])
        )
    )


# =========== Part 2 ============


def part2(data: list[str]) -> int:
    return sum(
        PRIORITIES[l]
        for e1, e2, e3 in map(
            lambda t: map(set, t), zip(data[::3], data[1::3], data[2::3])
        )
        for l in e1.intersection(e2.intersection(e3))
    )


if __name__ == "__main__":
    print("=*=*=*=*=*=*=*=*=*= Advent of Code 2022 =*=*=*=*=*=*=*=*=*=")
    print(f"Day {__day__}: {__title__}")
    print("-" * 59)
    filepath = Path(__file__).with_name(f"input.{__day__}")
    data = load(filepath=filepath)
    print(part1(data))
    print(part2(data))
