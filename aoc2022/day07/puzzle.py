""" -- Advent of Code 2022 --
Day 07, https://adventofcode.com/2022/day/7

Notes on Solutions:
For this puzzle I had lots of fun abusing with the Python Data Model.

I implemented my custom (implicitly recursive) File Tree
data structure which is capable of `+=` adding new entries, as well
as being an iterable (i.e. `__iter__`) and subscriptable (i.e. `__getitem__`)
object. The `size` of each node is calculated recursively, and then stored as the
folder structure is not going to change throughout the whole game.

Also, being the `Entry` object iterable, functions like `filter` could also be
used to filter directories or nodes satisfying other conditions (as those used to
solve part 1 and part2)
"""

__day__ = "07"
__title__ = "No Space Left On Device"
__author__ = "leriomaggio"

from typing import Union
from pathlib import Path


class Entry:
    def __init__(self, label: str, fsize: int = 0):
        self._nodes = list()
        self._label = label
        self._size = fsize
        self._parent = None

    def __iadd__(self, entry: "Entry") -> None:
        entry.parent = self
        self._nodes.append(entry)
        return self

    @property
    def is_directory(self) -> bool:
        return self._label.startswith("dir")

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, p: "Entry"):
        self._parent = p

    @property
    def name(self) -> str:
        return self._label.replace("dir:", "")

    @property
    def size(self) -> int:
        if not self._size:
            self._size = sum(n.size for n in self._nodes)
        return self._size

    def __iter__(self):
        for subtree in self._nodes:
            for n in subtree:
                yield n
        yield self

    def __getitem__(self, label):
        for n in self._nodes:
            if n.name == label:
                return n
        return None


def load(filepath: Union[str, Path]):
    return list(map(lambda l: l.strip(), open(filepath).read().split("\n")))


def parse(history_log: list[str]) -> Entry:
    root = Entry(label="/")
    curdir = root
    for line in history_log[1:]:
        if line.startswith("$ ls"):
            continue
        if line.startswith("$ cd"):
            _, _, label = line.split()
            if label == "..":
                curdir = curdir.parent
            else:
                curdir = curdir[label]
            continue
        if line.startswith("dir"):
            _, label = line.split()
            curdir += Entry(label=f"dir:{label}")
        else:
            fsize, label = line.split()
            curdir += Entry(label=label, fsize=int(fsize))
    return root


# =========== Part 1 ============


def part1(data: list[str]) -> int:
    root_dir = parse(data)
    return sum(
        entry.size for entry in root_dir if entry.is_directory and entry.size <= 100000
    )


# =========== Part 2 ============

TOTAL_DISK_SPACE = 70000000
MIN_REQUIRED = 30000000


def part2(data: list[str]) -> int:
    root_dir = parse(data)
    to_free = MIN_REQUIRED - (TOTAL_DISK_SPACE - root_dir.size)
    return min(
        n.size for n in filter(lambda n: n.is_directory and n.size >= to_free, root_dir)
    )


if __name__ == "__main__":
    print("=*=*=*=*=*=*=*=*=*= Advent of Code 2022 =*=*=*=*=*=*=*=*=*=")
    print(f"Day {__day__}: {__title__}")
    print("-" * 59)
    filepath = Path(__file__).with_name(f"input.{__day__}")
    data = load(filepath=filepath)
    # solve part 1
    print(part1(data))
    # solve part 2
    print(part2(data))
