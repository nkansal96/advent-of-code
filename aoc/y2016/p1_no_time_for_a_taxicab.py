from collections import deque
from typing import Iterable, Tuple, Iterator

from aoc.common import input
from aoc.common import solution


def traverse(instructions: Iterable[Tuple[str, int]]) -> Iterator[Tuple[int, int]]:
    x, y = 0, 0
    heading = 0

    for direction, delta in instructions:
        d_theta = 90 if direction == "R" else -90
        heading = (heading + d_theta) % 360
        while delta > 0:
            if heading == 0:
                y += 1
            if heading == 90:
                x += 1
            if heading == 180:
                y -= 1
            if heading == 270:
                x -= 1
            delta -= 1
            yield x, y


@solution.part_one(year=2016, problem=1)
def part_one(data: input.Tokenized[input.COMMA]) -> int:
    instructions = data.each_token_as(lambda d: (d[0], int(d[1:])))
    x, y = deque(traverse(instructions), maxlen=1).pop()
    return abs(x) + abs(y)


@solution.part_two(year=2016, problem=1)
def part_two(data: input.Tokenized[input.COMMA]) -> int:
    instructions = data.each_token_as(lambda d: (d[0], int(d[1:])))
    visited = {(0, 0)}
    for pos in traverse(instructions):
        if pos in visited:
            return sum(map(abs, pos))
        visited.add(pos)
    return 0
