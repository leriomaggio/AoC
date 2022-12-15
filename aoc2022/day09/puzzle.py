""" -- Advent of Code 2022 --
Day 09, https://adventofcode.com/2022/day/9

Notes on Solutions:
With this puzzle, I hadn't still discovered the trick of using complex numbers (
see solution to puzzle 14), therefore I am sticking with coordinates as tuples.
Therefore, the first thing I need is a function to move the knots.
This is `move` which simply implements the element-wise sum of tuples.

Large caveat with my implementation: it is going to be very reliant on itertools
and functional-style programming (intentionally, ed.)

Similarly, `distance` and `neighbourhood` calculate the distance between head (H) and
tail (T), and the neighbourhood of a pair of a generic pair of 2D coordinates, respectively.

The `direction` function is an extension of the latter adding labels to each direction
in the neighbourhood of given coordinates. This function will be leveraged to
call the respective pre-assembled `partial(move)` function, towards the corresponding
direction (according to instructions).

To check if T is adjacent to H, we simply check it belongs to H's neighbourhood.

Finally, we simulate the moves of H, and T inductively on each H-T pair with
`knots=2` in part1, and `knots=10` in part2.
"""

__day__ = "09"
__title__ = "Rope Bridge"
__author__ = "leriomaggio"

from typing import Union
from pathlib import Path
from functools import partial
from itertools import product
from typing import Iterable
from math import copysign


def load(filepath: Union[str, Path]) -> list[tuple[str, int]]:
    return list(
        map(
            lambda l: (l.split()[0], int(l.split()[1])),
            open(filepath).read().split("\n"),
        )
    )


# =========== Part 1 ============


def move(position: tuple[int], direction: tuple[int]):
    return tuple(map(sum, zip(position, direction)))


def distance(H, T):
    return tuple([(h - t) // max(1, abs(h - t)) for h, t in zip(H, T)])


def neighbourhood(coord: tuple[int, int]) -> Iterable[tuple[int, int]]:
    return map(lambda d: move(coord, d), tuple(product((-1, 0, 1), repeat=2)))


def directions(coord: tuple[int, int]) -> dict[str, tuple[int, int]]:
    return {
        label: direction
        for label, direction in zip(
            map(
                lambda dd: "P" if not "".join(dd) else "".join(dd),
                product(("D", "", "U"), ("L", "", "R")),
            ),
            neighbourhood(coord),
        )
    }


def adjacent(H, T) -> bool:
    return T in set(neighbourhood(H))


def simulate(instructions: list[tuple[str, int]], n_knots: int = 2) -> int:
    S = (0, 0)
    move_towards = {
        lbl: partial(move, direction=direction)
        for lbl, direction in directions(S).items()
    }
    direction_map = {direction: lbl for lbl, direction in directions(S).items()}
    knots = {i: S for i in range(n_knots)}
    t_marks = {S}
    for direction, steps in instructions:
        for _ in range(steps):
            knots[0] = move_towards[direction](knots[0])
            if adjacent(knots[0], knots[1]):
                continue
            for h, t in zip(range(n_knots), range(1, n_knots)):
                if not adjacent(knots[h], knots[t]):
                    dir_label = direction_map[distance(H=knots[h], T=knots[t])]
                    knots[t] = move_towards[dir_label](knots[t])
            t_marks.add(knots[n_knots - 1])
    return len(t_marks)


def part1(data: list[tuple[str, int]]) -> int:
    return simulate(instructions=data, n_knots=2)


# =========== Part 2 ============


def part2(data: list[int]) -> int:
    return simulate(instructions=data, n_knots=10)


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
