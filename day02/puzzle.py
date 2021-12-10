# -- Advent of Code 2021 --
# Day 02: Dive
# https://adventofcode.com/2021/day/s

from pathlib import Path
from dataclasses import dataclass


def load(filepath: str = "./input.txt"):
    return list(
        map(lambda l: tuple(l.split()), open(filepath).read().strip().splitlines())
    )


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
    print("Day 02: Dive")
    print("-" * 59)
    filepath = Path(__file__).with_name("input.txt")
    data = load(filepath=filepath)
    # solve part 1
    print(part1(data))
    # solve part 2
    print(part2(data))
