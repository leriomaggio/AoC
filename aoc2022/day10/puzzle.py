""" -- Advent of Code 2022 --
Day 10, https://adventofcode.com/2022/day/10

Notes on Solutions:
Having fun with Python generators.
The core of the solution relies on a CPU class implementation 
which reads from an infinite tape.

Every time a new instruction is read from the tape, the appropriate
`op` is called (thanks to Python `getattr`).

The `noop` operation, just ticks the clock and returns.
The `addx` operation ticks (i.e. yields) the clock twice while also
properly adding the value to X.

The timing of operations is automatically managed via the yield
operators, along with self contained (private, i.e. _xx) methods that
handle the ops atomically.
In more details:
- _draw manages the on screen operations
- _tick manages the clock tick.

Public OPs (`noop` and `addx`) leverages on atomic internal ops
to handle clock

The solutions simply consume the generator for each data entry, which 
automatically syncs with internal clock ticking.
"""

__day__ = "10"
__title__ = "Cathode-Ray Tube"
__author__ = "leriomaggio"

from typing import Union
from pathlib import Path


def load(filepath: Union[str, Path]) -> list[str]:
    return [line for line in open(filepath).read().split("\n")]


class CPU:

    SCREEN_ROWS = 40

    def __init__(self) -> None:
        self.clock = 1
        self.sprite = 1
        self.screen = ""
        self.signal_strength = 0

    def read(self):
        line = None
        while True:
            instruction = yield line
            op, *value = instruction.split()
            for tick in getattr(self, op)(value):
                yield tick
                if self.clock % self.SCREEN_ROWS == (self.SCREEN_ROWS / 2):
                    self.signal_strength += self.clock * self.sprite

    def _draw(self):
        position = (self.clock - 1) % self.SCREEN_ROWS
        self.screen += (
            "#" if position in range(self.sprite - 1, self.sprite + 2) else "."
        )
        if position == self.SCREEN_ROWS - 1:
            self.screen += "\n"

    def _tick(self):
        self._draw()
        self.clock += 1

    def noop(self, _):
        self._tick()
        yield self.clock

    def addx(self, values):
        self._tick()
        yield self.clock
        self._tick()
        self.sprite += int(values[0])
        yield self.clock


# =========== Part 1 ============


def part1(data: list[str]) -> int:
    cpu = CPU()
    tape = cpu.read()
    next(tape)
    for line in data:
        tick = tape.send(line)
        while next(tape):
            pass  # noop
    return cpu.signal_strength


# =========== Part 2 ============


def part2(data: list[int]) -> int:
    cpu = CPU()
    tape = cpu.read()
    next(tape)
    for line in data:
        tick = tape.send(line)
        while next(tape):
            pass  # noop
    print(cpu.screen)
    return cpu.signal_strength  # only for tests to pass


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
