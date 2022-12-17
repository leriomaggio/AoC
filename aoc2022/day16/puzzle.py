""" -- Advent of Code 2022 --
Day 16, https://adventofcode.com/2022/day/16

Notes on Solutions:
- Part 1: 
- Part 2: 
"""

__day__ = "16"
__title__ = "Proboscidea Volcanium"
__author__ = "leriomaggio"

from typing import Union
from pathlib import Path
from functools import cache
from math import inf
from collections import defaultdict
from functools import cache


class Graph:
    def __init__(self) -> None:
        self.valves = {}
        self.dist = defaultdict(lambda: defaultdict(lambda: inf))
        self._key = None

    def __iadd__(self, node: tuple[str, int, list[str]]):
        u, flow_rate, tunnels = node
        self.valves[u] = int(flow_rate)
        self.dist[u][u] = 0
        for v in tunnels:
            self.dist[u][v] = 1
        return self

    def __hash__(self) -> int:
        if not self._key:
            self._key = hash("".join(list(self.valves.keys())))
        return self._key

    def percolate_distances(self):
        for u in self.valves:
            for v in self.valves:
                for z in self.valves:
                    self.dist[v][z] = min(
                        self.dist[v][z], self.dist[v][u] + self.dist[u][z]
                    )

    @property
    def valves_to_open(self) -> frozenset:
        return frozenset(x for x in self.valves if self.valves[x] > 0)


def load(filepath: Union[str, Path]):
    return parse_input(open(filepath).read().split("\n"))


def parse_input(data: list[str]) -> Graph:
    graph = Graph()
    for line in data:
        line = line.replace(";", "").replace(",", "").replace("=", " ").split()
        _, u, _, _, _, rate, _, _, _, _, *tunnels = line
        graph += (u, rate, tunnels)
    graph.percolate_distances()
    return graph


@cache
def max_flow(
    g: Graph, u: str, t: int, valves_to_open: frozenset[str], with_elephant: bool
) -> int:
    pressure = max_flow(g, "AA", 26, valves_to_open, False) if with_elephant else 0
    for v in valves_to_open:
        if (tick := t - g.dist[u][v] - 1) >= 0:
            pressure = max(
                pressure,
                g.valves[v] * tick
                + max_flow(g, v, tick, valves_to_open - {v}, with_elephant),
            )
    return pressure


# =========== Part 1 ============


def part1(graph: Graph) -> int:
    return max_flow(graph, "AA", 30, graph.valves_to_open, False)


# =========== Part 2 ============


def part2(graph: Graph) -> int:
    return max_flow(graph, "AA", 26, graph.valves_to_open, True)


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
