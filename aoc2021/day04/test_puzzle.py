"""Test Module for Puzzles in Day 04: Giant Squid"""

import logging
from pathlib import Path
from pytest import fixture

from puzzle import load, part1, part2

LOGGER = logging.getLogger(__name__)

EXAMPLE_DATA = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
"""

from puzzle import __day__, __title__

LOGGER.warning(f"Test AoC21 Day {__day__}: {__title__}")


class AoCTest:
    @fixture(scope="function")
    def sample_input(self) -> list[int]:
        LOGGER.info("Test Input")
        return load(EXAMPLE_DATA.strip().splitlines())

    @fixture(scope="function")
    def game_input(self) -> list[int]:
        LOGGER.info("Game Input")
        filepath = Path(__file__).with_name(f"input.{__day__}")
        return load(open(filepath).read().strip().splitlines())


# ------ Part 1 ------


class TestPartOne(AoCTest):
    def test_part1_on_sample_data(self, sample_input):
        LOGGER.info(f"Part 1: Test Input")
        numbers, boards = sample_input
        assert part1(numbers, boards) == 4512, f"Part 1 - Test Input ❌"

    def test_part1_on_game_input(self, game_input):
        LOGGER.info(f"Part 1: Game Input")
        numbers, boards = game_input
        assert part1(numbers, boards) == 49686, f"Part 1 - Game Input ❌"


# ----- Part 2 -----


class TestPartTwo(AoCTest):
    def test_part2_on_sample_data(self, sample_input):
        LOGGER.info(f"Part 2: Test Input")
        numbers, boards = sample_input
        assert part2(numbers, boards) == 1924, f"Part 2 - Test Input ❌"

    def test_part2_on_game_input(self, game_input):
        LOGGER.info(f"Part 2: Game Input")
        numbers, boards = game_input
        assert part2(numbers, boards) == 26878, f"Part 2 - Game Input ❌"
