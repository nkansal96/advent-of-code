from typing import Tuple

from aoc.common import input
from aoc.common import solution


def parse_instruction(line: str) -> Tuple[str, int]:
    return line[0], int(line[1:])


@solution.part_one(year=2020, problem=12)
def _(data: input.Tokenized[input.NL]) -> int:
    d = 90
    x, y = 0, 0
    for (i, dd) in data.each_token_as(parse_instruction):
        if i == "L":
            d = (d - dd) % 360
        if i == "R":
            d = (d + dd) % 360

        y += (i == "N") * dd + (i == "S") * -dd
        x += (i == "E") * dd + (i == "W") * -dd

        if i == "F":
            x += dd if (d == 90) else -dd if (d == 270) else 0
            y += dd if (d == 0) else -dd if (d == 180) else 0

    return abs(y) + abs(x)


@solution.part_two(year=2020, problem=12)
def _(data: input.Tokenized[input.NL]) -> int:
    wx, wy = 10, 1
    x, y = 0, 0

    for (i, dd) in data.each_token_as(parse_instruction):
        if i == "L" or i == "R":
            dd = dd if i == "L" else (360 - dd)
            for _ in range(0, dd, 90):
                wx, wy = -wy, wx

        wy += (i == "N") * dd + (i == "S") * -dd
        wx += (i == "E") * dd + (i == "W") * -dd
        x += (i == "F") * wx * dd
        y += (i == "F") * wy * dd

    return abs(y) + abs(x)
