"""Test Module for Puzzles in Day 07: No Space Left On Device"""

import logging
from pathlib import Path
from pytest import fixture, mark

from puzzle import load, part1, part2
from puzzle import __day__, __title__

LOGGER = logging.getLogger(__name__)

EXAMPLE_DATA = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""

LOGGER.warning(f"Test AoC22 Day {__day__}: {__title__}")


class AoCTest:
    @fixture(scope="function")
    def sample_input(self) -> list[int]:
        LOGGER.info("Test Input")
        return list(map(lambda l: l.strip(), EXAMPLE_DATA.splitlines()))

    @fixture(scope="function")
    def game_input(self) -> list[int]:
        LOGGER.info("Game Input")
        return load(filepath=Path(__file__).with_name(f"input.{__day__}"))


# ------ Part 1 ------


class TestPartOne(AoCTest):
    def test_part1_on_sample_data(self, sample_input):
        LOGGER.info(f"Part 1: Test Input")
        assert part1(sample_input) == 95437, f"Part 1 - Test Input ❌"

    def test_part1_on_game_input(self, game_input):
        LOGGER.info(f"Part 1: Game Input")
        assert part1(game_input) == 1648397, f"Part 1 - Game Input ❌"


# ----- Part 2 -----


class TestPartTwo(AoCTest):
    def test_part2_on_sample_data(self, sample_input):
        LOGGER.info(f"Part 2: Test Input")
        assert part2(sample_input) == 24933642, f"Part 2 - Test Input ❌"

    def test_part2_on_game_input(self, game_input):
        LOGGER.info(f"Part 2: Game Input")
        assert part2(game_input) == 1815525, f"Part 2 - Game Input ❌"
