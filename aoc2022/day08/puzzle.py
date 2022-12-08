""" -- Advent of Code 2022 --
Day 08, https://adventofcode.com/2022/day/8

Notes on Solutions:
- Part 1: 
- Part 2: 
"""

__day__ = "08"
__title__ = "Treetop Tree House"
__author__ = "leriomaggio"

from typing import Union
from pathlib import Path
from typing import Generator, Iterable
from itertools import takewhile, product, tee
from math import sqrt, prod


def load(filepath: Union[str, Path]) -> list[list[int]]:
    return [[int(t) for t in line] for line in open(filepath).read().split("\n")]


# =========== Part 1 ============


def explore(
    trees: list[list[int]], row: int, col: int
) -> Generator[tuple[Iterable[int], Iterable[int]], None, None]:
    n_rows, n_cols = len(trees), len(trees[0])
    directions = product(
        zip(("row", "col"), (row, col), (n_rows, n_cols)), (True, False)
    )
    for (axis, dim, limit), reverse in directions:
        coords = reversed(range(0, dim)) if reverse else range(dim + 1, limit)
        neighbours_1, neighbours_2 = tee(
            map(lambda c: (row, c) if axis == "col" else (c, col), coords)
        )
        shorter_trees = takewhile(
            lambda c: trees[c[0]][c[1]] < trees[row][col], neighbours_2
        )
        yield neighbours_1, shorter_trees


def is_visible(trees: list[list[int]], row: int, col: int) -> bool:
    return any(
        len(list(neighbours)) == len(list(shorter_trees))
        for neighbours, shorter_trees in explore(trees, row, col)
    )


def part1(data: list[list[int]]) -> int:
    return sum(
        is_visible(data, i, j) for i, row in enumerate(data) for j, _ in enumerate(row)
    )


# =========== Part 2 ============


def scenic_cone(trees, row: int, col: int) -> int:
    return prod(
        len(st := list(shorter_trees))
        + (fringe := 1 if len(st) < len(list(neighbours)) else 0)
        for neighbours, shorter_trees in explore(trees, row, col)
    )


def part2(data: list[int]) -> int:
    return max(
        scenic_cone(data, i, j) for i, row in enumerate(data) for j, _ in enumerate(row)
    )


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
