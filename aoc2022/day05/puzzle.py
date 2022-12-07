""" -- Advent of Code 2022 --
Day 05, https://adventofcode.com/2022/day/5

Notes on Solutions:
Both solutions rely on the double-ended queues, and most of the
heavylifting is performed in the `parse` function.

The `parse` function is processing the input to return a
dictionary of double-ended queues (indexed by the queue number),
along with the list of instructions.

The second generalisation between the two solutions has been
achieved thanks to the `move` function which is moving
items from one stack to another. The only difference is in the
optional `key_fn` passed in. Identity function for part1,
reversed function for part2.

In other words, in part1, crates are added to the destination stack
in the same order they're extracted from the first stack (i.e. FIFO),
whilst part2 adds crates to the destination stack in reverse order from
how they're popped from the source stack.
"""

__day__ = "05"
__title__ = "Supply Stacks"
__author__ = "leriomaggio"

from typing import Union
from pathlib import Path
from collections import deque, defaultdict
from typing import Callable, Iterable


def load(filepath: Union[str, Path]) -> list[str]:
    return list(open(filepath).read().split("\n"))


def parse(
    data: list[str],
) -> tuple[defaultdict[int, deque], list[tuple[int, int, int]]]:
    stacks = defaultdict(deque)
    instructions = list()
    get_instructions = False

    for line in data:
        if not (ls := line.strip()) or ls.startswith("1"):
            get_instructions = True
            continue

        if get_instructions:
            instructions.append(tuple(map(int, ls.split()[1::2])))
        else:
            crates = {
                c + 1: ll[1]
                for c, i in enumerate(range(0, len(line), 4))
                if (ll := line[i : i + 3].strip())
            }
            for index, item in crates.items():
                stacks[index].append(item)
    return stacks, instructions


def move(data: list[str], reverse: bool = False) -> str:
    stacks, instructions = parse(data)
    key_fn = reversed if reverse else lambda l: l
    for amount, from_id, to_id in instructions:
        for crate in key_fn(
            list(map(lambda _: stacks[from_id].popleft(), range(amount)))
        ):
            stacks[to_id].appendleft(crate)
    return "".join([stacks[sk][0] for sk in sorted(stacks)])


# =========== Part 1 ============


def part1(data: list[str]) -> str:
    return move(data=data)


# =========== Part 2 ============


def part2(data: list[int]) -> int:
    return move(data=data, reverse=True)


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
