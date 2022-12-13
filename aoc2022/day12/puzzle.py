""" -- Advent of Code 2022 --
Day 12, https://adventofcode.com/2022/day/12

Notes on Solutions:
- Part 1: 
- Part 2: 
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
    return [list(l) for l in data.strip().split("\n")]


def source_target_coords(
    maze: list[list[str]],
) -> tuple[tuple[int, int], tuple[int, int]]:
    for r, row in enumerate(maze):
        for c, item in enumerate(row):
            if item == "S":
                s_coords = (r, c)
            if item == "E":
                e_coords = (r, c)
    return s_coords, e_coords


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
            lambda cc: cc not in visited,
            [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)],
        ):
            if not (is_within((nr, nc), (H, W))) or bounding(
                ord(maze[nr][nc]), ord(maze[r][c])
            ):
                continue
            if destination(nr, nc):
                return d + 1
            visited.add((nr, nc))
            fringe.append((d + 1, nr, nc))


# =========== Part 1 ============


def part1(data: list[int]) -> int:
    S, E = source_target_coords(maze=data)
    maze = [["a" if e == "S" else "z" if e == "E" else e for e in row] for row in data]
    return traverse(maze, S, E)


# # =========== Part 2 ============


def part2(data: list[int]) -> int:
    S, E = source_target_coords(maze=data)
    maze = [["a" if e == "S" else "z" if e == "E" else e for e in row] for row in data]
    return traverse(maze, S, E, reverse=True)


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
