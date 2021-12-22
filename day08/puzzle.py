""" -- Advent of Code 2021 --
Day 08, https://adventofcode.com/2021/day/08

Notes on Solutions:
- Part 1: Nothing particularly fancy here, apart from flattening a list of lists within a single iteration
          using [`itertools.chain.from_iterable`](https://docs.python.org/3/library/itertools.html?itertools.chain.from_iterable)
- Part 2: As for the second part, we need to dwelve into decoding each line (differently). The decoding strategy 
          will build on what we know about digits, starting from *known* digits (i.e. `1`, `4`, `7`, `8`), and 
          then trying to workout general decoding rules using the patterns for those. Eight is the only digit 
          that is completely useless, whereas _one_, _four_ and _seven_ can be effectively used to decode 
          all other digits, in combination with their corresponding `len`.
          Last but not least, once decoded, patterns in the output (right handside of the game input) will 
          be processed and decifered, accordingly.
          On this note, it's worth mentioning the use of [`frozenset`](https://docs.python.org/3/library/stdtypes.html?frozenset) as immutable sets in the decoding map.
"""

__day__ = "08"
__title__ = "Seven Segment Search"
__author__ = "leriomaggio"

from pathlib import Path
from itertools import chain


def load(lines: list[str]) -> tuple[list[str], list[str]]:
    left, right = [], []
    for line in lines:
        codes, output = line.split("|")
        left.append(codes.strip().split(" "))
        right.append(output.strip().split(" "))
    return left, right


# =========== Part 1 ============


def part1(data: tuple[list[str], list[str]]) -> int:
    _, output = data
    return len(
        list(filter(lambda d: len(d) in [2, 4, 3, 7], chain.from_iterable(output)))
    )


# =========== Part 2 ============


def one(msg: str) -> bool:
    return len(msg) == 2


def four(msg: str) -> bool:
    return len(msg) == 4


def seven(msg: str) -> bool:
    return len(msg) == 3


def eight(msg: str) -> bool:
    return len(msg) == 7


def two(msg: str, one_pattern: str, four_pattern: str, seven_pattern: str) -> bool:
    return (
        len(msg) == 5
        and len(set(seven_pattern).intersection(msg)) == 2
        and len(set(four_pattern).difference(one_pattern).intersection(msg)) == 1
    )


def three(msg: str, seven_pattern: str) -> bool:
    return len(msg) == 5 and len(set(seven_pattern).intersection(msg)) == 3


def five(msg: str, one_pattern, four_pattern) -> bool:
    return (
        len(msg) == 5
        and len(set(four_pattern).difference(one_pattern).intersection(msg)) == 2
    )


def zero(msg: str, four_pattern: str, seven_pattern: str) -> bool:
    return (
        len(msg) == 6
        and len(set(seven_pattern).intersection(msg)) == 3
        and len(set(four_pattern).difference(msg)) == 1
    )


def six(msg: str, four_pattern: str, seven_pattern: str) -> bool:
    return (
        len(msg) == 6
        and len(set(seven_pattern).intersection(msg)) == 2
        and len(set(four_pattern).difference(msg)) == 1
    )


def nine(msg: str, four_pattern: str, seven_pattern: str) -> bool:
    return (
        len(msg) == 6
        and len(set(four_pattern).intersection(msg)) == len(four_pattern)
        and len(set(seven_pattern).intersection(msg)) == len(seven_pattern)
    )


def part2(data: tuple[list[str], list[str]]) -> int:
    line_outputs = list()
    input_digits, output_messages = data
    for patterns, message in zip(input_digits, output_messages):
        digits = {}
        digits[1] = next(filter(one, patterns))
        digits[4] = next(filter(four, patterns))
        digits[7] = next(filter(seven, patterns))
        digits[8] = next(filter(eight, patterns))

        digits[3] = next(filter(lambda p: three(p, digits[7]), patterns))
        digits[5] = next(filter(lambda p: five(p, digits[1], digits[4]), patterns))
        digits[2] = next(
            filter(lambda p: two(p, digits[1], digits[4], digits[7]), patterns)
        )

        digits[0] = next(filter(lambda p: zero(p, digits[4], digits[7]), patterns))
        digits[6] = next(filter(lambda p: six(p, digits[4], digits[7]), patterns))
        digits[9] = next(filter(lambda p: nine(p, digits[4], digits[7]), patterns))

        decode_map = {frozenset(v): str(k) for k, v in digits.items()}
        line_outputs.append(int("".join([decode_map[frozenset(p)] for p in message])))
    return sum(line_outputs)


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
