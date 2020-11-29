from typing import List

from aoc.common import input
from aoc.common import solution


Grid = List[List[bool]]


def parse_grid_line(line: str) -> List[bool]:
    return [c == "#" for c in line.strip()]


def update_grid(grid: Grid) -> Grid:
    def get_on_neighbors(r: int, c: int) -> int:
        return sum(
            grid[y][x]
            for y in [r - 1, r, r + 1]
            for x in [c - 1, c, c + 1]
            if 0 <= y < len(grid) and 0 <= x < len(grid[0]) and (y, x) != (r, c)
        )

    new_grid = list(map(list, grid))
    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            num_on = get_on_neighbors(r, c)
            if col and num_on not in {2, 3}:
                new_grid[r][c] = False
            elif not col and num_on == 3:
                new_grid[r][c] = True

    return new_grid


@solution.part_one(year=2015, problem=18)
def part_one(data: input.Tokenized["\n"]) -> int:
    grid = list(data.each_token_as(parse_grid_line))
    for _ in range(100):
        grid = update_grid(grid)
    return sum(c for r in grid for c in r)


@solution.part_two(year=2015, problem=18)
def part_two(data: input.Tokenized["\n"]) -> int:
    grid = list(data.each_token_as(parse_grid_line))

    def set_corners(grid: Grid) -> Grid:
        for (y, x) in [(0, 0), (0, 99), (99, 0), (99, 99)]:
            grid[y][x] = True
        return grid

    for _ in range(100):
        grid = set_corners(update_grid(set_corners(grid)))

    return sum(c for r in grid for c in r)
