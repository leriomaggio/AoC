""" -- Advent of Code 2021 --
Day 01:
https://adventofcode.com/2021/day/1

Notes on Solutions:
- Part 1: I've used [`getattr`](https://docs.python.org/3/library/functions.html#getattr) to dynamically
          invoke methods from the `Submarine` class, as read from the input file. That's kinda cool.
          I've always found Python _built-in_ reflective features quite fascinating!
- Part 2: The whole point of `part2` is about _subclassing_. Why `dataclass`? Just becasuse they were
         quicker to implement in this case.
"""

__day__ = "02"
__title__ = "Dive"
__author__ = "leriomaggio"

from pathlib import Path
from typing import Union
from dataclasses import dataclass


def load(lines: list[str]) -> list[tuple[str, str]]:
    return list(map(lambda l: tuple(l.split()), lines))


# =========== Part 1 ============


@dataclass
class Submarine:
    x: int = 0
    y: int = 0

    def forward(self, x: int):
        self.x += x

    def up(self, y: int):
        self.y -= y

    def down(self, y: int):
        self.y += y


def part1(data: list[tuple[str, str]]) -> int:
    submarine = Submarine()
    for cmd, value in data:
        getattr(submarine, cmd)(int(value))
    return submarine.x * submarine.y


# =========== Part 2 ============


@dataclass
class Torpedo(Submarine):
    aim: int = 0

    def forward(self, x: int):
        self.x += x
        self.y += self.aim * x

    def up(self, a: int):
        self.aim -= a

    def down(self, a: int):
        self.aim += a


def part2(data: list[tuple[str, str]]) -> int:
    torpedo = Torpedo()
    for cmd, value in data:
        getattr(torpedo, cmd)(int(value))
    return torpedo.x * torpedo.y


if __name__ == "__main__":
    print("=*=*=*=*=*=*=*=*=*= Advent of Code 2021 =*=*=*=*=*=*=*=*=*=")
    print(f"Day {__day__}: {__title__}")
    print("-" * 59)
    filepath = Path(__file__).with_name(f"input.{__day__}")
    data = load(lines=open(filepath).read().strip().splitlines())
    # solve part 1
    print(part1(data))
    # solve part 2
    print(part2(data))
