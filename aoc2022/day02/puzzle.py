""" -- Advent of Code 2022 --
Day 02, https://adventofcode.com/2022/day/2

Notes on Solutions:
- Part 1: Most of the preparation happens in the `gamne_states` function which
calculate the map of scores for each played move, along with the
outcome of the game depending on all the possible states.
Rock-Paper-Scissors is indeed a finite-state game, so we could bear enumating all the states.

- Part 2: In this part, the only difference is in the fact that we need
another map (i.e. dict) to associate plays that will end in the desired outcome
(i.e. Draw, Win, Lose).
Therefore, the `move` dictionary is calculated - via dictionary comprehension -
and then used to calculate the score from the corresponding derived move.
"""

__day__ = "02"
__title__ = "Rock Paper Scissors"
__author__ = "leriomaggio"

from typing import Union
from pathlib import Path
from itertools import islice, cycle


def load(filepath: Union[str, Path]) -> list[tuple[str, str]]:
    return list(map(lambda p: tuple(p.split()), open(filepath).read().split("\n")))


# Game points
LOSS = 0
DRAW = 3
WIN = 6

# =========== Part 1 ============


def game_states(plays: str) -> tuple[dict[tuple[str, str], int], dict[str, int]]:
    """Calculates the score for each play (as specified by plays) along with the game states for all
    combinations of Rock(A), Paper(B), Scissors(C) and plays."""

    points = {l: score for l, score in zip(plays, range(1, 4))}
    states = {}
    for i, score in enumerate((DRAW, WIN, LOSS)):
        states.update(
            {(e, p): score for e, p in zip("ABC", islice(cycle(plays), i, i + 3))}
        )
    return states, points


def part1(data: list[tuple[str, str]]) -> int:
    matchups, points = game_states(plays="XYZ")
    return sum(matchups[(l1, l2)] + points[l2] for l1, l2 in data)


# =========== Part 2 ============


def part2(data: list[int]) -> int:
    matchups, points = game_states(plays="ABC")
    moves = {
        move: {e: p for e, p in zip("ABC", islice(cycle("ABC"), i, i + 3))}
        for i, move in enumerate(("Y", "Z", "X"))
    }
    return sum(
        matchups[(l1, (move := moves[l2][l1]))] + points[move] for l1, l2 in data
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
