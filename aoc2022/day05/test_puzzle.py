"""Test Module for Puzzles in Day 05: Supply Stacks"""

import logging
from pathlib import Path
from pytest import fixture, mark

from puzzle import load, part1, part2
from puzzle import __day__, __title__

LOGGER = logging.getLogger(__name__)

EXAMPLE_DATA = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""

LOGGER.warning(f"Test AoC22 Day {__day__}: {__title__}")


class AoCTest:
    @fixture(scope="function")
    def sample_input(self) -> list[int]:
        LOGGER.info("Test Input")
        return list(map(str, EXAMPLE_DATA.splitlines()))

    @fixture(scope="function")
    def game_input(self) -> list[int]:
        LOGGER.info("Game Input")
        return load(filepath=Path(__file__).with_name(f"input.{__day__}"))


# ------ Part 1 ------


class TestPartOne(AoCTest):
    def test_part1_on_sample_data(self, sample_input):
        LOGGER.info(f"Part 1: Test Input")
        assert part1(sample_input) == "CMZ", f"Part 1 - Test Input ❌"

    def test_part1_on_game_input(self, game_input):
        LOGGER.info(f"Part 1: Game Input")
        assert part1(game_input) == "TLNGFGMFN", f"Part 1 - Game Input ❌"


# ----- Part 2 -----


class TestPartTwo(AoCTest):
    def test_part2_on_sample_data(self, sample_input):
        LOGGER.info(f"Part 2: Test Input")
        assert part2(sample_input) == "MCD", f"Part 2 - Test Input ❌"

    def test_part2_on_game_input(self, game_input):
        LOGGER.info(f"Part 2: Game Input")
        assert part2(game_input) == "FGLQJCMBD", f"Part 2 - Game Input ❌"
