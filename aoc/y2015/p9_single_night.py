from collections import defaultdict
from typing import Dict, Callable

from aoc.common import input
from aoc.common import solution


def parse_input(data: input.Tokenized["\n"]) -> Dict[str, Dict[str, int]]:
    d = defaultdict(lambda: defaultdict(int))
    for line in data:
        src, _, dst, _, cost = line.split(" ")
        d[src][dst] = int(cost)
        d[dst][src] = int(cost)
    return d


def min_dist_to_cover(
    graph: Dict[str, Dict[str, int]],
    start: str,
    optimal_dist: Callable[[int, int], bool],
) -> int:
    shortest_path = None
    q = [([start], 0)]

    while q:
        curr_path, curr_cost = q.pop()
        for next, edge_cost in graph[curr_path[-1]].items():
            if next in curr_path:
                continue
            next_path = [*curr_path, next]
            next_cost = curr_cost + edge_cost
            if len(next_path) == len(graph):
                if shortest_path is None or optimal_dist(shortest_path[-1], next_cost):
                    shortest_path = (next_path, next_cost)
            q.append((next_path, next_cost))

    return shortest_path[-1]


@solution.part_one(year=2015, problem=9)
def part_one(data: input.Tokenized["\n"]) -> int:
    graph = parse_input(data)
    cmp = lambda curr_cost, next_cost: next_cost < curr_cost
    return min(min_dist_to_cover(graph, start, cmp) for start in graph)


@solution.part_two(year=2015, problem=9)
def part_two(data: input.Tokenized["\n"]) -> int:
    graph = parse_input(data)
    cmp = lambda curr_cost, next_cost: next_cost > curr_cost
    return max(min_dist_to_cover(graph, start, cmp) for start in graph)
