from pathlib import Path

from puzzle import load, part1, part2


EXAMPLE_DATA = """199
200
208
210
200
207
240
269
260
263
"""


class TestPuzzle:

    example_data = list(map(int, EXAMPLE_DATA.splitlines()))

    def test_part1_example_data(self):
        assert part1(self.example_data) == 7, "Part 1: Example data ❌"

    def test_part2_example_data(self):
        assert part2(self.example_data) == 5, "Part 2: Example data ❌"

    def test_part1(self):
        data = load(filepath=Path(__file__).with_name("input.txt"))
        assert part1(data) == 1681

    def test_part2(self):
        data = load(filepath=Path(__file__).with_name("input.txt"))
        assert part2(data) == 1704
