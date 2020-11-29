from aoc.common import input
from aoc.common import solution


@solution.part_one(year=2015, problem=2)
def part_one(data: input.Tokenized["\n"]) -> int:
    total = 0
    for (l, w, h) in data.each_token_as(lambda t: map(int, t.split("x"))):
        total += 2 * l * w + 2 * l * h + 2 * w * h
        total += min(l * w, l * h, w * h)

    return total


@solution.part_two(year=2015, problem=2)
def part_two(data: input.Tokenized["\n"]) -> int:
    total = 0
    for (l, w, h) in data.each_token_as(lambda t: map(int, t.split("x"))):
        total += l * w * h
        total += min(2 * l + 2 * w, 2 * l + 2 * h, 2 * w + 2 * h)

    return total
