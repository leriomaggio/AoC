""" -- Advent of Code 2021 --
Day 03, https://adventofcode.com/2021/day/3

Notes on Solutions:
- Part 1: I've used [`getattr`](https://docs.python.org/3/library/functions.html#getattr) to dynamically
          invoke methods from the `Submarine` class, as read from the input file. That's kinda cool.
          I've always found Python _built-in_ reflective features quite fascinating!
- Part 2: The whole point of `part2` is about _subclassing_. Why `dataclass`? Just becasuse they were
         quicker to implement in this case.
"""

__day__ = "03"
__title__ = "Binary Diagnostic"
__author__ = "leriomaggio"


from pathlib import Path
from typing import Union, Callable
from operator import add
from functools import reduce


def load(filepath: Union[str, Path]) -> list[str]:
    return open(filepath).read().strip().splitlines()


# =========== Part 1 ============


def most_common_bit(bits: str) -> str:
    ones = len(list(filter(lambda b: b == "1", bits)))
    zeros = len(bits) - ones
    return "1" if ones >= zeros else "0"


complement = lambda b: str((int(b) + 1) % 2)


def part1(data: list[str]) -> int:
    gamma_rate = reduce(add, map(most_common_bit, zip(*data)))
    epsilon_rate = reduce(add, map(complement, gamma_rate))
    return int(gamma_rate, base=2) * int(epsilon_rate, base=2)


# =========== Part 2 ============


def rate(diagnostics: list[str], f_bits: Callable[[str], str] = lambda b: b) -> str:
    nr_of_bits = len(diagnostics[0])
    for i in range(nr_of_bits):
        mcb = f_bits(most_common_bit([b[i] for b in diagnostics]))
        diagnostics = list(filter(lambda b: b[i] == mcb, diagnostics))
        if len(diagnostics) == 1:
            return diagnostics[0]


def part2(data: list[str]) -> int:
    oxygen_rate = rate(data)
    co2_rate = rate(data, f_bits=complement)
    return int(oxygen_rate, base=2) * int(co2_rate, base=2)


if __name__ == "__main__":
    print("=*=*=*=*=*=*=*=*=*= Advent of Code 2021 =*=*=*=*=*=*=*=*=*=")
    print(f"Day {__day__}: {__title__}")
    print("-" * 59)
    filepath = Path(__file__).with_name(f"input.{__day__}")
    data = load(filepath=filepath)
    # solve part 1
    print(part1(data))
    # solve part 2
    print(part2(data))
