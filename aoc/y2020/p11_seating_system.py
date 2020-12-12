import itertools

from typing import *

from aoc.common import input
from aoc.common import solution


Grid = List[List[str]]
AdjFn = Callable[[Grid, int, int], int]


def in_grid(grid: Grid, y: int, x: int) -> bool:
    return 0 <= y < len(grid) and 0 <= x < len(grid[y])


def next_grid(grid: Grid, get_adj: AdjFn, threshold: int) -> Tuple[Grid, bool]:
    orig_grid = list(map(list, grid))
    changed = False

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            count = get_adj(orig_grid, y, x)
            if grid[y][x] == "L" and count == 0:
                grid[y][x] = "#"
                changed = True
            elif grid[y][x] == "#" and count >= threshold:
                grid[y][x] = "L"
                changed = True

    return grid, changed


def simulate_and_count(grid: Grid, get_adj: AdjFn, threshold: int) -> int:
    changed = True
    while changed:
        grid, changed = next_grid(grid, get_adj, threshold)

    return sum(grid[y][x] == "#" for y in range(len(grid)) for x in range(len(grid[y])))


@solution.part_one(year=2020, problem=11)
def _(data: input.Tokenized[input.NL]) -> int:
    def get_adj_count(grid: Grid, y: int, x: int) -> int:
        return sum(
            grid[j][i] == "#"
            for j in [y - 1, y, y + 1]
            for i in [x - 1, x, x + 1]
            if (i != x or j != y) and in_grid(grid, j, i)
        )

    return simulate_and_count(list(data.each_token_as(list)), get_adj_count, 4)


@solution.part_two(year=2020, problem=11)
def _(data: input.Tokenized[input.NL]) -> int:
    def get_adj_count(grid: Grid, y: int, x: int) -> int:
        count = 0
        dds = itertools.product(range(-1, 2), range(-1, 2))
        for (dy, dx) in dds:
            if dy == 0 and dx == 0:
                continue
            yy = y + dy
            xx = x + dx
            while in_grid(grid, yy, xx):
                if grid[yy][xx] != ".":
                    count += grid[yy][xx] == "#"
                    break
                yy += dy
                xx += dx
        return count

    return simulate_and_count(list(data.each_token_as(list)), get_adj_count, 5)
