""" -- Advent of Code 2022 --
Day 04, https://adventofcode.com/2022/day/4

Notes on Solutions:
The core of both solutions rely on the `Range` implementation
which is using the Python Data Model to implement an iterable
range object which implements the `__contains__` (for part 1)
and `__le__` (for part 2)
Therefore, part1 relies on the `in` Python operator, whereas part 2
on <= (less then or equal).

Interestingly, the `__iter__` method is also fundamental
to allow for set conversion in other two magic methods.
"""

__day__ = "04"
__title__ = "Camp Cleanup"
__author__ = "leriomaggio"

from typing import Union
from pathlib import Path


class Range:
    def __init__(self, assignment: str) -> None:
        l, r = assignment.split("-")
        self.left, self.right = int(l.strip()), int(r.strip())

    def __contains__(self, other: "Range") -> bool:
        return self.left <= other.left <= other.right <= self.right

    def __iter__(self):
        yield from range(self.left, self.right + 1)

    def __le__(self, other: "Range") -> bool:
        return len(set(other).intersection(set(self))) > 0

    def __len__(self):
        return self.right - self.left


def load(filepath: Union[str, Path]) -> list[tuple[str]]:
    return list(
        map(lambda line: tuple(line.split(",")), open(filepath).read().split("\n"))
    )


# =========== Part 1 ============


def part1(data: list[list[str]]) -> int:
    assignments = list(map(lambda pair: tuple(map(lambda a: Range(a), pair)), data))
    return sum(first in second or second in first for first, second in assignments)


# =========== Part 2 ============


def part2(data: list[tuple[str]]) -> int:
    assignments = list(map(lambda pair: tuple(map(lambda a: Range(a), pair)), data))
    return sum(first <= second or second <= first for first, second in assignments)


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
