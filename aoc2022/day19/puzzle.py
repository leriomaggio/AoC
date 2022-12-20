""" -- Advent of Code 2022 --
Day 19, https://adventofcode.com/2022/day/19

"""

__day__ = "19"
__title__ = "Not Enough Minerals"
__author__ = "leriomaggio"

from typing import Union
from pathlib import Path
from functools import cached_property, cache
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Robot:
    mineral_id: int
    ore: int
    clay: int = 0
    obsidian: int = 0
    geode: int = 0

    @property
    def production_specs(self):
        for mineral_id, quantity in enumerate(
            (self.ore, self.clay, self.obsidian, self.geode)
        ):
            if quantity == 0:
                continue  # skip
            yield (mineral_id, quantity)


ORE_BOT = 0
CLAY_BOT = 1
OBSIDIAN_BOT = 2
GEODE_BOT = 3


class Blueprint:
    def __init__(self, bid: int, specs: list[int]) -> None:
        self._id = bid
        ore, clay_ore, obs_ore, obs_clay, goede_ore, geode_obs = specs
        self._robo_specs: tuple[Robot] = (
            Robot(mineral_id=ORE_BOT, ore=ore),
            Robot(mineral_id=CLAY_BOT, ore=clay_ore),
            Robot(mineral_id=OBSIDIAN_BOT, ore=obs_ore, clay=obs_clay),
            Robot(mineral_id=GEODE_BOT, ore=goede_ore, obsidian=geode_obs),
        )
        self.max_resources_required = [
            max(getattr(r, resource) for r in self._robo_specs)
            for resource in ("ore", "clay", "obsidian", "geode")
        ]
        self._production_cache = dict()

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        robots = "\n".join([str(r) for r in self._robo_specs])
        return f"Blueprint {self._id}: {robots}"

    def __hash__(self) -> int:
        return self._id

    def _mine(self, time, robots: tuple[Robot], inventory: tuple[int]):
        cache_key = tuple([time, *robots, *inventory])
        n_geodes = self._production_cache.get(cache_key, None)
        if n_geodes is not None:
            return n_geodes
        n_geodes = inventory[GEODE_BOT] + robots[GEODE_BOT] * time
        for robot in self._robo_specs:
            if (
                robot.mineral_id != GEODE_BOT
                and robots[robot.mineral_id]
                >= self.max_resources_required[robot.mineral_id]
            ):
                continue  # no need to produce more of this type!

            prod_elapsed_time = 0
            for mineral_id, quantity in robot.production_specs:
                if robots[mineral_id] == 0:
                    break  # we can't produce this material-producing robot
                prod_elapsed_time = max(
                    prod_elapsed_time,
                    -(-(quantity - inventory[mineral_id]) // robots[mineral_id]),
                )  # production time is either instant (we have everything we need )
            else:
                remaining_time = time - prod_elapsed_time - 1
                if remaining_time <= 0:
                    continue
                updated_robots = list(robots[:])
                updated_inventory = [
                    q_inv + (n_bots * (prod_elapsed_time + 1))
                    for q_inv, n_bots in zip(inventory, robots)
                ]
                for mineral_id, quantity in robot.production_specs:
                    updated_inventory[mineral_id] -= quantity

                updated_robots[robot.mineral_id] += 1
                for mineral_id in (ORE_BOT, CLAY_BOT, OBSIDIAN_BOT):
                    updated_inventory[mineral_id] = min(
                        updated_inventory[mineral_id],
                        self.max_resources_required[mineral_id] * remaining_time,
                    )
                n_geodes = max(
                    n_geodes,
                    self._mine(
                        remaining_time, tuple(updated_robots), tuple(updated_inventory)
                    ),
                )
        self._production_cache[cache_key] = n_geodes
        return n_geodes

    def quality_level(self, minutes: int) -> int:
        robots, inventory = (1, 0, 0, 0), (0, 0, 0, 0)
        self._production_cache = {}
        return self.bid * self._mine(minutes, robots, inventory)

    def produced_geodes(self, minutes: int):
        robots, inventory = (1, 0, 0, 0), (0, 0, 0, 0)
        self._production_cache = {}
        return self._mine(minutes, robots, inventory)

    @property
    def bid(self) -> int:
        return self._id


def load(filepath: Union[str, Path]):
    return parse_input(open(filepath).read().split("\n"))


def parse_input(data: list[str]) -> list[Blueprint]:
    blueprints = list()
    for line in data:
        bid, *specs = tuple(map(int, re.findall(r"\d+", line.strip())))
        blueprints.append(Blueprint(bid=int(bid), specs=specs))
    return blueprints


def dfs(bp, maxspend, cache, time, bots, amt):
    if time == 0:
        return amt[3]

    key = tuple([time, *bots, *amt])
    if key in cache:
        return cache[key]

    maxval = amt[3] + bots[3] * time

    for btype, recipe in enumerate(bp):
        if btype != 3 and bots[btype] >= maxspend[btype]:
            continue

        wait = 0
        for ramt, mineral_id in recipe:
            if bots[mineral_id] == 0:
                break
            wait = max(wait, -(-(ramt - amt[mineral_id]) // bots[mineral_id]))
        else:
            remtime = time - wait - 1
            if remtime <= 0:
                continue
            bots_ = bots[:]
            amt_ = [x + y * (wait + 1) for x, y in zip(amt, bots)]
            for ramt, mineral_id in recipe:
                amt_[mineral_id] -= ramt
            bots_[btype] += 1
            for i in range(3):
                amt_[i] = min(amt_[i], maxspend[i] * remtime)
            maxval = max(maxval, dfs(bp, maxspend, cache, remtime, bots_, amt_))

    cache[key] = maxval
    return maxval


# =========== Part 1 ============


def part1(data: list[Blueprint]) -> int:
    return sum(blueprint.quality_level(minutes=24) for blueprint in data)


# =========== Part 2 ============

from math import prod


def part2(data: list[Blueprint]) -> int:
    return prod(blueprint.produced_geodes(minutes=32) for blueprint in data[:3])


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
