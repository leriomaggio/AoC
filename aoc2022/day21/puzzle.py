""" -- Advent of Code 2022 --
Day 21, https://adventofcode.com/2022/day/21

Notes on Solutions:
- Part 1: 
- Part 2: 
"""

__day__ = "21"
__title__ = "Monkey Math"
__author__ = "leriomaggio"

from typing import Union
from pathlib import Path


def load(filepath: Union[str, Path]):
    return parse_input(open(filepath).read().split("\n"))


def parse_input(data: list[str]):
    monkeys = dict()
    for line in data:
        name, expr = line.strip().split(": ")
        if expr.isdigit():
            monkeys[name] = int(expr)
        else:
            m1, op, m2 = expr.split()
            monkeys[name] = (m1, op, m2)
    return monkeys


HUMAN = "humn"


def solve_monkey_math(monkeys, monkey="root"):
    if isinstance(monkeys[monkey], int):
        return monkeys[monkey], monkey == HUMAN

    monkey_a, op, monkey_b = monkeys[monkey]
    left, mleft_is_humn = solve_monkey_math(monkeys, monkey_a)
    right, mright_is_humn = solve_monkey_math(monkeys, monkey_b)

    match op:
        case "+":
            result = left + right
        case "-":
            result = left - right
        case "*":
            result = left * right
        case "/":
            result = left // right

    return result, mleft_is_humn or mright_is_humn


def inverse_monkey_math(monkeys, monkey="root", inv_result=None):
    if monkey == HUMAN:
        return inv_result

    monkey_a, op, monkey_b = monkeys[monkey]
    left, mleft_is_humn = solve_monkey_math(monkeys, monkey=monkey_a)
    right, mright_is_humn = solve_monkey_math(monkeys, monkey=monkey_b)

    if mleft_is_humn:
        if monkey == "root":
            return inverse_monkey_math(monkeys, monkey_a, right)

        match op:
            case "+":
                inv_result = inv_result - right
            case "-":
                inv_result = inv_result + right
            case "*":
                inv_result = inv_result // right
            case "/":
                inv_result = inv_result * right
        return inverse_monkey_math(monkeys, monkey_a, inv_result)

    if mright_is_humn:
        if monkey == "root":
            return inverse_monkey_math(monkeys, monkey_b, left)

        match op:
            case "+":
                inv_result = inv_result - left
            case "-":
                inv_result = left - inv_result
            case "*":
                inv_result = inv_result // left
            case "/":
                inv_result = left // inv_result
        return inverse_monkey_math(monkeys, monkey_b, inv_result)


# =========== Part 1 ============


def part1(data: list[int]) -> int:
    return solve_monkey_math(monkeys=data, monkey="root")[0]


# =========== Part 2 ============


def part2(data: list[int]) -> int:
    return inverse_monkey_math(monkeys=data)


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
