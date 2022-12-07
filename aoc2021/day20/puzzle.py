""" -- Advent of Code 2021 --
Day 20, https://adventofcode.com/2021/day/20

Notes on Solutions:
- Solutions to Part 1 and Part 2 are essentially the same (only the value of the parameter `times` in 
  the `enhance` function is different). Key to the solution are the `kernel_function` and the `enhance`
  in combination with the input algorithm. The former is very similar to the functions to calculate 
  the neighbourhood (see `Day09` or `Day11`, for example). However situation here is simpler as the
  image area is supposed to be infinite, and therefore there is no actual limit on the ranges.
  Secondly, key to the solution is understanding what happens at the (infinite) border, considering the 
  input algorithm. In my case, `algorithm` starts with `#` (i.e. `1`) and terminates on `511` with `.`.
  This means that (on odd-steps) all zeros become ones wich then turn back to zero in the next round!
  The rest of the solution is just padding the image at each step, and considering the padded image to 
  apply the `kernel` function.
"""

__day__ = "20"
__title__ = "Trench Map"
__author__ = "leriomaggio"

from typing import Union
from pathlib import Path
from itertools import product


def load(lines: str) -> Union[str, dict[tuple[int, int], bool]]:
    algo, img_data = lines.strip("\n").split("\n\n")
    img_array = {
        (r, c): (e == "#")
        for r, line in enumerate(img_data.splitlines())
        for c, e in enumerate(line.strip())
    }
    return algo, img_array


# =========== Part 1 ============


def kernel(img_array: dict[tuple[int, int], bool], r: int, c: int, border="0"):
    filter = ""
    for x, y in product((-1, 0, 1), repeat=2):
        filter += str(int(img_array.get((r + x, c + y), border)))
    return filter


def pad(img_array: dict[tuple[int, int], bool]) -> set[tuple[int, int]]:
    return {
        (r + x, c + y) for r, c in img_array for x, y in product((-1, 0, 1), repeat=2)
    }


def enanche(img_array: dict[tuple[int, int], bool], algo: str, times: int = 2):
    enhanced_img = None
    border = "0"
    for t in range(times):
        enhanced_img = {}
        padded_img = pad(img_array)
        for r, c in padded_img:
            mask = kernel(img_array, r, c, border=border)
            enhanced_img[(r, c)] = int(algo[int(mask, base=2)] == "#")
        img_array = enhanced_img
        if algo[0] == "#":
            border = "1" if (t % 2 == 0) else str(int(algo[511] == "#"))
    return enhanced_img


def part1(img_array: dict[tuple[int, int], bool], algo: str) -> int:
    enhanced_img = enanche(img_array, algo, times=2)
    return sum(enhanced_img.values())


# =========== Part 2 ============


def part2(img_array: dict[tuple[int, int], bool], algo: str) -> int:
    enhanced_img = enanche(img_array, algo, times=50)
    return sum(enhanced_img.values())


if __name__ == "__main__":
    print("=*=*=*=*=*=*=*=*=*= Advent of Code 2021 =*=*=*=*=*=*=*=*=*=")
    print(f"Day {__day__}: {__title__}")
    print("-" * 59)
    filepath = Path(__file__).with_name(f"input.{__day__}")
    algo, img = load(lines=open(filepath).read().strip())
    # solve part 1
    print(part1(img_array=img, algo=algo))
    # solve part 2
    print(part2(img_array=img, algo=algo))
