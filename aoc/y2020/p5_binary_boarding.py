from typing import *

from aoc.common import input
from aoc.common import solution


def find_seat(instr: str) -> Tuple[int, int]:
    yl, yh = (0, 128)
    xl, xh = (0, 8)

    for d in instr:
        if d == "F":
            yl, yh = (yl, yh - (yh - yl) // 2)
        if d == "B":
            yl, yh = (yl + (yh - yl) // 2, yh)
        if d == "L":
            xl, xh = (xl, xh - (xh - xl) // 2)
        if d == "R":
            xl, xh = (xl + (xh - xl) // 2, xh)

    return yl, xl


def seat_id(s: Tuple[int, int]) -> int:
    return 8 * s[0] + s[1]


@solution.part_one(year=2020, problem=5)
def _(data: input.Tokenized[input.NL]) -> int:
    return max(map(seat_id, map(find_seat, data)))


@solution.part_two(year=2020, problem=5)
def _(data: input.Tokenized[input.NL]) -> int:
    seats = set(map(find_seat, data))
    ids = set(map(seat_id, seats))

    for y in range(1, 127):
        for x in range(8):
            s = seat_id((y, x))
            if (y, x) not in seats and s + 1 in ids and s - 1 in ids:
                return s
