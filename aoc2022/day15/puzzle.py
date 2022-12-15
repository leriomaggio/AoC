""" -- Advent of Code 2022 --
Day 15, https://adventofcode.com/2022/day/15

Notes on Solutions:
After parsing the files, and loading the positions of all sensors and beacons, the intervals
of all sensors receptivity on target row (i.e. `y`) are calculated.
In particular: (A) all sensors with a positive signal strength on the target
row are considered, and (B) gathered signals are then refined to account for
any overlap receptivity range between sensors. These ranges are the common ground
on which solutions for part 1 and part 2 build upon.
- Part 1: Once we have all the (expanded) ranges of sensors' reception, all we need to do
to solve this puzzle is to count all the covered tiles, minus the ones actually occupied by beacons.
- Part 2: In part 2, all we need to do is to extend the research of coordinates for the distress signal,
considering the boundaries specified in the puzzle text (i.e. 0-4000000 for both x and y).
Therefore, for all the possible rows (i.e. values of y in the range), we could reuse calculation of
signal ranges on that row, and then look for the value of `distress_x` in those ranges.
In more details, for each row exploration, as soon as we find a value of `distress_x` which is outside
any receptive range of sensors on that row, we got our candidate and so we can return the tuning frequency.
"""

__day__ = "15"
__title__ = "Beacon Exclusion Zone"
__author__ = "leriomaggio"

from typing import Union
from pathlib import Path


def load(filepath: Union[str, Path]):
    return parse_input(open(filepath).read().split("\n"))


def parse_input(data: list[str]) -> list[tuple[int, int, int, int]]:
    positions = list()
    for line in data:
        _, sx, _, sy, _, bx, _, by = (
            line.replace("=", ",").replace(":", ",").strip().split(",")
        )
        positions.append(tuple(map(int, (sx, sy, bx, by))))
    return positions


def manhattan_distance(s: tuple[int, int], b: tuple[int, int]):
    return sum(abs(si - bi) for si, bi in zip(s, b))


def signal_intervals(positions: list[tuple[int, int, int, int]], row: int):
    ranges = sorted(
        [
            sx - signal_length,
            sx + signal_length,
        ]  # saved as lists as they'd need update afterwards
        for (sx, sy, bx, by) in positions
        if (signal_length := manhattan_distance((sx, sy), (bx, by)) - abs(sy - row)) > 0
    )
    span_intervals = [ranges[0]]
    for lx, hx in ranges[1:]:
        _, qhx = span_intervals[-1]
        if lx > qhx + 1:  # not overlapping
            span_intervals.append([lx, hx])
        else:
            span_intervals[-1][1] = max(qhx, hx)
    return span_intervals


# =========== Part 1 ============


def part1(data: list[int], y=2000000) -> int:
    ranges = signal_intervals(positions=data, row=y)
    beacons_in_row = set(bx for _, _, bx, by in data if by == y)
    covered_by = set(x for lo, hi in ranges for x in range(lo, hi + 1))
    return len(covered_by - beacons_in_row)


# =========== Part 2 ============


def part2(data: list[int], max_distress=4000000) -> int:
    for distress_y in range(max_distress + 1):
        ranges = signal_intervals(positions=data, row=distress_y)
        distress_x = 0
        for lx, hx in ranges:
            if distress_x < lx:
                return distress_x * 4000000 + distress_y
            distress_x = max(distress_x, hx + 1)
            if distress_x > max_distress:
                break


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
