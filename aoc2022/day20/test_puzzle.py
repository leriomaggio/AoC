"""Test Module for Puzzles in Day 20: Grove Positioning System"""

import logging
from pathlib import Path
from pytest import fixture, mark

from puzzle import load, parse_input, part1, part2
from puzzle import __day__, __title__

LOGGER = logging.getLogger(__name__)

EXAMPLE_DATA = """1
2
-3
3
-2
0
4
"""

LOGGER.warning(f"Test AoC22 Day {__day__}: {__title__}")


class AoCTest:
    @fixture(scope="function")
    def sample_input(self) -> list[int]:
        LOGGER.info("Test Input")
        return parse_input(EXAMPLE_DATA.splitlines())

    @fixture(scope="function")
    def game_input(self) -> list[int]:
        LOGGER.info("Game Input")
        return load(filepath=Path(__file__).with_name(f"input.{__day__}"))


# ------ Part 1 ------


class TestPartOne(AoCTest):
    def test_part1_on_sample_data(self, sample_input):
        LOGGER.info(f"Part 1: Test Input")
        assert part1(sample_input) == 3, f"Part 1 - Test Input ❌"

    def test_part1_on_game_input(self, game_input):
        LOGGER.info(f"Part 1: Game Input")
        assert part1(game_input) == 10707, f"Part 1 - Game Input ❌"


# ----- Part 2 -----


class TestPartTwo(AoCTest):
    def test_part2_on_sample_data(self, sample_input):
        LOGGER.info(f"Part 2: Test Input")
        assert part2(sample_input) == 1623178306, f"Part 2 - Test Input ❌"

    def test_part2_on_game_input(self, game_input):
        LOGGER.info(f"Part 2: Game Input")
        assert part2(game_input) == 2488332343098, f"Part 2 - Game Input ❌"
