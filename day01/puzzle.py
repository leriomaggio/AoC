""" -- Advent of Code 2021 --
Day 01:
https://adventofcode.com/2021/day/1

Notes on Solutions:
- Part 1: Uses the new `pairwise` function in itertools introduced in Python 3.10
- Part 2: Uses a sliding window function whose implementation has been borrowed from the 
          wonderful [`more-itertools`](https://pypi.org/project/more-itertools/) Python package
"""

__day__ = "01"
__title__ = "Sonar Sweep"
__author__ = "leriomaggio"

from itertools import pairwise
from pathlib import Path
from collections import deque
from itertools import islice


def load(filepath: str = "./input.txt") -> list[int]:
    return list(map(int, open(filepath).read().split("\n")))


# =========== Part 1 ============


def has_increased(left: int, right: int) -> bool:
    return right > left


def part1(data: list[int]) -> int:
    return len(list(filter(lambda p: has_increased(*p), pairwise(data))))


# =========== Part 2 ============


def sliding_window(iterable, n):
    # Implementation borrowed from more-itertools
    # https://pypi.org/project/more-itertools/
    it = iter(iterable)
    window = deque(islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)


def part2(data: list[int]) -> int:

    return len(
        list(
            filter(
                lambda p: has_increased(*p), pairwise(map(sum, sliding_window(data, 3)))
            )
        )
    )


if __name__ == "__main__":
    print("=*=*=*=*=*=*=*=*=*= Advent of Code 2021 =*=*=*=*=*=*=*=*=*=")
    print(f"Day {__day__}: {__title__}")
    print("-" * 59)
    filepath = Path(__file__).with_name("input.txt")
    data = load(filepath=filepath)
    # solve part 1
    print(part1(data))
    # solve part 2
    print(part2(data))
