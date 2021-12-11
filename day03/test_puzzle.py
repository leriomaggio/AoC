from pathlib import Path
from puzzle import part1, part2, load

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


class TestPuzzle:
    @staticmethod
    def load_example_data():
        return EXAMPLE_DATA.splitlines()

    example_data = load_example_data()

    def test_part1_example_data(self):
        assert part1(self.example_data) == 198, "Part 1: Example data ❌"

    def test_part2_example_data(self):
        assert part2(self.example_data) == 230, "Part 2: Example data ❌"

    def test_part1(self):
        data = load(filepath=Path(__file__).with_name("input.txt"))
        assert part1(data) == 3374136

    def test_part2(self):
        data = load(filepath=Path(__file__).with_name("input.txt"))
        # Test all sequence of bits have the same length!
        assert len(set(map(len, data))) == 1

        assert part2(data) == 4432698
