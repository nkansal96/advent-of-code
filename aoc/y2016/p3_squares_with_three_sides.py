import itertools
from typing import Iterable, Iterator, Tuple

from aoc.common import input
from aoc.common import solution


def is_valid_triangle(a: int, b: int, c: int) -> bool:
    return a + b > c and a + c > b and b + c > a


def vertical_triangles(data: Iterable[Iterable[int]]) -> Iterator[Tuple[int, int, int]]:
    data = iter(data)
    while True:
        try:
            # read 9 numbers (3x3)
            sides = [n for _ in range(3) for n in next(data)]
            yield sides[0], sides[3], sides[6]
            yield sides[1], sides[4], sides[7]
            yield sides[2], sides[5], sides[8]
        except StopIteration:
            return


@solution.part_one(year=2016, problem=3)
def part_one(data: input.Tokenized["\n"]) -> int:
    triangles = data.each_token_as(lambda d: map(int, d.split()))
    return sum(map(int, itertools.starmap(is_valid_triangle, triangles)))


@solution.part_two(year=2016, problem=3)
def part_two(data: input.Tokenized["\n"]) -> int:
    triangles = vertical_triangles(data.each_token_as(lambda d: map(int, d.split())))
    return sum(map(int, itertools.starmap(is_valid_triangle, triangles)))
