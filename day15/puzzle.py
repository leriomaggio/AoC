""" -- Advent of Code 2021 --
Day 15, https://adventofcode.com/2021/day/15

Notes on Solutions:
- Part 1: Solution to part 1 is pretty straightforward as we are asked to calculate the shortest
          path of a DAG (Directed Acyclic Graph), which can be determined in linear time wrt. to 
          the size of the Graph. Indeed this is a slightly simplified version as the graph is not
          dense, and connections only go in two possible directions (considering the input maze).
          As for the proposed solution, the shortest path is calculated using a recursive 
          algorithm **with memoization** 
          (using [`functools.cache`](https://docs.python.org/3/library/functools.html?#functools.cache)
          A do personally find the recursive solution very elegant, as it's shorter, easier to read, 
          and does not require using the topological sort (**thanks to memoization**) which would be 
          required by the iterative version. 
          Another fun part in this solution, is the `Graph` abstraction which leverages on the 
          Python Data Model to implement a more Python graph structure

- Part 2: Solution to Part 2 is more general, as it in fact implements a unique solution to part 1 too.
          This time, the [Dijkstra Algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm) 
          for shortest paths is used, generalised to a DAG `n`-times bigger (default `5 times`).
          The Dijkstra algorithm adopts a priority queue 
          ([`heapq`](https://docs.python.org/3/library/heapq.html#heapq.heappop))
          to implement the visit frontier at each step, along with a set (i.e. `S`) of visited nodes
          to bound the computation.
          A `DAG` graph class is used (subclassing `Graph` of Part 1) which includes the general 
          tiling for _all_ `chitons`, and the calculation of the `neighbourhood` for a pair of
          coordinates in the four cardinal directions (i.e. `N, S, W, E`).
          Interestingly, the `neighbourhood` function is the **same** already used on `day09` which 
          was also _specialised_ on `day11`.
          Please see _Day09 TOP NOTES_ for further details on the _quite convoluted_ implementation 
          of that `neighbourhood` function (in an eccessive functional take! :D)
"""

__day__ = "15"
__title__ = "Chiton"
__author__ = "leriomaggio"


from pathlib import Path
from functools import cache
from operator import sub
from itertools import chain
from collections import defaultdict

# part 2
from operator import and_, le, lt
from itertools import starmap
from heapq import heappop, heappush


def load(lines: list[str]) -> list[list[int]]:
    return [list(map(int, l)) for l in lines]


# =========== Part 1 ============


class Graph:
    def __init__(self, nodes: list[list[int]]) -> None:
        self.nodes = tuple(tuple(r) for r in nodes)
        self._code = None

    @property
    def shape(self) -> tuple[int, int]:
        return len(self.nodes), len(self.nodes[0])

    @property
    def limits(self) -> tuple[int, int]:
        return tuple(map(lambda p: sub(*p), zip(self.shape, (1, 1))))

    def __getitem__(self, index: tuple[int, int]) -> int:
        r, c = index
        return self.nodes[r][c]

    def __contains__(self, index: tuple[int, int]) -> bool:
        (r, c), (R, C) = index, self.shape
        return 0 <= r < R and 0 <= c < C

    def __hash__(self) -> int:  # necessary for cache
        if not self._code:
            self._code = sum(map(hash, chain.from_iterable(self.nodes)))
        return self._code


inf = float("inf")


@cache
def dist(G: Graph, r: int, c: int):
    if (r, c) not in G:
        return inf
    if (r, c) == G.limits:
        return G[(r, c)]
    return G[(r, c)] + min(dist(G, r + 1, c), dist(G, r, c + 1))


def part1(nodes: list[list[int]], s: tuple[int, int] = (0, 0)):
    graph = Graph(nodes)
    return dist(graph, *s) - graph[s]


# =========== Part 2 ============


class DAG(Graph):
    def __init__(self, nodes, size: int = 1):
        super(DAG, self).__init__(nodes=nodes)
        self.tiles = size
        R, C = self.shape

        self.chitons = [
            [
                (self.nodes[r % R][c % C] + (r // R) + (c // C) - 1) % 9 + 1
                for c in range(self.tiles * C)
            ]
            for r in range(self.tiles * R)
        ]

    def neighbours(self, r, c):
        n, s, w, e = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        borders = tuple(map(lambda s: s * self.tiles, self.shape))
        neighbours = filter(
            lambda l: and_(*starmap(le, zip((0, 0), l)))
            and and_(*starmap(lt, zip(l, borders))),
            map(lambda n: tuple(map(sum, zip((r, c), n))), (n, s, w, e)),
        )
        for rr, cc in neighbours:
            yield rr, cc


def dijkstra(G: DAG, s: tuple[int, int]):
    R, C = tuple(map(lambda s: s * G.tiles, G.shape))
    D, Q, S = [[inf for _ in range(C)] for _ in range(R)], [(0, *s)], set()
    while Q:
        d, r, c = heappop(Q)
        if (r, c) in S:
            continue
        S.add((r, c))
        if (rc_cost := d + G.chitons[r][c]) < D[r][c]:
            D[r][c] = rc_cost
            if (r, c) == (R - 1, C - 1):
                return D[r][c] - D[0][0]
        else:
            continue
        for rr, cc in G.neighbours(r, c):
            heappush(Q, (D[r][c], rr, cc))


def part2(nodes: list[list[int]], s: tuple[int, int] = (0, 0), size: int = 5) -> int:
    dag = DAG(nodes, size=size)
    return dijkstra(dag, s)


if __name__ == "__main__":
    print("=*=*=*=*=*=*=*=*=*= Advent of Code 2021 =*=*=*=*=*=*=*=*=*=")
    print(f"Day {__day__}: {__title__}")
    print("-" * 59)
    filepath = Path(__file__).with_name(f"input.{__day__}")
    nodes = load(lines=open(filepath).read().strip().splitlines())
    # solve part 1
    print(part1(nodes=nodes, s=(0, 0)))
    # solve part 2
    print(part2(nodes=nodes, s=(0, 0), size=5))
