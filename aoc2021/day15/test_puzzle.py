"""Test Module for Puzzles in Day 15: Chitons"""

import logging
from pathlib import Path
from pytest import fixture

from puzzle import load, part1, part2
from puzzle import __day__, __title__

LOGGER = logging.getLogger(__name__)

EXAMPLE_DATA = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
"""

LOGGER.warning(f"Test AoC21 Day {__day__}: {__title__}")


class AoCTest:
    @fixture(scope="function")
    def sample_input(self) -> list[int]:
        LOGGER.info("Test Input")
        return load(EXAMPLE_DATA.splitlines())

    @fixture(scope="function")
    def game_input(self) -> list[int]:
        LOGGER.info("Game Input")
        filepath = Path(__file__).with_name(f"input.{__day__}")
        return load(lines=open(filepath).read().strip().splitlines())


# ------ Part 1 ------


class TestPartOne(AoCTest):
    def test_part1_on_sample_data(self, sample_input):
        LOGGER.info(f"Part 1: Test Input")
        assert part1(sample_input) == 40, f"Part 1 - Test Input ❌"

    def test_part1_on_game_input(self, game_input):
        LOGGER.info(f"Part 1: Game Input")
        assert part1(game_input) == 673, f"Part 1 - Game Input ❌"


# ----- Part 2 -----


class TestPartTwo(AoCTest):
    def test_part2_on_sample_data(self, sample_input):
        LOGGER.info(f"Part 2: Test Input")
        assert part2(sample_input) == 315, f"Part 2 - Test Input ❌"

    def test_part2_on_game_input(self, game_input):
        LOGGER.info(f"Part 2: Game Input")
        assert part2(game_input, s=(0, 0), size=5) == 2893, f"Part 2 - Game Input ❌"
