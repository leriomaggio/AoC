"""Test Module for Puzzles in Day 06: Tuning Trouble"""

import logging
from pathlib import Path
from pytest import fixture, mark

from puzzle import load, part1, part2
from puzzle import __day__, __title__

LOGGER = logging.getLogger(__name__)

EXAMPLE_DATA = """mjqjpqmgbljsphdztnvjfqwrcgsmlb-7-19
bvwbjplbgvbhsrlpgdmjqwftvncz-5-23
nppdvjthqldpwncqszvftbrmjlhg-6-23
nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg-10-29
zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw-11-26
"""

LOGGER.warning(f"Test AoC22 Day {__day__}: {__title__}")


class AoCTest:
    @fixture(scope="function")
    def sample_input(self) -> list[int]:
        LOGGER.info("Test Input")
        return list(EXAMPLE_DATA.splitlines())

    @fixture(scope="function")
    def game_input(self) -> list[int]:
        LOGGER.info("Game Input")
        return load(filepath=Path(__file__).with_name(f"input.{__day__}"))


# ------ Part 1 ------


class TestPartOne(AoCTest):
    def test_part1_on_sample_data(self, sample_input):
        LOGGER.info(f"Part 1: Test Input")
        for sample in sample_input:
            s_input, result, _ = sample.split("-")
            assert part1(s_input) == int(result), f"Part 1 - Test Input ❌"

    def test_part1_on_game_input(self, game_input):
        LOGGER.info(f"Part 1: Game Input")
        assert part1(game_input) == 1282, f"Part 1 - Game Input ❌"


# ----- Part 2 -----


class TestPartTwo(AoCTest):
    def test_part2_on_sample_data(self, sample_input):
        LOGGER.info(f"Part 2: Test Input")
        for sample in sample_input:
            s_input, _, result = sample.split("-")
            assert part2(sample_input) == None, f"Part 2 - Test Input ❌"

    def test_part2_on_game_input(self, game_input):
        LOGGER.info(f"Part 2: Game Input")
        assert part2(game_input) == 3513, f"Part 2 - Game Input ❌"
