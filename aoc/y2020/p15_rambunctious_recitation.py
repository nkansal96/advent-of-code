from typing import Iterable

from aoc.common import input
from aoc.common import solution


def solve(data: Iterable[int], limit: int) -> int:
    last_index = {v: i + 1 for (i, v) in enumerate(data)}
    total_nums = len(last_index) + 1
    next_num = 0

    while total_nums < limit:
        prev = next_num
        next_num = 0 if prev not in last_index else total_nums - last_index[prev]
        last_index[prev] = total_nums
        total_nums += 1

    return next_num


@solution.part_one(year=2020, problem=15)
def _(data: input.Tokenized[input.COMMA]) -> int:
    return solve(data.each_token_as(int), 2020)


@solution.part_two(year=2020, problem=15)
def _(data: input.Tokenized[input.COMMA]) -> int:
    return solve(data.each_token_as(int), 30_000_000)
