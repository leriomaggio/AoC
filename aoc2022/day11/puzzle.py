""" -- Advent of Code 2022 --
Day 11, https://adventofcode.com/2022/day/11

Notes on Solutions:
- Part 1: This is quite straightforward, and does not require any particular adjustment
in the first attempt.
- Part 2: The solution to this part generalises the whole game by realising one important
thing: the whole game with monkeys is based on divisibility of items.
Since we have no `relief_factor` in this part, the **only** possible consideration that
we can derive to avoid our stress level going to the roof is that worry level of items
could never go beyon the product of all divisors.
"""

__day__ = "11"
__title__ = "Monkey in the Middle"
__author__ = "leriomaggio"

from typing import Union
from pathlib import Path
from math import prod
from operator import sub, add, truediv, mul
from typing import Optional
from collections import deque, namedtuple

operations = {"+": add, "-": sub, "*": mul, "/": truediv}
Item = namedtuple("Item", ["to", "item"])


class Monkey:
    def __init__(self, monkey_card: str) -> None:
        m_info = monkey_card.split("\n")
        self.items = deque(list(map(int, m_info[1].split(":")[1].strip().split(","))))
        self.divisible_by = int(m_info[3].split("divisible by")[1].strip())
        self._worry_expr = m_info[2].split("=")[1].strip()
        self._mates = [
            int(l.split("throw to monkey")[1].strip()) for l in (m_info[5], m_info[4])
        ]
        self.inspected = 0

    def play(self, relief_factor: int, prod_divisors: int) -> Optional[Item]:
        if not self.items:
            return None
        item = (self.worry_level(self.items.popleft()) // relief_factor) % prod_divisors
        self.inspected += 1
        return Item(item=item, to=self._mates[int((item % self.divisible_by == 0))])

    def worry_level(self, item):
        l_operand, operator, r_operand = self._worry_expr.split()
        l_operand = item if l_operand == "old" else int(l_operand)
        r_operand = item if r_operand == "old" else int(r_operand)
        return operations[operator](l_operand, r_operand)

    def catch_item(self, item):
        self.items.append(item)


def load(filepath: Union[str, Path]) -> list[Monkey]:
    return parse(open(filepath).read())


def parse(data: str) -> list[Monkey]:
    return [Monkey(m_card) for m_card in data.split("\n\n")]


def game(monkeys: list[Monkey], n_rounds: int, relief: int) -> int:
    prod_divisors = prod([monkey.divisible_by for monkey in monkeys])
    for r in range(n_rounds):
        for monkey in monkeys:
            while True:
                thrown_item = monkey.play(
                    prod_divisors=prod_divisors, relief_factor=relief
                )
                if thrown_item is None:
                    break
                monkeys[thrown_item.to].catch_item(thrown_item.item)
    return prod(sorted([m.inspected for m in monkeys], reverse=True)[:2])


# =========== Part 1 ============


def part1(data: list[Monkey]) -> int:
    return game(data, n_rounds=20, relief=3)


# =========== Part 2 ============


def part2(data: list[Monkey]) -> int:
    return game(data, n_rounds=10000, relief=1)


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
