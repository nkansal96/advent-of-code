import collections
import re

from typing import *

from aoc.common import input
from aoc.common import solution


dirs = {"e": (2, 0), "w": (-2, 0), "ne": (1, 2), "nw": (-1, 2), "se": (1, -2), "sw": (-1, -2)}


def create_hex_grid(data: input.Tokenized) -> Set[Tuple[int, int]]:
    paths = data.each_token_as(lambda l: re.findall(r"e|w|nw|ne|sw|se", l))
    active_tiles = set()

    for path in paths:
        x, y = 0, 0
        for step in path:
            dx, dy = dirs[step]
            x, y = x + dx, y + dy
        active_tiles ^= {(x, y)}

    return active_tiles


def next_active_tiles(coords: Set[Tuple]) -> Set[Tuple]:
    inactive_neighbors = collections.defaultdict(set)
    active_neighbors = collections.defaultdict(set)

    for coord in coords:
        for delta in dirs.values():
            next_coord = tuple(map(sum, zip(coord, delta)))

            # coord is active and next_coord is inactive
            if next_coord not in coords:
                inactive_neighbors[next_coord].add(coord)

            # coord is active and next_coord is active
            if next_coord in coords:
                active_neighbors[coord].add(next_coord)

    next_coords = set()
    for coord, n in inactive_neighbors.items():
        if len(n) == 2:
            next_coords.add(coord)

    for coord in coords:
        if 1 <= len(active_neighbors[coord]) <= 2:
            next_coords.add(coord)

    return next_coords


@solution.part_one(year=2020, problem=24)
def _(data: input.Tokenized[input.NL]) -> int:
    return len(create_hex_grid(data))


@solution.part_two(year=2020, problem=24)
def _(data: input.Tokenized[input.NL]) -> int:
    active_tiles = create_hex_grid(data)
    for _ in range(100):
        active_tiles = next_active_tiles(active_tiles)
    return len(active_tiles)
