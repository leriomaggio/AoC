""" -- Advent of Code 2021 --
Day 03, https://adventofcode.com/2021/day/3

Notes on Solutions:
- Part 1: This part is all about calculating the `gamma_rate`, since the `epsilon_rate` is easily
          determined as the _complement_ of the former. In fact, the `complement` (`lambda`) function
          has been defined, using `mod 2` arithmentic. Also, `most_common_bits` function's implementation
          uses the new _Walrus Operator_ in Python to define and use `ones` in one-liner.
- Part 2: Not very much to say here apart maybe mentioning the use of the `f_bits` paramenter in the
          `rate` function which allows to re-use the same implementation for both `oxygen` and `co2` rates.
          (Default is the identity function)
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
    zeros = len(bits) - (ones := len(list(filter(lambda b: b == "1", bits))))
    return "1" if ones >= zeros else "0"


complement = lambda b: str((int(b) + 1) % 2)


def part1(data: list[str]) -> int:
    gamma_rate = reduce(add, map(most_common_bit, zip(*data)))
    epsilon_rate = reduce(add, map(complement, gamma_rate))
    return int(gamma_rate, base=2) * int(epsilon_rate, base=2)


# =========== Part 2 ============


def rate(diagnostics: list[str], f_bits: Callable[[str], str] = lambda b: b) -> str:
    nr_of_bits = len(diagnostics[0])
    for idx in range(nr_of_bits):
        mcb = f_bits(most_common_bit([b[idx] for b in diagnostics]))
        diagnostics = list(filter(lambda b: b[idx] == mcb, diagnostics))
        if len(diagnostics) == 1:
            break
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
