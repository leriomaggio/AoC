""" -- Advent of Code 2022 --
Day XX, https://adventofcode.com/2022/day/13

Notes on Solutions:
The core of the solutions for both parts is the `compare_packets` (recursive) function.
`compare_packets` traverses the two packets, making sure the two compared
types are always (revursively) comparable.
The only relevant note with this implementation is the bounding criteria when items from
two packet lists are compared. As soon as a positive value is returned, the recursion could
be stopped as we know they're **not** in the right order.

- Part 1: Simply sum the indices (+1) where all `compare_packets` returns a negative value
- Part 2: The solution to the puzzle is quite simple: "sort the packets using the same
criterion as determined by the `compare_packets` function on the full list of packets to
which the two dividers have been added.
This means we could re-use entirely the previous implementation but two "problems" should
be handled first: (A) `data` is a list of pairs - so we need to flatten the list; and
(B) `compare_packets` needs to become a `key` function to be used in `sorted` or `list.sort`.

As for (A), we use `chain.from_iterable` from `itertools`. Easy.
As for (B), we leverage the magical `functools.cmp_to_key`
(https://docs.python.org/3/library/functools.html#functools.cmp_to_key)

Easy! The rest is pretty straightforward.

Now, the most interesting part of all, is how the `functools.cmp_to_key` is
actually implemented: https://github.com/python/cpython/blob/main/Lib/functools.py#L203
The implementation leverages the Python Data Model to create a custom comparator!
"""

__day__ = "13"
__title__ = "Distress Signal"
__author__ = "leriomaggio"

import sys
from typing import Union
from pathlib import Path
from functools import cmp_to_key
from itertools import chain

sys.setrecursionlimit(10000)


def load(filepath: Union[str, Path]):
    return parse_input(open(filepath).read())


def parse_input(data: str) -> list[tuple[str]]:
    return list(
        map(
            lambda pair: [eval(p) for p in pair],
            map(str.splitlines, data.split("\n\n")),
        )
    )


# =========== Part 1 ============


def compare_packets(l, r):
    if type(l) == int:
        if type(r) == int:
            return l - r
        return compare_packets([l], r)
    if type(r) == int:  # we know l is list at this point
        return compare_packets(l, [r])
    for ll, rr in zip(l, r):
        if c := compare_packets(ll, rr):  # bound comparison
            return c
    return len(l) - len(r)


def part1(data: list[tuple[str]]) -> int:
    return sum(
        i + 1
        for i, c in enumerate(map(lambda pair: compare_packets(*pair), data))
        if c < 0
    )


# =========== Part 2 ============


def part2(data: list[int]) -> int:
    all_packets = sorted(
        list(chain.from_iterable(data)) + [[[2]], [[6]]],
        key=cmp_to_key(compare_packets),
    )
    return (all_packets.index([[2]]) + 1) * (all_packets.index([[6]]) + 1)


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
