""" -- Advent of Code 2021 --
Day 06, https://adventofcode.com/2021/day/6

Notes on Solutions:
- Part 1: This solution solves the puzzle using _brute-force_, that is enumerating 
          all the generations of lanternfish up until generation `80`.
          The only sensible thing to mention here is how using `dataclass` is 
          appropriate in this case (only in terms of data abstractions), saving
          lots of boilerplate code.
- Part 2: This solution is **way** more interesting, and scales pretty easily to any number
          of days. First, we do not enumerate with brute force all the breeds (like in Part 1)
          as it is NOT computationally feasible. The growth rate is indeed exponential, so 
          it explodes quite soon. What we do instead, is to generate the counts of breeds
          in each day, given an initial state. Crucial for this solution is the 
          [`defaultdict`](https://docs.python.org/3/library/collections.html#collections.defaultdict)
          data structure, which is very flexible and handy to keep summing up counts, without needing
          to check the presence of keys.
          Just for fun, with a more functional take there is an alternative solution proposed using 
          a generator for the breeds, in combination with 
          [`itertools.groupby`](https://docs.python.org/3/library/itertools.html#itertools.groupby)
          which allows to group and sum counts accordingly, directly withing the **dictionary comprehension**.
"""

__day__ = "06"
__title__ = "Lanternfish"
__author__ = "leriomaggio"

from pathlib import Path
from dataclasses import dataclass
from collections import defaultdict
from timeit import repeat


# =========== Part 1 ============
@dataclass
class LanternFish:
    clock: int = 8

    def spawn(self):
        if self.clock > 0:
            self.clock -= 1
            return None
        self.clock = 6
        return LanternFish()


def part1(line: str) -> int:
    fish = [LanternFish(clock=c) for c in map(int, line.strip().split(","))]
    for _ in range(80):
        new_gen = []
        for lf in fish:
            breed = lf.spawn()
            if breed:
                new_gen.append(breed)
        fish += new_gen
    return len(fish)


# =========== Part 2 ============


def part2(line: str, days: int = 256) -> int:
    lanternfish = defaultdict(int)
    for clock in map(int, line.split(",")):
        lanternfish[clock] += 1

    for _ in range(days):
        lanternfish = defaultdict(int, {k - 1: v for k, v in lanternfish.items()})
        if breed := lanternfish.pop(-1, 0):
            lanternfish[6] += breed
            lanternfish[8] += breed
        fish = lanternfish
    return sum(fish.values())


# ------------- (ALTERNATIVE Solution) ----------------------

from itertools import groupby


def spawn(fish):
    """generate counts for the new breeds of lanternfish"""
    for clock, count in fish.items():
        if clock > 0:
            yield clock - 1, count
        else:
            yield 6, count
            yield 8, count


def part2_alternative(line: str, days: int = 256) -> str:
    """
    Alternative implementation of solution for part 2.
    It is essentially the same idea but using a generator
    yielding counts for clocks (twice in case of new breeds).
    Counters are then grouped per clock value, and accumulated
    directly within dict comprehension, so not requiring to use
    defaultdict anymore!!

    CAVEATS: ~=3x slower on my computer (mostly due to the generator),
             little more convoluted, made just for fun!
    """

    fish = defaultdict(int)
    for clock in map(int, line.split(",")):
        fish[clock] += 1

    for d in range(days):
        fish = {
            k: v
            for k, v in map(
                lambda g: (
                    g[0],
                    sum(map(lambda t: t[1], g[1])),
                ),
                groupby(sorted(spawn(fish)), key=lambda e: e[0]),
            )
        }

    return sum(fish.values())


def timeit_p1():
    filepath = Path(__file__).with_name(f"input.{__day__}")
    # solve part 1
    part1(line=open(filepath).read().strip())


def timeit_p2():
    filepath = Path(__file__).with_name(f"input.{__day__}")
    # solve part 2
    part2(line=open(filepath).read().strip())


def timeit_p2_alternative():
    filepath = Path(__file__).with_name(f"input.{__day__}")
    # solve part 2 - alternative implementation
    part2_alternative(line=open(filepath).read().strip())


if __name__ == "__main__":
    print("=*=*=*=*=*=*=*=*=*= Advent of Code 2021 =*=*=*=*=*=*=*=*=*=")
    print(f"Day {__day__}: {__title__}")
    print("-" * 59)
    filepath = Path(__file__).with_name(f"input.{__day__}")
    # solve part 1
    print(part1(line=open(filepath).read().strip()))
    # solve part 2
    print((p2_ans := part2(line=open(filepath).read().strip())))
    print(p2_ans == part2_alternative(open(filepath).read().strip()))

    import timeit

    # just once as it's pretty slow!
    print(
        "TIME Part [1] (just once): ",
        timeit.timeit("timeit_p1()", setup="from __main__ import timeit_p1", number=1),
    )
    print(
        "TIME Part [2] (1000 times)",
        timeit.timeit(
            "timeit_p2()", setup="from __main__ import timeit_p2", number=1000
        ),
    )
    print(
        "TIME Part [2] Alternative (1000 times)",
        timeit.timeit(
            "timeit_p2_alternative()",
            setup="from __main__ import timeit_p2_alternative",
            number=1000,
        ),
    )
