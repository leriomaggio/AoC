""" -- Advent of Code 2022 --
Day 01, https://adventofcode.com/2022/day/1

Notes on Solutions:
- Part 1: Most of the heavylifting is done on the parse function.
I created a simple data class to hold elves calories counting.
The max function in part1 calculates over a sequence of integer
(only to make the solution shorter in terms of LoC).
Similarly, I could have used the `max` function over the list of
elves, specifying a custom key function to account for calories.

- Part 2: Nothing particularly interesting than using the
`sorted` function properly (with key to account for counting and reverse to
have the fattest elves on top).
"""

__day__ = "01"
__title__ = "Calorie Counting"
__author__ = "leriomaggio"

from typing import Union
from pathlib import Path

from dataclasses import dataclass


def load(filepath: Union[str, Path]) -> list[str]:
    return open(filepath).read().split("\n")


# =========== Part 1 ============


@dataclass
class Elf:
    calories: int = 0


def parse(data: list[str]) -> list[Elf]:
    elves = list()
    elf = Elf()
    for line in data:
        try:
            calories = int(line)
        except ValueError:
            elves.append(elf)
            elf = Elf()
        else:
            elf.calories += calories
    else:
        elves.append(elf)  # Append the last elf
    return elves


def part1(data: list[str]) -> int:
    elves = parse(data)
    return max(e.calories for e in elves)


# =========== Part 2 ============


def part2(data: list[int]) -> int:
    elves = sorted(parse(data), key=lambda e: e.calories, reverse=True)
    return sum([e.calories for e in elves[:3]])


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
