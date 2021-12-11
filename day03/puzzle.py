# -- Advent of Code 2021 --
# Day 03: Binary Diagnostic
# https://adventofcode.com/2021/day/3

from pathlib import Path
from collections import Counter
from operator import add
from functools import reduce

from typing import Callable


def load(filepath: str = "./input.txt") -> list[str]:
    return open(filepath).read().strip().splitlines()


# =========== Part 1 ============

complement = lambda c: str(int(not (int(c))))


def most_common_bit(bits: str) -> str:
    ones = len(list(filter(lambda b: b == "1", bits)))
    zeros = len(bits) - ones
    return "1" if ones >= zeros else "0"


def part1(data: list[str]) -> int:
    gamma_rate = reduce(add, map(most_common_bit, zip(*data)))
    epsilon_rate = reduce(add, map(complement, gamma_rate))
    return int(gamma_rate, base=2) * int(epsilon_rate, base=2)


# =========== Part 2 ============


def rate(diagnostics: list[str], f_bits: Callable[[str], str] = lambda b: b) -> str:
    nr_of_bits, prefix = len(diagnostics[0]), ""
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
    print("Day 03: Binary Diagnostic")
    print("-" * 59)
    filepath = Path(__file__).with_name("input.txt")
    data = load(filepath=filepath)
    # solve part 1
    print(part1(data))
    # solve part 2
    print(part2(data))
