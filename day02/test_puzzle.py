"""Test Module for Puzzles in Day 01: Sonar Swipe"""

import logging
from pathlib import Path
from pytest import fixture

from puzzle import load, part1, part2

LOGGER = logging.getLogger(__name__)

EXAMPLE_DATA = """forward 5
down 5
forward 8
up 3
down 8
forward 2
"""


class AoCTest:
    @fixture(scope="function")
    def sample_input(self) -> list[int]:
        LOGGER.info("Test Input")
        return load(EXAMPLE_DATA.splitlines())

    @fixture(scope="function")
    def game_input(self) -> list[int]:
        LOGGER.info("Game Input")
        path = Path(__file__).with_name("input.02")
        return load(lines=open(path).read().strip().splitlines())


# ------ Part 1 ------


class TestPartOne(AoCTest):
    def test_part1_on_sample_data(self, sample_input):
        LOGGER.info(f"Part 1: Test Input")
        assert part1(sample_input) == 150, f"Part 1 - Test Input ❌"

    def test_part1_on_game_input(self, game_input):
        LOGGER.info(f"Part 1: Game Input")
        assert part1(game_input) == 1524750, f"Part 1 - Game Input ❌"


# ----- Part 2 -----


class TestPartTwo(AoCTest):
    def test_part2_on_sample_data(self, sample_input):
        LOGGER.info(f"Part 2: Test Input")
        assert part2(sample_input) == 900, f"Part 2 - Test Input ❌"

    def test_part2_on_game_input(self, game_input):
        LOGGER.info(f"Part 2: Game Input")
        assert part2(game_input) == 1592426537, f"Part 2 - Game Input ❌"
