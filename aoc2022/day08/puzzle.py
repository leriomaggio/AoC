""" -- Advent of Code 2022 --
Day 08, https://adventofcode.com/2022/day/8

Notes on Solutions:
The core of the two solutions is the `explore` function which generates the
neightbourhood and all the found shorter_tree, given a pair of coordinates.

Since it's all based on generators and lazy-sequence, we use `itertools.tee`
to generate two independent iterators on the neighbourhood. One to be returned,
the second one to be filtered looking for shorter_trees
(using `itertools.takewhile`).

- Part 1: Leveraging `explore`, part1 will simply sum how many times, for all
the possible nodes (i.e. coords), all trees in the neighbourhood are shorter
(and so it is visible)

- Part 2: In a very similar fashion, in part 2 we calculate the product of all
the shortest tree + 1 (i.e. the fringe) if the number of shorter_trees is not the
whole neighbourhood. The reason for this, is because the text of the puzzle
considers also trees with the **same** height, whereas the filter in `explore`
(i.e. `takewhile`) only consider shorter trees.
"""

__day__ = "08"
__title__ = "Treetop Tree House"
__author__ = "leriomaggio"

from typing import Union
from pathlib import Path
from typing import Generator, Iterable
from itertools import takewhile, product, tee
from math import prod


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
