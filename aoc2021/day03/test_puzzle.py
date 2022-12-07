"""Test Module for Puzzles in Day 03: Binary Diagnostic"""

import logging
from pathlib import Path
from pytest import fixture

from puzzle import load, part1, part2

LOGGER = logging.getLogger(__name__)

EXAMPLE_DATA = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
"""

from puzzle import __day__, __title__

LOGGER.warning(f"Test AoC21 Day {__day__}: {__title__}")


class AoCTest:
    @fixture(scope="function")
    def sample_input(self) -> list[int]:
        LOGGER.info("Test Input")
        return EXAMPLE_DATA.strip().splitlines()

    @fixture(scope="function")
    def game_input(self) -> list[int]:
        LOGGER.info("Game Input")
        return load(Path(__file__).with_name("input.03"))


# ------ Part 1 ------


class TestPartOne(AoCTest):
    def test_part1_on_sample_data(self, sample_input):
        LOGGER.info(f"Part 1: Test Input")
        assert part1(sample_input) == 198, f"Part 1 - Test Input ❌"

    def test_part1_on_game_input(self, game_input):
        LOGGER.info(f"Part 1: Game Input")
        assert part1(game_input) == 3374136, f"Part 1 - Game Input ❌"


# ----- Part 2 -----


class TestPartTwo(AoCTest):
    def test_part2_on_sample_data(self, sample_input):
        LOGGER.info(f"Part 2: Test Input")
        assert part2(sample_input) == 230, f"Part 2 - Test Input ❌"

    def test_part2_on_game_input(self, game_input):
        LOGGER.info(f"Part 2: Game Input")
        # Test all sequence of bits have the same length!
        assert len(set(map(len, game_input))) == 1
        assert part2(game_input) == 4432698, f"Part 2 - Game Input ❌"
