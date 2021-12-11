# -- Advent of Code 2021 --
# Day 04: Giant Squid
# https://adventofcode.com/2021/day/4

from pathlib import Path
from dataclasses import dataclass


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

    if len(board_numbers):
        boards.append(Board(board_id=len(boards), numbers=board_numbers))

    return numbers, boards


# =========== Part 1 ============


def part1(numbers: list[int], boards: list[Board]) -> int:
    bingo = Bingo(numbers=numbers, boards=boards)
    return bingo.play()


# =========== Part 2 ============


class ResilientBingo(Bingo):
    def play(self) -> int:
        boards_winning = list()
        for number in self.numbers:
            for board in filter(
                lambda b: b.board_id
                not in set(map(lambda p: p[0].board_id, boards_winning)),
                self.boards,
            ):
                board.mark(number)
                if board.bingo():
                    boards_winning.append((board, number))
        board, number = boards_winning.pop()
        return board.score(number)


def part2(numbers: list[int], boards: list[Board]) -> int:
    bingo = ResilientBingo(numbers, boards)
    return bingo.play()


if __name__ == "__main__":
    print("=*=*=*=*=*=*=*=*=*= Advent of Code 2021 =*=*=*=*=*=*=*=*=*=")
    print("Day 04: Giant Squid")
    print("-" * 59)
    filepath = Path(__file__).with_name("input.txt")
    numbers, boards = load(lines=open(filepath).read().strip().splitlines())
    # solve part 1
    print(part1(numbers, boards))
    # solve part 2
    print(part2(numbers, boards))
