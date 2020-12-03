import math

from typing import List, Tuple

from aoc.common import input
from aoc.common import solution


def count_trees(grid: List[str], slope: Tuple[int, int]) -> int:
    dx, dy = slope
    x, y, trees = 0, 0, 0
    while y < len(grid):
        trees += grid[y][x] == "#"
        x, y = (x + dx) % len(grid[y]), y + dy
    return trees


@solution.part_one(year=2020, problem=3)
def part_one(grid: input.Tokenized["\n"]) -> int:
    return count_trees(list(grid), (3, 1))


@solution.part_two(year=2020, problem=3)
def part_two(grid: input.Tokenized["\n"]) -> int:
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    return math.prod(count_trees(list(grid), slope) for slope in slopes)
