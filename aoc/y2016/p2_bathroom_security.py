from aoc.common import input
from aoc.common import solution
from aoc.common import utils


@solution.part_one(year=2016, problem=2)
def part_one(data: input.Tokenized["\n"]) -> str:
    digits = []
    x, y = (1, 1)
    for instruction in data:
        for d in instruction:
            if d == "L":
                x = max(0, x - 1)
            if d == "R":
                x = min(2, x + 1)
            if d == "U":
                y = max(0, y - 1)
            if d == "D":
                y = min(2, y + 1)
        digits.append(3 * y + x + 1)
    return "".join(map(str, digits))


@solution.part_two(year=2016, problem=2)
def part_two(data: input.Tokenized["\n"]) -> str:
    digits = []
    x, y = (-2, 0)
    for instruction in data:
        for d in instruction:
            if d == "L":
                x = max(-(2 - abs(y)), x - 1)
            if d == "R":
                x = min(2 - abs(y), x + 1)
            if d == "U":
                y = max(-(2 - abs(x)), y - 1)
            if d == "D":
                y = min(2 - abs(x), y + 1)
        digits.append(7 + (utils.sign(y) * (4 * (abs(y) > 0) + 2 * (abs(y) > 1))) + x)
    return "".join(hex(d)[2:] for d in digits)
