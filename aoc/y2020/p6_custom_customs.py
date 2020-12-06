import functools
import operator

from aoc.common import input
from aoc.common import solution


def solve(data: input.Tokenized, op) -> int:
    return sum(len(functools.reduce(op, map(set, group.split("\n")))) for group in data)


@solution.part_one(year=2020, problem=6)
def _(data: input.Tokenized[input.NLNL]) -> int:
    return solve(data, operator.or_)


@solution.part_two(year=2020, problem=6)
def _(data: input.Tokenized[input.NLNL]) -> int:
    return solve(data, operator.and_)
