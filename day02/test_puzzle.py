from pathlib import Path
from puzzle import part1, part2, load

EXAMPLE_DATA = """
forward 5
down 5
forward 8
up 3
down 8
forward 2
"""


class TestPuzzle:
    @staticmethod
    def load_example_data():
        return list(map(lambda l: tuple(l.split()), EXAMPLE_DATA.strip().splitlines()))

    example_data = load_example_data()

    def test_part1_example_data(self):
        assert part1(self.example_data) == 150, "Part 1: Example data ❌"

    def test_part2_example_data(self):
        assert part2(self.example_data) == 900, "Part 2: Example data ❌"

    def test_part1(self):
        data = load(filepath=Path(__file__).with_name("input.txt"))
        assert part1(data) == 1524750

    def test_part2(self):
        data = load(filepath=Path(__file__).with_name("input.txt"))
        assert part2(data) == 1592426537
