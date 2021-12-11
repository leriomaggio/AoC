""" -- Advent of Code 2021 --
Day 04, https://adventofcode.com/2021/day/4

Notes on Solutions:
- Part 1: The core implementation of the solution here lies in the `Board` class, which represents a board of number
          as a dictionary of pairs (i.e. coordinates). This is a generally convenient representation for a Matrix in
          pure Python (that is, not using the magics of [NumPy](http://numpy.org)).
          This is particularly convenient whenever solutions using `filter` and `lambda` are used, so that we don't
          require to parse coordinates for rows and cols.
- Part 2: This part was pretty straightforward to implement, as the only thing we had to change was the play rule/criterion.
          In particular, we have to keep on playing until the last `Board` marks its **bingo** (this will ultimately always
          happen as all the numbers are drawn from the pool!). This has been implemented using class _inheritance_.
          The only thing worthwhile mentioning here though is that new playing rules are implemented using an
          `OrderedDict` to keep track of the winning boards. This won't be _really_ necessary in Python 3.7+ since
          dictionaries now keep track of the insertion order by default (and we're using **Python 3.10!**),
          but I guess it is always a good practice making implementations as general as possible!
"""

__day__ = "04"
__title__ = "Giant Squid"
__author__ = "leriomaggio"


from pathlib import Path
from dataclasses import dataclass
from collections import OrderedDict


def load(lines: list[str]):
    numbers, boards, board_numbers = [], [], []
    for i, line in enumerate(lines):
        if i == 0:
            numbers = list(map(int, line.split(",")))
            continue
        if not line:  # empty line
            if len(board_numbers):
                boards.append(Board(board_id=len(boards), numbers=board_numbers))
                board_numbers = []
            continue
        board_numbers.append(list(map(int, line.split())))

    if board_numbers:
        boards.append(Board(board_id=len(boards), numbers=board_numbers))

    return numbers, boards


# =========== Part 1 ============


class Board:
    def __init__(self, board_id: int, numbers: list[list[int]]):
        self.board_id = board_id
        self.board = {
            (i, j): v for i, row in enumerate(numbers) for j, v in enumerate(row)
        }
        self.board_state = {k: 0 for k in self.board}
        self.nrows, self.ncols = self.shape(self.board)

    @staticmethod
    def shape(board: dict[tuple[int], int]) -> tuple[int]:
        return (max(l + 1 for l, _ in board), max(r + 1 for _, r in board))

    def mark(self, number: int):
        for coord in filter(lambda c: self.board[c] == number, self.board):
            self.board_state[coord] = 1

    def bingo(self):
        return any(
            map(
                lambda row: all(
                    map(
                        lambda c: self.board_state[c] == 1,
                        filter(lambda coord: coord[0] == row, self.board_state),
                    )
                ),
                range(self.nrows),
            )
        ) or any(
            map(
                lambda col: all(
                    map(
                        lambda c: self.board_state[c] == 1,
                        filter(lambda coord: coord[1] == col, self.board_state),
                    )
                ),
                range(self.ncols),
            )
        )

    def score(self, winning_number: int) -> int:

        return (
            sum(
                map(
                    self.board.get,
                    filter(lambda c: self.board_state[c] == 0, self.board_state),
                )
            )
            * winning_number
        )

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"Board{self.board_id}: \n {self.board}"


@dataclass
class Bingo:
    numbers: list[int]
    boards: list[Board]

    def play(self) -> int:
        for number in self.numbers:
            for board in self.boards:
                board.mark(number)
                if board.bingo():
                    return board.score(number)
        return 0


def part1(numbers: list[int], boards: list[Board]) -> int:
    bingo = Bingo(numbers=numbers, boards=boards)
    return bingo.play()


# =========== Part 2 ============


class ResilientBingo(Bingo):
    def play(self) -> int:
        boards_winning = OrderedDict()
        for number in self.numbers:
            for board in filter(
                lambda b: b.board_id not in boards_winning,
                self.boards,
            ):
                board.mark(number)
                if board.bingo():
                    boards_winning[board.board_id] = (board, number)
        board, number = list(
            boards_winning.values()
        ).pop()  # we're sure thanks to OrderedDict
        return board.score(number)


def part2(numbers: list[int], boards: list[Board]) -> int:
    bingo = ResilientBingo(numbers, boards)
    return bingo.play()


if __name__ == "__main__":
    print("=*=*=*=*=*=*=*=*=*= Advent of Code 2021 =*=*=*=*=*=*=*=*=*=")
    print(f"Day {__day__}: {__title__}")
    print("-" * 59)
    filepath = Path(__file__).with_name(f"input.{__day__}")
    numbers, boards = load(lines=open(filepath).read().strip().splitlines())
    # solve part 1
    print(part1(numbers, boards))
    # solve part 2
    print(part2(numbers, boards))
