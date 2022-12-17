""" -- Advent of Code 2022 --
Day 17, https://adventofcode.com/2022/day/17

Notes on Solutions:
The game is cyclic and repetitive (i.e. `itertools.cycle`),
therefore the key to unlock both Part1 (but mostly) Part 2
is to understand how to properly cache (dump) game states
so that it's possible to restore the game configuration to
that state.

The idea of caching is indeed quite straightfoward (once you can
see it 🙃): it would be necessary to store the corresponding
ids of the current piece and the current direction of the wind
(i.e. pattern), along with the configuration of the ceiling!.

If that configuration has been already calculated, the game
state (i.e. resting) could be restored so that each piece
will have coordinates which is proportional to the "current"
height AND number of pieces.

Similarly, the current number of pieces on the screen are rescaled
in a similar fashion, modulo the delta (current - cached).

With this trick in mind, part1 and 2 could be solved with the
same functions/methods.

Relevant tricks used in this puzzle:
- 2D coordinates as complex numbers (life savers!)
- rocks as sets so that we could leverage on & (intersection)
and | (union) for set operations.
"""

__day__ = "17"
__title__ = "Pyroclastic Flow"
__author__ = "leriomaggio"

from typing import Union
from pathlib import Path
from itertools import cycle


def load(filepath: Union[str, Path]):
    return parse_input(open(filepath).read())


def parse_input(data: str) -> str:
    return data.strip()  # noop


class Grid:
    def __init__(self):
        self._resting = set(x - 1j for x in range(7))
        self._cache = dict()

    @property
    def height(self) -> int:
        return max(int(r.imag) for r in self.resting)

    @property
    def ceiling(self) -> tuple[int]:
        return tuple(
            self.height - max(int(r.imag) for r in self.resting if r.real == i)
            for i in range(7)
        )

    @property
    def floor(self) -> complex:
        return 2 + (4 + self.height) * 1j

    @property
    def resting(self) -> set[complex]:
        return self._resting

    @resting.setter
    def resting(self, restings: set[complex]):
        self._resting = restings

    def __iter__(self):
        for p in self.resting:
            yield p

    def __contains__(self, rock: set[complex]) -> bool:
        return len(self._resting & rock)


class Tetris:
    PIECES = [  # (x, y), top to bottom
        # ➖
        {0 + 0j, 1 + 0j, 2 + 0j, 3 + 0j},
        # ➕
        {2 + 1j, 1 + 1j, 0 + 1j, 1 + 0j, 1 + 2j},
        # L
        {2 + 2j, 2 + 1j, 0 + 0j, 1 + 0j, 2 + 0j},
        # |
        {0 + 3j, 0 + 2j, 0 + 1j, 0 + 0j},
        # 🟫
        {1 + 0j, 1 + 1j, 0 + 0j, 0 + 1j},
    ]

    DIRECTIONS = {">": 1, "<": -1}

    def __init__(self, winds: str, n_rocks: int) -> None:
        self.n_rocks = n_rocks
        self.rocks = cycle(enumerate(self.PIECES))
        self.winds = cycle(enumerate(self.DIRECTIONS[d] for d in winds))
        self.grid = Grid()
        self.r_counter = n_rocks
        self.cache = dict()

    def move(self, rock: set[complex]):
        rock = {self.grid.floor + p for p in rock}
        while True:
            wind_idx, w = next(self.winds)
            w_rock = {r + w for r in rock}
            if all(0 <= r.real <= 6 for r in w_rock) and not w_rock in self.grid:
                rock = w_rock
            w_rock = {p - 1j for p in rock}  # move downwards
            if w_rock in self.grid:
                break
            rock = w_rock
        self.grid.resting |= rock
        return wind_idx

    def simulate(self):

        while self.r_counter > 0:
            rock_idx, rock = next(self.rocks)
            wind_idx = self.move(rock)
            self.r_counter -= 1
            cache_key = (rock_idx, wind_idx, self.grid.ceiling)
            r_counter_cache, cached_height = self.cache.setdefault(
                cache_key,
                (self.r_counter, self.grid.height),
            )
            if r_counter_cache != self.r_counter:
                delta_t, delta_y = (r_counter_cache - self.r_counter), (
                    self.grid.height - cached_height
                )
                self.grid.resting = {
                    r + (self.r_counter // delta_t) * (delta_y * 1j) for r in self.grid
                }
                self.r_counter %= delta_t

        return self.grid.height + 1


# =========== Part 1 ============


def part1(data: list[int]) -> int:
    return Tetris(winds=data, n_rocks=2022).simulate()


# =========== Part 2 ============


def part2(data: list[int]) -> int:
    return Tetris(winds=data, n_rocks=1000000000000).simulate()


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
