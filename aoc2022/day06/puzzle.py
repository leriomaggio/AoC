""" -- Advent of Code 2022 --
Day 06, https://adventofcode.com/2022/day/6

Notes on Solutions:
Also in this case, the implementation of the two solutions is the very same
apart from an input parameters that changes from `4` to `14` in part 2.

The `parse` function is adding one character at a time and returns as soon
as the first list of unique characters of target lenght has been found.
"""

__day__ = "06"
__title__ = "Tuning Trouble"
__author__ = "leriomaggio"

from typing import Union
from pathlib import Path


def load(filepath: Union[str, Path]) -> str:
    return open(filepath).read().strip()


def parse(message: str, length: int) -> int:
    received = list(message[: (st := length - 1)])
    for character in message[st:]:
        received.append(character)
        if len(set(received[-length:])) == length:
            return len(received)


# =========== Part 1 ============


def part1(data: str) -> int:
    return parse(message=data, length=4)


# =========== Part 2 ============


def part2(data: list[int]) -> int:
    return parse(message=data, length=14)


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
