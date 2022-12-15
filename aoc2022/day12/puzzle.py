""" -- Advent of Code 2022 --
Day 12, https://adventofcode.com/2022/day/12

Notes on Solutions:
The core of the solutions for the two parts lies in the `traverse` function,
which simply implements a BFS visit on a graph, with a twist.
The twist is the added bounding criterion on the search, which consider the heights
of the vertices during the traversal.

- Part 1: Simple implementation of the BFS from Source to Target (modified so that S ="a" and E = "z")
- Part 2: BFS traverse in reverse mode: therefore, we start from E (destination in part 1) and we bound the search
as soon as an "a" has been found!
"""

__day__ = "12"
__title__ = "Hill Climbing Algorithm"
__author__ = "leriomaggio"

from typing import Union
from pathlib import Path
from collections import deque


def load(filepath: Union[str, Path]):
    return parse_input(open(filepath).read())


def parse_input(data: str) -> list[list[str]]:
    grid = [list(l) for l in data.strip().split("\n")]
    for r, row in enumerate(grid):
        for c, item in enumerate(row):
            if item == "S":
                s_coords = (r, c)
            if item == "E":
                e_coords = (r, c)
            grid[r][c] = (
                ord("a") if item == "S" else ord("z") if item == "E" else ord(item)
            )
    return grid, s_coords, e_coords


def is_within(coord: tuple[int, int], boundaries: tuple[int, int]) -> bool:
    return all(map(lambda p: 0 <= p[0] < p[1], zip(coord, boundaries)))


def traverse(
    maze: list[list[int]], S: tuple[int, int], E: tuple[int, int], reverse: bool = False
):
    fringe = deque()
    (sr, sc, er, ec) = (*S, *E) if not reverse else (*E, *S)
    stop_traverse = lambda a, b: (a - b) > 1
    bounding = lambda a, b: stop_traverse(a, b) if not reverse else stop_traverse(b, a)
    destination = (
        lambda nr, nc: maze[nr][nc] == maze[er][ec] if reverse else (nr, nc) == (er, ec)
    )

    W, H = len(maze[0]), len(maze)
    fringe.append((0, sr, sc))
    visited = {(sr, sc)}
    while fringe:
        d, r, c = fringe.popleft()
        for nr, nc in filter(
            lambda cc: is_within(cc, (H, W)) and cc not in visited,
            [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)],
        ):
            if bounding(maze[nr][nc], maze[r][c]):
                continue
            if destination(nr, nc):
                return d + 1
            visited.add((nr, nc))
            fringe.append((d + 1, nr, nc))


# =========== Part 1 ============


def part1(data: tuple[list, tuple, tuple]) -> int:
    return traverse(*data)


# # =========== Part 2 ============


def part2(data: tuple[list, tuple, tuple]) -> int:
    return traverse(*data, reverse=True)


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
