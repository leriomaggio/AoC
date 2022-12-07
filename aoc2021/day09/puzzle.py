""" -- Advent of Code 2021 --
Day 09, https://adventofcode.com/2021/day/9

Notes on Solutions:
- Part 1: I had lots of fun in implementing the two parts of this challenge in a _functional_
          fashion, both for Part 1 and 2. For this reason, the area of basins is implemented 
          as a dictionary of coordinates: *not* the most efficient data abstraction possible
          (being the area a dense matrix, and not a sparse one), but preferrable IMO over the
          list of lists for readability (esp. in functional iterations).

          Crucial to this part (and the next) is the `neighbourood` function. This 
          function generates the `n, s, w, e` pair of coordinates for an input `coord`
          making sure that resulting coordinates are within the `shape` of the area 
          (i.e. `borders`). This is done by using `le` and `lt` functions from the
          [`operator`](https://docs.python.org/3/library/operator.html#module-operator)
          module, in combination with 
          [`starmap`](https://docs.python.org/3/library/itertools.html#itertools.starmap) 
          which applies those operators on each pair of elements.

          The `low_point_filter` function is predefined with `functools.partial`, pre-set
          on `area` so that only coordinates could be passed in during the `filter` calls.

- Part 2: This part is way more interesting (and more challenging). The idea is to implement
          a BFS (Breadth-First Search) traversal over basins' area, interpreted as a graph.
          The [`collections.deque`](https://docs.python.org/3/library/collections.html#collections.deque) (double-ended queue) is used to implement the FIFO queue required in BFS.
          Interestingly, the search frontier is updated considering the neighbourhood of 
          the current coordinates, filtered by BFS visit and height values of `9`.
"""

__day__ = "09"
__title__ = "Smoke Basin"
__author__ = "leriomaggio"

from pathlib import Path
from itertools import starmap
from operator import le, lt, and_
from functools import partial

# -- part 2
from collections import deque
from functools import reduce
from operator import mul


def load(lines: list[str]) -> dict[tuple[int, int], int]:
    # Caveat: Basins' Area is represented as a dictionary of
    # coordinates. Not the most efficient data abstraction
    # but easier to deal with in a functional way.
    return {
        (r, c): height
        for r, line in enumerate(lines)
        for c, height in enumerate(map(int, line))
    }


# =========== Part 1 ============


def neighbourhood(coord, borders):
    n, s, w, e = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 883
    return filter(
        lambda l: and_(*starmap(le, zip((0, 0), l)))
        and and_(*starmap(lt, zip(l, borders))),
        map(lambda d: tuple(map(sum, zip(coord, d))), (n, s, w, e)),
    )


def shape(area: dict[tuple[int], int]) -> tuple[int]:
    return (max(l + 1 for l, _ in area), max(r + 1 for _, r in area))


def is_low_point(coord, area, shape):
    return all(
        map(
            lambda v: v > area[coord],
            map(lambda l: area[l], neighbourhood(coord, shape)),
        )
    )


def part1(area: dict[tuple[int, int], int]) -> int:
    shape_ = shape(area)
    low_point_filter = partial(is_low_point, area=area, shape=shape_)
    return sum(area[c] + 1 for c in filter(lambda c: low_point_filter(coord=c), area))


# =========== Part 2 ============


def part2(area: dict[tuple[int, int], int]) -> int:
    shape_ = shape(area)
    marked = set()  # set of tuples, i.e. coordinates
    basin_filter = lambda l: l not in marked and area[l] != 9

    def traverse_basin(r, c):
        basin, nodes = list(), deque([(r, c)])
        while nodes:
            if (coord := nodes.popleft()) in marked:
                continue
            marked.add(coord)
            basin.append(coord)
            nodes += filter(basin_filter, neighbourhood(coord, shape_))
        return basin

    basins = [traverse_basin(r, c) for r, c in filter(basin_filter, area)]
    return reduce(mul, sorted(map(len, basins), reverse=True)[:3])


if __name__ == "__main__":
    print("=*=*=*=*=*=*=*=*=*= Advent of Code 2021 =*=*=*=*=*=*=*=*=*=")
    print(f"Day {__day__}: {__title__}")
    print("-" * 59)
    filepath = Path(__file__).with_name(f"input.{__day__}")
    area = load(open(filepath).read().strip().splitlines())
    # solve part 1
    print(part1(area))
    # solve part 2
    print(part2(area))
