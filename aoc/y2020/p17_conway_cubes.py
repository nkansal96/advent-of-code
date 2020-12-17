import collections
import functools
import itertools

from typing import Set, Tuple

from aoc.common import input
from aoc.common import solution


def next_active_coords(coords: Set[Tuple], dim: int):
    neighbors = collections.defaultdict(int)

    for coord in coords:
        for delta in itertools.product(*[range(-1, 2)] * dim):
            if all(d == 0 for d in delta):
                continue
            next_coord = tuple(map(sum, zip(coord, delta)))
            neighbors[next_coord] += 1

    next_coords = set()
    for coord, count in neighbors.items():
        if coord in coords and (count == 2 or count == 3):
            next_coords.add(coord)
        if coord not in coords and count == 3:
            next_coords.add(coord)

    return next_coords


def get_active_coords(data: input.Tokenized, dim: int):
    grid = list(data)
    return {
        (*(0 for _ in range(dim - 2)), y, x)
        for y in range(len(grid))
        for x in range(len(grid[y]))
        if grid[y][x] == "#"
    }


@solution.part_one(year=2020, problem=17)
def _(data: input.Tokenized[input.NL]) -> int:
    start = get_active_coords(data, 3)
    return len(functools.reduce(lambda c, _: next_active_coords(c, 3), range(6), start))


@solution.part_two(year=2020, problem=17)
def _(data: input.Tokenized[input.NL]) -> int:
    start = get_active_coords(data, 4)
    return len(functools.reduce(lambda c, _: next_active_coords(c, 4), range(6), start))
