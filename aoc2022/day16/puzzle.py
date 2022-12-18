""" -- Advent of Code 2022 --
Day 16, https://adventofcode.com/2022/day/16

Notes on Solutions:
This puzzle considers a maximum flow optimisation problem over a
graph of interconnected valves.
In particular, the solution to both puzzles considers a limited
number of steps (i.e. minutes) to go from an input source node
(i.e. "AA") so that the maximum flow (i.e. pressure) could be
obtained.

We will start therefore by processing the input, and storing
all the "graph" infos within a custom `Graph` class.
This class will be crucial for the `max_flow` [cached!] recursive
function. Thanks to the fantastic "Python Data Model", we can create
a custom `Graph` type which is `__hashable__` and therefore cache-able
using the built-in `functools.cache` (conversely, plain dictionaries
would be not!!)

Crucial in this graph representation is the caculation of all distances
within each valves (see `Graph.percolate_distances`) which
leverages on the same rule|trick used in the Djikstra Shortest_parth
algorithm, namely: the distance between each node is inductively 
calculated as the minimum between the distance following the direct edge
(u,v) and the length of the path with one op, i.e. d(u,k) + d(k,v)

That being said, part 1 and part 2 are essentially identical except
for one parameter (i.e. considering elephant or not), which
essentially changes the base-case in the recursion.

With no-elephant (part 1), we start with 30 mins and no-pressure.
With elephant (part 2). we start at 26 mins, and the starting pressure
is part1 at 26 mins (i.e. with no elephant).

We will keep a `frozenset` (crucial for caching as immutable) of
all the valves remained to open recursively (starting from all of those
having any positive pressure rate).
Then we will recursively explore any tunnel that is reachable within the
time constraints, retaining the pressure as the maximum
between the current_value, current_value + opening the valve, or
following the _next_ tunnel.
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
