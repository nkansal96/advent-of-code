import re
from dataclasses import dataclass
from typing import Union, List, Iterable

from aoc.common import input
from aoc.common import solution


Grid = List[List[bool]]


@dataclass
class Rect:
    w: int
    h: int

    def apply(self, grid: Grid) -> Grid:
        for i in range(self.h):
            grid[i][: self.w] = [True] * self.w
        return grid


@dataclass
class RotateRow:
    row: int
    by: int

    def apply(self, grid: Grid) -> Grid:
        by = self.by % len(grid[0])
        grid[self.row] = grid[self.row][-by:] + grid[self.row][:-by]
        return grid


@dataclass
class RotateCol:
    col: int
    by: int

    def apply(self, grid: Grid) -> Grid:
        col_as_row = [grid[i][self.col] for i in range(len(grid))]
        rotated_col_as_row = RotateRow(0, self.by).apply([col_as_row])
        for i, v in enumerate(rotated_col_as_row[0]):
            grid[i][self.col] = v
        return grid


Transformation = Union[Rect, RotateRow, RotateCol]


def parse_transformation(line: str) -> Transformation:
    if line.startswith("rect"):
        return Rect(*map(int, re.search(r"(\d+)x(\d+)", line).groups()))

    cls = RotateRow if "row" in line else RotateCol
    return cls(*map(int, re.search(r"=(\d+) by (\d+)", line).groups()))


def transformed_grid(w: int, h: int, transformations: Iterable[Transformation]) -> Grid:
    grid = [[False] * w for _ in range(h)]
    for transformation in transformations:
        grid = transformation.apply(grid)
    return grid


def print_grid(grid: Grid):
    for line in grid:
        print("".join("\u2588" if c else " " for c in line))


@solution.part_one(year=2016, problem=8)
def part_one(data: input.Tokenized["\n"]) -> int:
    grid = transformed_grid(50, 6, data.each_token_as(parse_transformation))
    return sum(map(sum, grid))


@solution.part_two(year=2016, problem=8)
def part_two(data: input.Tokenized["\n"]):
    print_grid(transformed_grid(50, 6, data.each_token_as(parse_transformation)))
