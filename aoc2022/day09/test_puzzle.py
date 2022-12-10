"""Test Module for Puzzles in Day 09: Rope Bridge"""

import logging
from pathlib import Path
from pytest import fixture, mark

from puzzle import load, part1, part2
from puzzle import __day__, __title__

LOGGER = logging.getLogger(__name__)

EXAMPLE_DATA = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""

EXAMPLE_DATA_PART_2 = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
"""

LOGGER.warning(f"Test AoC22 Day {__day__}: {__title__}")


class AoCTest:
    @fixture(scope="function")
    def sample_input(self) -> list[int]:
        LOGGER.info("Test Input")
        return list(
            map(
                lambda l: (l.split()[0], int(l.split()[1])),
                EXAMPLE_DATA.splitlines(),
            )
        )

    @fixture(scope="function")
    def sample_input_part_2(self) -> list[int]:
        LOGGER.info("Test Input")
        return list(
            map(
                lambda l: (l.split()[0], int(l.split()[1])),
                EXAMPLE_DATA_PART_2.splitlines(),
            )
        )

    @fixture(scope="function")
    def game_input(self) -> list[int]:
        LOGGER.info("Game Input")
        return load(filepath=Path(__file__).with_name(f"input.{__day__}"))


# ------ Part 1 ------


class TestPartOne(AoCTest):
    def test_part1_on_sample_data(self, sample_input):
        LOGGER.info(f"Part 1: Test Input")
        assert part1(sample_input) == 13, f"Part 1 - Test Input ❌"

    def test_part1_on_game_input(self, game_input):
        LOGGER.info(f"Part 1: Game Input")
        assert part1(game_input) == 6209, f"Part 1 - Game Input ❌"


# ----- Part 2 -----


class TestPartTwo(AoCTest):
    def test_part2_on_sample_data(self, sample_input_part_2):
        LOGGER.info(f"Part 2: Test Input")
        assert part2(sample_input_part_2) == 36, f"Part 2 - Test Input ❌"

    def test_part2_on_game_input(self, game_input):
        LOGGER.info(f"Part 2: Game Input")
        assert part2(game_input) == 2460, f"Part 2 - Game Input ❌"
