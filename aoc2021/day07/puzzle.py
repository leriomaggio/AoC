""" -- Advent of Code 2021 --
Day 07, https://adventofcode.com/2021/day/07

Notes on Solutions:
- Part 1: The solution to this challenge is pretty straightforward, and there isn't
          really much to say about it. In Part 1 we enumerate all the 
          fuel consumptions, that is the sum of all the corresponding 
          (absolute) distances, for all the **unique** available positions, 
          and we take the minimum.
- Part 2: This solution reuses exactly the same code (in a functional fashion)
          of the previous solution. However, this time all possible positions
          on the board should be considered. Therefore, the outer iterable
          is set to `range(max(positions) + 1)`. 
          The fuel consumptions rule can be calculated immediately as it does
          correspond to the sum of the first `N` naturals (absolute differences, 
          in this case!). To do so, the `walrus` operator is first used to 
          store the value of the distance, which is then used within the same 
          calculation for the final result!.
"""

__day__ = "07"
__title__ = "The Threachery of Wales"
__author__ = "leriomaggio"

from typing import Union
from pathlib import Path


def load(filepath: Union[str, Path]):
    return list(map(int, open(filepath).read().strip().split(",")))


# =========== Part 1 ============


def part1(positions: list[int]) -> int:
    return min(
        map(
            lambda target: sum(map(lambda p: abs(target - p), positions)),
            set(positions),
        )
    )


# =========== Part 2 ============

from itertools import product


def part2(positions: list[int]) -> int:
    return min(
        map(
            lambda target: sum(
                map(lambda p: ((d := abs(target - p)) * (d + 1)) // 2, positions)
            ),
            range(max(positions) + 1),
        )
    )


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
